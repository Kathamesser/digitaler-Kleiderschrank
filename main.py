# =============================================================
# main.py – Hauptdatei der digitalen Kleiderschrankverwaltung
# Starten mit:  flask run   (oder: python main.py)
# =============================================================
import os
import uuid

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from models import db, User, Kleidungsstueck

# ---------------------------------------------------------------
# Grundkonfiguration
# ---------------------------------------------------------------
app = Flask(__name__)
app.config["SECRET_KEY"] = "bitte-in-etwas-geheimes-aendern"  # für Sessions/Cookies
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kleiderschrank.db"
app.config["UPLOAD_ORDNER"] = os.path.join(app.static_folder, "uploads")
ERLAUBTE_ENDUNGEN = {"png", "jpg", "jpeg", "webp"}

db.init_app(app)

# Flask-Login kümmert sich um "wer ist gerade eingeloggt?"
login_manager = LoginManager(app)
login_manager.login_view = "login"          # wohin, wenn Login fehlt
login_manager.login_message = "Bitte melde dich zuerst an."


@login_manager.user_loader
def lade_nutzer(user_id):
    """Flask-Login ruft diese Funktion auf, um den Nutzer zur Session zu laden."""
    return db.session.get(User, int(user_id))


# ---------------------------------------------------------------
# Hilfsfunktion für den Foto-Upload
# ---------------------------------------------------------------
def speichere_foto(datei):
    """Speichert ein hochgeladenes Foto und gibt den Dateinamen zurück
    (oder None, wenn kein gültiges Foto dabei war)."""
    if not datei or datei.filename == "":
        return None
    endung = datei.filename.rsplit(".", 1)[-1].lower()
    if endung not in ERLAUBTE_ENDUNGEN:
        return None
    # Eindeutiger Dateiname, damit sich Uploads nicht überschreiben:
    dateiname = f"{uuid.uuid4().hex}_{secure_filename(datei.filename)}"
    datei.save(os.path.join(app.config["UPLOAD_ORDNER"], dateiname))
    return dateiname


# ---------------------------------------------------------------
# Startseite
# ---------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------------------------------------------------------
# Registrierung
# ---------------------------------------------------------------
@app.route("/registrieren", methods=["GET", "POST"])
def registrieren():
    if request.method == "POST":
        benutzername = request.form.get("benutzername", "").strip()
        passwort = request.form.get("passwort", "")

        if not benutzername or not passwort:
            flash("Bitte Benutzername und Passwort ausfüllen.", "fehler")
        elif User.query.filter_by(benutzername=benutzername).first():
            flash("Dieser Benutzername ist schon vergeben.", "fehler")
        else:
            # Passwort niemals im Klartext speichern -> Hash!
            neuer_nutzer = User(
                benutzername=benutzername,
                passwort_hash=generate_password_hash(passwort),
            )
            db.session.add(neuer_nutzer)
            db.session.commit()
            login_user(neuer_nutzer)
            flash("Willkommen! Dein Konto wurde erstellt.", "erfolg")
            return redirect(url_for("kleiderschrank"))

    return render_template("registrieren.html")


# ---------------------------------------------------------------
# Login / Logout
# ---------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nutzer = User.query.filter_by(
            benutzername=request.form.get("benutzername", "").strip()
        ).first()
        if nutzer and check_password_hash(nutzer.passwort_hash, request.form.get("passwort", "")):
            login_user(nutzer)
            return redirect(url_for("kleiderschrank"))
        flash("Benutzername oder Passwort ist falsch.", "fehler")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Du bist jetzt abgemeldet.", "erfolg")
    return redirect(url_for("index"))


# ---------------------------------------------------------------
# Kleiderschrank: Übersicht
# ---------------------------------------------------------------
@app.route("/kleiderschrank")
@login_required
def kleiderschrank():
    # Optionaler Filter über die URL, z. B. /kleiderschrank?kategorie=Hosen
    kategorie = request.args.get("kategorie")
    abfrage = Kleidungsstueck.query.filter_by(besitzer_id=current_user.id)
    if kategorie:
        abfrage = abfrage.filter_by(kategorie=kategorie)
    stuecke = abfrage.order_by(Kleidungsstueck.name).all()

    # Alle Kategorien des Nutzers für die Filter-Buttons sammeln
    kategorien = sorted(
        {s.kategorie for s in current_user.kleidungsstuecke}
    )
    return render_template(
        "kleiderschrank.html",
        stuecke=stuecke,
        kategorien=kategorien,
        aktive_kategorie=kategorie,
    )


# ---------------------------------------------------------------
# Kleidungsstück anlegen
# ---------------------------------------------------------------
@app.route("/kleidungsstueck/neu", methods=["GET", "POST"])
@login_required
def kleidungsstueck_neu():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        kategorie = request.form.get("kategorie", "").strip()
        if not name or not kategorie:
            flash("Bitte mindestens Name und Kategorie ausfüllen.", "fehler")
        else:
            stueck = Kleidungsstueck(
                name=name,
                kategorie=kategorie,
                farbe=request.form.get("farbe", "").strip(),
                foto=speichere_foto(request.files.get("foto")),
                besitzer_id=current_user.id,
            )
            db.session.add(stueck)
            db.session.commit()
            flash(f"„{stueck.name}“ hängt jetzt in deinem Kleiderschrank.", "erfolg")
            return redirect(url_for("kleiderschrank"))

    return render_template("kleidungsstueck_form.html")


# ---------------------------------------------------------------
# Kleidungsstück löschen
# ---------------------------------------------------------------
@app.route("/kleidungsstueck/<int:stueck_id>/loeschen", methods=["POST"])
@login_required
def kleidungsstueck_loeschen(stueck_id):
    stueck = db.session.get(Kleidungsstueck, stueck_id)
    # Sicherheitscheck: Nur der Besitzer darf löschen!
    if stueck is None or stueck.besitzer_id != current_user.id:
        flash("Dieses Kleidungsstück gehört nicht dir.", "fehler")
    else:
        db.session.delete(stueck)
        db.session.commit()
        flash(f"„{stueck.name}“ wurde entfernt.", "erfolg")
    return redirect(url_for("kleiderschrank"))


# ---------------------------------------------------------------
# TODO für euer Team (siehe MoSCoW-Anforderungen):
#  - Favorisieren (Herz-Button): neues Feld `favorit` am Modell + Route
#  - Kleidungsstück bearbeiten: Route /kleidungsstueck/<id>/bearbeiten
#  - Outfits: eigenes Modell + Seiten (siehe Hinweis in models.py)
#  - Freunde & Verleihen: Freundschafts-Modell + "verliehen_an"-Logik
# ---------------------------------------------------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # legt die Datenbank beim ersten Start an
    app.run(debug=True)
