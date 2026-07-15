# =============================================================
# models.py – Datenbankmodelle (Tabellen als Python-Klassen)
# =============================================================
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """Ein Nutzerkonto. UserMixin gibt der Klasse alles,
    was Flask-Login braucht (is_authenticated, get_id, ...)."""
    id = db.Column(db.Integer, primary_key=True)
    benutzername = db.Column(db.String(50), unique=True, nullable=False)
    passwort_hash = db.Column(db.String(200), nullable=False)

    # Beziehung: user.kleidungsstuecke liefert alle Stücke des Nutzers
    kleidungsstuecke = db.relationship(
        "Kleidungsstueck", backref="besitzer", lazy=True,
        cascade="all, delete-orphan",
    )


class Kleidungsstueck(db.Model):
    """Ein einzelnes Kleidungsstück im digitalen Kleiderschrank."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)      # z. B. "Blaue Levi's 501"
    kategorie = db.Column(db.String(50), nullable=False)  # z. B. "Hosen"
    farbe = db.Column(db.String(30))
    foto = db.Column(db.String(200))                      # Dateiname in static/uploads
    besitzer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # TODO (Must-have "Favorisieren"):
    # favorit = db.Column(db.Boolean, default=False)

    # TODO (Must-have "Verleihen"): merkt sich, bei wem das Stück gerade ist.
    # verliehen_an_id = db.Column(db.Integer, db.ForeignKey("user.id"))


# =============================================================
# TODO für später – so könnten die nächsten Modelle aussehen:
#
# class Outfit(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     besitzer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     # Ein Outfit besteht aus mehreren Kleidungsstücken und ein
#     # Kleidungsstück kann in mehreren Outfits sein
#     # -> "viele zu viele"-Beziehung über eine Zwischentabelle.
#
# class Freundschaft(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nutzer_a_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     nutzer_b_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     bestaetigt = db.Column(db.Boolean, default=False)
# =============================================================
