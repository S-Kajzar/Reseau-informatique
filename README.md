# Réseau informatique : cours et exercices interactifs

Construction reprise du dépôt « Chaîne fonctionnelle » (lui-même repris du dépôt « Résistance des matériaux ») :
une page autonome (un seul fichier HTML, aucune dépendance externe, utilisable hors ligne), publiée par GitHub Pages
depuis `index.html`. Le dépôt est prêt à recevoir les cours et les exercices : tant qu'une rubrique est vide, une carte
« En cours d'édition » l'annonce.

| Adresse | Contenu |
|---|---|
| `index.html` | accueil, en cartes illustrées à mots-clés : **Les cours**, **Les exercices**, **Études de cas** (pastilles Niveau 1 / Niveau 2) ; pour l'instant, une carte « En cours d'édition » par rubrique |
| `?ex=cours-…` | un cours (à venir) |
| `?ex=…` | un exercice ou une étude de cas (à venir), en mode entraînement ou en mode examen |
| `modele.html` | page modèle, non publiée (`python3 src/generer.py --modele`) : un cours et un exercice qui montrent chaque élément disponible |

Chaque exercice propose le mode entraînement ou le mode examen, avec sa propre note pondérée par la durée de ses
parties. Décisions de construction : [`NOTE-DE-LIVRAISON.md`](NOTE-DE-LIVRAISON.md).

## Ajouter un contenu

Tout se décrit dans `src/generer.py` ; `src/modele.py` donne un exemple complet de chaque élément (on y recopie un
bloc, en retirant le préfixe `g.`), et `python3 src/generer.py --modele` l'affiche dans `modele.html`.

- **Un cours** : une entrée de `COURS` (adresse `cours-…`, étiquette « Cours 1 », niveau, titre, 3 à 5 mots-clés,
  image de carte, fonction `render` qui renvoie son HTML). Éléments prêts : `course_head`, `course_fiche` (objectifs,
  prérequis), `course_nav`, `course_section`, `cartes_html` (cartes à retourner), `jeu_html` (jeu de classement),
  `quiz_section` (quiz noté), `course_foot`. Un cours qui a son propre script le donne dans `js` et nomme sa fonction
  d'initialisation dans `init` (elle appelle `initCours(home)`), son style dans `css`.
- **Un exercice** : une entrée de `EXO_DEFS` (adresse, préfixe d'une lettre, « Exercice 1.1 » : le premier chiffre donne
  le niveau, parties, documents, consignes, image, mots-clés, image de carte). Blocs d'une partie :
  - `Q` : question à une case, saisie au clavier ;
  - `GRP` : question à plusieurs cases validées ensemble, saisies au clavier ou remplies avec des **étiquettes** à
    glisser (`etiquettes=…`) ; avec `reperes=…`, les cases sont posées sur le **schéma** de la partie
    (`"plan"` : dessin SVG et rectangles des cases), avec un bandeau d'étiquettes collé sous la figure ;
  - `qcm.QCM` : question à propositions, réponse unique ou multiple (un exercice entièrement en QCM porte
    `"qcm": True` et les consignes `qcm.CONSIGNES`) ;
  - `QBAR` (documents à consulter), `HTML` (texte, figure) ; documents du sujet : `DOC("DP1", …)`, `DOC("DT1", …)`.
- **Les correcteurs** : `KW(P(…))` mots-clés (petite faute tolérée, mots interdits `forbid=`), `NUM` valeur numérique
  (tolérance, unité), `IP` adresse écrite seule, en notation pointée ou CIDR (seule l'écriture exacte est juste).
- **Une étude de cas** : un exercice avec `"etude": True`.

La carte apparaît d'elle-même sur l'accueil, à la place de l'annonce « En cours d'édition » de sa rubrique. Les images
des cartes (`src/images/carte-*`, 480 × 270) sont préparées par `outils/preparer-images.sh`.

## Régénérer les pages

Les pages sont produites par un script, à partir du gabarit (`src/gabarit-exercice-interactif.html`, copie conforme de
celui des dépôts RDM et Chaîne fonctionnelle, recopié sans modification de son style ni de ses moteurs) et du contenu
décrit dans `src/generer.py`.

```sh
NODE_PATH=$(npm root -g) node outils/captures.js  # seulement si un dessin SVG de src/images/originaux change
bash outils/preparer-images.sh   # seulement si les images de src/images/originaux changent (ImageMagick 6)
python3 src/generer.py           # écrit index.html
python3 src/generer.py --modele  # écrit modele.html (page modèle, non suivie par git)
```

## Tester

```sh
node --test tests/correction.test.js                          # gabarit, configuration, correcteurs, étiquettes
NODE_PATH=$(npm root -g) node --test tests/navigateur.test.js # accueil, cours, entraînement, examen, étiquettes, schéma, QCM, documents
```

Les deux fichiers régénèrent `modele.html`. Ils vérifient l'accueil publié tel qu'il est (et chaque cours ou exercice
qu'il propose, au fur et à mesure qu'ils arrivent), puis chaque mécanisme sur la page modèle : un sujet entièrement
juste donne 20/20, sans erreur JavaScript.

## Organisation

| Chemin | Rôle |
|---|---|
| `src/gabarit-exercice-interactif.html` | gabarit de référence (charte, moteurs de correction et d'application), repris du dépôt Chaîne fonctionnelle |
| `src/generer.py` | contenu (cours, exercices, études), accueil, aiguillage et assemblage |
| `src/qcm.py` | questions à propositions : rendu, correction par le gabarit, images partagées |
| `src/modele.py` | cours et exercice modèles (page `modele.html`) : un exemple de chaque élément |
| `src/images/originaux/` | dessins du site (`accueil.svg`, un réseau local) et leurs rendus ; figures d'origine des contenus à venir |
| `src/images/` | images intégrées en data URI : illustration de l'accueil, images des cartes |
| `outils/captures.js` | rendu des dessins SVG en PNG (Playwright) |
| `outils/preparer-images.sh` | quantification, illustration de l'accueil, images des cartes |
| `tests/` | tests Node et Playwright |
| `.github/workflows/static.yml` | publication GitHub Pages (déclenchée sur la branche `main`) |
