// Tests unitaires : gabarit, moteur de correction et configuration des exercices.
//   node --test tests/correction.test.js
// Le moteur (Grading) et la configuration (__EXOS__) sont lus dans les pages générées : on teste exactement ce que
// l'élève utilisera. index.html (la page publiée) et modele.html (le cours et l'exercice modèles, src/modele.py,
// régénérée ici) passent les mêmes contrôles ; les correcteurs du modèle sont ensuite essayés un par un.
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const { execFileSync } = require("node:child_process");

const RACINE = path.join(__dirname, "..");
execFileSync("python3", [path.join(RACINE, "src", "generer.py"), "--modele"]);
const PAGES = { "index.html": lire("index.html"), "modele.html": lire("modele.html") };

function lire(nom) {
  const html = fs.readFileSync(path.join(RACINE, nom), "utf8");
  const code = html.slice(html.indexOf("/*GRADING-START*/"), html.indexOf("/*GRADING-END*/"));
  const mod = { exports: {} };
  new Function("module", code + "\nmodule.exports = Grading;")(mod);
  return { html, G: mod.exports, EXOS: JSON.parse(html.match(/window\.__EXOS__ = (.*?);<\/script>/)[1]) };
}
const texte = (s) => s.replace(/&#x27;/g, "'").replace(/&quot;/g, '"').replace(/&lt;/g, "<").replace(/&gt;/g, ">")
  .replace(/&amp;/g, "&");
// listes d'étiquettes de la page, et cases qui les reçoivent (avec l'étiquette montrée sur un schéma corrigé) ; chaque
// exercice est dans son propre gabarit (template), où les listes d'un schéma ont des noms communs à tous (bk-1-1…) :
// une case est rapprochée de la liste de son exercice (etq)
function etiquettes(html) {
  const listes = {}, cases = [];
  const exos = [...html.matchAll(/<template id="tpl-parts-[^"]+">([\s\S]*?)<\/template>/g)].map((m) => m[1]);
  for (const src of exos.length ? exos : [html]) {
    const ici = {};
    for (const m of src.matchAll(/<div class="bank" id="([^"]+)"[^>]*>([\s\S]*?)<\/div>/g))
      ici[m[1]] = [...m[2].matchAll(/<button type="button" class="etq"[^>]*>([^<]*)<\/button>/g)].map((x) => texte(x[1]));
    for (const m of src.matchAll(/<button type="button" class="dz[^"]*" id="dz-([^"]+)" data-bank="([^"]+)"(?: data-attendu="([^"]*)")?/g))
      cases.push({ id: m[1], liste: m[2], etq: ici[m[2]], attendu: m[3] === undefined ? null : texte(m[3]) });
    Object.assign(listes, ici);
  }
  return { listes, cases };
}

test("gabarit : copie conforme de celui des dépôts RDM et Chaîne fonctionnelle", () => {
  const g = fs.readFileSync(path.join(RACINE, "src", "gabarit-exercice-interactif.html"));
  assert.equal(crypto.createHash("sha256").update(g).digest("hex"),
    "d39968afd8d398aed6e0b56968445e3b9ddbd19d503efe9adabef898d93db91a");
});

for (const [nom, { html, G, EXOS }] of Object.entries(PAGES)) {
  test(`${nom} : configuration de chaque exercice (parties, durées, points, correcteurs)`, () => {
    for (const [cle, E] of Object.entries(EXOS)) {
      assert.ok(E.parts.length >= 1, cle);
      assert.equal(E.minutes, E.parts.reduce((s, p) => s + p.minutes, 0), cle);
      for (const p of E.parts) assert.ok(p.minutes > 0 && p.points > 0, `${cle}, partie ${p.num}`);
      assert.equal(E.parts.reduce((s, p) => s + p.points, 0), Object.keys(E.qcfg).length, cle);
      for (const [id, q] of Object.entries(E.qcfg)) {
        const r = G.grade("réponse", q.grader);
        assert.notEqual(r.invalid, "Type de question inconnu.", `${cle} : ${id}`);
        assert.ok(E.parts.some((p) => p.num === q.part), `${cle} : ${id}`);
        assert.ok(html.includes(`data-q="${id}"`), `${cle} : ${id} absente de la page`);
      }
    }
  });

  test(`${nom} : étiquettes — chaque case en accepte au moins une, et celle montrée sur le schéma corrigé`, () => {
    const qcfg = Object.assign({}, ...Object.values(EXOS).map((E) => E.qcfg));
    const { cases } = etiquettes(html);
    for (const c of cases) {
      const g = qcfg[c.id].grader, liste = c.etq;
      assert.ok(liste && liste.length, `${c.id} : liste ${c.liste}`);
      assert.ok(liste.some((e) => G.grade(e, g).ok), `${c.id} : aucune étiquette de « ${c.liste} » n'est juste`);
      if (c.attendu !== null) {
        assert.ok(liste.includes(c.attendu), `${c.id} : ${c.attendu}`);
        assert.ok(G.grade(c.attendu, g).ok, `${c.id} : l'étiquette montrée (${c.attendu}) est refusée`);
      }
    }
  });
}

// ------------------------------------------------------------ correcteurs du modèle
const M = PAGES["modele.html"];
const QM = M.EXOS["exercice-modele"].qcfg;
const juste = (id, rep) => M.G.grade(rep, QM[id].grader).ok;

test("modèle : mots-clés (petite faute tolérée, mot interdit), nombre", () => {
  for (const r of ["commutateur", "Le commutateur", "un switch", "comutateur"]) assert.ok(juste("m1_1", r), r);
  for (const r of ["routeur", "commutateur et routeur", "concentrateur"]) assert.equal(juste("m1_1", r), false, r);
  for (const r of ["254", "254 adresses", "254,0"]) assert.ok(juste("m1_3", r), r);
  for (const r of ["256", "253", "2"]) assert.equal(juste("m1_3", r), false, r);
});

test("modèle : adresses — seule l'écriture exacte est juste, même quand la ponctuation retirée la confond", () => {
  for (const r of ["192.168.1.12", " 192.168.1.12 ", "192. 168. 1. 12"]) assert.ok(juste("m1_2", r), r);
  // 192.168.11.2 et 192.168.1.12 s'écrivent 192168112 sans leurs points : le moteur seul les confondrait
  for (const r of ["192.168.11.2", "192.168.1.120", "192.168.1.1", "192.168.1.12/24", "l'adresse 192.168.1.12", "19216811 2"])
    assert.equal(juste("m1_2", r), false, r);
  assert.ok(juste("m1_4_1", "192.168.1.0"));
  assert.equal(juste("m1_4_1", "192.168.10"), false, "même chiffres que 192.168.1.0");
  assert.ok(juste("m1_4_2", "192.168.1.255"));
  assert.equal(juste("m1_4_2", "192.168.1.254"), false);
  assert.ok(M.G.grade("", QM.m1_2.grader).invalid, "réponse vide refusée sans être comptée");
});

test("modèle : étiquettes — la bonne est la seule acceptée de sa liste", () => {
  const { listes, cases } = etiquettes(M.html);
  const ATTENDU = { m2_1_1: "Le routeur", m2_1_2: "Le commutateur", m2_1_3: "Le serveur",
    m2_2_1: "Adresse IP", m2_2_2: "Adresse MAC", m2_2_3: "Masque de sous-réseau" };
  assert.deepEqual(cases.map((c) => c.id).sort(), Object.keys(ATTENDU).sort());
  for (const c of cases)
    assert.deepEqual(listes[c.liste].filter((e) => juste(c.id, e)), [ATTENDU[c.id]], c.id);
  assert.deepEqual(listes["bk-2-1"], ["Le commutateur", "Le point d'accès Wi-Fi", "Le poste client", "Le routeur", "Le serveur"],
    "ordre alphabétique, sans l'article");
});

test("modèle : QCM — réponse unique (repère), réponses multiples (toutes et elles seules)", () => {
  for (const r of ["B", "b"]) assert.ok(juste("m3_1_1", r), r);
  for (const r of ["A", "C", "A,B"]) assert.equal(juste("m3_1_1", r), false, r);
  assert.ok(juste("m3_2_1", "1,2,4"));
  assert.ok(juste("m3_2_1", "4,1,2"));
  for (const r of ["1,2", "1,2,3,4", "3"]) assert.equal(juste("m3_2_1", r), false, r);
});
