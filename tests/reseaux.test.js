// Tests navigateur (Playwright + Chromium) du cours 1, du QCM 1.1 et de l'exercice 1.2 (index.html).
//   NODE_PATH=$(npm root -g) node --test tests/reseaux.test.js
const test = require("node:test");
const assert = require("node:assert/strict");
const path = require("node:path");
const fs = require("node:fs");
const os = require("node:os");
const { chromium } = require("playwright");

const URL = "file://" + path.join(__dirname, "..", "index.html");
const COURS = URL + "?ex=cours-reseaux", QCM = URL + "?ex=qcm-reseaux", SITE = URL + "?ex=site-html";
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
const contenu = (page, sel) => page.locator(sel).first().textContent();
// une animation se termine : le texte de sa légende change
async function attendre(page, sel, re, timeout) {
  await page.waitForFunction(([s, r]) => new RegExp(r).test(document.querySelector(s).textContent), [sel, re.source], { timeout: timeout || 20000 });
}

// ============================================================ cours 1
test("cours 1 : en-tête, sommaire, neuf sections, dix-huit figures numérotées, téléphone", async () => {
  const { context, page, errors } = await open(COURS);
  assert.match(await text(page, "#home .home-head"), /Cours 1[\s\S]*Niveau 1[\s\S]*Réseaux informatiques[\s\S]*Problématique/);
  assert.match(await text(page, ".c-fiche"), /Objectifs[\s\S]*full\/half-duplex[\s\S]*Prérequis[\s\S]*bit et octet/);
  assert.equal(await page.locator(".cours-sec").count(), 9);
  assert.equal(await page.locator(".cours-nav a").count(), 9);
  const figures = await page.locator(".cr-fig > figcaption").allInnerTexts();
  assert.deepEqual(figures.map((f) => +f.match(/^Figure (\d+)/)[1]), Array.from({ length: 18 }, (_, i) => i + 1));
  // aucune image du Word : toutes les figures sont dessinées
  assert.equal(await page.locator("#cours-reseaux img").count(), 0);
  const src = await page.locator("#cours-reseaux").textContent();
  assert.doesNotMatch(src, /\b(STI2D|lycée|Nom :|Prénom :|Groupe :|CO\?\.\?)/, "blocs d'enseignant non repris");
  assert.match(src, /28:87:a5:ef:18:5d/, "adresse MAC d'exemple");
  assert.match(src, /pour chaque segment reçu/, "TCP acquitte des segments");
  assert.match(src, /échanges du Web/, "HTTP : le Web");
  await page.setViewportSize({ width: 390, height: 844 });
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
  assert.deepEqual(errors, []);
  await context.close();
});

test("cours 1, partie 1 : duplex, supports, portée, simulateur de débit", async () => {
  const { context, page, errors } = await open(COURS);
  assert.match(await text(page, "#cr-dx-t"), /^Full-duplex/);
  await page.click("#cr-duplex [data-dx=half]");
  assert.match(await text(page, "#cr-dx-t"), /^Half-duplex[\s\S]*talkie-walkie/);
  assert.match(await contenu(page, "#cr-dx-lab"), /émet, . écoute/);
  assert.ok(await page.locator("#cr-duplex.dx-ba, #cr-duplex[data-mode=half]").count());
  // supports : onglets et légende
  assert.ok(!(await page.isVisible("#cr-supports [data-pane=fibre]")));
  await page.click("#cr-supports [data-sup=fibre]");
  assert.ok(await page.isVisible("#cr-supports [data-pane=fibre]"));
  await page.click("#cr-supports [data-pane=fibre] .cr-leg-b[data-part=renfort]");
  assert.ok(await page.locator("#cr-supports .cr-part.cr-hl[data-part=renfort]").count());
  // portée
  await page.fill("#cr-portee", "30");
  assert.match(await text(page, "#cr-portee-t"), /30 m : Bluetooth ✘ hors de portée — Wi-Fi ✔ capté/);
  await page.fill("#cr-portee", "8");
  assert.match(await text(page, "#cr-portee-t"), /Bluetooth ✔ capté — Wi-Fi ✔ capté/);
  await page.fill("#cr-portee", "45");
  assert.match(await text(page, "#cr-portee-t"), /Wi-Fi ✘ hors de portée/);
  // débit : une photo de 4 Mo en Wi-Fi (300 Mbit/s), un film de 4 Go en Bluetooth (2 Mbit/s)
  assert.equal(await text(page, "#cr-deb-q"), "4 Mo = 32 Mbit");
  assert.equal(await text(page, "#cr-deb-t"), "107 ms");
  await page.selectOption("#cr-deb-f", "film");
  await page.selectOption("#cr-deb-l", "bt");
  assert.equal(await text(page, "#cr-deb-t"), "4 h 27 min");
  assert.match(await text(page, "#cr-deb-calc"), /32\s000 Mbit ÷ 2 Mbit\/s/);
  await page.click("#cr-deb-go");
  assert.match(await text(page, "#cr-deb-note"), /accélérée/);
  await attendre(page, "#cr-deb-note", /Transfert terminé/, 10000);
  assert.equal(await page.locator("#cr-debit [role=progressbar]").getAttribute("aria-valuenow"), "100");
  assert.deepEqual(errors, []);
  await context.close();
});

test("cours 1, partie 2 : le switch lit l'adresse MAC, topologies coupées, adresse MAC octet par octet", async () => {
  const { context, page, errors } = await open(COURS);
  await page.selectOption("#cr-sw-de", "2");
  await page.selectOption("#cr-sw-a", "3");
  await page.click("#cr-sw-go");
  await attendre(page, "#cr-sw-t", /Trame reçue par PC3/);
  assert.ok(await page.locator('#cr-sw-tab tr.cr-on[data-port="3"]').count());
  assert.ok(await page.locator("#cr-swp-3.cr-dest").count());
  assert.equal(await page.locator("#cr-switch .cr-dest").count(), 1, "seule la machine destinataire reçoit la trame");
  // topologies : une liaison coupée
  const couper = (i) => page.locator(`#cr-topo-svg .cr-tl[data-l="${i}"]`).dispatchEvent("click");
  await page.click("#cr-topo [data-topo=bus]");
  await couper(6);
  assert.match(await text(page, "#cr-topo-t"), /coupé en 2 groupes[\s\S]*\{PC1, PC2\} · \{PC3, PC4, PC5\}/);
  await page.click("#cr-topo [data-topo=anneau]");
  await couper(0);
  assert.match(await text(page, "#cr-topo-t"), /communiquent encore : les messages passent par un autre chemin/);
  await couper(3);
  assert.match(await text(page, "#cr-topo-t"), /coupé en 2 groupes/);
  await page.click("#cr-topo-reset");
  assert.match(await text(page, "#cr-topo-t"), /^Toutes les machines communiquent\./);
  await page.click("#cr-topo [data-topo=etoile]");
  await page.locator("#cr-topo-svg .cr-tsw").dispatchEvent("click");
  assert.match(await text(page, "#cr-topo-t"), /Plus aucune machine ne communique/);
  await page.click("#cr-topo [data-topo=maille]");
  await couper(0); await couper(5);
  assert.match(await text(page, "#cr-topo-t"), /communiquent encore/, "le maillage offre un autre chemin");
  assert.ok(await page.isVisible("[data-topo-txt=maille]"));
  // adresse MAC
  assert.match(await text(page, "#cr-mac-t"), /48 bits[\s\S]*28:87:A5/);
  await page.fill("#cr-mac", "00:40:05:a9:aa:71");
  assert.equal(await contenu(page, "#cr-mac-etq-t"), "00:40:05:A9:AA:71");
  await page.click("#cr-mac-oct .cr-oct >> nth=1");
  assert.match(await text(page, "#cr-mac-oct .cr-oct >> nth=1"), /40\s*01000000/);
  await page.fill("#cr-mac", "00:40:05:a9");
  assert.match(await text(page, "#cr-mac-t"), /6 couples/);
  assert.deepEqual(errors, []);
  await context.close();
});

test("cours 1, partie 3 : WAN, box, routage, dorsales, adresse IP et masque", async () => {
  const { context, page, errors } = await open(COURS);
  await page.click("#cr-wan-go");
  await attendre(page, "#cr-wan-t", /paquet/);
  await attendre(page, "#cr-wan-t", /Message reçu par B3/);
  // la box
  assert.ok(!(await page.isVisible("[data-mod-txt=modem]")));
  await page.click("#cr-box-go");
  await page.waitForTimeout(700);
  await page.click("#cr-box [data-mod=modem]");
  assert.match(await text(page, "[data-mod-txt=modem]"), /FAI/);
  // routage : une liaison de la route coupée, le paquet en prend une autre
  assert.equal(await text(page, "#cr-rt-t"), "Route : R1 → R3 → R6 → R11 → R14 → R17 (5 liaisons).");
  const couper = (k) => page.locator(`#cr-rt-svg .cr-tl[data-l="${k}"]`).dispatchEvent("click");
  await couper(4);
  assert.match(await text(page, "#cr-rt-t"), /route précédente est coupée[\s\S]*R1 → R4 → R6/);
  await page.locator('#cr-rt-svg .cr-rtn[data-r="1"]').dispatchEvent("click");
  assert.match(await text(page, "#cr-rt-t"), /Départ : R2/);
  await page.locator('#cr-rt-svg .cr-rtn[data-r="15"]').dispatchEvent("click");
  assert.match(await text(page, "#cr-rt-t"), /^Route : R2 → .* → R16/);
  await page.locator('#cr-rt-svg .cr-rtn[data-r="5"]').dispatchEvent("click");
  assert.match(await text(page, "#cr-rt-t"), /R16/, "un routeur « rond-point » n'est ni un départ ni une arrivée");
  for (const k of [24, 25]) await couper(k);
  assert.match(await text(page, "#cr-rt-t"), /Aucune route ne relie R2 à R16/);
  await page.click("#cr-rt-reset");
  assert.match(await text(page, "#cr-rt-t"), /^Route : R2 →/);
  // dorsales
  await page.locator("#cr-dorsales .cr-dors >> nth=0").dispatchEvent("click");
  assert.match(await text(page, "#cr-dors-t"), /Transatlantique Nord/);
  // adresse IP et découpage
  for (const [v, re] of [["89.234.17.105", /valide/], ["1.2.3", /4 nombres[\s\S]*ici 3/], ["300.1.1.1", /300 dépasse 255/], ["a.b.c.d", /« a »/]]) {
    await page.fill("#cr-ipv-in", v);
    assert.match(await text(page, "#cr-ipv-t"), re, v);
  }
  assert.match(await text(page, "#cr-dec-t"), /net-ID : 82\.162[\s\S]*host-ID : 240\.19[\s\S]*65 534/);
  await page.click('#cr-dec [data-dec="102.122.201.17|255.255.255.0"]');
  assert.match(await text(page, "#cr-dec-t"), /net-ID : 102\.122\.201[\s\S]*host-ID : 17[\s\S]*254 machines/);
  await page.click('#cr-dec [data-dec="19.102.12.193|255.0.0.0"]');
  assert.match(await text(page, "#cr-dec-t"), /net-ID : 19 [\s\S]*host-ID : 102\.12\.193[\s\S]*16 777 214/);
  assert.equal(await page.locator("#cr-dec-tab .cr-net").count(), 1);
  assert.deepEqual(errors, []);
  await context.close();
});

test("cours 1, partie 4 : traduction d'adresses, adresses privées, sous-réseaux logiques", async () => {
  const { context, page, errors } = await open(COURS);
  await page.selectOption("#cr-nat-p", "2");
  await page.click("#cr-nat-go");
  await attendre(page, "#cr-nat-t", /NAT/);
  assert.equal(await contenu(page, "#cr-nat-j text"), "92.169.148.17 → 216.58.206.238");
  await attendre(page, "#cr-nat-t", /Réponse reçue par l'ordinateur 192\.168\.1\.10[\s\S]*92\.169\.148\.17/);
  for (const [v, re] of [["172.20.5.1", /privée[\s\S]*172\.16\.0\.0/], ["172.32.0.1", /publique/], ["10.1.2.3", /privée/], ["192.169.0.1", /publique/]]) {
    await page.fill("#cr-priv-in", v);
    assert.match(await text(page, "#cr-priv-t"), re, v);
  }
  // sous-réseaux : PC1 et PC4 (192.168.0), PC2 et PC3 (192.168.1)
  assert.match(await text(page, "#cr-sr-t"), /2 sous-réseaux logiques/);
  assert.equal(await page.locator("#cr-sr-mat td.ok").count(), 4);
  await page.click("#cr-sr-go");
  await attendre(page, "#cr-sr-t", /net-ID différents[\s\S]*PC1 ne peut pas communiquer avec PC2/);
  await page.selectOption("#cr-sr-a", "4");
  await page.click("#cr-sr-go");
  await attendre(page, "#cr-sr-t", /PC1 et PC4 ont le même net-ID \(192\.168\.0\) : ils communiquent/);
  for (const i of [2, 3]) await page.fill(`#cr-sr-in${i}`, `192.168.0.${i}`);
  assert.match(await text(page, "#cr-sr-t"), /même net-ID : un seul sous-réseau/);
  assert.equal(await page.locator("#cr-sr-mat td.ok").count(), 12);
  await page.fill("#cr-sr-in2", "192.168.0.300");
  assert.equal(await page.locator("#cr-sr-in2").getAttribute("aria-invalid"), "true");
  assert.deepEqual(errors, []);
  await context.close();
});

test("cours 1, partie 5 : requête et réponse HTTP, segments TCP perdus et renvoyés", async () => {
  const { context, page, errors } = await open(COURS);
  await page.click("#cr-http-go");
  await attendre(page, "#cr-http-t", /^4\. Le navigateur affiche la page/);
  assert.match(await text(page, "#cr-http-req"), /GET \/index\.html HTTP\/1\.1/);
  assert.match(await text(page, "#cr-http-rep"), /200 OK[\s\S]*<!DOCTYPE html>/);
  assert.match(await text(page, "#cr-http-page"), /Bienvenue/);
  await page.selectOption("#cr-http-url", "/photos.html");
  await page.click("#cr-http-go");
  await attendre(page, "#cr-http-t", /^4\. Le navigateur affiche le message d'erreur/);
  assert.match(await text(page, "#cr-http-rep"), /404 Not Found/);
  assert.match(await text(page, "#cr-http-page"), /Erreur 404/);
  await page.check("#cr-tcp-perte");
  await page.click("#cr-tcp-go");
  await attendre(page, "#cr-tcp-t", /perdu en route/);
  await attendre(page, "#cr-tcp-t", /Message reconstitué dans l'ordre[\s\S]*4 segments ont été acquittés[\s\S]*renvoyé/, 25000);
  assert.equal(await contenu(page, "#cr-tcp-recu"), "Bonjour, comment ça va ?");
  assert.equal(await page.locator("#cr-tcp .cr-tcp-case.cr-on").count(), 4);
  assert.deepEqual(errors, []);
  await context.close();
});

test("cours 1, partie 6 : couches OSI, encapsulation, parcours à travers les couches", async () => {
  const { context, page, errors } = await open(COURS);
  await page.click('#cr-osi-g .cr-osi-d[data-c="3"] >> nth=0');
  assert.match(await text(page, "#cr-osi-t"), /Couche 3 — Réseau \(paquet\)[\s\S]*IP, adresse IP, routeurs/);
  assert.equal(await page.locator("#cr-osi-g .cr-c.cr-on").count(), 2, "les couches 3 de l'émetteur et du destinataire");
  await page.click("#cr-osi-go");
  await attendre(page, "#cr-osi-t", /Flux binaire/);
  await attendre(page, "#cr-osi-t", /a descendu les 7 couches de l'émetteur/);
  // encapsulation : 6 étapes, puis désencapsulation
  assert.ok(await page.locator("#cr-enc-prec").isDisabled());
  for (let i = 0; i < 4; i++) await page.click("#cr-enc-suiv");
  assert.match(await text(page, "#cr-enc-et"), /étape 5 \/ 6 : trame/);
  assert.deepEqual(await page.locator("#cr-enc-blocs .cr-blk").allInnerTexts(),
    ["En-tête Ethernet", "En-tête IP", "En-tête TCP", "En-tête applicatif", "Données", "Remorque Ethernet"]);
  await page.click("#cr-enc-blocs .cr-blk >> nth=1");
  assert.match(await text(page, "#cr-enc-det"), /adresse IP de l'émetteur et adresse IP du destinataire/i);
  assert.match(await text(page, "#cr-enc-pile li.cr-on"), /Liaison de données/);
  await page.click("#cr-enc-suiv");
  assert.ok(await page.isVisible("#cr-enc-blocs .cr-bits"));
  assert.ok(await page.locator("#cr-enc-suiv").isDisabled());
  await page.click("#cr-enc-dec");
  await page.click("#cr-enc-suiv");
  assert.match(await text(page, "#cr-enc-t"), /lit l'en-tête Ethernet[\s\S]*il reste un paquet/);
  assert.equal(await page.locator("#cr-enc-blocs .cr-blk").count(), 6);
  // parcours : pas à pas, puis d'un trait
  await page.click("#cr-par-pas");
  await attendre(page, "#cr-par-t", /^PC1 : le message descend les sept couches/);
  await page.waitForTimeout(3500);
  await page.click("#cr-par-pas");
  await attendre(page, "#cr-par-t", /^SW1 : le switch remonte jusqu'à la couche 2/);
  await page.click("#cr-par-go");
  await attendre(page, "#cr-par-t", /^R1 : le routeur remonte jusqu'à la couche 3/);
  await attendre(page, "#cr-par-t", /^PC2 : [\s\S]*Message reçu/, 30000);
  assert.deepEqual(errors, []);
  await context.close();
});

test("cours 1 : jeux, quiz, cartes, impression, liens vers les exercices", async () => {
  const { context, page, errors } = await open(COURS);
  for (const id of ["#cr-jeu-adr", "#cr-jeu-osi"]) {
    const lignes = page.locator(id + " .jeu-l"), n = await lignes.count();
    for (let i = 0; i < n; i++) await lignes.nth(i).locator(`button[data-v="${await lignes.nth(i).getAttribute("data-ok")}"]`).click();
    assert.equal((await text(page, id + " .jeu-s")).trim(), `${n} / ${n}`);
  }
  const q = await page.locator(".quiz-q").count();
  assert.equal(q, 10);
  for (let i = 0; i < q; i++) {
    const fs_ = page.locator(".quiz-q").nth(i);
    await fs_.locator(`input[value="${await fs_.getAttribute("data-ok")}"]`).check();
  }
  assert.equal((await text(page, "#qz-stars")).trim(), "★★★");
  await page.click("#cr-essentiel .carte >> nth=3");
  assert.match(await text(page, "#cr-essentiel .carte >> nth=3"), /net-ID/);
  // impression : le contenu des figures à onglets est imprimé
  await page.emulateMedia({ media: "print" });
  assert.ok(await page.isVisible("#cr-supports [data-pane=fibre]"));
  assert.ok(await page.isVisible("[data-topo-txt=bus]"));
  assert.ok(!(await page.isVisible(".cours-nav")));
  await page.emulateMedia({ media: "screen" });
  assert.deepEqual(await page.locator(".cours-foot a").evaluateAll((l) => l.map((a) => a.getAttribute("href"))),
    ["?ex=qcm-reseaux", "?ex=site-html", "?ex=adressage-maison", "?ex=requete-http", "?ex=etude-mediatheque", "?"]);
  assert.deepEqual(errors, []);
  await context.close();
});

// ============================================================ QCM 1.1
test("QCM 1.1 : 20/20 en entraînement, réponses fausses expliquées, examen sur une partie", async () => {
  const bons = (page) => page.evaluate(() => [...document.querySelectorAll(".qcm")].map((q) => {
    const g = window.__QCFG__[q.querySelector(".sol input").dataset.q].grader;
    return [q.id, q.getAttribute("data-multi") === "1", (g.equals || g.value.map(String))];
  }));
  const { context, page, errors } = await open(QCM);
  assert.match(await text(page, "#home .home-head"), /QCM 1\.1[\s\S]*Niveau 1[\s\S]*QCM : réseaux informatiques/);
  await page.click("[data-mode=training]");
  assert.match(await text(page, ".cartouche"), /47 questions, réparties en 6 parties/);
  assert.ok(await page.isVisible("#q2_4 figure svg"), "le schéma du bus");
  await page.click("#q1_9 .qcm-o[data-k='1']");
  await page.click("#q1_9 .btn-fast");
  assert.equal(await text(page, "#q1_9 .q-status"), "Réponse fausse");
  assert.ok(await page.locator("#q1_9 .qcm-o.ok[data-k='3']").count(), "40 Mbit/s, oubliée, est montrée");
  assert.match(await text(page, "#q1_9 .q-expl"), /5 × 8 = 40 Mbit\/s/);
  await context.close();
  const b = await open(QCM);
  await b.page.click("[data-mode=training]");
  for (const [id, multi, ks] of await bons(b.page)) {
    for (const k of multi ? ks : [ks[0]]) await b.page.click(`#${id} .qcm-o[data-k='${k}' i]`);
    await b.page.click(`#${id} .btn-fast`);
  }
  assert.equal((await text(b.page, "#recap .final-note")).trim(), "20,0/20");
  const c = await open(QCM);
  await c.page.click("[data-mode=exam]");
  for (const [id, multi, ks] of (await bons(c.page)).filter(([id]) => id.startsWith("q1_")))
    for (const k of multi ? ks : [ks[0]]) await c.page.click(`#${id} .qcm-o[data-k='${k}' i]`);
  await c.page.click("#exam-submit"); await c.page.click("#exam-submit");
  // partie 1 : 20/20, pèse 9 min sur 47 → 3,8/20
  assert.equal((await text(c.page, "#recap .final-note")).trim(), "3,8/20");
  assert.deepEqual(errors.concat(b.errors, c.errors), []);
  await b.context.close(); await c.context.close();
});

// ============================================================ exercice 1.2
const INDEX = `<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Mon réseau</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<h1>Le réseau de la maison</h1>
<p>Chez moi, la <strong>box</strong> relie à Internet les ordinateurs, les téléphones et la console.</p>
<h2>Les équipements</h2>
<ul><li>La box</li><li>L'ordinateur</li><li>Le téléphone</li></ul>
<img src="reseau.png" alt="Le réseau de la maison">
<a href="materiel.html">Le matériel</a>
</body>
</html>
`;
const MATERIEL = `<!DOCTYPE html>
<html lang="fr">
<head><title>Le matériel</title><link rel="stylesheet" href="style.css"></head>
<body>
<h1>Le matériel</h1>
<table>
<tr><th>Appareil</th><th>Adresse IP</th></tr>
<tr><td>Box</td><td>192.168.1.1</td></tr>
<tr><td>Ordinateur</td><td>192.168.1.10</td></tr>
</table>
<a href="index.html">Accueil</a>
</body>
</html>
`;
const STYLE = "body { background-color: lightyellow; font-family: Arial, sans-serif; }\nh1 { color: navy; }\ntable, th, td { border: 1px solid gray; }\n";
const GROUPES = ["h1_1", "h2_1", "h2_2", "h2_3", "h3_1", "h3_2", "h4_1", "h4_2"];
// écrire dans l'éditeur d'une partie (l'onglet du fichier d'abord)
async function ecrire(page, partie, fichier, code) {
  await page.click(`#partie-${partie} .ed-ong[data-f="${fichier}"]`);
  await page.fill(`#partie-${partie} .ed-ta`, code);
}
const verdicts = (page, gid) => page.locator(`#${gid} .grp-l .sol input`).evaluateAll((l) => l.map((i) => i.value));
// l'aperçu, lu depuis la page (l'iframe n'exécute aucun script)
const apercu = (page, partie, js) => page.evaluate(([p, f]) => new Function("d", f)(document.querySelector(`#partie-${p} .ed-if`).contentDocument), [partie, js]);

test("exercice 1.2 : l'éditeur, l'aperçu en direct, les liens, la feuille de style, 20/20", async () => {
  const { context, page, errors } = await open(SITE);
  assert.match(await text(page, "#home .home-head"), /Exercice 1\.2[\s\S]*Niveau 1[\s\S]*Mon premier site/);
  assert.match(await text(page, "#home .home-facts"), /4 parties[\s\S]*8 questions[\s\S]*3 documents[\s\S]*23 critères/);
  await page.click("[data-mode=training]");
  assert.match(await text(page, ".cartouche"), /8 questions, 23 critères vérifiés, réparties en 4 parties/);
  assert.equal(await page.locator("#parts .ed").count(), 4);
  // rien n'est écrit : les critères restent vides, la validation est refusée
  assert.deepEqual(await verdicts(page, "h1_1"), ["", "", ""]);
  await page.click("#h1_1 .btn-fast");
  assert.match(await text(page, "#h1_1 .q-msg"), /Complète au moins une case/);
  // une erreur : le titre de l'onglet n'est pas « Mon réseau »
  await ecrire(page, 1, "index.html", INDEX.replace("<title>Mon réseau</title>", "<title>Accueil</title>"));
  assert.deepEqual(await verdicts(page, "h1_1"), ["oui", "non", "oui"]);
  assert.equal(await page.locator("#partie-2 .ed-ta").inputValue(), INDEX.replace("<title>Mon réseau</title>", "<title>Accueil</title>"),
    "les éditeurs des parties partagent les fichiers");
  await page.click("#h1_1 .btn-fast");
  assert.match(await text(page, "#h1_1 .q-status"), /2 cases justes sur 3/);
  assert.match(await text(page, "#h1_1 .grp-sol"), /Mon réseau/);
  // l'aperçu : la page, l'image fournie ; la feuille de style est encore vide
  await page.waitForTimeout(500);
  assert.equal(await apercu(page, 1, "return d.querySelector('h1').textContent"), "Le réseau de la maison");
  assert.ok(await apercu(page, 1, "return d.querySelector('img').src.startsWith('data:image/png')"));
  // un lien vers une page encore vide, puis le retour
  await page.evaluate(() => document.querySelector("#partie-1 .ed-if").contentDocument.querySelector("a").click());
  await page.waitForTimeout(400);
  assert.equal(await text(page, "#partie-1 .ed-url"), "mon-site/materiel.html");
  await page.click("#partie-1 .ed-retour");
  assert.equal(await text(page, "#partie-1 .ed-url"), "mon-site/index.html");
  // la page du matériel, la feuille de style
  await ecrire(page, 3, "materiel.html", MATERIEL);
  assert.deepEqual(await verdicts(page, "h3_1"), ["oui", "oui", "oui", "oui", "oui"]);
  await ecrire(page, 4, "style.css", STYLE.replace("color: navy", "color: bleu"));
  assert.deepEqual(await verdicts(page, "h4_2"), ["oui", "oui", "non", "oui"], "une couleur mal écrite est ignorée");
  await ecrire(page, 4, "style.css", STYLE);
  assert.deepEqual(await verdicts(page, "h4_2"), ["oui", "oui", "oui", "oui"]);
  await page.waitForTimeout(500);
  assert.equal(await apercu(page, 4, "return getComputedStyle(d.querySelector('h1')).color"), "rgb(0, 0, 128)", "style.css appliqué");
  for (const g of GROUPES.slice(1)) await page.click(`#${g} .btn-fast`);
  for (const g of GROUPES.slice(1)) assert.match(await text(page, `#${g} .q-status`), /(\d+) cases? justes? sur \1/, g);
  // partie 1 : 2/3 → 13,33 (8 min) ; parties 2 à 4 : 20 → (8 × 13,33 + 40 × 20) / 48 = 18,9
  assert.equal((await text(page, "#recap .final-note")).trim(), "18,9/20");
  // un critère validé est figé, même si le code change ensuite
  await ecrire(page, 1, "index.html", "<p>effacé</p>");
  assert.deepEqual(await verdicts(page, "h1_1"), ["oui", "non", "oui"]);
  assert.deepEqual(errors, []);
  await context.close();
});

test("exercice 1.2 : erreur 404, réinitialisation, clavier, archive .zip, impression, téléphone", async () => {
  const { context, page, errors } = await open(SITE, { acceptDownloads: true });
  await page.click("[data-mode=training]");
  await ecrire(page, 1, "index.html", INDEX.replace('href="materiel.html"', 'href="materiels.html"'));
  assert.deepEqual(await verdicts(page, "h3_2"), ["non", ""]);
  await page.waitForTimeout(500);
  await page.evaluate(() => document.querySelector("#partie-1 .ed-if").contentDocument.querySelector("a").click());
  await page.waitForTimeout(400);
  assert.match(await text(page, "#partie-1 .ed-etat"), /erreur 404/);
  assert.match(await apercu(page, 1, "return d.body.textContent"), /Erreur 404[\s\S]*materiels\.html/);
  // clavier : Tab insère deux espaces, Entrée garde le retrait
  await page.click("#partie-4 .ed-ta");
  await page.keyboard.press("Control+End");
  await page.keyboard.type("h1 {");
  await page.keyboard.press("Enter");
  await page.keyboard.press("Tab");
  await page.keyboard.type("color: navy;");
  await page.keyboard.press("Enter");
  await page.keyboard.type("}");
  assert.match(await page.locator("#partie-4 .ed-ta").inputValue(), /h1 \{\n  color: navy;\n  \}$/);
  assert.equal(await verdicts(page, "h4_2").then((v) => v[2]), "oui");
  assert.match(await page.locator("#partie-4 .ed-hl").innerHTML(), /<span class="hl-prop">color<\/span>/, "coloration du code");
  // réinitialiser un fichier
  await page.click("#partie-4 .ed-reinit");
  assert.match(await page.locator("#partie-4 .ed-ta").inputValue(), /^\/\* La feuille de style/);
  assert.deepEqual(await verdicts(page, "h4_2"), ["", "", "", ""]);
  // télécharger le site
  await ecrire(page, 3, "materiel.html", MATERIEL);
  const [dl] = await Promise.all([page.waitForEvent("download"), page.click("#partie-3 .ed-zip")]);
  assert.equal(dl.suggestedFilename(), "mon-site.zip");
  const zip = path.join(fs.mkdtempSync(path.join(os.tmpdir(), "site-")), "mon-site.zip");
  await dl.saveAs(zip);
  const octets = fs.readFileSync(zip);
  assert.equal(octets.subarray(0, 4).toString("binary"), "PK\x03\x04");
  for (const f of ["index.html", "materiel.html", "style.css", "reseau.png"]) assert.ok(octets.includes(Buffer.from("mon-site/" + f)), f);
  assert.ok(octets.includes(Buffer.from(MATERIEL)), "fichiers enregistrés tels quels");
  // impression : le code de chaque partie remplace l'éditeur
  await page.evaluate(() => window.dispatchEvent(new Event("beforeprint")));
  await page.emulateMedia({ media: "print" });
  assert.ok(await page.isVisible("#partie-3 .ed-print"));
  assert.match(await text(page, "#partie-3 .ed-print"), /— materiel\.html —[\s\S]*<h1>Le matériel<\/h1>/);
  assert.ok(!(await page.isVisible("#partie-3 .ed-corps")));
  await page.emulateMedia({ media: "screen" });
  await page.setViewportSize({ width: 390, height: 844 });
  assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
  assert.deepEqual(errors, []);
  await context.close();
});

test("exercice 1.2 en examen : le code est vérifié à la remise de la copie", async () => {
  const { context, page, errors } = await open(SITE);
  await page.click("[data-mode=exam]");
  assert.ok(!(await page.isVisible("#h1_1 .btn-fast")));
  await ecrire(page, 1, "index.html", '<!DOCTYPE html>\n<html lang="fr">\n<head><title>Mon réseau</title></head>\n<body><h1>Mon réseau</h1></body>\n</html>\n');
  assert.match(await text(page, "#score-count"), /12 réponse\(s\) renseignée\(s\) sur 23/);
  assert.ok(!(await page.isVisible("#h1_1 .q-expl")));
  await page.click("#exam-submit");
  assert.match(await text(page, "#exam-warn"), /11 réponse\(s\) encore vide\(s\)/);
  await page.click("#exam-submit");
  assert.ok(await page.locator("body.graded").count());
  assert.match(await text(page, "#h1_1 .q-status"), /3 cases justes sur 3/);
  assert.match(await text(page, "#h2_2 .q-status"), /0 case juste sur 3/);
  // partie 1 : 20 (8 min sur 48), le reste 0 → 3,3/20
  assert.equal((await text(page, "#recap .final-note")).trim(), "3,3/20");
  assert.deepEqual(errors, []);
  await context.close();
});
