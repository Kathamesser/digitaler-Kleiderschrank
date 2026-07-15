# Digitaler Kleiderschrank 


Eine Web-App zum Digitalisieren des eigenen Kleiderschranks: Kleidungsstücke erfassen,
Outfits planen und Stücke an Freunde verleihen oder verschenken.

Voraussetzung: Python 3.10 oder neuer ist installiert (`python --version`).

```bash
# 1. Repo holen
git clone https://github.com/EUER-NAME/digitaler-kleiderschrank.git
cd digitaler-kleiderschrank

# 2. Virtuelle Umgebung anlegen und aktivieren
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 3. Abhängigkeiten installieren
pip install -r requirements.txt
```

## Starten

```bash
python main.py
```

Dann im Browser öffnen: http://localhost:5000

Die Datenbank (`kleiderschrank.db`) wird beim ersten Start automatisch angelegt.

### Am Handy testen (gleiches WLAN)

```bash
flask run --host=0.0.0.0
```

Dann am Handy die IP des Laptops aufrufen, z. B. `http://192.168.1.23:5000`
(die IP findet ihr mit `ipconfig` unter Windows bzw. `ifconfig` unter macOS/Linux).

## Projektstruktur

```
main.py                 Routen und App-Konfiguration
models.py               Datenbankmodelle (User, Kleidungsstueck, ...)
templates/              HTML-Seiten (Jinja2-Templates)
static/style.css        Design (mobile-first, responsiv)
static/uploads/         hochgeladene Fotos (nicht in Git!)
requirements.txt        benötigte Python-Pakete
```

## Was schon funktioniert (Must-haves)

- [x] Registrierung, Login, Logout (Passwörter werden gehasht gespeichert)
- [x] Kleidungsstück anlegen (mit Foto-Upload) und löschen
- [x] Übersicht mit Kategorie-Filter

## Nächste Schritte

- [ ] Kleidungsstück bearbeiten
- [ ] Favorisieren (Herz-Button)
- [ ] Outfits erstellen/bearbeiten/löschen
- [ ] Freunde hinzufügen/entfernen
- [ ] Verleihen / Zurückgeben / Verschenken

Hinweise dazu stehen als `TODO`-Kommentare in `main.py` und `models.py`.
