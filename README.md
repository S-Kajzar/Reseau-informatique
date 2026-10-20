# Réseau informatique : cours et exercices interactifs

Construction reprise du dépôt « Chaîne fonctionnelle » (lui-même repris du dépôt « Résistance des matériaux ») :
une page autonome (un seul fichier HTML, aucune dépendance externe, utilisable hors ligne), publiée par GitHub Pages
depuis `index.html`. Tant qu'une rubrique de l'accueil est vide, une carte « En cours d'édition » l'annonce.

| Adresse | Contenu |
|---|---|
| `index.html` | accueil, en cartes illustrées à mots-clés : **Les cours**, **Les exercices**, **Études de cas** (pastilles Niveau 1 / Niveau 2) |
| `?ex=cours-reseaux` | Cours 1 — Réseaux informatiques (Niveau 1), de la liaison point-à-point au modèle OSI : le cours Word repris section par section, 18 figures redessinées et interactives (duplex, supports, portée, débit, switch et adresses MAC, topologies que l'on coupe, box, routage, dorsales, découpage IP, NAT, sous-réseaux logiques, HTTP, TCP, OSI, encapsulation, parcours des couches), synthèse, deux jeux, quiz |
| `?ex=qcm-reseaux` | QCM 1.1 — Réseaux informatiques (Niveau 1) : 6 parties, 47 questions, 47 min |
| `?ex=site-html` | Exercice 1.2 — Mon premier site (Niveau 1) : deux pages HTML et une feuille de style écrites dans un éditeur intégré, aperçu en direct, 23 critères vérifiés dans le code, 48 min |
| `?ex=adressage-maison` | Exercice 1.3 — Le plan d'adressage de la maison (Niveau 1) : schéma de la box et de ses appareils, net-ID et host-ID, adresses privées et publiques, durées de téléchargement ; 16 questions, 28 cases, 45 min |
| `?ex=requete-http` | Exercice 2.1 — Suivre une requête à travers le réseau (Niveau 2) : couches de chaque appareil, encapsulation, adresses MAC et IP des trames de la maison et du centre de données, traduction d'adresses, trajet animé une fois la copie corrigée ; 13 questions, 30 cases, 45 min |
| `?ex=etude-mediatheque` | Étude 1 — Le réseau d'une médiathèque (Niveau 2) : deux bâtiments, deux réseaux, un routeur qui filtre ; matériels et supports sur le plan, plan d'adressage, choix des switchs, débits, échanges transmis ou bloqués ; 20 questions, 32 cases, 1 h 05 |
| `modele.html` | page modèle, non publiée (`python3 src/generer.py --modele`) : un cours et un exercice qui montrent chaque élément disponible |

Chaque exercice propose le mode entraînement ou le mode examen, avec sa propre note pondérée par la durée de ses parties. Corrections apportées au cours d'origine
et décisions : [`NOTE-DE-LIVRAISON.md`](NOTE-DE-LIVRAISON.md).

## Ajouter un contenu

Un cours ou un exercice vit dans son module (`src/cours_reseaux.py`, `src/qcm_reseaux.py`, `src/site_html.py`,
`src/exo_adressage.py`, `src/exo_requete.py`, `src/etude_mediatheque.py`), qui
reçoit le module `generer` (blocs, correcteurs, éléments des cours) ; il s'inscrit dans la section « CONTENU » de
`src/generer.py`, dans `COURS` ou `EXO_DEFS` (l'ordre est celui des cartes de l'accueil). `src/modele.py` donne un
exemple complet de chaque élément, et `python3 src/generer.py --modele` l'affiche dans `modele.html`.

- **Un cours** : adresse `cours-…`, étiquette « Cours 2 », niveau, titre, 3 à 5 mots-clés, image de carte, fonction
  `render` qui renvoie son HTML. Éléments prêts : `course_head`, `course_fiche` (objectifs, prérequis), `course_nav`,
  `course_section`, `cartes_html` (cartes à retourner), `jeu_html` (jeu de classement), `quiz_section` (quiz noté),
  `course_foot`. Un cours qui a son propre script le donne dans `js` et nomme sa fonction d'initialisation dans `init`
  (elle appelle `initCours(home)`), son style dans `css`.
- **Un exercice** : adresse, préfixe d'une lettre, « Exercice 1.3 » (le premier chiffre donne le niveau), parties,
  documents, consignes, image, mots-clés, image de carte ; au besoin `js` et `css` (script et style propres à
  l'exercice) et `unite` (nom des points). Blocs d'une partie :
  - `Q` : question à une case, saisie au clavier ;
  - `GRP` : question à plusieurs cases validées ensemble, saisies au clavier ou remplies avec des **étiquettes** à
    glisser (`etiquettes=…`) ; avec `reperes=…`, les cases sont posées sur le **schéma** de la partie
    (`"plan"` : dessin SVG et rectangles des cases), avec un bandeau d'étiquettes collé sous la figure ; avec
    `auto=True`, les cases sont des **critères** que le script de l'exercice remplit (« oui », « non ») ;
  - `qcm.QCM` : question à propositions, réponse unique ou multiple, image (`img`) ou figure HTML (`fig`) ; un
    exercice entièrement en QCM porte `"qcm": True` et les consignes `qcm.CONSIGNES` ;
  - `QBAR` (documents à consulter), `HTML` (texte, figure, éditeur) ; documents du sujet : `DOC("DP1", …)`,
    `DOC("DT1", …)`.
- **Les correcteurs** : `KW(P(…))` mots-clés (petite faute tolérée, mots interdits `forbid=`), `NUM` valeur numérique
  (tolérance, unité), `IP` adresse écrite seule, en notation pointée ou CIDR (seule l'écriture exacte est juste).
- **Une étude de cas** : un exercice avec `"etude": True`.

La carte apparaît d'elle-même sur l'accueil, à la place de l'annonce « En cours d'édition » de sa rubrique. Les images
des cartes (`src/images/carte-*`, 480 × 270) sont préparées par `outils/preparer-images.sh`.

## Régénérer les pages

Les pages sont produites par un script, à partir du gabarit (`src/gabarit-exercice-interactif.html`, copie conforme de
celui des dépôts RDM et Chaîne fonctionnelle, recopié sans modification de son style ni de ses moteurs) et du contenu
décrit dans `src/`.

```sh
python3 src/generer.py                            # écrit index.html
NODE_PATH=$(npm root -g) node outils/captures.js  # seulement si un dessin SVG ou une figure photographiée pour une carte change
bash outils/preparer-images.sh                    # seulement si les images de src/images/originaux changent (ImageMagick 6)
python3 src/generer.py --modele                   # écrit modele.html (page modèle, non suivie par git)
```

Après `captures.js` et `preparer-images.sh`, relancer `python3 src/generer.py` pour intégrer les nouvelles images.

## Tester

```sh
node --test tests/correction.test.js                          # gabarit, configuration, correcteurs, étiquettes
node --test tests/qcm.test.js                                 # QCM 1.1 : bonnes réponses acceptées, toutes les autres refusées
NODE_PATH=$(npm root -g) node --test tests/navigateur.test.js # accueil, page modèle : cours, entraînement, examen, étiquettes, schéma, QCM, documents
NODE_PATH=$(npm root -g) node --test tests/reseaux.test.js    # cours 1 (chaque figure), QCM 1.1, exercice 1.2 (éditeur, aperçu, critères, .zip)
NODE_PATH=$(npm root -g) node --test tests/exercices.test.js  # exercices 1.3 et 2.1, étude 1 : correcteurs, copies justes, animation, examen
```

`correction.test.js` et `navigateur.test.js` régénèrent `modele.html`. Les tests vérifient l'accueil publié tel qu'il
est (et chaque cours ou exercice qu'il propose), chaque mécanisme sur la page modèle, puis le cours 1, le QCM 1.1,
les exercices 1.2, 1.3 et 2.1 et l'étude 1 : un sujet entièrement juste donne 20/20, sans erreur JavaScript.

## Organisation

| Chemin | Rôle |
|---|---|
| `src/gabarit-exercice-interactif.html` | gabarit de référence (charte, moteurs de correction et d'application), repris du dépôt Chaîne fonctionnelle |
| `src/generer.py` | blocs, correcteurs, rendu, accueil, aiguillage et assemblage ; section « CONTENU » : les cours et exercices publiés |
| `src/cours_reseaux.py` | cours 1 : texte, figures SVG, comportement et style |
| `src/qcm_reseaux.py` | QCM 1.1 : les 47 questions et leurs explications |
| `src/site_html.py` | exercice 1.2 : l'éditeur du site (coloration, aperçu, liens, archive .zip), les critères vérifiés, les documents |
| `src/exo_adressage.py` | exercice 1.3 : le schéma de la maison, les questions, les documents |
| `src/exo_requete.py` | exercice 2.1 : le chemin et les trames à compléter, le trajet animé, les documents |
| `src/etude_mediatheque.py` | étude 1 : le plan de la médiathèque, les questions, les documents (besoins, matériels, supports) |
| `src/qcm.py` | questions à propositions : rendu, correction par le gabarit, images partagées |
| `src/modele.py` | cours et exercice modèles (page `modele.html`) : un exemple de chaque élément |
| `src/images/originaux/` | dessin de l'accueil (`accueil.svg`, un réseau local) et son rendu ; figures photographiées pour les cartes |
| `src/images/` | images intégrées en data URI : illustration de l'accueil (aussi l'image `reseau.png` du site de l'exercice 1.2), images des cartes |
| `outils/captures.js` | rendu des dessins SVG, figures photographiées dans la page (Playwright) |
| `outils/preparer-images.sh` | quantification, illustration de l'accueil, images des cartes |
| `tests/` | tests Node et Playwright |
| `.github/workflows/static.yml` | publication GitHub Pages (déclenchée sur la branche `main`) |
