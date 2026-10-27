"""Pydantic-Modelle des Moduls kleidung: wie Daten in die API hinein- und herauskommen.

Typisch je Objekt: ein Modell zum Anlegen, eins zum Ändern, eins für die Antwort.
Die Felder richten sich nach Manuels ERM vom 20.10.2026
(docs/datenmodell/ERM-SHARELY.md, Abschnitt 3, 6 und 10).
"""

from datetime import date, datetime
from enum import Enum

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator


class Kleidungsart(str, Enum):
    """Pflicht-Einordnung, feste Liste (ERM 20.10.2026). Die Anzeigenamen und
    die 3D-Vorlage kommen später aus der Collection `kleidungsarten`."""

    tops = "tops"
    pullover = "pullover"
    hosen = "hosen"
    roecke = "roecke"
    kleider = "kleider"
    jacken = "jacken"
    schuhe = "schuhe"
    unterwaesche = "unterwaesche"
    einteiler = "einteiler"
    accessoires = "accessoires"


class Farbe(str, Enum):
    schwarz = "schwarz"
    weiss = "weiss"
    grau = "grau"
    beige = "beige"
    braun = "braun"
    rot = "rot"
    rosa = "rosa"
    orange = "orange"
    gelb = "gelb"
    gruen = "gruen"
    blau = "blau"
    dunkelblau = "dunkelblau"
    lila = "lila"
    bunt = "bunt"


class Material(str, Enum):
    baumwolle = "baumwolle"
    polyester = "polyester"
    wolle = "wolle"
    leinen = "leinen"
    seide = "seide"
    leder = "leder"
    jeans = "jeans"
    viskose = "viskose"
    sonstiges = "sonstiges"


class Saison(str, Enum):
    fruehling = "fruehling"
    sommer = "sommer"
    herbst = "herbst"
    winter = "winter"
    ganzjaehrig = "ganzjaehrig"


class Status(str, Enum):
    """Statuswerte laut ERM (Manuel, 20.10.2026). Verschenken ist ein
    Besitzwechsel und deshalb kein Status."""

    im_schrank = "im_schrank"
    geliehen = "geliehen"
    verliehen = "verliehen"
    wunsch = "wunsch"


class StatusBeimAnlegen(str, Enum):
    """Was der Nutzer beim Anlegen wählen darf. „verliehen“ setzt nur das
    Modul verleihen, wenn eine Leihe beginnt."""

    im_schrank = "im_schrank"
    geliehen = "geliehen"
    wunsch = "wunsch"


class Messpunkt(str, Enum):
    """Die 24 Messbänder der Avatar-GLB, Schlüssel wie in
    docs/avatar/messpunkte.json (ein Test prüft, dass beide gleich sind)."""

    neck_circ = "neck-circ"
    neck_height = "neck-height"
    upperarm_circ = "upperarm-circ"
    upperarm_length = "upperarm-length"
    lowerarm_length = "lowerarm-length"
    wrist_circ = "wrist-circ"
    frontchest_dist = "frontchest-dist"
    bust_circ = "bust-circ"
    underbust_circ = "underbust-circ"
    waist_circ = "waist-circ"
    napetowaist_dist = "napetowaist-dist"
    waisttohip_dist = "waisttohip-dist"
    shoulder_dist = "shoulder-dist"
    hips_circ = "hips-circ"
    upperleg_height = "upperleg-height"
    thigh_circ = "thigh-circ"
    lowerleg_height = "lowerleg-height"
    calf_circ = "calf-circ"
    ankle_circ = "ankle-circ"
    knee_circ = "knee-circ"
    schrittlaenge = "schrittlaenge"
    fusslaenge = "fusslaenge"
    schulterbreite_ruecken = "schulterbreite_ruecken"
    armlaenge = "armlaenge"


class Mass(BaseModel):
    """Ein Maß des Kleidungsstücks in cm (ERM: Kleidungsmass)."""

    messpunkt: Messpunkt
    wert_cm: float = Field(gt=0, le=300)

    @field_validator("wert_cm")
    @classmethod
    def auf_mm_runden(cls, wert):
        return round(wert, 1)


class KleidungsstueckAngaben(BaseModel):
    """Eigenschaften eines Kleidungsstücks nach dem ERM vom 20.10.2026.
    Pflicht ist nur die Kleidungsart, dazu kommt beim Anlegen das Foto.
    Ohne Namen zeigt die App die Kleidungsart an."""

    kleidungsart: Kleidungsart
    name: str | None = Field(None, max_length=100)
    favorit: bool = False
    # privat: nur der Nutzer selbst sieht es; sonst auch seine Freunde
    privat: bool = False
    farbe: Farbe | None = None
    material: Material | None = None
    saison: list[Saison] = []
    preis: float | None = Field(None, ge=0, le=100_000, description="in Euro")
    kaufdatum: date | None = None
    # Vorbereitet, noch ohne eigene Logik: Kategorien kommen mit eigenem
    # Modul; ob die IDs existieren und dem Nutzer gehören, prüft erst das.
    kategorie_ids: list[str] = []
    masse: list[Mass] = []

    @field_validator("name", mode="before")
    @classmethod
    def leer_ist_none(cls, wert):
        if isinstance(wert, str):
            wert = wert.strip()
        return wert or None

    @field_validator("preis")
    @classmethod
    def auf_cent_runden(cls, wert):
        return round(wert, 2) if wert is not None else None

    @field_validator("saison")
    @classmethod
    def saison_pruefen(cls, wert):
        wert = list(dict.fromkeys(wert))
        if Saison.ganzjaehrig in wert and len(wert) > 1:
            raise ValueError("„Ganzjährig“ kann nicht mit einzelnen Saisons kombiniert werden.")
        return wert

    @field_validator("kaufdatum")
    @classmethod
    def nicht_in_zukunft(cls, wert):
        if wert is not None and wert > date.today():
            raise ValueError("Das Kaufdatum darf nicht in der Zukunft liegen.")
        return wert

    @field_validator("kategorie_ids")
    @classmethod
    def kategorie_ids_pruefen(cls, wert):
        wert = list(dict.fromkeys(wert))
        for kategorie_id in wert:
            if not ObjectId.is_valid(kategorie_id):
                raise ValueError(f"Ungültige Kategorie-ID: {kategorie_id}")
        return wert

    @field_validator("masse")
    @classmethod
    def je_messpunkt_ein_wert(cls, wert):
        messpunkte = [m.messpunkt for m in wert]
        if len(messpunkte) != len(set(messpunkte)):
            raise ValueError("Jeder Messpunkt darf nur einmal vorkommen.")
        return wert


class KleidungsstueckNeu(KleidungsstueckAngaben):
    """Angaben beim Anlegen: zusätzlich der Status, den der Nutzer wählt."""

    status: StatusBeimAnlegen = StatusBeimAnlegen.im_schrank


class KleidungsstueckAntwort(KleidungsstueckAngaben):
    """Ein Kleidungsstück, wie es die API zurückgibt. Statt des Dateipfads gibt
    es die Adresse, unter der das Bild abgerufen werden kann."""

    id: str
    status: Status
    # setzt nur das System, wenn ein Teil über einen Leihvorgang geliehen ist
    leihvorgang_id: str | None = None
    bild_url: str
    erstellt_am: datetime
