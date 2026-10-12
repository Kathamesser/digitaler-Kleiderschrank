# StyleHUB: Baut aus avatar_shapekeys.blend (alle 547 Shape Keys)
#   1. Avatar_Editorgeruest.glb  -> Auswahl für den Web-Editor (siehe regler-auswahl.md)
#   2. Avatar_Aussehen_spaeter/  -> alle übrigen Shape Keys als .blend für später
# Linke/rechte Regler (l-/r-) werden im Editorgerüst zu einem Key zusammengelegt.
# Aufruf in Blender (Scripting-Tab) oder: blender -b --python blender_editorgeruest_bauen.py

import bpy
import os
import re
import numpy as np

FIG_DIR = r"C:\Users\chris\Favorites\Desktop\Abschlussprojekt\Avatar-Editor_Datein\Figuren"
OUT_DIR = FIG_DIR
SOURCE = os.path.join(FIG_DIR, "avatar_shapekeys.blend")
GLB_PATH = os.path.join(OUT_DIR, "Avatar_Editorgeruest.glb")
LATER_DIR = os.path.join(OUT_DIR, "Avatar_Aussehen_spaeter")
LATER_BLEND = os.path.join(LATER_DIR, "Avatar_Aussehen_spaeter.blend")

MACRO = ["gender", "age", "weight", "muscle", "height", "bodyproportions"]
SINGLE = [  # Regler ohne Seite (jeweils min_ und max_)
    "torso_scale-horiz-decr-incr", "torso_scale-depth-decr-incr", "torso_scale-vert-decr-incr",
    "torso_vshape-decr-incr", "torso_muscle-pectoral-decr-incr", "torso_muscle-dorsi-decr-incr",
    "hip_scale-horiz-decr-incr", "hip_scale-depth-decr-incr", "hip_scale-vert-decr-incr",
    "hip_waist-down-up", "stomach_pregnant-decr-incr", "buttocks_volume-decr-incr",
    "breast_breastsize", "breast_breastfirmness",
    "armslegs_upperlegs-height-decr-incr", "armslegs_lowerlegs-height-decr-incr",
]
SIDED = [  # armslegs_l-... und armslegs_r-... werden zusammengelegt
    "foot-scale-decr-incr", "upperarm-fat-decr-incr", "upperleg-fat-decr-incr",
    "lowerleg-fat-decr-incr", "leg-valgus-decr-incr",
]

bpy.ops.wm.open_mainfile(filepath=SOURCE)
src = bpy.data.objects["Avatar"]
keys = src.data.shape_keys.key_blocks
names = [k.name for k in keys][1:]
n = len(src.data.vertices)


def co(key_name):
    a = np.empty(n * 3, dtype=np.float32)
    keys[key_name].data.foreach_get("co", a)
    return a


basis = co("Basis")

# --- Auswahl bestimmen --------------------------------------------------------
plain = []
for m in MACRO + SINGLE:
    plain += [d + "_" + m for d in ("min", "max") if d + "_" + m in keys]
plain += [k for k in names if re.match(r"(min|max)_measure_", k)]
plain += [k for k in names if k.startswith("max_bodyshapes_")]
merged = []   # (neuer Name, linker Key, rechter Key)
for s in SIDED:
    for d in ("min", "max"):
        merged.append(("%s_armslegs_%s" % (d, s),
                       "%s_armslegs_l-%s" % (d, s), "%s_armslegs_r-%s" % (d, s)))
missing = [k for k in plain if k not in keys] + [x for _, l, r in merged for x in (l, r) if x not in keys]
if missing:
    raise RuntimeError("Fehlende Shape Keys: " + ", ".join(missing))
used = set(plain) | {x for _, l, r in merged for x in (l, r)}
later = [k for k in names if k not in used]

# Deltas vorab sichern, bevor Keys gelöscht werden
editor_data = [(k, co(k)) for k in plain]
editor_data += [(name, co(l) + co(r) - basis) for name, l, r in merged]
later_data = [(k, co(k)) for k in later]


def build(name, data):
    obj = src.copy()
    obj.data = src.data.copy()
    obj.name = name
    bpy.context.scene.collection.objects.link(obj)
    obj.shape_key_clear()
    obj.shape_key_add(name="Basis", from_mix=False)
    for key_name, coords in data:
        key = obj.shape_key_add(name=key_name, from_mix=False)
        key.data.foreach_set("co", coords)
        key.value = 0.0   # Startwert: neutrale Figur (figur_default); sonst landet 1 im GLB
    return obj


editor = build("Avatar_Editorgeruest", editor_data)
aussehen = build("Avatar_Aussehen_spaeter", later_data)
bpy.data.objects.remove(src)

# --- 1. GLB für den Editor ------------------------------------------------------
for o in bpy.data.objects:
    o.select_set(o == editor)
bpy.context.view_layer.objects.active = editor
# Glatt schattieren: sonst teilt der Export jede Fläche in eigene Vertices (4x so groß)
for p in editor.data.polygons:
    p.use_smooth = True
# Drehung vom OBJ-Import in die Vertices übernehmen, damit der Knoten im GLB neutral ist
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
bpy.ops.export_scene.gltf(
    filepath=GLB_PATH, export_format="GLB", use_selection=True,
    export_morph=True, export_morph_normal=False, export_apply=False,
)

# --- 2. Rest für später ----------------------------------------------------------
os.makedirs(LATER_DIR, exist_ok=True)
bpy.data.objects.remove(editor)
for img in bpy.data.images:   # Texturpfad relativ zum Unterordner anpassen
    if img.filepath.startswith("//textures"):
        img.filepath = "//../" + img.filepath[2:]
bpy.ops.wm.save_as_mainfile(filepath=LATER_BLEND, relative_remap=False)
with open(os.path.join(LATER_DIR, "Shape_Keys_Liste.txt"), "w", encoding="utf-8") as f:
    f.write("Shape Keys in Avatar_Aussehen_spaeter.blend (%d)\n" % len(later))
    f.write("Quelle: Figuren/avatar_shapekeys.blend, Basis = figur_default\n\n")
    f.write("\n".join(later) + "\n")

print("Editorgerüst: %d Shape Keys -> %s" % (len(editor_data), GLB_PATH))
print("Für später: %d Shape Keys -> %s" % (len(later), LATER_BLEND))
