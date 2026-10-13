"""Pydantic-Modelle des Moduls kleidung: wie Daten in die API hinein- und herauskommen.

Typisch je Objekt: ein Modell zum Anlegen, eins zum Ändern, eins für die Antwort.
Die Felder richten sich nach dem Datenmodell in docs/datenmodell/.
"""

from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class Kategorie(str, Enum):
    """Vorläufige feste Liste (Wireframes/User Stories). Ob Liste oder eigene
    Collection, entscheidet das ERM; dann wird nur diese Klasse ersetzt."""

    oberteile = "oberteile"
    hosen = "hosen"
    roecke = "roecke"
    kleider = "kleider"
    jacken = "jacken"
    schuhe = "schuhe"
    accessoires = "accessoires"


class Saison(str, Enum):
    fruehling = "fruehling"
    sommer = "sommer"
    herbst = "herbst"
    winter = "winter"


class Anlass(str, Enum):
    alltag = "alltag"
    sport = "sport"
    edel = "edel"


class Herkunft(str, Enum):
    laden = "laden"
    flohmarkt = "flohmarkt"
    online = "online"


class Status(str, Enum):
    """Statuswerte laut ERM (Manuel, 13.10.2026). „wunsch“ und „archiviert“
    kommen erst mit Wunschliste bzw. Archiv dazu."""

    im_schrank = "im_schrank"
    verliehen = "verliehen"
    verschenkt = "verschenkt"


class KleidungsstueckAngaben(BaseModel):
    """Eigenschaften eines Kleidungsstücks (Festlegung Katha, 13.10.2026).
    Pflicht ist nur die Kategorie, dazu kommt beim Anlegen das Foto."""

    kategorie: Kategorie
    favorit: bool = False
    # privat: nur der Nutzer selbst sieht es; sonst auch seine Freunde
    privat: bool = False
    groesse: str | None = Field(None, max_length=20)
    marke: str | None = Field(None, max_length=50)
    farbe: str | None = Field(None, max_length=50)
    material: str | None = Field(None, max_length=100)
    saison: list[Saison] = []
    anlass: list[Anlass] = []
    preis: float | None = Field(None, ge=0, le=100_000, description="in Euro")
    kaufdatum: date | None = None
    herkunft: Herkunft | None = None
    notiz: str | None = Field(None, max_length=1000)

    @field_validator("groesse", "marke", "farbe", "material", "notiz", mode="before")
    @classmethod
    def leer_ist_none(cls, wert):
        if isinstance(wert, str):
            wert = wert.strip()
        return wert or None

    @field_validator("preis")
    @classmethod
    def auf_cent_runden(cls, wert):
        return round(wert, 2) if wert is not None else None

    @field_validator("saison", "anlass")
    @classmethod
    def ohne_doppelte(cls, wert):
        return list(dict.fromkeys(wert))

    @field_validator("kaufdatum")
    @classmethod
    def nicht_in_zukunft(cls, wert):
        if wert is not None and wert > date.today():
            raise ValueError("Das Kaufdatum darf nicht in der Zukunft liegen.")
        return wert


class KleidungsstueckAntwort(KleidungsstueckAngaben):
    """Ein Kleidungsstück, wie es die API zurückgibt. Statt des Dateipfads gibt
    es die Adresse, unter der das Bild abgerufen werden kann."""

    id: str
    status: Status
    bild_url: str
    erstellt_am: datetime
