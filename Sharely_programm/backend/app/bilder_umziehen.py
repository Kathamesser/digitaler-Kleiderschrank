"""Zieht vorhandene Bilder aus einem Upload-Ordner in den Railway Storage Bucket um.

Hintergrund: Bis 24.11.2026 lagen die Bilder im Ordner des jeweiligen Rechners bzw. auf
dem Railway-Volume. Jedes Teammitglied lässt das Skript einmal auf seinem Rechner laufen,
dazu einmal auf Railway für das Volume. Danach sind alle Bilder an einer Stelle.

Aufruf im Ordner backend/ mit aktivierter .venv (in der .env stehen schon die Bucket-Werte):

    python -m app.bilder_umziehen                     # nur anzeigen, was passieren würde
    python -m app.bilder_umziehen --ausfuehren        # wirklich hochladen
    python -m app.bilder_umziehen --quelle /data/uploads --ausfuehren   # auf Railway

Hochgeladen werden nur Bilder, auf die ein Eintrag in der Datenbank verweist
(`kleidungsstuecke.bild_pfad`, `nutzer.profilbild_pfad`) und die im Bucket noch fehlen.
Das Skript löscht nichts, weder im Ordner noch im Bucket noch in der Datenbank;
den alten Ordner leert ihr danach selbst. Die Datenbank bleibt unverändert, weil der
Schlüssel im Bucket genau der gespeicherte Pfad ist.
"""

import argparse
import sys
from pathlib import Path

from botocore.exceptions import ClientError
from pymongo import MongoClient

from app.core import bildspeicher
from app.core.config import get_settings


def verweise(mongodb_url: str, datenbank: str) -> list[str]:
    """Alle Bildschlüssel, auf die die Datenbank verweist."""
    with MongoClient(mongodb_url) as client:
        db = client[datenbank]
        schluessel = [d["bild_pfad"] for d in db["kleidungsstuecke"].find(
            {"bild_pfad": {"$type": "string"}}, {"bild_pfad": 1})]
        schluessel += [d["profilbild_pfad"] for d in db["nutzer"].find(
            {"profilbild_pfad": {"$type": "string"}}, {"profilbild_pfad": 1})]
    return sorted(set(schluessel))


def im_bucket(schluessel: str) -> bool:
    client, name = bildspeicher._bucket()
    try:
        client.head_object(Bucket=name, Key=schluessel)
        return True
    except ClientError as fehler:
        if fehler.response.get("Error", {}).get("Code") in ("404", "NoSuchKey", "NotFound"):
            return False
        raise


def umziehen(quelle: Path, schluessel: list[str], ausfuehren: bool) -> dict[str, list[str]]:
    ergebnis: dict[str, list[str]] = {"hochgeladen": [], "schon_da": [], "nicht_hier": []}
    for s in schluessel:
        if im_bucket(s):
            ergebnis["schon_da"].append(s)
            continue
        datei = quelle / s
        if not datei.is_file():
            ergebnis["nicht_hier"].append(s)  # liegt vermutlich auf einem anderen Rechner
            continue
        if ausfuehren:
            bildspeicher._bucket_speichern(s, datei.read_bytes())
        ergebnis["hochgeladen"].append(s)
    return ergebnis


def main() -> int:
    s = get_settings()
    parser = argparse.ArgumentParser(description="Bilder aus dem Upload-Ordner in den Bucket umziehen.")
    parser.add_argument("--quelle", default=s.upload_ordner, help=f"Upload-Ordner (Vorgabe: {s.upload_ordner})")
    parser.add_argument("--ausfuehren", action="store_true", help="wirklich hochladen (sonst nur anzeigen)")
    args = parser.parse_args()

    quelle = Path(args.quelle)
    if not quelle.is_dir():
        print(f"Ordner {quelle} gibt es nicht. Hier liegen keine Bilder, nichts zu tun.")
        return 0
    try:
        bildspeicher._bucket()  # meldet fehlende Bucket-Einstellungen verständlich
    except RuntimeError as fehler:
        print(fehler)
        return 1

    ergebnis = umziehen(quelle, verweise(s.mongodb_url, s.mongodb_datenbank), args.ausfuehren)
    verb = "Hochgeladen" if args.ausfuehren else "Würde hochladen"
    print(f"{verb}: {len(ergebnis['hochgeladen'])}")
    for schluessel in ergebnis["hochgeladen"]:
        print(f"  {schluessel}")
    print(f"Schon im Bucket: {len(ergebnis['schon_da'])}")
    print(f"Nicht in {quelle} (liegt evtl. auf einem anderen Rechner oder ist verloren): {len(ergebnis['nicht_hier'])}")
    for schluessel in ergebnis["nicht_hier"]:
        print(f"  {schluessel}")
    if not args.ausfuehren and ergebnis["hochgeladen"]:
        print("Nur angezeigt. Zum Hochladen noch einmal mit --ausfuehren starten.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
