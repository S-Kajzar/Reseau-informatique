// Exercices 1.3 et 2.1, étude de cas 1 (index.html) : correcteurs (Node), puis copies complètes dans le navigateur
// (Playwright + Chromium).
//   NODE_PATH=$(npm root -g) node --test tests/exercices.test.js
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");

const FICHIER = path.join(__dirname, "..", "index.html");
const URL = "file://" + FICHIER;
const html = fs.readFileSync(FICHIER, "utf8");
const code = html.slice(html.indexOf("/*GRADING-START*/"), html.indexOf("/*GRADING-END*/"));
const mod = { exports: {} };
new Function("module", code + "\nmodule.exports = Grading;")(mod);
const G = mod.exports;
const EXOS = JSON.parse(html.match(/window\.__EXOS__ = (.*?);<\/script>/)[1]);

// les copies entièrement justes : étiquettes posées, cases saisies au clavier, propositions cochées
const COPIES = {
  "adressage-maison": {
    etq: { a1_1_1: "Modem", a1_1_2: "Routeur", a1_1_3: "Switch", a1_1_4: "Point d'accès Wi-Fi", a1_2_1: "Fibre optique",
      a1_2_2: "Câble Ethernet", a1_2_3: "Wi-Fi", a1_2_4: "Câble Ethernet", a2_4_1: "Adresse privée",
      a2_4_2: "Adresse publique", a2_4_3: "Adresse privée", a2_4_4: "Adresse privée", a2_4_5: "Adresse publique" },
    txt: { a2_1_1: "192.168.1", a2_1_2: "10", a2_1_3: "31", a2_2: "192.168.1.1", a2_3: "86.245.12.40", a3_1: "254",
      a3_2: "192.168.1.32", a3_4: "192.168.1.50", a4_1: "400 s", a4_2: "1333 s", a4_3: "48 Mbit/s" },
    qcm: { a1_3: ["A"], a3_3: [1, 2], a3_5: ["B"], a4_4: ["A"] },
  },
  "requete-http": {
    etq: { r1_1_1: "Couches 1 à 7", r1_1_2: "Couches 1 à 3", r1_1_3: "Couches 1 et 2", r1_1_4: "Couches 1 à 7",
      r2_1_1: "En-tête Ethernet", r2_1_2: "En-tête IP", r2_1_3: "En-tête TCP", r2_1_4: "Requête HTTP",
      r2_1_5: "Remorque Ethernet", r2_2_1: "Application (couches 5 à 7)", r2_2_2: "Transport (couche 4)",
      r2_2_3: "Réseau (couche 3)", r2_2_4: "Liaison de données (couche 2)",
      r3_1_1: "3C:52:A1:10:20:01 (box)", r3_1_2: "28:87:A5:EF:18:5D (ordinateur portable)",
      r3_1_3: "192.168.1.30 (ordinateur portable)", r3_1_4: "203.0.113.80 (serveur web)",
      r4_1_1: "00:1B:44:11:3A:B7 (serveur web)", r4_1_2: "00:1B:44:22:00:01 (routeur du centre)",
      r4_1_3: "86.245.12.40 (box, adresse publique)", r4_1_4: "203.0.113.80 (serveur web)" },
    txt: { r2_3: "4", r4_3_1: "203.0.113.80", r4_3_2: "86.245.12.40", r4_4: "192.168.1.30" },
    qcm: { r1_2: ["B"], r1_3: ["A"], r2_4: [1, 2], r3_2: ["A"], r4_2: [1, 2] },
  },
  "etude-mediatheque": {
    etq: { e1_1_1: "Routeur", e1_1_2: "Switch", e1_1_3: "Point d'accès Wi-Fi", e1_2_1: "Fibre optique",
      e1_2_2: "Câble Ethernet", e4_1_1: "Transmise par le routeur", e4_1_2: "Bloquée par le routeur",
      e4_1_3: "Sans passer par le routeur", e4_1_4: "Transmise par le routeur", e4_1_5: "Bloquée par le routeur" },
    txt: { e2_1_1: "192.168.10.1", e2_1_2: "192.168.20.1", e2_1_3: "192.168.10.2", e2_1_4: "192.168.10.3",
      e2_1_5: "192.168.10.11", e2_1_6: "192.168.20.110", e2_2: "100", e3_1: "12", e3_4: "750 Mbit/s", e3_5: "1440 s",
      e3_6: "16 s", e4_4: "198.51.100.25" },
    qcm: { e1_3: ["A"], e1_4: ["A"], e2_3: ["B"], e2_4: [1, 2], e2_5: ["A"], e3_2: ["C"], e3_3: ["B"], e4_2: ["A"],
      e4_3: ["C"], e4_5: [1, 2] },
  },
};
const CLE = { a: "adressage-maison", r: "requete-http", e: "etude-mediatheque" };
const cle = (id) => CLE[id[0]];
const qid = (id) => (id in EXOS[cle(id)].qcfg ? id : id + "_1");
const juste = (id, rep) => G.grade(String(rep), EXOS[cle(id)].qcfg[qid(id)].grader).ok;

// ============================================================ correcteurs
test("configuration : parties, durées, cases et points de chaque exercice", () => {
  const attendu = {
    "adressage-maison": [["Le schéma du réseau", "Le tableau d'adressage", "Des adresses à choisir", "Le débit de la connexion"], 45, 28],
    "requete-http": [["Les appareils et leurs couches", "L'encapsulation de la requête", "Les adresses dans la maison",
      "Au centre de données, puis la réponse"], 45, 30],
    "etude-mediatheque": [["L'architecture du réseau", "Le plan d'adressage", "Le choix des matériels et les débits",
      "Les échanges à travers le routeur"], 65, 32],
  };
  for (const [k, [titres, minutes, cases]] of Object.entries(attendu)) {
    assert.deepEqual(EXOS[k].parts.map((p) => p.title), titres, k);
    assert.equal(EXOS[k].minutes, minutes, k);
    assert.equal(Object.keys(EXOS[k].qcfg).length, cases, k);
    // la copie juste remplit chaque case, une fois
    const c = COPIES[k], ids = [...Object.keys(c.etq), ...Object.keys(c.txt), ...Object.keys(c.qcm)].map(qid);
    assert.deepEqual(ids.sort(), Object.keys(EXOS[k].qcfg).sort(), k);
  }
});

test("copies justes : chaque réponse est acceptée par son correcteur", () => {
  for (const c of Object.values(COPIES)) {
    for (const [id, v] of [...Object.entries(c.etq), ...Object.entries(c.txt)]) assert.ok(juste(id, v), `${id} : ${v}`);
    for (const [id, ks] of Object.entries(c.qcm)) {
      assert.ok(juste(id, ks.join(",")), id);
      if (ks.length > 1) assert.equal(juste(id, ks[0]), false, `${id} : une seule des bonnes propositions`);
    }
  }
});

test("étiquettes des trois exercices : la bonne est la seule acceptée de sa liste", () => {
  // chaque exercice a son gabarit, où les listes d'un schéma portent des noms communs à tous (bk-1-1…)
  for (const [k, c] of Object.entries(COPIES)) {
    const src = html.match(new RegExp(`<template id="tpl-parts-${k}">([\\s\\S]*?)</template>`))[1], listes = {};
    for (const m of src.matchAll(/<div class="bank" id="([^"]+)"[^>]*>([\s\S]*?)<\/div>/g))
      listes[m[1]] = [...m[2].matchAll(/<button type="button" class="etq"[^>]*>([^<]*)<\/button>/g)].map((x) => x[1].replace(/&#x27;/g, "'"));
    for (const [id, v] of Object.entries(c.etq)) {
      const liste = listes[src.match(new RegExp(`id="dz-${id}" data-bank="([^"]+)"`))[1]];
      assert.deepEqual(liste.filter((e) => juste(id, e)), [v], id);
    }
  }
});

test("cases saisies : formes admises, erreurs courantes refusées", () => {
  const ok = { a2_1_1: ["192.168.1", " 192.168.1 "], a4_1: ["400 s", "400s", "400 secondes", "400,0 s"],
    a4_2: ["1333 s", "1 333 s", "1334 s"], a4_3: ["48 Mbit/s", "48 mbits/s"], e3_4: ["750 Mbit/s", "750 Mbps"],
    e3_5: ["1440 s", "1 440 secondes"], e3_6: ["16 s"], e2_1_6: ["192.168.20.110"], r4_4: ["192.168.1.30"] };
  const ko = { a2_1_1: ["192.168.1.0", "192.168.1.10"], a3_2: ["192.168.1.31", "192.168.1.320"],
    a4_1: ["50 s", "3200 s"], a4_3: ["6 Mbit/s", "24 Mbit/s"], e2_1_1: ["192.168.20.1", "192.168.10.0"],
    e2_1_6: ["192.168.10.110", "192.168.20.10"], e2_2: ["99", "249"], e3_1: ["10", "11"],
    e3_4: ["1000 Mbit/s", "350 Mbit/s"], e3_5: ["180 s", "720 s"], e3_6: ["2 s", "128 s"],
    e4_4: ["192.168.20.1", "192.168.20.163"], r4_3_2: ["192.168.1.30"], r4_4: ["86.245.12.40"] };
  for (const [id, l] of Object.entries(ok)) for (const r of l) assert.ok(juste(id, r), `${id} : ${r}`);
  for (const [id, l] of Object.entries(ko)) for (const r of l) assert.equal(juste(id, r), false, `${id} : ${r}`);
});

// ============================================================ navigateur
let browser;
test.before(async () => { browser = await chromium.launch(); });
test.after(async () => { await browser.close(); });

async function open(url, opts) {
  const context = await browser.newContext(Object.assign({ viewport: { width: 1366, height: 900 } }, opts || {}));
  const page = await context.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  page.on("dialog", (d) => d.accept());
  await page.goto(url);
  return { context, page, errors };
}
const text = (page, sel) => page.locator(sel).first().innerText();
// une étiquette : la toucher dans la liste que la case accepte, puis toucher la case
async function poser(page, id, etiquette) {
  const liste = await page.locator(`#dz-${id}`).getAttribute("data-bank");
  await page.locator(`#${liste}`).getByRole("button", { name: etiquette, exact: true }).click();
  await page.click(`#dz-${id}`);
}
async function remplir(page, copie, garder) {
  garder = garder || (() => true);
  for (const [id, v] of Object.entries(copie.etq)) if (garder(id)) await poser(page, id, v);
  for (const [id, v] of Object.entries(copie.txt)) if (garder(id)) await page.fill(`#in-${id}`, v);
  for (const [id, ks] of Object.entries(copie.qcm))
    if (garder(id)) for (const k of ks) await page.click(`#${id} .qcm-o[data-k='${k}' i]`);
}
// valider une question : à une case, à plusieurs cases (sur un schéma, son bouton est sous la figure), QCM
async function valider(page, id) {
  const relais = page.locator(`.btn-plan[data-g=${id}]`);
  if (await relais.count()) await relais.click();
  else await page.click(`#${id} .btn-validate, #${id} .btn-fast`);
}
const questions = (page) => page.locator(".q[data-q], .fast-q[id]").evaluateAll((l) => l.map((q) => q.id));

for (const [k, copie] of Object.entries(COPIES)) {
  test(`${k} : la copie juste vaut 20/20 en entraînement, sans erreur JavaScript`, async () => {
    const { context, page, errors } = await open(URL + "?ex=" + k);
    await page.click("[data-mode=training]");
    await remplir(page, copie);
    for (const id of await questions(page)) await valider(page, id);
    // aucune case refusée (la liste des refusées, si la note n'est pas 20)
    assert.deepEqual(await page.locator(".is-ko").evaluateAll((l) => l.map((e) => e.id || e.closest("[id]").id)), []);
    assert.equal((await text(page, "#recap .final-note")).trim(), "20,0/20");
    assert.deepEqual(errors, []);
    await context.close();
  });
}

test("exercice 1.3 : schéma de la maison, mauvaise étiquette corrigée sur le schéma", async () => {
  const { context, page, errors } = await open(URL + "?ex=adressage-maison");
  await page.click("[data-mode=training]");
  assert.equal(await page.locator(".plan-fig").count(), 1);
  assert.equal(await page.locator("#plan-1 .dz-f").count(), 8);
  await poser(page, "a1_1_1", "Routeur");
  await poser(page, "a1_1_2", "Modem");
  for (const id of ["a1_1_3", "a1_1_4"]) await poser(page, id, COPIES["adressage-maison"].etq[id]);
  await valider(page, "a1_1");
  assert.match(await text(page, "#a1_1 .q-status"), /2 cases justes sur 4/);
  assert.ok(await page.locator("#dz-a1_1_1.is-ko").count());
  assert.ok(await page.locator("#dz-a1_1_3.is-ok").count());
  await page.fill("#in-a3_2", "192.168.1.31");
  await page.click("#a3_2 .btn-validate");
  assert.match(await text(page, "#a3_2 .q-status"), /Faux/);
  assert.match(await text(page, "#a3_2 .q-expected"), /192\.168\.1\.32/);
  assert.deepEqual(errors, []);
  await context.close();
});

test("exercice 2.1 : l'animation du trajet attend la correction des parties 3 et 4, puis rejoue les adresses", async () => {
  const k = "requete-http", copie = COPIES[k];
  const { context, page, errors } = await open(URL + "?ex=" + k, { reducedMotion: "reduce" });
  await page.click("[data-mode=training]");
  assert.equal(await page.locator(".plan-fig").count(), 3);
  assert.ok(await page.locator("#rq-go").isDisabled());
  await remplir(page, copie, (id) => /^r[34]/.test(id));
  for (const id of ["r3_1", "r3_2", "r4_1", "r4_2", "r4_3"]) await valider(page, id);
  await page.waitForTimeout(700);
  assert.ok(await page.locator("#rq-go").isDisabled(), "Q4.4 n'est pas encore corrigée");
  await valider(page, "r4_4");
  await page.waitForFunction(() => !document.getElementById("rq-go").disabled, null, { timeout: 3000 });
  assert.equal(await text(page, "#rq-verrou"), "");
  await page.click("#rq-go");
  await page.waitForFunction(() => /Trajet terminé/.test(document.getElementById("rq-t").textContent), null, { timeout: 10000 });
  // dernière étape : la réponse arrive à l'ordinateur portable, adressée à son adresse privée
  assert.match(await page.locator("#rq-mac").textContent(), /3C:52:A1:10:20:01 → 28:87:A5:EF:18:5D/);
  assert.match(await page.locator("#rq-ip").textContent(), /203\.0\.113\.80 → 192\.168\.1\.30/);
  assert.deepEqual(errors, []);
  await context.close();
});

test("exercice 2.1 en examen : l'animation se déverrouille à la remise de la copie", async () => {
  const { context, page, errors } = await open(URL + "?ex=requete-http", { reducedMotion: "reduce" });
  await page.click("[data-mode=exam]");
  assert.ok(await page.locator("#rq-go").isDisabled());
  await page.click("#exam-submit"); await page.click("#exam-submit");
  await page.waitForFunction(() => !document.getElementById("rq-go").disabled, null, { timeout: 3000 });
  assert.equal((await text(page, "#recap .final-note")).trim(), "0,0/20");
  assert.deepEqual(errors, []);
  await context.close();
});

test("étude de cas 1 : rubrique de l'accueil, plan, documents, examen pondéré par la durée des parties", async () => {
  const a = await open(URL);
  assert.deepEqual(await a.page.locator(".etude-grid .mode-card").evaluateAll((cs) => cs.map((c) =>
    [c.querySelector(".mc-tag").textContent.trim(), c.querySelector("h3").textContent, c.querySelector("a").getAttribute("href")])),
  [["Étude 1 Niveau 2", "Le réseau d'une médiathèque", "?ex=etude-mediatheque"]]);
  assert.equal(await a.page.locator(".en-edition").count(), 0, "plus aucune rubrique « En cours d'édition »");
  assert.deepEqual(await a.page.locator(".exo-grid .mode-card h3").allInnerTexts(), ["QCM : réseaux informatiques",
    "Mon premier site", "Le plan d'adressage de la maison", "Suivre une requête à travers le réseau"]);
  await a.context.close();
  const { context, page, errors } = await open(URL + "?ex=etude-mediatheque");
  assert.match(await text(page, "#home .home-head"), /Étude 1[\s\S]*Niveau 2[\s\S]*Le réseau d'une médiathèque/);
  await page.click("[data-mode=exam]");
  assert.equal(await page.locator("#plan-1 .dz-f").count(), 5);
  await page.click(".qbar[aria-label='Q1.1'] .doc-chip[data-doc=DT1]");
  assert.match(await text(page, "#doc-DT1"), /Switch[\s\S]*130\s€/);
  await page.click(".dp-tabs [data-doc=DT2]");
  assert.match(await text(page, "#doc-DT2"), /100 m au plus/);
  await page.keyboard.press("Escape");
  await remplir(page, COPIES["etude-mediatheque"], (id) => id.startsWith("e1_"));
  await page.click("#exam-submit"); await page.click("#exam-submit");
  // partie 1 juste : 15 min sur 65 → 20 × 15 / 65 = 4,6/20
  assert.equal((await text(page, "#recap .final-note")).trim(), "4,6/20");
  assert.equal(await page.locator("#plan-1 .dz-f.is-ok").count(), 5);
  assert.deepEqual(errors, []);
  await context.close();
});
