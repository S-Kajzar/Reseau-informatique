// Dessins du site rendus en PNG (Playwright + Chromium), pour l'accueil :
//   - src/images/originaux/accueil.png : rendu du dessin accueil.svg (un réseau local), en double définition ;
//     outils/preparer-images.sh en tire l'illustration de l'accueil et les images des cartes.
//   NODE_PATH=$(npm root -g) node outils/captures.js && bash outils/preparer-images.sh && python3 src/generer.py
const path = require("node:path");
const { chromium } = require("playwright");
(async () => {
  const ORIG = path.join(__dirname, "..", "src/images/originaux");
  const DESSINS = [["accueil", 1120, 620]];
  const b = await chromium.launch();
  for (const [nom, w, h] of DESSINS) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
    await p.goto("file://" + path.join(ORIG, nom + ".svg"));
    await p.screenshot({ path: path.join(ORIG, nom + ".png") });
    await p.close();
  }
  await b.close();
})();
