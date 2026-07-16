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
    profilbild = db.Column(db.String(200))                 # Dateiname in static/uploads

    # Beziehung: user.kleidungsstuecke liefert alle Stücke des Nutzers
    kleidungsstuecke = db.relationship(
        "Kleidungsstueck", backref="besitzer", lazy=True,
        cascade="all, delete-orphan",
    )
    outfits = db.relationship(
        "Outfit", backref="besitzer", lazy=True,
        cascade="all, delete-orphan",
    )


class Kleidungsstueck(db.Model):
    """Ein einzelnes Kleidungsstück im digitalen Kleiderschrank."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)      # z. B. "Blaue Levi's 501"
    kategorie = db.Column(db.String(50), nullable=False)  # z. B. "Hosen"
    farbe = db.Column(db.String(30))
    foto = db.Column(db.String(200))                      # Dateiname in static/uploads
    favorit = db.Column(db.Boolean, default=False, nullable=False)
    marke = db.Column(db.String(60))
    groesse = db.Column(db.String(30))
    kaufdatum = db.Column(db.Date)
    preis = db.Column(db.Numeric(8, 2))
    # "Eigener Artikel", "Geliehener Artikel" oder "Verliehener Artikel"
    status = db.Column(db.String(30), default="Eigener Artikel", nullable=False)
    besitzer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


# Zwischentabelle für die "viele zu viele"-Beziehung: ein Outfit besteht aus
# mehreren Kleidungsstücken, und ein Kleidungsstück kann in mehreren
# Outfits stecken.
outfit_stuecke = db.Table(
    "outfit_stuecke",
    db.Column("outfit_id", db.Integer, db.ForeignKey("outfit.id"), primary_key=True),
    db.Column("stueck_id", db.Integer, db.ForeignKey("kleidungsstueck.id"), primary_key=True),
)


class Outfit(db.Model):
    """Eine Zusammenstellung aus mehreren Kleidungsstücken."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    besitzer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # outfit.stuecke liefert alle enthaltenen Kleidungsstücke,
    # stueck.outfits (backref) liefert umgekehrt alle Outfits eines Stücks
    stuecke = db.relationship(
        "Kleidungsstueck", secondary=outfit_stuecke, backref="outfits"
    )


class Follow(db.Model):
    """Ein Nutzer (folger) will einem anderen Nutzer (gefolgter) folgen.
    Erst wenn der Gefolgte die Anfrage annimmt (akzeptiert=True), darf der
    Folger dessen Kleiderschrank/Outfits sehen. Folgen sich zwei Nutzer
    gegenseitig, entstehen einfach zwei unabhängige Follow-Zeilen."""
    id = db.Column(db.Integer, primary_key=True)
    folger_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    gefolgter_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    akzeptiert = db.Column(db.Boolean, default=False, nullable=False)

    # user.folgt          -> Follow-Zeilen, in denen der Nutzer der Folger ist
    # user.gefolgt_von     -> Follow-Zeilen, in denen der Nutzer der Gefolgte ist
    folger = db.relationship(
        "User", foreign_keys=[folger_id],
        backref=db.backref("folgt", lazy=True, cascade="all, delete-orphan"),
    )
    gefolgter = db.relationship(
        "User", foreign_keys=[gefolgter_id],
        backref=db.backref("gefolgt_von", lazy=True, cascade="all, delete-orphan"),
    )

    __table_args__ = (
        db.UniqueConstraint("folger_id", "gefolgter_id", name="eindeutige_folge"),
    )
