// Tests navigateur (Playwright + Chromium) : accueil, cours, parcours entraînement et examen, étiquettes, QCM, documents.
//   NODE_PATH=$(npm root -g) node --test tests/navigateur.test.js
// L'accueil publié (index.html) est vérifié tel quel : rubriques, cartes, puis chaque cours et chaque exercice qu'il
// propose (aucun tant que tout est « En cours d'édition »). La page modèle (modele.html, régénérée ici) exerce chaque
// mécanisme sur le cours et l'exercice modèles de src/modele.py.
const test = require("node:test");
const assert = require("node:assert/strict");
const path = require("node:path");
const fs = require("node:fs");
const { execFileSync } = require("node:child_process");
const { chromium } = require("playwright");

const RACINE = path.join(__dirname, "..");
execFileSync("python3", [path.join(RACINE, "src", "generer.py"), "--modele"]);
const INDEX = "file://" + path.join(RACINE, "index.html");
const MODELE = "file://" + path.join(RACINE, "modele.html");
const EX = MODELE + "?ex=exercice-modele";
let browser;

test.before(async () => { browser = await chromium.launch(); });
test.after(async () => { await browser.close(); });

async function open(url, viewport) {
  const context = await browser.newContext({ viewport: viewport || { width: 1366, height: 900 } });
  const page = await context.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  page.on("dialog", (d) => d.accept());
  await page.goto(url);
  return { context, page, errors };
}
const text = (page, sel) => page.locator(sel).first().innerText();
// une case se remplit comme le fait l'élève : toucher l'étiquette (dans la liste que la case accepte), puis la case
async function poser(page, id, etiquette) {
  const liste = await page.locator(`#dz-${id}`).getAttribute("data-bank");
  await page.locator(`#${liste}`).getByRole("button", { name: etiquette, exact: true }).click();
  await page.click(`#dz-${id}`);
}
// question posée sur un schéma : son bouton « Valider » est dans le bandeau sous la figure
async function valider(page, gid) {
  const relais = page.locator(`.btn-plan[data-g=${gid}]`);
  await ((await relais.count()) ? relais.click() : page.click(`#${gid} .btn-fast`));
}
async function saisir(page, id, v) { await page.fill(`#in-${id}`, v); }
// toutes les réponses justes de l'exercice modèle
const JUSTE = { m1_1: "commutateur", m1_2: "192.168.1.12", m1_3: "254", m1_4_1: "192.168.1.0", m1_4_2: "192.168.1.255" };
const ETQ = { m2_1_1: "Le routeur", m2_1_2: "Le commutateur", m2_1_3: "Le serveur", m2_2_1: "Adresse IP",
  m2_2_2: "Adresse MAC", m2_2_3: "Masque de sous-réseau" };
async function toutJuste(page, sauf) {
  sauf = sauf || {};
  for (const [id, v] of Object.entries(JUSTE)) await saisir(page, id, id in sauf ? sauf[id] : v);
  for (const [id, v] of Object.entries(ETQ)) await poser(page, id, v);
  await page.click("#m3_1 .qcm-o[data-k='B']");
  if (!sauf.m3_2) for (const k of ["1", "2", "4"]) await page.click(`#m3_2 .qcm-o[data-k='${k}']`);
}
async function toutValider(page) {
  for (const id of ["m1_1", "m1_2", "m1_3"]) await page.click(`#${id} .btn-validate`);
  for (const gid of ["m1_4", "m2_1", "m2_2", "m3_1", "m3_2"]) await valider(page, gid);
}
// cartes d'une rubrique de l'accueil : [étiquette, titre, lien]
const cartes = (page, sel) => page.locator(sel + " .mode-card").evaluateAll((cs) => cs.map((c) => [
  c.querySelector(".mc-tag").textContent.trim(), c.querySelector("h3").textContent,
  c.querySelector("a") ? c.querySelector("a").getAttribute("href") : null]));

async function verifierCartes(page) {
  // chaque carte : une vignette chargée, 3 à 5 mots-clés, aucun paragraphe de texte ; toutes de la même taille
  const cs = await page.locator("#home .carte-v").evaluateAll((l) => l.map((c) => ({
    img: c.querySelector("img.cv-img") ? c.querySelector("img.cv-img").naturalWidth : -1,
    mots: c.querySelectorAll(".cv-mots li").length, p: c.querySelectorAll("p:not(.etat)").length,
    taille: [Math.round(c.offsetWidth), c.offsetHeight] })));
  for (const c of cs) {
    assert.ok(c.mots >= 3 && c.mots <= 5, JSON.stringify(c));
    assert.equal(c.p, 0);
    assert.ok(c.img > 0, "carte illustrée");
    assert.equal(c.taille[0], cs[0].taille[0]);
    assert.ok(Math.abs(c.taille[1] - cs[0].taille[1]) <= 1, JSON.stringify(cs.map((x) => x.taille)));
  }
  return cs.length;
}

test("accueil publié : trois rubriques en cartes illustrées, « En cours d'édition » tant qu'une rubrique est vide", async () => {
  const { context, page, errors } = await open(INDEX);
  assert.ok(await page.locator("body.hub").count());
  assert.ok(await page.isVisible("#home"));
  assert.ok(!(await page.isVisible("main.page")));
  assert.ok(!(await page.isVisible(".banner")));
  assert.match(await text(page, "#home h1"), /Réseau informatique/);
  assert.equal(await page.title(), "Réseau informatique — cours et exercices interactifs");
  assert.ok(await page.evaluate(() => [...document.querySelectorAll("#home img")].every((i) => i.complete && i.naturalWidth > 0)));
  assert.deepEqual(await page.locator("#home h2").allInnerTexts(), ["Les cours", "Les exercices", "Études de cas"]);
  // une rubrique vide montre une seule carte, « En cours d'édition », sans lien ; sinon chaque carte a son lien
  for (const sel of [".cours-grid", ".exo-grid", ".etude-grid"]) {
    const cs = await cartes(page, sel);
    const vides = await page.locator(sel + " .en-edition").count();
    assert.ok(cs.length >= 1, sel);
    if (vides) {
      assert.equal(cs.length, 1, sel);
      assert.equal(cs[0][2], null);
      assert.match(await text(page, sel + " .etat"), /En cours d'édition/);
    } else for (const c of cs) assert.match(c[2], /^\?ex=[a-z0-9-]+$/, sel);
  }
  assert.ok(await verifierCartes(page) >= 3);
  assert.equal(await page.locator("#home .btn-mode").count(), 0);
  await page.setViewportSize({ width: 390, height: 844 });
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
  const src = fs.readFileSync(path.join(RACINE, "index.html"), "utf8").replace(/data:[^"]+/g, "");
  assert.doesNotMatch(src, /\b(BTS|STI2D|bac(calaur[ée]at)?|session \d|[ée]preuve|acad[ée]mie|sujet z[ée]ro|brevet)\b/i);
  assert.deepEqual(errors, []);
  await context.close();
});

test("adresse inconnue : retour à l'accueil", async () => {
  for (const url of [INDEX + "?ex=inconnu", INDEX + "?ex=cours-inconnu", MODELE + "?ex=hub"]) {
    const { context, page, errors } = await open(url);
    assert.ok(await page.locator("body.hub .cours-grid").count(), url);
    assert.deepEqual(errors, []);
    await context.close();
  }
});

for (const [nom, url] of [["index.html", INDEX], ["modele.html", MODELE]]) {
  test(`${nom} : chaque cours et chaque exercice de l'accueil s'ouvrent, en entraînement et en examen, sans erreur`, async () => {
    const a = await open(url);
    const liens = await a.page.locator("#home .carte-v a[href^='?ex=']").evaluateAll((l) => l.map((x) => [x.getAttribute("href"), x.closest(".carte-v").querySelector("h3").textContent]));
    await a.context.close();
    if (nom === "modele.html") assert.equal(liens.length, 2);
    for (const [lien, titre] of liens) {
      if (lien.startsWith("?ex=cours-")) {
        const { context, page, errors } = await open(url + lien);
        assert.ok(await page.locator("body.cours-page").count(), lien);
        assert.equal(await text(page, "#home h1"), titre);
        assert.ok(await page.locator(".cours-sec").count() >= 1, lien);
        assert.ok(await page.isVisible(".cours-foot .cours-print"), lien);
        assert.ok(await page.isVisible(".cours-foot a[href='?']"), lien);
        assert.deepEqual(errors, [], lien);
        await context.close();
        continue;
      }
      for (const mode of ["training", "exam"]) {
        const { context, page, errors } = await open(url + lien);
        assert.equal(await text(page, "#home h1"), titre);
        await page.click(`[data-mode=${mode}]`);
        assert.ok(await page.isVisible("main.page"), lien);
        assert.equal(await text(page, ".cartouche h1"), titre);
        const n = await page.evaluate(() => window.__PARTS__.length);
        assert.equal(await page.locator("#parts .part").count(), n, lien);
        assert.ok(n >= 1);
        if (mode === "exam") assert.equal(await page.locator(".btn-validate:visible, .btn-fast:visible, .btn-plan:visible").count(), 0);
        assert.deepEqual(errors, [], `${lien} (${mode})`);
        await context.close();
      }
    }
  });
}

test("page modèle : l'accueil montre les cartes du cours et de l'exercice, la rubrique vide reste annoncée", async () => {
  const { context, page, errors } = await open(MODELE);
  assert.match(await text(page, "#home .home-modele"), /Page modèle/);
  assert.deepEqual(await cartes(page, ".cours-grid"), [["Cours modèle Niveau 1", "Les matériels du réseau local", "?ex=cours-modele"]]);
  assert.deepEqual(await cartes(page, ".exo-grid"), [["Exercice modèle Niveau 1", "Le réseau de la salle", "?ex=exercice-modele"]]);
  assert.deepEqual(await cartes(page, ".etude-grid"), [["Étude 1", "Étude de cas", null]]);
  assert.equal(await page.locator(".en-edition").count(), 1);
  assert.equal(await verifierCartes(page), 3);
  assert.deepEqual(errors, []);
  await context.close();
});

test("cours modèle : sections, cartes, script propre au cours, jeu, quiz, impression, lien vers l'exercice", async () => {
  const { context, page, errors } = await open(MODELE + "?ex=cours-modele");
  assert.match(await text(page, "#home .home-head"), /Cours modèle[\s\S]*Niveau 1[\s\S]*Les matériels du réseau local/);
  assert.equal(await page.title(), "Les matériels du réseau local — cours — Réseau informatique");
  assert.equal(await page.locator(".cours-sec").count(), 4);
  assert.deepEqual(await page.locator(".cours-nav a").allInnerTexts(), ["1. Les matériels", "2. En binaire", "3. Jeu", "4. Quiz"]);
  assert.match(await text(page, ".c-fiche"), /Objectifs[\s\S]*Prérequis/);
  // cartes à retourner
  const carte = page.locator(".carte").nth(1);
  assert.equal(await carte.getAttribute("aria-expanded"), "false");
  await carte.click();
  assert.equal(await carte.getAttribute("aria-expanded"), "true");
  assert.match(await carte.innerText(), /passerelle/);
  // élément interactif propre au cours (clés js et init)
  assert.equal(await text(page, "#cm-bin"), "11000000 . 10101000 . 00000001 . 00001100");
  await page.fill("#cm-ip", "10.0.0.300");
  assert.ok(await page.locator("#cm-bin.ko").count());
  await page.fill("#cm-ip", "255.255.255.0");
  assert.equal(await text(page, "#cm-bin"), "11111111 . 11111111 . 11111111 . 00000000");
  // jeu : une erreur (le bon bouton est montré), le reste juste
  const lignes = page.locator("#jeu-materiel .jeu-l");
  const n = await lignes.count();
  for (let i = 0; i < n; i++) {
    const ok = await lignes.nth(i).getAttribute("data-ok");
    await lignes.nth(i).locator(`button[data-v="${i === 0 ? (ok === "com" ? "rou" : "com") : ok}"]`).click();
  }
  assert.equal((await text(page, "#jeu-materiel .jeu-s")).trim(), `${n - 1} / ${n}`);
  assert.ok(await page.locator("#jeu-materiel .jeu-l >> nth=0 >> .pick-good").count());
  await page.click("#jeu-materiel .jeu-reset");
  assert.equal((await text(page, "#jeu-materiel .jeu-s")).trim(), `0 / ${n}`);
  // quiz : tout juste, trois étoiles
  const q = await page.locator(".quiz-q").count();
  for (let i = 0; i < q; i++) {
    const fs_ = page.locator(".quiz-q").nth(i);
    await fs_.locator(`input[value="${await fs_.getAttribute("data-ok")}"]`).check();
  }
  assert.equal((await text(page, "#qz-score")).trim(), `${q} / ${q}`);
  assert.equal((await text(page, "#qz-stars")).trim(), "★★★");
  assert.ok(await page.locator(".quiz-why:visible").count() === q);
  // impression : sommaire et pied masqués, explications et dos des cartes imprimés
  await page.emulateMedia({ media: "print" });
  assert.ok(!(await page.isVisible(".cours-nav")));
  assert.ok(await page.isVisible(".carte >> nth=0 >> .dos"));
  await page.emulateMedia({ media: "screen" });
  await page.click(".cours-foot a[href='?ex=exercice-modele']");
  await page.waitForURL(/\?ex=exercice-modele$/);
  assert.match(await text(page, "#home h1"), /Le réseau de la salle/);
  assert.deepEqual(errors, []);
  await context.close();
});

test("exercice modèle en entraînement : saisies, cases groupées, étiquettes, schéma, QCM ; tout juste = 20/20", async () => {
  const { context, page, errors } = await open(EX);
  assert.match(await text(page, "#home .home-head"), /Exercice modèle[\s\S]*Niveau 1[\s\S]*Le réseau de la salle/);
  assert.match(await text(page, "#home .home-facts"), /3 parties[\s\S]*8 questions[\s\S]*25\s*min[\s\S]*2 documents[\s\S]*DP1 et DT1[\s\S]*13 cases/);
  await page.click("[data-mode=training]");
  assert.match(await text(page, ".cartouche"), /8 questions, 13 cases notées, réparties en 3 parties/);
  assert.match(await text(page, ".consignes"), /Réponses écrites[\s\S]*Des étiquettes à glisser[\s\S]*Questions à propositions/);
  assert.match(await text(page, "#partie-1 .duree"), /12\s*min · Barème : 5 points, soit 48,0 %/);
  // questions à une case : réponse vide refusée sans être comptée, réponse fausse, réponses justes
  await page.click("#m1_2 .btn-validate");
  assert.match(await text(page, "#m1_2 .q-msg"), /Saisis une réponse/);
  assert.ok(!(await page.locator("#in-m1_2").isDisabled()));
  await saisir(page, "m1_1", "le routeur");
  await page.press("#in-m1_1", "Enter");
  assert.match(await text(page, "#m1_1 .q-status"), /Faux/);
  assert.ok(await page.isVisible("#m1_1 .q-expl"));
  assert.match(await text(page, "#m1_1 .q-expected"), /Le commutateur/);
  await saisir(page, "m1_2", "192.168.1.12"); await page.click("#m1_2 .btn-validate");
  await saisir(page, "m1_3", "254"); await page.click("#m1_3 .btn-validate");
  assert.match(await text(page, "#m1_2 .q-status"), /Juste/);
  assert.match(await text(page, "#m1_3 .q-status"), /Juste/);
  // cases groupées saisies : une case vide, confirmation demandée
  await valider(page, "m1_4");
  assert.match(await text(page, "#m1_4 .q-msg"), /Complète au moins une case/);
  await saisir(page, "m1_4_1", "192.168.1.0");
  await valider(page, "m1_4");
  assert.match(await text(page, "#m1_4 .btn-fast"), /Valider quand même \(1 case vide\)/);
  await valider(page, "m1_4");
  assert.match(await text(page, "#m1_4 .q-status"), /1 case juste sur 2/);
  assert.match(await text(page, "#m1_4 .btn-fast"), /Réponses validées/);
  assert.ok(await page.locator("#in-m1_4_2").evaluate((i) => i.disabled && i.closest(".sol").classList.contains("is-ko")));
  // schéma : énoncé au-dessus, cases sur la figure, bandeau d'étiquettes et de boutons sous la figure
  assert.ok(!(await page.isVisible("#m2_1")), "la question posée sur le schéma n'affiche que sa correction");
  assert.match(await text(page, "#plan-2 .plan-qs"), /Q2\.1/);
  assert.equal(await page.locator("#plan-2 .dz-f").count(), 3);
  await page.click("#dz-m2_1_1");
  assert.match(await text(page, "#plan-2 .plan-msg"), /Choisis d'abord une étiquette/);
  await poser(page, "m2_1_1", "Le routeur");
  assert.equal(await text(page, "#plan-2 .plan-msg"), "", "le message s'efface quand on pose une étiquette");
  assert.equal(await page.locator("#in-m2_1_1").inputValue(), "Le routeur");
  await poser(page, "m2_1_2", "Le serveur");
  // une étiquette touchée éclaire les cases de sa liste ; une case d'une autre liste la refuse
  await page.locator("#bk-2-1").getByRole("button", { name: "Le commutateur", exact: true }).click();
  assert.equal(await page.locator(".dz.cible").count(), 3);
  await page.click("#dz-m2_2_1");
  assert.match(await text(page, "#m2_2 .q-msg"), /attend une étiquette de la liste « Étiquettes »/);
  await page.keyboard.press("Escape");
  assert.equal(await page.locator(".dz.cible").count(), 0);
  await valider(page, "m2_1");
  assert.match(await text(page, ".btn-plan[data-g=m2_1]"), /valider quand même/);
  await valider(page, "m2_1");
  assert.match(await text(page, "#m2_1 .q-status"), /1 case juste sur 3/);
  assert.ok(await page.isVisible("#m2_1 .q-expl"));
  assert.ok(await page.locator(".btn-plan[data-g=m2_1].moy").isDisabled());
  assert.ok(await page.locator("#dz-m2_1_1.is-ok").count());
  assert.ok(await page.locator("#dz-m2_1_2.is-ko").isDisabled());
  assert.equal(await page.locator("#dz-m2_1_2 .dz-a").textContent(), "Le commutateur");
  assert.equal(await page.locator("#bk-2-1 .etq:not([disabled])").count(), 0, "liste verrouillée");
  // étiquettes sous l'énoncé : glisser-déposer, échange entre deux cases, toucher puis toucher
  await page.dragAndDrop("#bk-m2_2 .etq >> text=Adresse IP", "#dz-m2_2_1");
  assert.equal(await page.locator("#in-m2_2_1").inputValue(), "Adresse IP");
  await poser(page, "m2_2_2", "Masque de sous-réseau");
  await poser(page, "m2_2_3", "Adresse MAC");
  await page.dragAndDrop("#dz-m2_2_2", "#dz-m2_2_3");
  assert.equal(await page.locator("#in-m2_2_2").inputValue(), "Adresse MAC");
  assert.equal(await page.locator("#in-m2_2_3").inputValue(), "Masque de sous-réseau");
  await valider(page, "m2_2");
  assert.match(await text(page, "#m2_2 .q-status"), /3 cases justes sur 3/);
  // QCM : Valider inactif sans choix, une réponse unique remplace la précédente, réponses multiples incomplètes
  assert.ok(await page.locator("#m3_1 .btn-fast").isDisabled());
  await page.click("#m3_1 .qcm-o[data-k='A']"); await page.click("#m3_1 .qcm-o[data-k='B']");
  assert.equal(await page.locator("#m3_1 .qcm-o[aria-checked=true]").count(), 1);
  await valider(page, "m3_1");
  assert.equal(await text(page, "#m3_1 .q-status"), "Bonne réponse");
  await page.click("#m3_2 .qcm-o[data-k='1']"); await page.click("#m3_2 .qcm-o[data-k='2']");
  assert.equal(await page.locator("#m3_2 .qcm-o[aria-checked=true]").count(), 2);
  await valider(page, "m3_2");
  assert.equal(await text(page, "#m3_2 .q-status"), "Réponse fausse");
  assert.ok(await page.locator("#m3_2 .qcm-o.ok[data-k='4']").count(), "bonne réponse oubliée montrée");
  assert.match(await text(page, "#m3_2 .qcm-rep"), /1\) 192\.168\.1\.12 ; 2\) 10\.0\.0\.5 ; 4\) 172\.16\.4\.1/);
  // P1 : 3/5 → 12 (12 min) ; P2 : 4/6 → 13,33 (8 min) ; P3 : 1/2 → 10 (5 min) → 300,67 / 25 = 12,0
  assert.equal((await text(page, "#recap .final-note")).trim(), "12,0/20");
  assert.match(await text(page, "#recap-body"), /Partie 1 — Adresses du réseau[\s\S]*3,0 \/ 5[\s\S]*12,0/);
  assert.deepEqual(errors, []);
  await context.close();

  // second passage : tout juste
  const b = await open(EX);
  await b.page.click("[data-mode=training]");
  await toutJuste(b.page);
  await toutValider(b.page);
  assert.equal((await text(b.page, "#recap .final-note")).trim(), "20,0/20");
  assert.equal((await text(b.page, "#score-val")).replace(/\s/g, ""), "20,0/20");
  assert.equal(await b.page.locator(".dz-f.is-ok").count(), 3);
  assert.deepEqual(b.errors, []);
  await b.context.close();
});

test("exercice modèle en examen : rien ne filtre avant la remise, y compris à l'impression ; remise en deux temps", async () => {
  const { context, page, errors } = await open(EX);
  await page.click("[data-mode=exam]");
  assert.ok(!(await page.isVisible("#score-val")));
  assert.ok(!(await page.isVisible("#m1_1 .btn-validate")));
  assert.ok(!(await page.isVisible("#plan-2 .plan-val")), "pas de bouton « Valider » en examen");
  assert.ok(await page.isVisible("#plan-2 .plan-tray"));
  await toutJuste(page, { m1_1: "routeur", m3_2: true });
  assert.match(await text(page, "#score-count"), /12 réponse\(s\) renseignée\(s\) sur 13/);
  await page.evaluate(() => window.dispatchEvent(new Event("beforeprint")));
  await page.emulateMedia({ media: "print" });
  assert.ok(await page.isVisible(".print-nograde"));
  assert.ok(!(await page.isVisible(".print-note-line")));
  assert.ok(!(await page.isVisible("#m1_1 .q-expl")));
  assert.ok(!(await page.isVisible("#recap-graded")));
  assert.ok(!(await page.isVisible("#plan-2 .plan-tray")));
  assert.equal(await page.locator(".dz-f.is-ok, .dz-f.is-ko, .qcm-o.ok").count(), 0);
  await page.emulateMedia({ media: "screen" });
  await page.click("#exam-submit");
  assert.match(await text(page, "#exam-warn"), /1 réponse\(s\) encore vide\(s\)/);
  await page.click("#exam-submit");
  assert.ok(await page.locator("body.graded").count());
  assert.match(await text(page, "#m1_1 .q-status"), /Faux/);
  assert.match(await text(page, "#m2_1 .q-status"), /3 cases justes sur 3/);
  assert.equal(await text(page, "#m3_2 .q-status"), "Pas de réponse");
  assert.equal(await page.locator("#plan-2 .dz-f.is-ok").count(), 3, "la copie corrigée se lit aussi sur le schéma");
  const t1 = await text(page, "#timer-val");
  await page.waitForTimeout(1300);
  assert.equal(await text(page, "#timer-val"), t1, "chronomètre arrêté");
  // P1 : 4/5 → 16 ; P2 : 20 ; P3 : 1/2 → 10 → (12 × 16 + 8 × 20 + 5 × 10) / 25 = 16,1
  assert.equal((await text(page, "#recap .final-note")).trim(), "16,1/20");
  await page.evaluate(() => window.dispatchEvent(new Event("beforeprint")));
  await page.emulateMedia({ media: "print" });
  assert.ok(await page.isVisible(".print-note-line"));
  assert.ok(await page.isVisible("#m1_1 .q-expl"));
  assert.deepEqual(errors, []);
  await context.close();
});

test("documents et téléphone : rail, panneau, Échap, barre de documents ; bouton « Documents » sur petit écran", async () => {
  const { context, page, errors } = await open(EX);
  await page.click("[data-mode=training]");
  assert.deepEqual(await page.locator(".rail .tab[data-doc]").evaluateAll((t) => t.map((x) => x.textContent)), ["DP1", "DT1"]);
  await page.click(".rail .tab[data-doc=DP1]");
  assert.ok(await page.locator("body.panel-open").count());
  assert.match(await text(page, "#dp-title"), /DP1 : Le réseau de la salle/);
  assert.match(await text(page, "#doc-DP1"), /Poste 2[\s\S]*192\.168\.1\.12/);
  await page.click(".dp-tabs [data-doc=DT1]");
  assert.match(await text(page, "#doc-DT1"), /adresse de diffusion/);
  await page.keyboard.press("Escape");
  assert.equal(await page.locator("body.panel-open").count(), 0);
  await page.click(".qbar[aria-label='Q1.1'] .doc-chip[data-doc=DT1]");
  assert.ok(await page.locator("body.panel-open").count());
  await page.keyboard.press("Escape");
  await page.setViewportSize({ width: 420, height: 860 });
  assert.ok(await page.isVisible("#btn-docs"));
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
  // sur téléphone, le bandeau du schéma reste sous la figure
  assert.equal(await page.locator("#plan-2 .plan-tray").evaluate((e) => getComputedStyle(e).position), "static");
  assert.deepEqual(errors, []);
  await context.close();
});
