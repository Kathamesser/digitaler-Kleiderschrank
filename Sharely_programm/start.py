"""Sharely mit einem Befehl starten: alle Dienste für die Entwicklung auf diesem Rechner.

Start im Ordner Sharely_programm:  python start.py
Beenden: Strg+C (beendet alle Dienste zusammen)

Optionen:
  --ohne-browser   den Browser nicht automatisch öffnen

Hier werden ALLE Dienste eingetragen, die zum Starten der App nötig sind (Entscheidung
Christian, 29.10.2026). Kommt ein Dienst dazu (weiterer Server, Worker …), bekommt er einen
Eintrag in DIENSTE unten, statt dass jeder ihn von Hand in einem eigenen Terminal startet.

Was das Skript bewusst NICHT macht, weil es nur einmal bzw. nach Änderungen nötig ist:
Pakete installieren (pip install -r requirements.txt) und die Datenbank einrichten
(python -m app.datenbank_einrichten). Anleitung: backend/README.md.
"""

import argparse
import os
import signal
import socket
import subprocess
import sys
import time
import urllib.request
import webbrowser
from dataclasses import dataclass
from pathlib import Path

ORDNER = Path(__file__).resolve().parent  # Sharely_programm, egal von wo gestartet
BACKEND = ORDNER / "backend"
WINDOWS = os.name == "nt"
VENV_PYTHON = BACKEND / ".venv" / ("Scripts/python.exe" if WINDOWS else "bin/python")

# Diese Adresse öffnet sich im Browser, wenn alles läuft (führt zur Anmeldung)
START_ADRESSE = "http://localhost:5173/"


@dataclass
class Dienst:
    name: str
    befehl: list[str]
    ordner: Path
    port: int
    bereit_url: str          # wird abgefragt, bis der Dienst antwortet
    voraussetzungen: list    # [(Bedingung, Hinweis bei Fehlen)], geprüft vor dem Start


DIENSTE = [
    Dienst(
        name="Backend (FastAPI)",
        befehl=[str(VENV_PYTHON), "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"],
        ordner=BACKEND,  # dort liegt die .env
        port=8000,
        bereit_url="http://localhost:8000/api/health",
        voraussetzungen=[
            (VENV_PYTHON.exists(),
             "Die Python-Umgebung des Backends fehlt. Einmal einrichten, im Ordner Sharely_programm\\backend:\n"
             "    python -m venv .venv\n"
             "    .\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt"),
            ((BACKEND / ".env").exists(),
             "Die Datei backend\\.env fehlt. Vorlage kopieren (copy .env.example .env) und die Datenbank-Adresse eintragen."),
        ],
    ),
    Dienst(
        name="Seiten (seiten_server.py)",
        befehl=[sys.executable, "seiten_server.py"],
        ordner=ORDNER,
        port=5173,
        bereit_url="http://localhost:5173/",
        voraussetzungen=[],
    ),
    # Neuer Dienst? Hier einen weiteren Eintrag anlegen, z. B. später für das Frontend-Framework:
    # Dienst(name="Frontend (Vite)", befehl=["npm", "run", "dev"], ordner=ORDNER / "frontend",
    #        port=5173, bereit_url="http://localhost:5173/", voraussetzungen=[...]),
]


def port_belegt(port: int) -> bool:
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0


def antwortet(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=1):
            return True
    except Exception:  # noqa: BLE001 – jede Art „noch nicht da“ zählt gleich
        return False


def starten(dienst: Dienst) -> subprocess.Popen:
    # Eigene Prozessgruppe: Strg+C landet nur bei diesem Skript, das dann alle Dienste
    # samt Unterprozessen beendet (uvicorn --reload startet einen eigenen Arbeitsprozess).
    if WINDOWS:
        return subprocess.Popen(dienst.befehl, cwd=dienst.ordner, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    return subprocess.Popen(dienst.befehl, cwd=dienst.ordner, start_new_session=True)


def beenden(prozess: subprocess.Popen) -> None:
    if prozess.poll() is not None:
        return
    if WINDOWS:
        # /T beendet auch die Unterprozesse; sonst bleibt unter Windows gern ein alter
        # uvicorn auf Port 8000 hängen (siehe Wissensspeicher in BRAIN.md)
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(prozess.pid)], capture_output=True)
    else:
        os.killpg(prozess.pid, signal.SIGTERM)
    try:
        prozess.wait(timeout=5)
    except subprocess.TimeoutExpired:
        prozess.kill()


def main() -> int:
    parser = argparse.ArgumentParser(description="Alle Sharely-Dienste starten (beenden mit Strg+C).")
    parser.add_argument("--ohne-browser", action="store_true", help="Browser nicht automatisch öffnen")
    args = parser.parse_args()

    # 1. Vorher prüfen, damit nicht ein Dienst halb startet
    probleme = [f"{d.name}: {hinweis}" for d in DIENSTE for ok, hinweis in d.voraussetzungen if not ok]
    probleme += [
        f"{d.name}: Port {d.port} ist schon belegt. Läuft Sharely schon in einem anderen Fenster?\n"
        f"    Prüfen mit:  netstat -ano | findstr :{d.port}"
        for d in DIENSTE if port_belegt(d.port)
    ]
    if probleme:
        print("Sharely startet nicht:\n\n" + "\n\n".join(probleme))
        return 1

    # 2. Starten
    laufend: list[tuple[Dienst, subprocess.Popen]] = []
    try:
        for d in DIENSTE:
            print(f"Starte {d.name} …")
            laufend.append((d, starten(d)))

        # 3. Warten, bis alle antworten (Backend braucht ein paar Sekunden für die Datenbank)
        offen = list(laufend)
        frist = time.monotonic() + 30
        while offen and time.monotonic() < frist:
            for d, p in list(offen):
                if p.poll() is not None:
                    print(f"\n{d.name} ist beim Start abgebrochen (siehe Meldungen oben).")
                    return 1
                if antwortet(d.bereit_url):
                    offen.remove((d, p))
            time.sleep(0.5)
        for d, _ in offen:
            print(f"Hinweis: {d.name} antwortet noch nicht unter {d.bereit_url}.")

        print(f"\nSharely läuft: {START_ADRESSE}   (beenden mit Strg+C)\n")
        if not args.ohne_browser:
            webbrowser.open(START_ADRESSE)

        # 4. Laufen lassen, bis Strg+C kommt oder ein Dienst ausfällt
        while True:
            for d, p in laufend:
                if p.poll() is not None:
                    print(f"\n{d.name} wurde beendet (Code {p.returncode}), stoppe alle Dienste.")
                    return 1
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nBeende Sharely …")
        return 0
    finally:
        for _, p in reversed(laufend):
            beenden(p)


if __name__ == "__main__":
    sys.exit(main())
