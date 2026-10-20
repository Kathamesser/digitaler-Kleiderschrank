# Avatar-Editor (Three.js)

Machbarkeits-Prototyp hat Vorrang (siehe `CLAUDE.md`). Ablauf:

1. `Avatar_Editorgeruest.glb` mit dem `GLTFLoader` laden.
2. Reglerwerte −100…+100 nach `docs/avatar/AVATAR-REGLER.md` Abschnitt 1 in Morph-Werte umrechnen (`min_…`/`max_…`).
3. Figur mit `OrbitControls` drehbar und zoombar anzeigen.
4. Reglerwerte als Figur über die API speichern (`/api/figuren`, Format: `docs/avatar/FIGUR-DATENMODELL.md`).
