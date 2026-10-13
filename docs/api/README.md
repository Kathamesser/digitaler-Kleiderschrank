# API

Das Backend erzeugt die API-Beschreibung automatisch aus dem Code. Bei laufendem Backend:

- http://localhost:8000/docs (interaktiv, Swagger UI)
- http://localhost:8000/redoc

Alle Endpunkte liegen unter `/api/<modul>`, z. B. `/api/kleidung`, `/api/outfits`. Absprachen zur API, die nicht aus dem Code hervorgehen (Fehlerformat, Paginierung, Anmeldung), kommen in diese Datei.
