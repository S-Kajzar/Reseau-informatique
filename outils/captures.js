// Images rendues ou photographiées (Playwright + Chromium), pour l'accueil :
//   - src/images/originaux/accueil.png : rendu du dessin accueil.svg (un réseau local), en double définition ;
//   - src/images/originaux/carte-*.png : figures photographiées dans la page générée (python3 src/generer.py
//     d'abord) — le parcours d'un message à travers les couches (cours 1), le maillage de routeurs (QCM 1.1),
//     l'éditeur du site avec un exemple de code (exercice 1.2).
//   outils/preparer-images.sh en tire l'illustration de l'accueil et les images des cartes.
//   python3 src/generer.py && NODE_PATH=$(npm root -g) node outils/captures.js && bash outils/preparer-images.sh && python3 src/generer.py
const path = require("node:path");
const { chromium } = require("playwright");
const EXEMPLE = `<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="utf-8">
    <title>Mon réseau</title>
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
    <h1>Le réseau de la maison</h1>
    <p>La <strong>box</strong> relie les appareils à Internet.</p>
    <h2>Les équipements</h2>
    <ul>
      <li>La box</li>
      <li>L'ordinateur</li>
      <li>Le téléphone</li>
    </ul>
  </body>
</html>
`;
(async () => {
  const racine = path.join(__dirname, "..");
  const ORIG = path.join(racine, "src/images/originaux");
  const PAGE = "file://" + path.join(racine, "index.html");
  const FIGE = "*{animation:none!important;transition:none!important}";
  const DESSINS = [["accueil", 1120, 620]];
  const b = await chromium.launch();
  for (const [nom, w, h] of DESSINS) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
    await p.goto("file://" + path.join(ORIG, nom + ".svg"));
    await p.screenshot({ path: path.join(ORIG, nom + ".png") });
    await p.close();
  }
  const p = await b.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 2 });
  await p.goto(PAGE + "?ex=cours-reseaux");
  await p.click("#cr-par-go");
  await p.waitForFunction(() => /Message reçu/.test(document.querySelector("#cr-par-t").textContent), null, { timeout: 30000 });
  await p.addStyleTag({ content: FIGE });
  await p.locator("#cr-par-svg").screenshot({ path: path.join(ORIG, "carte-cours-1.png") });
  await p.locator("#cr-rt-svg").screenshot({ path: path.join(ORIG, "carte-qcm.png") });
  await p.goto(PAGE + "?ex=site-html");
  await p.click("[data-mode=training]");
  await p.fill("#partie-1 .ed-ta", EXEMPLE);
  await p.fill("#partie-4 .ed-ta", "body { background-color: lightyellow; font-family: Arial, sans-serif; }\nh1 { color: navy; }\n");
  await p.waitForTimeout(800);
  await p.addStyleTag({ content: FIGE + " .ed-etat{display:none}" });
  await p.locator("#partie-1 .ed-corps").screenshot({ path: path.join(ORIG, "carte-site.png") });
  await b.close();
})();
