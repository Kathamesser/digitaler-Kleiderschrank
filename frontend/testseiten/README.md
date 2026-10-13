# Testseiten

Schlichte HTML-Seiten ohne Framework, um Backend-Endpunkte im Browser auszuprobieren, solange React oder Vue noch nicht entschieden ist. Sie sind **nicht** Teil des späteren Frontends und werden gelöscht, sobald die echten Seiten stehen.

| Seite | Zweck |
|---|---|
| `kleidung-hochladen.html` | User Story 8: Foto aufnehmen oder auswählen, Angaben eintragen, speichern; darunter die Liste „Mein Schrank“ |

## Starten

1. MongoDB und Backend starten (siehe `backend/README.md`).
2. In einem zweiten Terminal in diesem Ordner einen einfachen Webserver auf Port 5173 starten. Das Backend erlaubt Zugriffe nur von dieser Adresse (CORS, `FRONTEND_URLS` in `.env`):

   ```bash
   cd frontend/testseiten
   python -m http.server 5173
   ```

3. Im Browser öffnen: http://localhost:5173/kleidung-hochladen.html

Direktes Öffnen per Doppelklick (`file://…`) funktioniert nicht, weil der Browser die Anfragen ans Backend dann blockiert.
