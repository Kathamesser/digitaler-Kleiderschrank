# Sharely: Misst die Körpermaße des Avatars in Zentimetern.
#
# Aufruf (Python 3 mit numpy, kein Blender nötig), im Repo-Ordner:
#   python docs/avatar/skripte/zentimeter_messen.py
# Ohne Angaben nimmt es Sharely_programm/assets/avatar/Avatar_Editorgeruest.glb und
# Sharely_programm/assets/avatar/werkstatt/figur_default.obj und schreibt nach docs/avatar/,
# messpunkte.json zusätzlich als Kopie neben die GLB (für den Avatar-Konfigurator).
# Andere Dateien: python zentimeter_messen.py <glb> <figur_default.obj> <Ausgabeordner>
#
# Ergebnis im Ausgabeordner:
#   messpunkte.json         Messbänder als Vertex-Indizes der GLB (für den Editor)
#   ZENTIMETER-TABELLE.md   cm-Werte der Standardfigur und Wirkung jedes Targets
#
# Die Messbänder stammen aus MakeHuman (plugins/0_modeling_a_measurement.py, Klasse
# Ruler). Dort sind sie als Vertex-Nummern des MakeHuman-Grundmodells angegeben. Diese
# Nummern gelten auch in unserer OBJ-Datei figur_default.obj. In der GLB ist die
# Reihenfolge eine andere. Deshalb sucht das Skript jeden Punkt über seine Position
# in der GLB und schreibt die GLB-Indizes in messpunkte.json. Wird die GLB neu gebaut,
# muss dieses Skript noch einmal laufen.

import json
import os
import struct
import sys

import numpy as np

# MakeHuman-Vertex-Nummern je Maß (aus MakeHuman 1.x, Ruler.Measures)
MH_RULER = {
    "neck-circ": [7514,10358,7631,7496,7488,7489,7474,7475,7531,7537,7543,7549,7555,7561,7743,7722,856,1030,1051,850,844,838,832,826,820,756,755,770,769,777,929,3690,804,800,808,801,799,803,7513,7515,7521,7514],
    "neck-height": [853,854,855,856,857,858,1496,1491],
    "upperarm-circ": [8383,8393,8392,8391,8390,8394,8395,8399,10455,10516,8396,8397,8398,8388,8387,8386,10431,8385,8384,8389],
    "upperarm-length": [8274,10037],
    "lowerarm-length": [10040,10548],
    "wrist-circ": [10208,10211,10212,10216,10471,10533,10213,10214,10215,10205,10204,10203,10437,10202,10201,10206,10200,10210,10209,10208],
    "frontchest-dist": [1437,8125],
    "bust-circ": [8439,8455,8462,8446,8478,8494,8557,8510,8526,8542,10720,10601,10603,10602,10612,10611,10610,10613,10604,10605,10606,3942,3941,3940,3950,3947,3948,3949,3938,3939,3937,4065,1870,1854,1838,1885,1822,1806,1774,1790,1783,1767,1799,8471],
    "underbust-circ": [10750,10744,10724,10725,10748,10722,10640,10642,10641,10651,10650,10649,10652,10643,10644,10645,10646,10647,10648,3988,3987,3986,3985,3984,3983,3982,3992,3989,3990,3991,3980,3981,3979,4067,4098,4073,4072,4094,4100,4082,4088,4088],
    "waist-circ": [4121,10760,10757,10777,10776,10779,10780,10778,10781,10771,10773,10772,10775,10774,10814,10834,10816,10817,10818,10819,10820,10821,4181,4180,4179,4178,4177,4176,4175,4196,4173,4131,4132,4129,4130,4128,4138,4135,4137,4136,4133,4134,4108,4113,4118,4121],
    "napetowaist-dist": [1491,4181],
    "waisttohip-dist": [4121,4341],
    "shoulder-dist": [7478,8274],
    "hips-circ": [4341,10968,10969,10971,10970,10967,10928,10927,10925,10926,10923,10924,10868,10875,10861,10862,4228,4227,4226,4242,4234,4294,4293,4296,4295,4297,4298,4342,4345,4346,4344,4343,4361,4341],
    "upperleg-height": [10970,11230],
    "thigh-circ": [11071,11080,11081,11086,11076,11077,11074,11075,11072,11073,11069,11070,11087,11085,11084,12994,11083,11082,11079,11071],
    "lowerleg-height": [11225,12820],
    "calf-circ": [11339,11336,11353,11351,11350,13008,11349,11348,11345,11337,11344,11346,11347,11352,11342,11343,11340,11341,11338,11339],
    "ankle-circ": [11460,11464,11458,11459,11419,11418,12958,12965,12960,12963,12961,12962,12964,12927,13028,12957,11463,11461,11457,11460],
    "knee-circ": [11223,11230,11232,11233,11238,11228,11229,11226,11227,11224,11225,11221,11222,11239,11237,11236,13002,11235,11234,11223],
}

# Eigene Ergänzungen für Hosen und Schuhe (MakeHuman-Vertex-Nummern, am Modell gewählt)
EXTRA = {
    "schrittlaenge": [4372],        # tiefster Punkt im Schritt; Maß = Höhe über dem Boden
    "fusslaenge": [12453, 11551],   # linke Ferse, linke Zehenspitze; Maß = Abstand in Laufrichtung
    # rechter Schulterpunkt (8274) über den Rücken zum linken (1602, Spiegelpunkt); Maß = straffes Band
    "schulterbreite_ruecken": [8274, 8273, 8237, 8243, 8249, 8229, 8227, 8228, 1550, 1549, 1548, 1551, 1571, 1565, 1559, 1601, 1602],
    "armlaenge": [8274, 10037, 10548],  # Schulterpunkt, Ellbogen, Handgelenk; Maß = Ärmellänge
}

# Anzeige: Schlüssel -> (deutscher Name, Art, Reglerschlüssel aus FIGUR-DATENMODELL.md)
INFO = {
    "koerpergroesse": ("Körpergröße", "hoehe", "koerpergroesse"),
    "neck-circ": ("Halsumfang", "umfang", "halsumfang"),
    "neck-height": ("Halslänge", "laenge", "halslaenge"),
    "shoulder-dist": ("Schulterbreite (eine Seite, Hals bis Schulter)", "laenge", "schulterbreite"),
    "frontchest-dist": ("Brustbreite vorn", "laenge", "brustbreite_vorn"),
    "bust-circ": ("Brustumfang", "umfang", "brustumfang"),
    "underbust-circ": ("Unterbrustumfang", "umfang", "unterbrustumfang"),
    "waist-circ": ("Taillenumfang", "umfang", "taillenumfang"),
    "hips-circ": ("Hüftumfang", "umfang", "hueftumfang"),
    "napetowaist-dist": ("Rückenlänge", "laenge", "rueckenlaenge"),
    "waisttohip-dist": ("Abstand Taille bis Hüfte", "laenge", "abstand_taille_huefte"),
    "upperarm-circ": ("Oberarmumfang", "umfang", "oberarmumfang"),
    "upperarm-length": ("Oberarmlänge", "laenge", "oberarmlaenge"),
    "lowerarm-length": ("Unterarmlänge", "laenge", "unterarmlaenge"),
    "wrist-circ": ("Handgelenkumfang", "umfang", "handgelenkumfang"),
    "thigh-circ": ("Oberschenkelumfang", "umfang", "oberschenkelumfang"),
    "knee-circ": ("Knieumfang", "umfang", "knieumfang"),
    "calf-circ": ("Wadenumfang", "umfang", "wadenumfang"),
    "ankle-circ": ("Knöchelumfang", "umfang", "knoechelumfang"),
    "upperleg-height": ("Oberschenkellänge", "laenge", "oberschenkellaenge_mass"),
    "lowerleg-height": ("Unterschenkellänge", "laenge", "unterschenkellaenge_mass"),
    "schrittlaenge": ("Schrittlänge (Innenbein)", "hoehe_punkt", None),
    "fusslaenge": ("Fußlänge", "fuss", None),
    "schulterbreite_ruecken": ("Schulterbreite (über den Rücken, Schulterpunkt bis Schulterpunkt)", "bogen", None),
    "armlaenge": ("Armlänge (Schulterpunkt über Ellbogen bis Handgelenk)", "laenge", None),
}

# Für die Tabelle: welche Maße als Spalten in der Wirkungstabelle stehen
SPALTEN = ["koerpergroesse", "bust-circ", "underbust-circ", "waist-circ", "hips-circ",
           "neck-circ", "thigh-circ", "schulterbreite_ruecken", "armlaenge", "schrittlaenge", "fusslaenge"]


def load_glb(path):
    b = open(path, "rb").read()
    n = struct.unpack("<I", b[12:16])[0]
    J = json.loads(b[20:20 + n])
    o = 20 + n
    bl = struct.unpack("<I", b[o:o + 4])[0]
    B = b[o + 8:o + 8 + bl]

    def acc(i):
        a = J["accessors"][i]
        if "bufferView" in a:
            bv = J["bufferViews"][a["bufferView"]]
            off = bv.get("byteOffset", 0) + a.get("byteOffset", 0)
            arr = np.frombuffer(B, np.float32, a["count"] * 3, off).reshape(-1, 3).copy()
        else:
            arr = np.zeros((a["count"], 3), np.float32)
        if "sparse" in a:
            s = a["sparse"]
            it = {5121: np.uint8, 5123: np.uint16, 5125: np.uint32}[s["indices"]["componentType"]]
            ib = J["bufferViews"][s["indices"]["bufferView"]]
            idx = np.frombuffer(B, it, s["count"], ib.get("byteOffset", 0) + s["indices"].get("byteOffset", 0))
            vb = J["bufferViews"][s["values"]["bufferView"]]
            val = np.frombuffer(B, np.float32, s["count"] * 3, vb.get("byteOffset", 0) + s["values"].get("byteOffset", 0))
            arr[idx] = val.reshape(-1, 3)
        return arr

    mesh = J["meshes"][0]
    names = mesh["extras"]["targetNames"]
    prim = mesh["primitives"][0]   # Körper; [1] sind die Augen
    pos = acc(prim["attributes"]["POSITION"])
    targets = [acc(t["POSITION"]) for t in prim["targets"]]
    return pos, names, targets


def load_obj(path):
    return np.array([list(map(float, l.split()[1:4])) for l in open(path, encoding="utf-8") if l.startswith("v ")])


def hull_perimeter(pts):
    """Umfang wie ein straff angelegtes Maßband: konvexe Hülle in der Ebene des Bands."""
    c = pts.mean(0)
    _, _, vt = np.linalg.svd(pts - c)
    q = sorted(map(tuple, (pts - c) @ vt[:2].T))

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lo, up = [], []
    for p in q:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(q):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    h = np.array(lo[:-1] + up[:-1])
    return float(np.linalg.norm(np.diff(np.vstack([h, h[:1]]), axis=0), axis=1).sum())


def measure(X, rings):
    out = {"koerpergroesse": float(X[:, 1].max() - X[:, 1].min()) * 100}
    floor = X[:, 1].min()
    for k, idx in rings.items():
        art = INFO[k][1]
        p = X[idx]
        if art == "umfang":
            v = hull_perimeter(p)
        elif art == "bogen":  # offenes Band über eine Wölbung: straff gespannt, ohne die Sehne
            v = hull_perimeter(p) - float(np.linalg.norm(p[-1] - p[0]))
        elif art == "laenge":
            v = float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum())
        elif art == "hoehe_punkt":
            v = float(p[0, 1] - floor)
        elif art == "fuss":
            v = float(abs(p[1, 2] - p[0, 2]))
        out[k] = v * 100
    return out


def main(glb, obj, outdir):
    pos, names, targets = load_glb(glb)
    base = load_obj(obj)
    rings, mh = {}, {}
    for k, idx in list(MH_RULER.items()) + list(EXTRA.items()):
        gl = []
        for i in idx:
            d = np.linalg.norm(pos - base[i], axis=1)
            j = int(d.argmin())
            if d[j] > 1e-5:
                sys.exit(f"Punkt {i} von {k} nicht in der GLB gefunden (Abstand {d[j]:.6f} m)")
            gl.append(j)
        rings[k], mh[k] = gl, idx

    default = measure(pos, rings)
    effect = {}
    for t, n in enumerate(names):
        m = measure(pos + targets[t], rings)
        effect[n] = {k: round(m[k] - default[k], 1) for k in m}

    data = {
        "beschreibung": "Messbänder für Avatar_Editorgeruest.glb. Indizes beziehen sich auf das erste Primitive (Körper). Erzeugt von docs/avatar/skripte/zentimeter_messen.py.",
        "einheit_modell": "Meter",
        "masse": {
            k: {"name": INFO[k][0], "art": INFO[k][1], "regler": INFO[k][2],
                "glb_vertices": rings[k], "makehuman_vertices": mh[k],
                "standardfigur_cm": round(default[k], 1)}
            for k in rings
        },
        "koerpergroesse": {"name": "Körpergröße", "art": "hoehe", "regler": "koerpergroesse",
                           "standardfigur_cm": round(default["koerpergroesse"], 1)},
        "wirkung_je_target_cm": effect,
    }
    json.dump(data, open(f"{outdir}/messpunkte.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # Kopie neben der GLB für den Avatar-Konfigurator im Browser (der Seiten-Server sieht docs/ nicht)
    editor_kopie = os.path.join(os.path.dirname(os.path.abspath(glb)), "messpunkte.json")
    json.dump(data, open(editor_kopie, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    L = ["# Zentimeter-Tabelle (automatisch erzeugt)", "",
         "Erzeugt von `skripte/zentimeter_messen.py` aus `Avatar_Editorgeruest.glb`. Nicht von Hand ändern, sondern das Skript neu laufen lassen. Erklärung in `ZENTIMETER.md`.", "",
         "## Standardfigur (alle Regler auf 0)", "", "| Maß | cm |", "|---|---|"]
    for k in ["koerpergroesse"] + list(rings):
        L.append(f"| {INFO[k][0]} | {default[k]:.1f} |")
    L += ["", "## Wirkung der Targets bei voller Stärke (UI-Wert ±100)", "",
          "Änderung in cm gegenüber der Standardfigur. Nur Targets, die mindestens eines dieser Maße um 0,5 cm oder mehr ändern.", "",
          "| Target | " + " | ".join(INFO[k][0].split(" (")[0] for k in SPALTEN) + " |",
          "|---|" + "---|" * len(SPALTEN)]
    for n in names:
        e = effect[n]
        if max(abs(e[k]) for k in SPALTEN) < 0.5:
            continue
        L.append(f"| `{n}` | " + " | ".join(f"{e[k]:+.1f}" for k in SPALTEN) + " |")
    open(f"{outdir}/ZENTIMETER-TABELLE.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("fertig:", len(rings), "Messbänder,", len(names), "Targets")


if __name__ == "__main__":
    if len(sys.argv) == 4:
        main(*sys.argv[1:])
    elif len(sys.argv) == 1:
        repo = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
        main(os.path.join(repo, "Sharely_programm", "assets", "avatar", "Avatar_Editorgeruest.glb"),
             os.path.join(repo, "Sharely_programm", "assets", "avatar", "werkstatt", "figur_default.obj"),
             os.path.join(repo, "docs", "avatar"))
    else:
        sys.exit("Aufruf: python zentimeter_messen.py [<glb> <figur_default.obj> <ausgabeordner>]")
