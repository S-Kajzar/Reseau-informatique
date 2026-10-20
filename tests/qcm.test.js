// QCM 1.1 « réseaux informatiques » : chaque bonne réponse est acceptée, chaque autre proposition refusée.
//   node --test tests/qcm.test.js
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const html = fs.readFileSync(path.join(__dirname, "..", "index.html"), "utf8");
const code = html.slice(html.indexOf("/*GRADING-START*/"), html.indexOf("/*GRADING-END*/"));
const mod = { exports: {} };
new Function("module", code + "\nmodule.exports = Grading;")(mod);
const G = mod.exports;
const EX = JSON.parse(html.match(/window\.__EXOS__ = (.*?);<\/script>/)[1])["qcm-reseaux"];
// questions lues dans la page : identifiant de la case, réponse multiple ou non, repères des propositions
const Q = [...html.matchAll(/<div class="fast-q grp qcm" id="(\w+)" data-multi="(\d)">([\s\S]*?)<div class="fast-foot">/g)]
  .map((m) => ({ id: m[1] + "_1", multi: m[2] === "1", keys: [...m[3].matchAll(/data-k="([^"]+)"/g)].map((x) => x[1]), src: m[3] }))
  .filter((q) => q.id in EX.qcfg);
const juste = (q) => { const g = EX.qcfg[q.id].grader; return (g.equals || g.value.map(String)); };
const ok = (q, v) => G.grade(v, EX.qcfg[q.id].grader).ok;
const enonce = (re) => Q.find((q) => re.test(q.src));

test("configuration : 6 parties qui suivent le plan du cours, 47 questions d'un point, 47 min", () => {
  assert.equal(Q.length, 47);
  assert.equal(Object.keys(EX.qcfg).length, 47);
  assert.deepEqual(EX.parts.map((p) => p.title), ["Liaison point-à-point", "Mise en réseau", "WAN et Internet",
    "Adressage IP et LAN", "Communication entre logiciels", "Modèle OSI"]);
  assert.equal(EX.minutes, 47);
  assert.equal(EX.parts.reduce((s, p) => s + p.points, 0), 47);
});

test("réponse unique : chaque bonne proposition acceptée, toutes les autres refusées", () => {
  let n = 0;
  for (const q of Q.filter((x) => !x.multi)) {
    const bons = juste(q);
    assert.equal(bons.length, 1, q.id);
    for (const k of q.keys) { assert.equal(ok(q, k), bons.includes(k.toLowerCase()), `${q.id} : ${k}`); n++; }
    assert.equal(ok(q, q.keys.join(",")), false, `${q.id} : tout cocher`);
  }
  assert.ok(n > 100, `${n} propositions testées`);
});

test("réponses multiples : il faut toutes les bonnes, et elles seules", () => {
  const multi = Q.filter((x) => x.multi);
  assert.ok(multi.length >= 8, `${multi.length} questions à réponses multiples`);
  for (const q of multi) {
    const bons = juste(q);
    assert.ok(bons.length >= 2, q.id);
    assert.ok(ok(q, bons.join(",")), q.id);
    assert.equal(ok(q, bons.slice(1).join(",")), false, `${q.id} : incomplet`);
    const intrus = q.keys.find((k) => !bons.includes(k));
    if (intrus) assert.equal(ok(q, bons.concat(intrus).join(",")), false, `${q.id} : avec un intrus`);
  }
});

test("réponses vérifiées sur le cours : débit, adresses, masques, couches", () => {
  assert.deepEqual(juste(enonce(/20 Mo est transmis en 4 s/)).sort(), ["1", "3"], "5 Mo/s = 40 Mbit/s");
  assert.deepEqual(juste(enonce(/adresses privées, réservées/)).sort(), ["1", "2", "4"], "10.x, 172.20.x, 192.168.x");
  assert.deepEqual(juste(enonce(/192\.168\.0\.54/)).sort(), ["1", "3"], "même net-ID 192.168.0");
  assert.deepEqual(juste(enonce(/Que contient une box/)).sort(), ["1", "2", "3", "4"]);
  assert.deepEqual(juste(enonce(/net-ID de l'adresse 102\.122\.201\.17/)), ["b"]);
  assert.deepEqual(juste(enonce(/host-ID de l'adresse 19\.102\.12\.193/)), ["b"]);
  assert.deepEqual(juste(enonce(/Un routeur met en œuvre/)), ["b"], "couches 1 à 3");
  // chaque question a son explication, affichée à la correction
  for (const q of Q) {
    const bloc = html.slice(html.indexOf(`id="${q.id.slice(0, -2)}"`)).split('<div class="fast-q')[0];
    assert.match(bloc, /<p class="why-t">Explication<\/p><p>\S/, q.id);
  }
});
