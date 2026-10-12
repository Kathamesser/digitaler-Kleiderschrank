# Zentimeter-Tabelle (automatisch erzeugt)

Erzeugt von `skripte/zentimeter_messen.py` aus `Avatar_Editorgeruest.glb`. Nicht von Hand ändern, sondern das Skript neu laufen lassen. Erklärung in `ZENTIMETER.md`.

## Standardfigur (alle Regler auf 0)

| Maß | cm |
|---|---|
| Körpergröße | 165.9 |
| Halsumfang | 32.6 |
| Halslänge | 9.9 |
| Oberarmumfang | 26.8 |
| Oberarmlänge | 27.2 |
| Unterarmlänge | 23.2 |
| Handgelenkumfang | 13.6 |
| Brustbreite vorn | 29.2 |
| Brustumfang | 86.6 |
| Unterbrustumfang | 75.2 |
| Taillenumfang | 72.4 |
| Rückenlänge | 37.4 |
| Abstand Taille bis Hüfte | 18.6 |
| Schulterbreite (eine Seite, Hals bis Schulter) | 13.5 |
| Hüftumfang | 91.6 |
| Oberschenkellänge | 34.7 |
| Oberschenkelumfang | 52.3 |
| Unterschenkellänge | 50.1 |
| Wadenumfang | 36.4 |
| Knöchelumfang | 19.7 |
| Knieumfang | 34.1 |
| Schrittlänge (Innenbein) | 78.3 |
| Fußlänge | 23.4 |

## Wirkung der Targets bei voller Stärke (UI-Wert ±100)

Änderung in cm gegenüber der Standardfigur. Nur Targets, die mindestens eines dieser Maße um 0,5 cm oder mehr ändern.

| Target | Körpergröße | Brustumfang | Unterbrustumfang | Taillenumfang | Hüftumfang | Halsumfang | Oberschenkelumfang | Schrittlänge | Fußlänge |
|---|---|---|---|---|---|---|---|---|---|
| `min_gender` | -7.0 | -4.1 | -7.5 | -2.4 | +0.9 | -4.5 | -1.6 | -4.8 | -2.4 |
| `max_gender` | +7.1 | +5.3 | +8.2 | +3.0 | +0.0 | +4.6 | +2.1 | +5.0 | +2.4 |
| `min_age` | -105.8 | -50.8 | -40.9 | -35.4 | -54.7 | -12.1 | -30.3 | -55.9 | -14.8 |
| `max_age` | -2.2 | +0.0 | -0.5 | +4.2 | +2.5 | +0.7 | -2.9 | +0.4 | -0.1 |
| `min_weight` | +0.0 | -1.7 | -2.0 | -6.3 | -5.7 | -1.1 | -5.6 | -0.2 | +0.0 |
| `max_weight` | +0.0 | +4.1 | +4.8 | +9.4 | +6.9 | +0.0 | +4.5 | -0.4 | +0.0 |
| `min_muscle` | +0.0 | +2.0 | +5.4 | +11.6 | +8.1 | +0.2 | +4.3 | -0.6 | +0.0 |
| `max_muscle` | +0.0 | -1.5 | -3.0 | -1.7 | -4.4 | -0.0 | +0.5 | +0.1 | +0.0 |
| `min_height` | -36.7 | -10.3 | -8.5 | -9.1 | -11.8 | -3.6 | -5.4 | -22.7 | -2.7 |
| `max_height` | +72.3 | +24.6 | +22.3 | +21.4 | +26.9 | +9.8 | +14.5 | +42.4 | +11.1 |
| `min_bodyproportions` | -0.3 | -1.2 | +1.6 | +4.5 | +3.0 | -0.1 | +0.2 | -2.0 | +0.8 |
| `max_bodyproportions` | +0.5 | +2.4 | +0.4 | -2.1 | -1.0 | -0.0 | -0.1 | +1.8 | -0.5 |
| `min_torso_scale-horiz-decr-incr` | +0.0 | -8.7 | -8.1 | -9.2 | +0.0 | -1.5 | +0.0 | +0.0 | +0.0 |
| `max_torso_scale-horiz-decr-incr` | +0.0 | +9.0 | +8.4 | +0.2 | +0.0 | +0.8 | +0.0 | +0.0 | +0.0 |
| `min_torso_scale-depth-decr-incr` | +0.0 | -5.1 | -4.0 | -2.3 | +0.0 | -1.6 | +0.0 | +0.0 | +0.0 |
| `max_torso_scale-depth-decr-incr` | +0.0 | +9.7 | +7.9 | +2.5 | +0.0 | +0.2 | +0.0 | +0.0 | +0.0 |
| `min_torso_scale-vert-decr-incr` | -4.3 | +0.0 | -0.1 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `max_torso_scale-vert-decr-incr` | +10.3 | +0.0 | +0.7 | -0.0 | +0.0 | -0.0 | +0.0 | +0.0 | +0.0 |
| `min_torso_vshape-decr-incr` | +0.0 | -2.9 | -1.0 | +0.3 | +0.0 | -0.0 | +0.0 | +0.0 | +0.0 |
| `max_torso_vshape-decr-incr` | +0.0 | +3.4 | +1.0 | -0.2 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `min_torso_muscle-pectoral-decr-incr` | +0.0 | -0.9 | -0.1 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `max_torso_muscle-pectoral-decr-incr` | +0.0 | +3.6 | +0.4 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `min_torso_muscle-dorsi-decr-incr` | +0.0 | -6.2 | -4.1 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `max_torso_muscle-dorsi-decr-incr` | +0.0 | +7.9 | +4.6 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `min_hip_scale-horiz-decr-incr` | +0.0 | -0.0 | -1.7 | -8.6 | -12.0 | +0.0 | -4.6 | +0.0 | +0.0 |
| `max_hip_scale-horiz-decr-incr` | +0.0 | +0.0 | +1.8 | +8.9 | +12.3 | +0.0 | +5.0 | +0.0 | +0.0 |
| `min_hip_scale-depth-decr-incr` | +0.0 | +0.0 | -1.2 | -6.6 | -9.2 | +0.0 | -6.7 | +0.0 | +0.0 |
| `max_hip_scale-depth-decr-incr` | +0.0 | +0.0 | +1.4 | +7.8 | +10.8 | +0.0 | +8.0 | +0.0 | +0.0 |
| `min_hip_scale-vert-decr-incr` | +0.0 | +0.0 | +0.0 | +0.0 | +0.1 | +0.0 | +0.4 | +2.1 | +0.0 |
| `max_hip_scale-vert-decr-incr` | +0.0 | +0.0 | -0.0 | -0.0 | -0.1 | +0.0 | -0.3 | -2.1 | +0.0 |
| `min_stomach_pregnant-decr-incr` | +0.0 | +0.0 | +0.0 | -1.1 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `max_stomach_pregnant-decr-incr` | +0.0 | +0.0 | +0.1 | +14.0 | -0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `min_buttocks_volume-decr-incr` | +0.0 | +0.0 | +0.0 | +0.0 | -2.8 | +0.0 | +0.0 | +0.0 | +0.0 |
| `max_buttocks_volume-decr-incr` | +0.0 | +0.0 | +0.0 | +0.4 | +5.9 | +0.0 | +0.9 | +0.0 | +0.0 |
| `min_breast_breastsize` | +0.0 | -2.4 | +0.1 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `max_breast_breastsize` | +0.0 | +5.9 | +0.1 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `min_armslegs_upperlegs-height-decr-incr` | -7.5 | +0.0 | +0.0 | -0.0 | +0.0 | +0.0 | -0.3 | -7.4 | +0.0 |
| `max_armslegs_upperlegs-height-decr-incr` | +10.4 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.1 | +10.4 | +0.0 |
| `min_armslegs_lowerlegs-height-decr-incr` | -5.9 | +0.0 | +0.0 | -0.0 | +0.0 | +0.0 | +0.0 | -5.9 | +0.0 |
| `max_armslegs_lowerlegs-height-decr-incr` | +8.1 | +0.0 | +0.0 | -0.0 | +0.0 | +0.0 | +0.0 | +8.1 | +0.0 |
| `max_measure_bust-circ-decr-incr` | +0.0 | +17.1 | +12.4 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `max_measure_frontchest-dist-decr-incr` | +0.0 | +2.4 | +0.2 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `max_measure_hips-circ-decr-incr` | +0.0 | +0.0 | +0.0 | +0.4 | +19.2 | +0.0 | +4.5 | +0.0 | +0.0 |
| `max_measure_lowerleg-height-decr-incr` | +8.1 | +0.0 | +0.0 | -0.0 | +0.0 | +0.0 | +0.0 | +8.1 | +0.0 |
| `max_measure_napetowaist-dist-decr-incr` | +7.8 | -0.0 | +0.1 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `max_measure_neck-circ-decr-incr` | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +5.4 | +0.0 | +0.0 | +0.0 |
| `max_measure_neck-height-decr-incr` | +3.0 | +0.0 | +0.0 | +0.0 | +0.0 | -0.0 | +0.0 | +0.0 | +0.0 |
| `max_measure_thigh-circ-decr-incr` | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +8.7 | +0.0 | +0.0 |
| `max_measure_underbust-circ-decr-incr` | +0.0 | +12.8 | +13.6 | +3.2 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `max_measure_upperleg-height-decr-incr` | +10.4 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.1 | +10.4 | +0.0 |
| `max_measure_waist-circ-decr-incr` | +0.0 | +0.4 | +4.6 | +10.3 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `max_measure_waisttohip-dist-decr-incr` | +7.6 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `min_measure_bust-circ-decr-incr` | +0.0 | -13.9 | -5.4 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `min_measure_frontchest-dist-decr-incr` | +0.0 | -2.3 | -1.8 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `min_measure_hips-circ-decr-incr` | +0.0 | +0.0 | +0.0 | -0.2 | -9.6 | +0.0 | -2.2 | +0.0 | +0.0 |
| `min_measure_lowerleg-height-decr-incr` | -5.9 | +0.0 | +0.0 | -0.0 | +0.0 | +0.0 | +0.0 | -5.9 | +0.0 |
| `min_measure_napetowaist-dist-decr-incr` | -4.6 | +0.0 | -0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `min_measure_neck-circ-decr-incr` | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | -5.2 | +0.0 | +0.0 | +0.0 |
| `min_measure_neck-height-decr-incr` | -3.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `min_measure_shoulder-dist-decr-incr` | +0.0 | -0.7 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `min_measure_thigh-circ-decr-incr` | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | -5.7 | +0.0 | +0.0 |
| `min_measure_underbust-circ-decr-incr` | +0.0 | -4.2 | -4.5 | -1.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `min_measure_upperleg-height-decr-incr` | -7.5 | +0.0 | +0.0 | -0.0 | +0.0 | +0.0 | -0.3 | -7.4 | +0.0 |
| `min_measure_waist-circ-decr-incr` | +0.0 | -0.3 | -4.5 | -10.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `min_measure_waisttohip-dist-decr-incr` | -4.8 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 |
| `max_figur_frau_apfel` | +0.0 | -0.6 | +1.5 | +12.2 | +5.0 | -1.0 | +0.8 | +0.0 | +0.0 |
| `max_figur_frau_raute` | +0.0 | -1.1 | +1.0 | +9.8 | +6.5 | -1.5 | +1.8 | +0.0 | +0.0 |
| `max_figur_frau_sanduhr-kurvig` | +0.0 | +1.3 | -0.3 | -5.0 | +3.3 | +0.1 | -0.9 | +0.0 | +0.0 |
| `max_figur_frau_v-form` | +0.0 | +1.4 | -0.2 | -6.6 | -6.2 | +0.8 | -2.1 | +0.0 | +0.0 |
| `max_figur_frau_saeule` | +0.0 | -0.6 | -0.2 | -5.1 | -8.1 | -0.7 | -2.1 | +0.0 | +0.0 |
| `max_figur_frau_bauchbetont` | +0.0 | +8.9 | +10.9 | +27.8 | +6.0 | +4.4 | +4.8 | -0.3 | +0.0 |
| `max_figur_frau_sanduhr-schlank` | +0.0 | +1.2 | -0.2 | -3.4 | +2.2 | +0.2 | -0.6 | +0.0 | +0.0 |
| `max_figur_frau_birne-kraeftig` | +0.0 | +0.4 | +4.2 | +11.8 | +19.2 | +0.0 | +20.6 | +0.0 | +0.2 |
| `max_figur_frau_rechteck` | +0.0 | +0.6 | +0.3 | +5.4 | -1.1 | +0.4 | -1.0 | +0.0 | +0.0 |
| `max_figur_frau_vollschlank` | +0.0 | +19.5 | +19.9 | +32.9 | +22.1 | +7.5 | +19.9 | +0.1 | -0.1 |
| `max_figur_frau_birne` | +0.0 | -1.1 | -0.2 | -0.3 | +7.0 | -1.9 | +3.6 | +0.0 | +0.0 |
| `max_figur_mann_apfel` | +0.0 | +0.1 | +5.1 | +14.1 | -0.4 | -0.5 | -0.0 | +0.0 | +0.0 |
| `max_figur_mann_hueftbetont` | +0.0 | +3.3 | +0.1 | +13.4 | +6.7 | +0.0 | +6.1 | +0.0 | +0.0 |
| `max_figur_mann_v-form` | +0.0 | +0.4 | +2.5 | +5.3 | -0.5 | +0.4 | -0.9 | +0.1 | +0.0 |
| `max_figur_mann_saeule` | +0.0 | -1.8 | -0.5 | +0.8 | -0.7 | -0.5 | -1.4 | +0.0 | +0.0 |
| `max_figur_mann_bauchbetont` | +0.0 | +1.1 | -0.2 | +7.2 | -0.2 | +0.0 | +0.0 | +0.0 | +0.0 |
| `max_figur_mann_rechteck` | +0.0 | +0.2 | +3.2 | +9.3 | +3.8 | +0.0 | +0.5 | +0.0 | +0.0 |
| `max_figur_mann_vollschlank` | +0.0 | +5.3 | +7.9 | +27.9 | +14.2 | +4.2 | +10.6 | +0.1 | +0.6 |
| `max_figur_mann_trapez` | +0.0 | +0.3 | +2.7 | +6.6 | +0.8 | +0.3 | -0.5 | +0.0 | +0.0 |
| `max_figur_mann_birne` | +0.0 | -0.6 | +0.0 | +4.7 | +8.2 | -0.3 | +1.8 | -0.1 | +0.0 |
| `min_armslegs_foot-scale-decr-incr` | +0.3 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.3 | -4.8 |
| `max_armslegs_foot-scale-decr-incr` | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +7.2 |
| `min_armslegs_upperleg-fat-decr-incr` | +0.0 | +0.0 | +0.0 | +0.0 | -0.2 | +0.0 | -4.6 | +0.0 | +0.0 |
| `max_armslegs_upperleg-fat-decr-incr` | +0.0 | +0.0 | +0.0 | +0.0 | +3.3 | +0.0 | +5.9 | +0.0 | +0.0 |
| `min_armslegs_leg-valgus-decr-incr` | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | +0.0 | -1.3 | +0.0 | +0.0 |
