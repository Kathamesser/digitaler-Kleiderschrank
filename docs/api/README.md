# API

Das Backend erzeugt die API-Beschreibung automatisch aus dem Code. Bei laufendem Backend:

- http://localhost:8000/docs (interaktiv, Swagger UI)
- http://localhost:8000/redoc

Alle Endpunkte liegen unter `/api/<modul>`, z. B. `/api/kleidung`, `/api/outfits`. Absprachen zur API, die nicht aus dem Code hervorgehen (Fehlerformat, Paginierung, Anmeldung), kommen in diese Datei.

## Absprachen

- **Fehlermeldungen:** Fehler kommen im FastAPI-Format `{"detail": "…"}`. Bei fachlichen Fehlern ist `detail` ein deutscher Satz, den das Frontend direkt anzeigen kann (z. B. „Das Bild ist zu groß. Erlaubt sind höchstens 10 MB.“). Bei Eingabefehlern (Status 422) ist `detail` eine Liste mit den betroffenen Feldern.
- **Anmeldung (seit 27.10.2026, ERM-Entscheidung 13):** Registrieren oder Anmelden setzt das Cookie `sharely_sitzung` (httpOnly, SameSite=Lax, gültig 14 Tage). Alle übrigen Endpunkte holen den Nutzer über `Depends(aktueller_nutzer)` (`Sharely_programm/backend/app/core/sicherheit.py`) und antworten ohne gültige Sitzung mit **401** „Bitte melde dich an.“. Das Frontend schickt das Cookie mit `credentials: "include"` (Funktion `api()` in `gemeinsam.js`) und leitet bei 401 zur Anmeldeseite. Wichtig: Das Frontend unter `http://localhost:5173` öffnen, nicht unter `127.0.0.1`, sonst gilt das Cookie von `localhost:8000` als fremde Website und wird nicht mitgeschickt.
- **Bilder:** Hochgeladene Bilder sind nicht öffentlich erreichbar. Sie werden über den Endpunkt des Objekts abgerufen (z. B. `GET /api/kleidung/{id}/bild`), der prüft, ob das Bild dem Nutzer gehört. Die Adresse steht in der Antwort als `bild_url`.

- **Kleidungsstück-Felder (ERM vom 20.10.2026, umgesetzt am 20.10.2026):**
  - `kleidungsart` (Pflicht): `tops`, `pullover`, `hosen`, `roecke`, `kleider`, `jacken`, `schuhe`, `unterwaesche`, `einteiler`, `accessoires`
  - `name`: optional, bis 100 Zeichen (z. B. „Wintermantel“). Ohne Namen zeigt das Frontend die Kleidungsart an.
  - `farbe`: optional, `schwarz`, `weiss`, `grau`, `beige`, `braun`, `rot`, `rosa`, `orange`, `gelb`, `gruen`, `blau`, `dunkelblau`, `lila`, `bunt`
  - `material`: optional, `baumwolle`, `polyester`, `wolle`, `leinen`, `seide`, `leder`, `jeans`, `viskose`, `sonstiges`
  - `saison`: Mehrfachauswahl als wiederholtes Feld (`saison=herbst&saison=winter`) aus `fruehling`, `sommer`, `herbst`, `winter`, `ganzjaehrig`; `ganzjaehrig` nur allein
  - `status`: beim Anlegen `im_schrank` (Standard, „Eigenes“), `geliehen` oder `wunsch`. `verliehen` setzt nur das Modul `verleihen`; in Antworten kommen alle vier Werte vor.
  - `kategorie_ids`: wiederholtes Feld mit IDs aus der Collection `kategorien`. Vorbereitet: Das Backend prüft nur das ID-Format, ob die Kategorie existiert, prüft erst das Modul Kategorien.
  - `masse`: JSON-Text, z. B. `[{"messpunkt": "waist-circ", "wert_cm": 80}]`. Messpunkte sind die 22 Schlüssel aus `docs/avatar/messpunkte.json`, je Messpunkt höchstens ein Wert, cm auf eine Nachkommastelle.
  - `leihvorgang_id`: nur in Antworten, setzt nur das System bei geliehenen Teilen (wird beim Anlegen ignoriert).
  - Entfallen: `kategorie` (jetzt `kleidungsart`), `anlass` (geht in den Kategorien auf), `groesse`, `marke`, `herkunft`, `notiz`; Status `verschenkt` (Verschenken ist ein Besitzwechsel).

## Endpunkte (Überblick)

| Methode | Pfad | Zweck | User Story |
|---|---|---|---|
| POST | `/api/kleidung` | Kleidungsstück mit Foto anlegen (multipart). Pflicht: `bild`, `kleidungsart`. Optional: `name`, `favorit`, `privat` (true/false, Standard false), `farbe`, `material`, `saison`, `preis` (Euro), `kaufdatum` (JJJJ-MM-TT), `status`, `kategorie_ids`, `masse`. Werte siehe unten | 8 |
| GET | `/api/kleidung` | Alle Kleidungsstücke des Nutzers, neueste zuerst | 1 (Grundform) |
| GET | `/api/kleidung/{id}` | Ein Kleidungsstück | 1 |
| GET | `/api/kleidung/{id}/bild` | Bild eines Kleidungsstücks | 8 |
| POST | `/api/nutzer/registrieren` | Konto anlegen (JSON: `email`, `nutzername`, `passwort`) und gleich angemeldet sein; 201, 422 bei falschem Format, 409 wenn E-Mail oder Nutzername vergeben ist | US 6, Desktop 2 |
| POST | `/api/nutzer/anmelden` | Anmelden (JSON: `nutzername`, `passwort`; Groß-/Kleinschreibung des Namens egal); 401 „Nutzername oder Passwort ist falsch.“ | US 6, Desktop 1 |
| POST | `/api/nutzer/abmelden` | Sitzung löschen, Cookie entfernen; 204, klappt auch ohne Sitzung | US 6 |
| GET | `/api/nutzer/ich` | Eigenes Profil: `id`, `nutzername`, `email`, `mitglied_seit`, `profilbild_url` (`null` ohne Bild) | Mockup „Mein Profil“ |
| PUT | `/api/nutzer/ich/profilbild` | Profilbild hochladen oder ersetzen (multipart, Feld `bild`, JPEG/PNG/WebP, höchstens `MAX_BILD_MB`); das alte Bild wird gelöscht | Mockup „Mein Profil“ |
| DELETE | `/api/nutzer/ich/profilbild` | Profilbild löschen (Datei und Verweis) | Mockup „Mein Profil“ |
| GET | `/api/nutzer/ich/profilbild` | Das Profilbild selbst, nur für den Nutzer; die Adresse aus `profilbild_url` enthält `?v=…`, das sich mit jedem neuen Bild ändert | Mockup „Mein Profil“ |
