"""Feste Wertelisten aus dem ERM (docs/datenmodell/ERM-SHARELY.md, Stand 20.10.2026).

Eine Stelle für alle Listen, die sich nur mit einer Code-Änderung ändern:
Die Datenbank-Prüfregeln (app/core/datenbank_struktur.py) nutzen sie, und die
Module (z. B. kleidung/schemas.py) sollen ihre Enums daraus bauen, damit Code
und Datenbank nie auseinanderlaufen.

Schlüssel: klein, ohne Umlaute, mit `_` getrennt. Anzeigenamen stehen daneben.
"""

# Kleidungsart: Pflicht-Einordnung eines Kleidungsstücks („eine Auswahl“), in
# dieser Reihenfolge in Auswahl und Filter. Liegt zusätzlich als Collection
# `kleidungsarten` vor, weil daran die 3D-Vorlage hängt.
KLEIDUNGSARTEN = {
    "tops": "Tops",
    "pullover": "Pullover",
    "hosen": "Hosen",
    "roecke": "Röcke",
    "kleider": "Kleider",
    "jacken": "Jacken",
    "schuhe": "Schuhe",
    "unterwaesche": "Unterwäsche",
    "einteiler": "Einteiler",
    "accessoires": "Accessoires",
}

# Farbe: feste Palette aus dem Mockup „Kleidung filtern“ (Name, Farbwert für die Farbkreise).
FARBEN = {
    "schwarz": ("Schwarz", "#1F1F1F"),
    "weiss": ("Weiß", "#FFFFFF"),
    "grau": ("Grau", "#9E9E9E"),
    "beige": ("Beige", "#E3CBA8"),
    "braun": ("Braun", "#8B5A3C"),
    "rot": ("Rot", "#C8463D"),
    "rosa": ("Rosa", "#F2A7B5"),
    "orange": ("Orange", "#EE8A3A"),
    "gelb": ("Gelb", "#F2C53D"),
    "gruen": ("Grün", "#4E9A5B"),
    "blau": ("Blau", "#3A6FC4"),
    "dunkelblau": ("Dunkelblau", "#2C3A5E"),
    "lila": ("Lila", "#8E5BB5"),
    "bunt": ("Bunt", None),  # Farbverlauf in der Oberfläche
}

MATERIALIEN = {
    "baumwolle": "Baumwolle",
    "polyester": "Polyester",
    "wolle": "Wolle",
    "leinen": "Leinen",
    "seide": "Seide",
    "leder": "Leder",
    "jeans": "Jeans",
    "viskose": "Viskose",
    "sonstiges": "Sonstiges",
}

SAISONS = {
    "fruehling": "Frühling",
    "sommer": "Sommer",
    "herbst": "Herbst",
    "winter": "Winter",
    "ganzjaehrig": "Ganzjährig",
}

# Status eines Kleidungsstücks. „geliehen“: Teil eines Freundes (oder von
# jemandem ohne Sharely) im eigenen Schrank; „verliehen“ setzt nur das Leihen.
STATUS = {
    "im_schrank": "Eigenes",
    "geliehen": "Geliehen",
    "verliehen": "Verliehen",
    "wunsch": "Wunschartikel",
}

# Messpunkte: die 22 Messbänder der Avatar-GLB (docs/avatar/messpunkte.json).
# Maße von Kleidungsstücken werden an denselben Stellen genommen.
MESSPUNKTE = {
    "neck-circ": "Halsumfang",
    "neck-height": "Halslänge",
    "upperarm-circ": "Oberarmumfang",
    "upperarm-length": "Oberarmlänge",
    "lowerarm-length": "Unterarmlänge",
    "wrist-circ": "Handgelenkumfang",
    "frontchest-dist": "Brustbreite vorn",
    "bust-circ": "Brustumfang",
    "underbust-circ": "Unterbrustumfang",
    "waist-circ": "Taillenumfang",
    "napetowaist-dist": "Rückenlänge",
    "waisttohip-dist": "Abstand Taille bis Hüfte",
    "shoulder-dist": "Schulterbreite",
    "hips-circ": "Hüftumfang",
    "upperleg-height": "Oberschenkellänge",
    "thigh-circ": "Oberschenkelumfang",
    "lowerleg-height": "Unterschenkellänge",
    "calf-circ": "Wadenumfang",
    "ankle-circ": "Knöchelumfang",
    "knee-circ": "Knieumfang",
    "schrittlaenge": "Schrittlänge",
    "fusslaenge": "Fußlänge",
    "schulterbreite_ruecken": "Schulterbreite",
    "armlaenge": "Armlänge",
}

# Welche Messpunkte bei einer Kleidungsart abgefragt und für die Passform
# verglichen werden (besprochen mit Christian, 20.10.2026), mit der Zugabe,
# bei der das Teil „passt“ (Startwerte, entschieden von Christian, 26.10.2026;
# Herleitung: docs/datenmodell/ZUGABEN.md).
#   (pflicht, zugabe_min, zugabe_max)
#   pflicht = True: bestimmt die Ampel „passt / eng / weit“; False: nur Hinweis
#   zugabe = Maß Kleidungsstück − Maß Figur, bei Umfängen in Prozent des
#   Körpermaßes, bei Längen in cm (siehe einheit_der_zugabe).
# Liegt zusätzlich in `kleidungsarten.messpunkte`.
MESSPUNKTE_JE_KLEIDUNGSART = {
    "tops": {
        "bust-circ": (True, 4, 15), "waist-circ": (True, 3, 25),
        "schulterbreite_ruecken": (False, -1, 3), "armlaenge": (False, -3, 3), "neck-circ": (False, 2, 6),
        "upperarm-circ": (False, 8, 25), "napetowaist-dist": (False, -2, 6),
    },
    "pullover": {
        "bust-circ": (True, 6, 25), "waist-circ": (True, 5, 35),
        "schulterbreite_ruecken": (False, -1, 6), "armlaenge": (False, -2, 4),
        "upperarm-circ": (False, 10, 35), "napetowaist-dist": (False, -2, 8),
    },
    # Schrittlänge optional, weil Shorts mit unter „Hosen“ fallen. Sie ist
    # negativ, weil das Körpermaß bis zum Boden geht.
    "hosen": {
        "waist-circ": (True, 0, 5), "hips-circ": (True, 3, 15),
        "schrittlaenge": (False, -6, 0), "thigh-circ": (False, 5, 30), "ankle-circ": (False, 0, 100),
    },
    "roecke": {"waist-circ": (True, 0, 5), "hips-circ": (True, 3, 20)},
    "kleider": {
        "bust-circ": (True, 5, 15), "waist-circ": (True, 3, 20), "hips-circ": (True, 4, 25),
        "underbust-circ": (False, 3, 15), "schulterbreite_ruecken": (False, -1, 3),
    },
    "jacken": {
        "bust-circ": (True, 10, 25), "waist-circ": (True, 10, 35),
        "hips-circ": (False, 5, 25), "schulterbreite_ruecken": (False, 0, 4), "armlaenge": (False, 0, 4),
        "upperarm-circ": (False, 25, 45),
    },
    # Innenlänge Schuh = Fußlänge + 1,5 cm (Pariser Stich)
    "schuhe": {"fusslaenge": (True, 1, 2), "calf-circ": (False, 0, 6)},
    # BH und Slip stecken in einer Art, deshalb alles optional
    "unterwaesche": {
        "underbust-circ": (False, -10, 0), "bust-circ": (False, -5, 5),
        "waist-circ": (False, -15, 0), "hips-circ": (False, -15, 0),
    },
    "einteiler": {
        "bust-circ": (True, 5, 20), "waist-circ": (True, 3, 25), "hips-circ": (True, 4, 20),
        "schrittlaenge": (False, -6, 0), "napetowaist-dist": (False, -1, 4),
    },
    "accessoires": {},
}


def einheit_der_zugabe(messpunkt: str) -> str:
    """Umfänge (Schlüssel endet auf -circ) in Prozent, alles andere in cm."""
    return "prozent" if messpunkt.endswith("-circ") else "cm"

# Vorgegebene Kategorien (für alle Nutzer, Nutzer können sie ausblenden und
# eigene ergänzen). Liegen in der Collection `kategorien` mit nutzer_id = null.
VORGEGEBENE_KATEGORIEN = [
    "Business", "Freizeit", "Abend", "Sport", "Party", "Urlaub", "Feiertage",
    "Winterkleidung", "Sommerkleidung", "Lieblingsteile", "Second Hand", "Geschenk",
]

FREUNDSCHAFT_STATUS = ["angefragt", "angenommen", "abgelehnt", "blockiert"]
LEIH_TYPEN = ["leihen", "verschenken"]
LEIH_ANGEFRAGT_VON = ["besitzer", "empfaenger"]
LEIH_STATUS = ["angefragt", "aktiv", "abgelehnt", "zurueckgegeben", "abgeschlossen"]
NEUIGKEIT_TYPEN = ["update", "hinweis", "info"]
IMPORTIERT_PER = ["link", "beschreibung"]
