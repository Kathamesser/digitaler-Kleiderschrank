// 3D-Anzeige des Avatars mit Three.js: GLB laden, Morph-Werte setzen, Drehen/Zoomen, Zentimeter messen.
// Bewusst ohne Framework und ohne Oberfläche, damit React/Vue das Modul später übernehmen können.
// Grundlage: docs/avatar/AVATAR-REGLER.md (Morph-Werte) und docs/avatar/ZENTIMETER.md (Messen).

import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

// Die Avatar-Dateien liegen zentral in Sharely_programm/assets/avatar/ (relativ zu diesem Modul).
export const GLB_URL = new URL("../../../assets/avatar/Avatar_Editorgeruest.glb", import.meta.url);
export const MESSPUNKTE_URL = new URL("../../../assets/avatar/messpunkte.json", import.meta.url);

const KAMERA_ZIEL = new THREE.Vector3(0, 0.88, 0);
const ANSICHTEN = { vorne: 0, seite: Math.PI / 2, hinten: Math.PI };

export class AvatarAnsicht {
  /** @param {HTMLElement} buehne Element, in das die Zeichenfläche gesetzt wird */
  constructor(buehne) {
    this.buehne = buehne;
    this.meshes = [];          // Körper (erstes Primitive) und Augen
    this.koerper = null;

    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    buehne.append(this.renderer.domElement);

    this.szene = new THREE.Scene();
    this.szene.add(new THREE.HemisphereLight(0xffffff, 0xd8cbb8, 2.2));
    const licht = new THREE.DirectionalLight(0xffffff, 1.6);
    licht.position.set(1.5, 3, 2.5);
    this.szene.add(licht);
    const gegenlicht = new THREE.DirectionalLight(0xffffff, 0.6);
    gegenlicht.position.set(-2, 2, -2);
    this.szene.add(gegenlicht);

    // Schattenfleck unter den Füßen, damit die Figur nicht schwebt
    const boden = new THREE.Mesh(
      new THREE.CircleGeometry(0.42, 48),
      new THREE.MeshBasicMaterial({ color: 0x2c3a5e, transparent: true, opacity: 0.08 }),
    );
    boden.rotation.x = -Math.PI / 2;
    this.szene.add(boden);

    this.kamera = new THREE.PerspectiveCamera(30, 1, 0.05, 50);
    this.steuerung = new OrbitControls(this.kamera, this.renderer.domElement);
    this.steuerung.enablePan = false;
    this.steuerung.enableDamping = true;
    this.steuerung.minDistance = 1.2;
    this.steuerung.maxDistance = 6;
    this.steuerung.minPolarAngle = 0.2;
    this.steuerung.maxPolarAngle = Math.PI / 2 + 0.15;
    this.ansicht("vorne");

    new ResizeObserver(() => this.groesseAnpassen()).observe(buehne);
    this.groesseAnpassen();
    this.renderer.setAnimationLoop(() => {
      this.steuerung.update();
      this.renderer.render(this.szene, this.kamera);
    });
  }

  /** GLB laden. fortschritt(anteil 0…1) wird während des Ladens aufgerufen. */
  async laden(fortschritt = () => {}) {
    const gltf = await new GLTFLoader().loadAsync(GLB_URL.href, (e) => {
      if (e.lengthComputable) fortschritt(e.loaded / e.total);
    });
    gltf.scene.traverse((o) => {
      if (o.isMesh && o.morphTargetDictionary) this.meshes.push(o);
    });
    // Die Messpunkte beziehen sich auf das erste Primitive der GLB, den Körper.
    this.koerper = this.meshes[0];
    this.szene.add(gltf.scene);
  }

  /** Alle Targets setzen, immer auf Körper und Augen (beide haben dieselben Target-Namen). */
  setzeMorphWerte(werte) {
    for (const mesh of this.meshes) {
      for (const [name, wert] of Object.entries(werte)) {
        const i = mesh.morphTargetDictionary[name];
        if (i !== undefined) mesh.morphTargetInfluences[i] = wert;
      }
    }
  }

  /** Kamera auf eine feste Ansicht drehen: "vorne", "seite" oder "hinten". */
  ansicht(name) {
    const winkel = ANSICHTEN[name] ?? 0;
    const abstand = 3.6;
    this.kamera.position.set(Math.sin(winkel) * abstand, 1.0, Math.cos(winkel) * abstand);
    this.steuerung.target.copy(KAMERA_ZIEL);
    this.steuerung.update();
  }

  groesseAnpassen() {
    const { clientWidth: b, clientHeight: h } = this.buehne;
    if (!b || !h) return;
    this.renderer.setSize(b, h, false);
    this.kamera.aspect = b / h;
    this.kamera.updateProjectionMatrix();
  }

  // ---------- Messen (ZENTIMETER.md Abschnitt 5) ----------

  /** Position eines Körper-Vertex mit allen aktiven Morph-Werten (glTF-Targets sind Verschiebungen). */
  punkt(i, ziel = new THREE.Vector3()) {
    const g = this.koerper.geometry;
    const pos = g.attributes.position.array;
    ziel.set(pos[3 * i], pos[3 * i + 1], pos[3 * i + 2]);
    const einfluss = this.koerper.morphTargetInfluences;
    g.morphAttributes.position.forEach((attr, t) => {
      const w = einfluss[t];
      if (w) ziel.x += attr.array[3 * i] * w, ziel.y += attr.array[3 * i + 1] * w, ziel.z += attr.array[3 * i + 2] * w;
    });
    return ziel;
  }

  /** Tiefster und höchster Punkt der verformten Figur (y in Metern). */
  hoehenbereich() {
    const g = this.koerper.geometry;
    const anzahl = g.attributes.position.count;
    const y = Float32Array.from({ length: anzahl }, (_, i) => g.attributes.position.array[3 * i + 1]);
    const einfluss = this.koerper.morphTargetInfluences;
    g.morphAttributes.position.forEach((attr, t) => {
      const w = einfluss[t];
      if (!w) return;
      for (let i = 0; i < anzahl; i++) y[i] += attr.array[3 * i + 1] * w;
    });
    let unten = Infinity, oben = -Infinity;
    for (const v of y) { if (v < unten) unten = v; if (v > oben) oben = v; }
    return { unten, oben };
  }

  /**
   * Alle Maße in cm an der aktuell verformten Figur messen.
   * @param messpunkte Inhalt von messpunkte.json
   * @returns { koerpergroesse: 165.9, "waist-circ": 72.4, … }
   */
  messen(messpunkte) {
    const { unten, oben } = this.hoehenbereich();
    const cm = { koerpergroesse: 100 * (oben - unten) };
    for (const [schluessel, band] of Object.entries(messpunkte.masse)) {
      const p = band.glb_vertices.map((i) => this.punkt(i));
      let m;
      if (band.art === "laenge") m = p.slice(1).reduce((s, q, k) => s + q.distanceTo(p[k]), 0);
      else if (band.art === "hoehe_punkt") m = p[0].y - unten;
      else if (band.art === "fuss") m = Math.abs(p[1].z - p[0].z);
      else if (band.art === "bogen") m = huellenUmfang(p) - p[0].distanceTo(p[p.length - 1]);
      else m = huellenUmfang(p);
      cm[schluessel] = 100 * m;
    }
    return cm;
  }
}

/**
 * Umfang wie ein straff angelegtes Maßband: Punkte in ihre Hauptebene projizieren, konvexe Hülle
 * bilden, Umfang addieren. Entspricht hull_perimeter in docs/avatar/skripte/zentimeter_messen.py.
 */
export function huellenUmfang(punkte) {
  const mitte = new THREE.Vector3();
  punkte.forEach((p) => mitte.add(p));
  mitte.divideScalar(punkte.length);
  const d = punkte.map((p) => p.clone().sub(mitte));

  // Hauptebene: die beiden größten Eigenvektoren der Kovarianzmatrix (statt SVD wie in Python)
  const c = [0, 0, 0, 0, 0, 0, 0, 0, 0];
  for (const v of d) {
    const a = [v.x, v.y, v.z];
    for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) c[3 * i + j] += a[i] * a[j];
  }
  const e1 = eigenvektor(c, null);
  const e2 = eigenvektor(c, e1);
  const q = d.map((v) => [v.dot(e1), v.dot(e2)]).sort((a, b) => a[0] - b[0] || a[1] - b[1]);

  // konvexe Hülle (Monotone Chain, wie im Python-Skript)
  const kreuz = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
  const unten = [], oben = [];
  for (const p of q) {
    while (unten.length >= 2 && kreuz(unten[unten.length - 2], unten[unten.length - 1], p) <= 0) unten.pop();
    unten.push(p);
  }
  for (const p of [...q].reverse()) {
    while (oben.length >= 2 && kreuz(oben[oben.length - 2], oben[oben.length - 1], p) <= 0) oben.pop();
    oben.push(p);
  }
  const h = unten.slice(0, -1).concat(oben.slice(0, -1));
  return h.reduce((s, p, k) => s + Math.hypot(p[0] - h[(k + 1) % h.length][0], p[1] - h[(k + 1) % h.length][1]), 0);
}

/** Größter Eigenvektor einer symmetrischen 3×3-Matrix (Potenzmethode), senkrecht zu `ohne`. */
function eigenvektor(m, ohne) {
  const v = new THREE.Vector3(0.577, 0.577, 0.577);
  if (ohne) {
    // Startvektor senkrecht zu `ohne`: Kreuzprodukt mit der Achse, auf der `ohne` am kleinsten ist
    const a = [Math.abs(ohne.x), Math.abs(ohne.y), Math.abs(ohne.z)];
    const achse = new THREE.Vector3().setComponent(a.indexOf(Math.min(...a)), 1);
    v.crossVectors(ohne, achse).normalize();
  }
  for (let k = 0; k < 60; k++) {
    if (ohne) v.addScaledVector(ohne, -v.dot(ohne));
    v.set(
      m[0] * v.x + m[1] * v.y + m[2] * v.z,
      m[3] * v.x + m[4] * v.y + m[5] * v.z,
      m[6] * v.x + m[7] * v.y + m[8] * v.z,
    ).normalize();
  }
  if (ohne) v.addScaledVector(ohne, -v.dot(ohne)).normalize();
  return v;
}
