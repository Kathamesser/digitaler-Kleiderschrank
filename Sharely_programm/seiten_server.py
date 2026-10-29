"""Seiten-Server für die Entwicklung: wie `python -m http.server 5173`, aber ohne veraltete Dateien.

Start im Ordner Sharely_programm:  python seiten_server.py
Dann im Browser: http://localhost:5173/

`python -m http.server` erlaubt dem Browser, JS- und CSS-Dateien eine Weile
zwischenzuspeichern. Nach einem `git pull` lief dann noch die alte gemeinsam.js
(14.10. und 27.10.2026). Hier fragt der Browser bei jeder Datei nach, ob sie sich
geändert hat (`Cache-Control: no-cache`); unveränderte Dateien kommen trotzdem
schnell als „304 Not Modified“.
"""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORT = 5173


class OhneVeralteteDateien(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


if __name__ == "__main__":
    ordner = Path(__file__).resolve().parent  # immer Sharely_programm, egal von wo gestartet
    # Nur auf diesem Rechner erreichbar, nicht für andere im (Schul-)Netz
    server = ThreadingHTTPServer(("127.0.0.1", PORT), partial(OhneVeralteteDateien, directory=str(ordner)))
    print(f"Sharely-Seiten: http://localhost:{PORT}/  (beenden mit Strg+C)")
    server.serve_forever()
