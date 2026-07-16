# =============================================================
# main.py – Hauptdatei der digitalen Kleiderschrankverwaltung
# Starten mit:  flask run   (oder: python main.py)
# =============================================================
import os
import uuid
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user
)
from sqlalchemy import inspect, text
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from models import db, User, Kleidungsstueck, Outfit, Follow

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


def stelle_profilbild_spalte_sicher():
    """Ergänzt die Spalte 'profilbild' in einer bereits bestehenden
    Datenbank nachträglich (db.create_all() legt nur neue Tabellen an,
    ändert aber keine bestehenden)."""
    inspektor = inspect(db.engine)
    spalten = [s["name"] for s in inspektor.get_columns("user")]
    if "profilbild" not in spalten:
        db.session.execute(text("ALTER TABLE user ADD COLUMN profilbild VARCHAR(200)"))
        db.session.commit()


def stelle_favorit_spalte_sicher():
    """Ergänzt die Spalte 'favorit' in einer bereits bestehenden Datenbank
    nachträglich (siehe stelle_profilbild_spalte_sicher)."""
    inspektor = inspect(db.engine)
    spalten = [s["name"] for s in inspektor.get_columns("kleidungsstueck")]
    if "favorit" not in spalten:
        db.session.execute(
            text("ALTER TABLE kleidungsstueck ADD COLUMN favorit BOOLEAN DEFAULT 0 NOT NULL")
        )
        db.session.commit()


def stelle_verleih_spalten_sicher():
    """Ergänzt die Spalten 'marke', 'groesse', 'kaufdatum', 'preis' und 'status'
    in einer bereits bestehenden Datenbank nachträglich
    (siehe stelle_profilbild_spalte_sicher)."""
    inspektor = inspect(db.engine)
    spalten = [s["name"] for s in inspektor.get_columns("kleidungsstueck")]
    if "marke" not in spalten:
        db.session.execute(text("ALTER TABLE kleidungsstueck ADD COLUMN marke VARCHAR(60)"))
    if "groesse" not in spalten:
        db.session.execute(text("ALTER TABLE kleidungsstueck ADD COLUMN groesse VARCHAR(30)"))
    if "kaufdatum" not in spalten:
        db.session.execute(text("ALTER TABLE kleidungsstueck ADD COLUMN kaufdatum DATE"))
    if "preis" not in spalten:
        db.session.execute(text("ALTER TABLE kleidungsstueck ADD COLUMN preis NUMERIC(8, 2)"))
    if "status" not in spalten:
        db.session.execute(
            text("ALTER TABLE kleidungsstueck ADD COLUMN status VARCHAR(30) "
                 "DEFAULT 'Eigener Artikel' NOT NULL")
        )
    db.session.commit()


def stelle_akzeptiert_spalte_sicher():
    """Ergänzt die Spalte 'akzeptiert' in einer bereits bestehenden Datenbank
    nachträglich (siehe stelle_profilbild_spalte_sicher)."""
    inspektor = inspect(db.engine)
    spalten = [s["name"] for s in inspektor.get_columns("follow")]
    if "akzeptiert" not in spalten:
        db.session.execute(
            text("ALTER TABLE follow ADD COLUMN akzeptiert BOOLEAN DEFAULT 0 NOT NULL")
        )
        db.session.commit()


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
# Profilbild hochladen / ändern
# ---------------------------------------------------------------
@app.route("/profil/bild", methods=["POST"])
@login_required
def profilbild_hochladen():
    dateiname = speichere_foto(request.files.get("profilbild"))
    if dateiname:
        current_user.profilbild = dateiname
        db.session.commit()
        flash("Profilbild wurde aktualisiert.", "erfolg")
    else:
        flash("Bitte ein gültiges Bild auswählen (png, jpg, jpeg, webp).", "fehler")
    return redirect(url_for("kleiderschrank"))


# ---------------------------------------------------------------
# Konto: Benutzername & Passwort ändern
# ---------------------------------------------------------------
@app.route("/konto")
@login_required
def konto():
    return render_template("konto.html")


@app.route("/konto/benutzername", methods=["POST"])
@login_required
def konto_benutzername_aendern():
    neuer_benutzername = request.form.get("benutzername", "").strip()
    passwort = request.form.get("passwort", "")

    if not check_password_hash(current_user.passwort_hash, passwort):
        flash("Falsches Passwort.", "fehler")
    elif not neuer_benutzername:
        flash("Bitte einen Benutzernamen angeben.", "fehler")
    elif neuer_benutzername != current_user.benutzername and \
            User.query.filter_by(benutzername=neuer_benutzername).first():
        flash("Dieser Benutzername ist schon vergeben.", "fehler")
    else:
        current_user.benutzername = neuer_benutzername
        db.session.commit()
        flash("Benutzername wurde geändert.", "erfolg")

    return redirect(url_for("konto"))


@app.route("/konto/passwort", methods=["POST"])
@login_required
def konto_passwort_aendern():
    aktuelles_passwort = request.form.get("aktuelles_passwort", "")
    neues_passwort = request.form.get("neues_passwort", "")
    neues_passwort_wiederholen = request.form.get("neues_passwort_wiederholen", "")

    if not check_password_hash(current_user.passwort_hash, aktuelles_passwort):
        flash("Aktuelles Passwort ist falsch.", "fehler")
    elif len(neues_passwort) < 6:
        flash("Das neue Passwort muss mindestens 6 Zeichen lang sein.", "fehler")
    elif neues_passwort != neues_passwort_wiederholen:
        flash("Die Passwörter stimmen nicht überein.", "fehler")
    else:
        current_user.passwort_hash = generate_password_hash(neues_passwort)
        db.session.commit()
        flash("Passwort wurde geändert.", "erfolg")

    return redirect(url_for("konto"))


# ---------------------------------------------------------------
# Kleiderschrank: Übersicht
# ---------------------------------------------------------------
@app.route("/kleiderschrank")
@login_required
def kleiderschrank():
    # Optionaler Filter über die URL, z. B. /kleiderschrank?kategorie=Hosen
    # "Favoriten" ist keine echte Kategorie, sondern filtert über favorit=True
    kategorie = request.args.get("kategorie")
    abfrage = Kleidungsstueck.query.filter_by(besitzer_id=current_user.id)
    if kategorie == "Favoriten":
        abfrage = abfrage.filter_by(favorit=True)
    elif kategorie:
        abfrage = abfrage.filter_by(kategorie=kategorie)
    stuecke = abfrage.order_by(Kleidungsstueck.name).all()

    # Alle Kategorien des Nutzers für die Filter-Buttons sammeln
    kategorien = sorted(
        {s.kategorie for s in current_user.kleidungsstuecke}
    )
    favoriten = sorted(
        (s for s in current_user.kleidungsstuecke if s.favorit),
        key=lambda s: s.name,
    )

    # Ohne aktiven Filter: Stücke pro Kategorie gruppieren (für die
    # nach Kategorie sortierte Übersicht mit den horizontalen Reihen)
    stuecke_nach_kategorie = {}
    if not kategorie:
        for k in kategorien:
            stuecke_nach_kategorie[k] = [s for s in stuecke if s.kategorie == k]

    return render_template(
        "kleiderschrank.html",
        stuecke=stuecke,
        kategorien=kategorien,
        aktive_kategorie=kategorie,
        stuecke_nach_kategorie=stuecke_nach_kategorie,
        favoriten=favoriten,
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
# Kleidungsstück favorisieren / entfavorisieren
# ---------------------------------------------------------------
@app.route("/kleidungsstueck/<int:stueck_id>/favorit", methods=["POST"])
@login_required
def kleidungsstueck_favorit(stueck_id):
    stueck = db.session.get(Kleidungsstueck, stueck_id)
    if stueck is None or stueck.besitzer_id != current_user.id:
        flash("Dieses Kleidungsstück gehört nicht dir.", "fehler")
    else:
        stueck.favorit = not stueck.favorit
        db.session.commit()
    # Zurück zur selben Ansicht (Kategorie-Filter bleibt erhalten)
    return redirect(url_for("kleiderschrank", kategorie=request.form.get("kategorie") or None))


# ---------------------------------------------------------------
# Kleidungsstück bearbeiten (aus dem Detail-Menü im Kleiderschrank)
# ---------------------------------------------------------------
@app.route("/kleidungsstueck/<int:stueck_id>/bearbeiten", methods=["POST"])
@login_required
def kleidungsstueck_bearbeiten(stueck_id):
    stueck = db.session.get(Kleidungsstueck, stueck_id)
    ziel_kategorie = request.form.get("aktive_kategorie") or None

    if stueck is None or stueck.besitzer_id != current_user.id:
        flash("Dieses Kleidungsstück gehört nicht dir.", "fehler")
        return redirect(url_for("kleiderschrank", kategorie=ziel_kategorie))

    name = request.form.get("name", "").strip()
    kategorie = request.form.get("kategorie", "").strip()
    if not name or not kategorie:
        flash("Bitte mindestens Name und Kategorie ausfüllen.", "fehler")
        return redirect(url_for("kleiderschrank", kategorie=ziel_kategorie))

    stueck.name = name
    stueck.kategorie = kategorie
    stueck.farbe = request.form.get("farbe", "").strip()
    stueck.marke = request.form.get("marke", "").strip()
    stueck.groesse = request.form.get("groesse", "").strip()
    stueck.status = request.form.get("status") or "Eigener Artikel"

    kaufdatum_text = request.form.get("kaufdatum", "").strip()
    try:
        stueck.kaufdatum = datetime.strptime(kaufdatum_text, "%Y-%m-%d").date() if kaufdatum_text else None
    except ValueError:
        stueck.kaufdatum = None

    preis_text = request.form.get("preis", "").strip().replace(",", ".")
    try:
        stueck.preis = float(preis_text) if preis_text else None
    except ValueError:
        stueck.preis = None

    db.session.commit()
    flash(f"„{stueck.name}“ wurde aktualisiert.", "erfolg")
    # Falls die Kategorie sich geändert hat, bleibt der alte Filter evtl. leer -
    # dann eben zur neuen Kategorie springen, sonst wirkt die Änderung "verschwunden".
    if ziel_kategorie and ziel_kategorie not in ("Favoriten",) and ziel_kategorie != stueck.kategorie:
        ziel_kategorie = stueck.kategorie
    return redirect(url_for("kleiderschrank", kategorie=ziel_kategorie))


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
# Outfits: Übersicht
# ---------------------------------------------------------------
@app.route("/outfits")
@login_required
def outfits():
    eigene_outfits = Outfit.query.filter_by(besitzer_id=current_user.id) \
        .order_by(Outfit.name).all()
    return render_template("outfits.html", outfits=eigene_outfits)


# ---------------------------------------------------------------
# Outfit zusammenstellen
# ---------------------------------------------------------------
@app.route("/outfits/neu", methods=["GET", "POST"])
@login_required
def outfit_neu():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        stueck_ids = request.form.getlist("stuecke")

        # Nur Stücke übernehmen, die dem Nutzer auch wirklich gehören
        ausgewaehlte_stuecke = Kleidungsstueck.query.filter(
            Kleidungsstueck.id.in_(stueck_ids),
            Kleidungsstueck.besitzer_id == current_user.id,
        ).all()

        if not name:
            flash("Bitte einen Namen für das Outfit angeben.", "fehler")
        elif not ausgewaehlte_stuecke:
            flash("Bitte mindestens ein Kleidungsstück auswählen.", "fehler")
        else:
            outfit = Outfit(name=name, besitzer_id=current_user.id, stuecke=ausgewaehlte_stuecke)
            db.session.add(outfit)
            db.session.commit()
            flash(f"Outfit „{outfit.name}“ wurde erstellt.", "erfolg")
            return redirect(url_for("outfits"))

    # Kleidungsstücke gruppiert nach Kategorie, damit man sie beim
    # Zusammenstellen übersichtlich anhaken kann.
    kategorien = sorted({s.kategorie for s in current_user.kleidungsstuecke})
    stuecke_nach_kategorie = {
        k: [s for s in current_user.kleidungsstuecke if s.kategorie == k]
        for k in kategorien
    }
    return render_template("outfit_form.html", stuecke_nach_kategorie=stuecke_nach_kategorie)


# ---------------------------------------------------------------
# Outfit löschen
# ---------------------------------------------------------------
@app.route("/outfits/<int:outfit_id>/loeschen", methods=["POST"])
@login_required
def outfit_loeschen(outfit_id):
    outfit = db.session.get(Outfit, outfit_id)
    if outfit is None or outfit.besitzer_id != current_user.id:
        flash("Dieses Outfit gehört nicht dir.", "fehler")
    else:
        db.session.delete(outfit)
        db.session.commit()
        flash(f"Outfit „{outfit.name}“ wurde entfernt.", "erfolg")
    return redirect(url_for("outfits"))


# ---------------------------------------------------------------
# Hilfsfunktion: nach einer Folgen-Aktion zurück zur richtigen Seite
# ---------------------------------------------------------------
def zurueck_nach_folgen_aktion(nutzer_id):
    # "von" ist ein verstecktes Formularfeld: entweder die Profilseite des
    # betroffenen Nutzers oder die Freunde-Seite (mit erhaltenem Suchbegriff)
    if request.form.get("von") == "profil":
        return redirect(url_for("nutzer_profil", nutzer_id=nutzer_id))
    return redirect(url_for("freunde", suche=request.form.get("suche") or None))


# ---------------------------------------------------------------
# Freunde: Übersicht & Suche
# ---------------------------------------------------------------
@app.route("/freunde")
@login_required
def freunde():
    suche = request.args.get("suche", "").strip()
    treffer = []
    if suche:
        treffer = User.query.filter(
            User.benutzername.ilike(f"%{suche}%"),
            User.id != current_user.id,
        ).order_by(User.benutzername).limit(20).all()

    # Status meiner eigenen ausgehenden Anfragen: nutzer_id -> akzeptiert?
    eigene_follows = {f.gefolgter_id: f.akzeptiert for f in current_user.folgt}

    return render_template(
        "freunde.html",
        suche=suche,
        treffer=treffer,
        eigene_follows=eigene_follows,
        folgt=[f.gefolgter for f in current_user.folgt if f.akzeptiert],
        anfragen_gesendet=[f.gefolgter for f in current_user.folgt if not f.akzeptiert],
        anfragen_erhalten=[f.folger for f in current_user.gefolgt_von if not f.akzeptiert],
        gefolgt_von=[f.folger for f in current_user.gefolgt_von if f.akzeptiert],
    )


# ---------------------------------------------------------------
# Nutzerprofil: nur Kleiderschrank/Outfits sichtbar, wenn der
# Nutzer die Folge-Anfrage von mir angenommen hat
# ---------------------------------------------------------------
@app.route("/nutzer/<int:nutzer_id>")
@login_required
def nutzer_profil(nutzer_id):
    profil_nutzer = db.session.get(User, nutzer_id)
    if profil_nutzer is None:
        flash("Diesen Nutzer gibt es nicht.", "fehler")
        return redirect(url_for("freunde"))
    if profil_nutzer.id == current_user.id:
        return redirect(url_for("kleiderschrank"))

    ausgehende_anfrage = Follow.query.filter_by(
        folger_id=current_user.id, gefolgter_id=profil_nutzer.id
    ).first()
    eingehende_anfrage = Follow.query.filter_by(
        folger_id=profil_nutzer.id, gefolgter_id=current_user.id
    ).first()
    darf_sehen = bool(ausgehende_anfrage and ausgehende_anfrage.akzeptiert)

    stuecke_nach_kategorie = {}
    outfits_liste = []
    if darf_sehen:
        kategorien = sorted({s.kategorie for s in profil_nutzer.kleidungsstuecke})
        stuecke_nach_kategorie = {
            k: [s for s in profil_nutzer.kleidungsstuecke if s.kategorie == k]
            for k in kategorien
        }
        outfits_liste = sorted(profil_nutzer.outfits, key=lambda o: o.name)

    return render_template(
        "nutzer_profil.html",
        profil_nutzer=profil_nutzer,
        ausgehende_anfrage=ausgehende_anfrage,
        eingehende_anfrage=eingehende_anfrage,
        darf_sehen=darf_sehen,
        stuecke_nach_kategorie=stuecke_nach_kategorie,
        outfits_liste=outfits_liste,
    )


# ---------------------------------------------------------------
# Folge-Anfrage senden / zurückziehen oder entfolgen
# ---------------------------------------------------------------
@app.route("/nutzer/<int:nutzer_id>/folgen", methods=["POST"])
@login_required
def nutzer_folgen(nutzer_id):
    ziel = db.session.get(User, nutzer_id)
    if ziel is None or ziel.id == current_user.id:
        flash("Das geht nicht.", "fehler")
    elif Follow.query.filter_by(folger_id=current_user.id, gefolgter_id=ziel.id).first():
        flash(f"Du hast „{ziel.benutzername}“ schon angefragt oder folgst bereits.", "fehler")
    else:
        db.session.add(Follow(folger_id=current_user.id, gefolgter_id=ziel.id, akzeptiert=False))
        db.session.commit()
        flash(f"Folge-Anfrage an „{ziel.benutzername}“ gesendet.", "erfolg")
    return zurueck_nach_folgen_aktion(nutzer_id)


@app.route("/nutzer/<int:nutzer_id>/entfolgen", methods=["POST"])
@login_required
def nutzer_entfolgen(nutzer_id):
    # Löscht die eigene ausgehende Follow-Zeile – je nach Zustand ist das
    # ein "Entfolgen" (schon akzeptiert) oder ein Zurückziehen der Anfrage.
    folge = Follow.query.filter_by(folger_id=current_user.id, gefolgter_id=nutzer_id).first()
    if folge:
        war_akzeptiert = folge.akzeptiert
        db.session.delete(folge)
        db.session.commit()
        flash("Du folgst diesem Nutzer nicht mehr." if war_akzeptiert
              else "Anfrage zurückgezogen.", "erfolg")
    return zurueck_nach_folgen_aktion(nutzer_id)


# ---------------------------------------------------------------
# Erhaltene Folge-Anfrage annehmen / ablehnen
# ---------------------------------------------------------------
@app.route("/nutzer/<int:nutzer_id>/anfrage/annehmen", methods=["POST"])
@login_required
def folge_anfrage_annehmen(nutzer_id):
    anfrage = Follow.query.filter_by(folger_id=nutzer_id, gefolgter_id=current_user.id).first()
    if anfrage is None:
        flash("Diese Anfrage gibt es nicht (mehr).", "fehler")
    else:
        anfrage.akzeptiert = True
        db.session.commit()
        flash(f"„{anfrage.folger.benutzername}“ folgt dir jetzt.", "erfolg")
    return zurueck_nach_folgen_aktion(nutzer_id)


@app.route("/nutzer/<int:nutzer_id>/anfrage/ablehnen", methods=["POST"])
@login_required
def folge_anfrage_ablehnen(nutzer_id):
    anfrage = Follow.query.filter_by(folger_id=nutzer_id, gefolgter_id=current_user.id).first()
    if anfrage:
        db.session.delete(anfrage)
        db.session.commit()
        flash("Anfrage abgelehnt.", "erfolg")
    return zurueck_nach_folgen_aktion(nutzer_id)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # legt die Datenbank beim ersten Start an
        stelle_profilbild_spalte_sicher()
        stelle_favorit_spalte_sicher()
        stelle_verleih_spalten_sicher()
        stelle_akzeptiert_spalte_sicher()
    app.run(debug=True)
