"""Pydantic-Modelle des Moduls kleidung: wie Daten in die API hinein- und herauskommen.

Typisch je Objekt: ein Modell zum Anlegen, eins zum Ändern, eins für die Antwort.
Die Felder richten sich nach dem Datenmodell in docs/datenmodell/.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Kategorie(str, Enum):
    """Vorläufige feste Liste (Wireframes/User Stories). Ob Liste oder eigene
    Collection, entscheidet das ERM; dann wird nur diese Klasse ersetzt."""

    oberteile = "oberteile"
    hosen = "hosen"
    roecke_kleider = "roecke_kleider"
    jacken = "jacken"
    schuhe = "schuhe"
    accessoires = "accessoires"


class Status(str, Enum):
    aktiv = "aktiv"
    verliehen = "verliehen"
    verschenkt = "verschenkt"


class KleidungsstueckAntwort(BaseModel):
    """Ein Kleidungsstück, wie es die API zurückgibt. Statt des Dateipfads gibt
    es die Adresse, unter der das Bild abgerufen werden kann."""

    id: str
    name: str
    kategorie: Kategorie
    farbe: str | None = None
    groesse: str | None = None
    favorit: bool
    status: Status
    bild_url: str
    erstellt_am: datetime
