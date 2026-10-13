# Sharely: Exportiert jeden MakeHuman-Regler einzeln als Min- und Max-Figur (OBJ).
#
# So geht's:
#   1. In MakeHuman die Standardfigur einstellen (wie figur_default).
#   2. Unter Files > Export einmal "Wavefront obj" wählen und die Optionen setzen
#      (Meter, Feet on Ground an, Normals aus, Helper geometry aus).
#      Das Skript übernimmt genau diese Einstellungen.
#   3. Utilities > Scripting: diesen Text einfügen, dann Tab "Execute" > "Execute".
#
# Vor jedem Export wird die Ausgangsfigur neu geladen (statt Reset), damit immer
# nur ein Regler verändert ist und Augen/Material erhalten bleiben.
# Dateien heißen figur_min_<regler>.obj / figur_max_<regler>.obj.
# Hinweis: Keine eigenen Funktionen definieren, der Scripting-Tab führt den Code
# per exec() aus, dort sehen Funktionen die Variablen des Skripts nicht.

import os
import tempfile
from core import G

OUT_DIR = r"C:\Users\chris\Favorites\Desktop\Abschlussprojekt\Avatar-Editor_Datein\Figuren\Formsammlung"
PREFIX = "figur"
SKIP_EXISTING = True   # schon vorhandene Dateien nicht neu exportieren
ONLY_GROUPS = []       # z. B. ["macrodetails", "torso", "legs"]; leer = alle Gruppen
SKIP_GROUPS = []       # z. B. ["eyes", "mouth", "nose", "ears"]
DRY_RUN = False        # True = nur auflisten, nichts exportieren

human = G.app.selectedHuman
exporter = G.app.getTask('Files', 'Export').getExporter('Wavefront obj')

base_mhm = os.path.join(tempfile.gettempdir(), 'stylehub_ausgangsfigur.mhm')
human.save(base_mhm)
start_values = dict((m.fullName, m.getValue()) for m in human.modifiers)

jobs = []
for m in sorted(human.modifiers, key=lambda x: x.fullName):
    group = m.groupName.split('-')[0]
    if ONLY_GROUPS and group not in ONLY_GROUPS:
        continue
    if group in SKIP_GROUPS:
        continue
    if m.groupName.startswith('macrodetails'):
        short = m.name.lower()                      # gender, weight, muscle, ...
    else:
        short = m.name.replace('|', '-')
        if short.startswith(m.groupName + '-'):
            short = short[len(m.groupName) + 1:]
        short = (m.groupName + '_' + short).lower()  # z. B. torso_scale-depth-decr-incr
    for label, value in (('min', m.getMin()), ('max', m.getMax())):
        if abs(value - start_values[m.fullName]) < 1e-6:
            continue                                 # einseitiger Regler, kein Extrem in diese Richtung
        jobs.append((m.fullName, value, '%s_%s_%s' % (PREFIX, label, short)))

print('%d Exporte geplant' % len(jobs))
exported = []
skipped = []
for full_name, value, file_base in jobs:
    path_base = os.path.join(OUT_DIR, file_base)
    if SKIP_EXISTING and os.path.exists(path_base + '.obj'):
        skipped.append(file_base)
        continue
    if DRY_RUN:
        print('  ' + file_base)
        continue
    human.load(base_mhm, update=False)
    human.getModifier(full_name).setValue(value)
    human.applyAllTargets()
    exporter.export(human, lambda ext, different=False, p=path_base: p + '.' + ext)
    exported.append(file_base)
    print('exportiert: %s (%s = %s)' % (file_base, full_name, value))

human.load(base_mhm, update=True)

with open(os.path.join(os.path.dirname(OUT_DIR), '_export_liste.txt'), 'w') as f:
    for full_name, value, file_base in jobs:
        f.write('%s\t%s\t%s\n' % (file_base, full_name, value))

print('Fertig: %d exportiert, %d übersprungen (gab es schon).' % (len(exported), len(skipped)))
