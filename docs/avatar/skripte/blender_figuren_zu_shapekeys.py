# Sharely: Baut aus den MakeHuman-Exporten eine Figur mit Shape Keys.
#
# So geht's:
#   1. Blender öffnen, oben den Reiter "Scripting" wählen.
#   2. "Open" > diese Datei öffnen (oder Text einfügen), dann "Run Script" (Play-Knopf).
#   3. Ergebnis: Objekt "Avatar" mit Basis = figur_default und je einem Shape Key pro
#      Datei (Name ohne "figur_", z. B. "max_weight"). Die .blend wird im Figuren-Ordner
#      gespeichert (die OBJ-Dateien liegen im Unterordner Formsammlung). Fortschritt erscheint unter Window > Toggle System Console.
#
# Statt jede Datei zu importieren und "Join as Shapes" zu klicken, liest das Skript
# nur die Vertex-Positionen aus den OBJ-Dateien. Das ist viel schneller und
# garantiert dieselbe Vertex-Reihenfolge.

import bpy
import os
import time

FIG_DIR = r"C:\Users\chris\Favorites\Desktop\Abschlussprojekt\Avatar-Editor_Datein\Figuren\Formsammlung"
BASIS_FILE = "figur_default.obj"
PREFIX = "figur_"
ONLY_GROUPS = []   # z. B. ["macrodetails", "torso", "hip", "armslegs", "measure"]; leer = alle
OBJECT_NAME = "Avatar"
SAVE_AS = "avatar_shapekeys.blend"


def read_vertices(path, convert_axes):
    """Vertex-Positionen einer OBJ-Datei. convert_axes: Y-up -> Z-up wie ältere Blender-Importer."""
    coords = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("v "):
                _, x, y, z = line.split()[:4]
                if convert_axes:
                    coords.extend((float(x), -float(z), float(y)))
                else:
                    coords.extend((float(x), float(y), float(z)))
    return coords


def load_groups():
    """Datei -> Regler-Gruppe aus _export_liste.txt (vom MakeHuman-Skript geschrieben)."""
    groups = {}
    path = os.path.join(os.path.dirname(FIG_DIR), "_export_liste.txt")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                parts = line.rstrip("\n").split("\t")
                if len(parts) >= 2:
                    groups[parts[0] + ".obj"] = parts[1].split("/")[0].split("-")[0]
    return groups


def main():
    start = time.time()
    basis_path = os.path.join(FIG_DIR, BASIS_FILE)

    # Ausgangsszene leeren
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    # Basis normal importieren (mit Material und UVs)
    if hasattr(bpy.ops.wm, "obj_import"):
        bpy.ops.wm.obj_import(filepath=basis_path, use_split_objects=False, use_split_groups=False)
    else:
        bpy.ops.import_scene.obj(filepath=basis_path, split_mode="OFF")
    obj = bpy.context.selected_objects[0]
    # Texturen liegen eine Ebene höher (Figuren/textures), nicht neben den OBJ-Dateien
    for img in bpy.data.images:
        tex = os.path.join(os.path.dirname(FIG_DIR), "textures", os.path.basename(img.filepath))
        if img.filepath and os.path.exists(tex):
            img.filepath = tex
    obj.name = OBJECT_NAME
    mesh = obj.data
    n = len(mesh.vertices)

    # Prüfen, dass die Vertex-Reihenfolge beim Import erhalten blieb. Neuere Blender-
    # Versionen drehen das Objekt statt der Vertices, ältere rechnen die Achsen um.
    imported = [0.0] * (n * 3)
    mesh.vertices.foreach_get("co", imported)
    convert_axes = None
    for option in (False, True):
        basis = read_vertices(basis_path, option)
        if len(basis) == len(imported) and max(abs(a - b) for a, b in zip(basis, imported)) < 1e-4:
            convert_axes = option
            break
    if convert_axes is None:
        raise RuntimeError("Vertex-Reihenfolge der Basis passt nicht zum Import (%d Vertices)" % n)

    obj.shape_key_add(name="Basis", from_mix=False)

    files = sorted(f for f in os.listdir(FIG_DIR)
                   if f.startswith(PREFIX) and f.endswith(".obj") and f != BASIS_FILE)
    if ONLY_GROUPS:
        groups = load_groups()
        files = [f for f in files if groups.get(f) in ONLY_GROUPS]

    added, unchanged, broken = 0, [], []
    for i, file_name in enumerate(files, 1):
        coords = read_vertices(os.path.join(FIG_DIR, file_name), convert_axes)
        if len(coords) != len(basis):
            broken.append(file_name)
            continue
        if max(abs(a - b) for a, b in zip(coords, basis)) < 1e-6:
            unchanged.append(file_name)   # Regler verändert die Form nicht
            continue
        key = obj.shape_key_add(name=file_name[len(PREFIX):-4], from_mix=False)
        key.data.foreach_set("co", coords)
        added += 1
        if i % 25 == 0:
            print("%d/%d ..." % (i, len(files)))

    mesh.update()
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(os.path.dirname(FIG_DIR), SAVE_AS))

    print("Fertig in %.0f s: %d Shape Keys" % (time.time() - start, added))
    if unchanged:
        print("Ohne Wirkung (übersprungen): %d, z. B. %s" % (len(unchanged), ", ".join(unchanged[:5])))
    if broken:
        print("Andere Vertex-Zahl (übersprungen): " + ", ".join(broken))


main()
