# API

Das Backend erzeugt die API-Beschreibung automatisch aus dem Code. Bei laufendem Backend:

- http://localhost:8000/docs (interaktiv, Swagger UI)
- http://localhost:8000/redoc

Alle Endpunkte liegen unter `/api/<modul>`, z. B. `/api/kleidung`, `/api/outfits`. Absprachen zur API, die nicht aus dem Code hervorgehen (Fehlerformat, Paginierung, Anmeldung), kommen in diese Datei.

## Absprachen

- **Fehlermeldungen:** Fehler kommen im FastAPI-Format `{"detail": "…"}`. Bei fachlichen Fehlern ist `detail` ein deutscher Satz, den das Frontend direkt anzeigen kann (z. B. „Das Bild ist zu groß. Erlaubt sind höchstens 10 MB.“). Bei Eingabefehlern (Status 422) ist `detail` eine Liste mit den betroffenen Feldern.
- **Anmeldung (vorläufig, 13.10.2026):** Solange das Anmeldeverfahren offen ist, gehören alle Anfragen einem festen Test-Nutzer (`aktueller_nutzer()` in `backend/app/core/sicherheit.py`). Endpunkte holen den Nutzer immer über `Depends(aktueller_nutzer)`; später wird nur diese Funktion ersetzt.
- **Bilder:** Hochgeladene Bilder sind nicht öffentlich erreichbar. Sie werden über den Endpunkt des Objekts abgerufen (z. B. `GET /api/kleidung/{id}/bild`), der prüft, ob das Bild dem Nutzer gehört. Die Adresse steht in der Antwort als `bild_url`.

## Endpunkte (Überblick)

| Methode | Pfad | Zweck | User Story |
|---|---|---|---|
| POST | `/api/kleidung` | Kleidungsstück mit Foto anlegen (multipart: `bild`, `name`, `kategorie`, optional `farbe`, `groesse`) | 8 |
| GET | `/api/kleidung` | Alle Kleidungsstücke des Nutzers, neueste zuerst | 1 (Grundform) |
| GET | `/api/kleidung/{id}` | Ein Kleidungsstück | 1 |
| GET | `/api/kleidung/{id}/bild` | Bild eines Kleidungsstücks | 8 |
