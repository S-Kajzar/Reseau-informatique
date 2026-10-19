# Note de livraison — Réseau informatique : cours et exercices interactifs

## Construction reprise du dépôt Chaîne fonctionnelle

**Source** : le dépôt « Chaîne fonctionnelle » (construction : générateur, gabarit, accueil en cartes, pastilles,
moteurs des étiquettes, des schémas à compléter et des QCM, éléments des cours, outils d'images, tests, publication).
Il a été consulté sans être modifié.

**Gabarit** : copié tel quel dans `src/gabarit-exercice-interactif.html` (fichier identique à celui des dépôts RDM et
Chaîne fonctionnelle, vérifié octet par octet ; `tests/correction.test.js` en contrôle l'empreinte SHA-256).

**Repris sans changement** : le moteur applicatif et ses remplacements vérifiés (`CONSEIL_MIN` lue dans
`window.__CONSEIL_MIN__`, `DECOR` et `DR_NAMES` vides, texte de la fenêtre « Imprimer les DR », libellé « Réponses
validées »), le correctif d'impression des tracés, l'aiguillage `?ex=…`, l'accueil et ses cartes de même taille, les
modes entraînement et examen, les étiquettes à glisser (toucher puis toucher, glisser-déposer, clavier, échange), les
schémas à compléter et leur bandeau collant, les QCM, les éléments des cours (sections, sommaire, cartes à retourner,
jeux de classement, quiz noté, impression), la publication GitHub Pages (`.github/workflows/static.yml`, identique).

**Non repris** : tout le contenu propre à la chaîne fonctionnelle (cours 1 à 3, exercice 1.1, QCM 2.1, formulaire de
la chaîne de puissance, portail animé, figures du RAV4, schémas de l'exercice 1.1, images). La rubrique « Le
formulaire » de l'accueil n'est pas reprise ; elle se rétablirait sur le même modèle si un formulaire venait.

## Ce qui change pour accueillir les contenus à venir

- **Accueil** : trois rubriques, **Les cours**, **Les exercices** et **Études de cas** ; chacune, tant qu'elle est vide,
  affiche une carte « En cours d'édition » (image grisée, mots-clés), remplacée d'elle-même par les cartes des
  contenus décrits dans `COURS` et `EXO_DEFS`. Les numéros suivent la logique RDM : le premier chiffre d'un exercice
  donne son niveau (1.1, puis 1.2… et 2.1… au niveau 2).
- **Blocs généralisés** : dans le dépôt source, les étiquettes, les schémas et les documents étaient rattachés à
  l'exercice 1.1 (listes `EX1_ETIQUETTES`, `EX1_PLANS`, documents communs `DOCS`). Ici, une question `GRP` reçoit
  directement ses étiquettes (`etiquettes=`, `liste=`) et ses repères sur le schéma (`reperes=`), une partie son
  schéma (`"plan"`), un exercice ses propres documents (`DOC`). Une question `GRP` sans étiquettes se remplit au
  clavier (nouveau : cases saisies). Une question à une case se décrit avec `Q`.
- **QCM** : `src/qcm.py` garde le rendu, la correction et les images partagées du QCM 2.1, sans la lecture de sa page
  source ; une question se décrit avec `qcm.QCM(énoncé, propositions, repères justes, explication)`. Des QCM peuvent
  se mêler aux autres questions d'un exercice (paragraphe de consignes `qcm.C_QCM`).
- **Correcteurs ajoutés** : `NUM` (valeur numérique, tolérance, unité) et `IP` (adresse en notation pointée ou CIDR).
  Le moteur du gabarit compare les réponses « code » sans leur ponctuation : 192.168.1.12 et 192.168.11.2 s'y
  écriraient tous deux 192168112. `IP` refuse donc d'abord toute écriture autre que l'adresse attendue (motif
  `rejectRaw`), sans modifier le moteur ; les tests le vérifient.
- **Cours** : une fonction d'initialisation commune, `initCours` (cartes, jeux, quiz, bouton « Imprimer le cours »),
  s'applique à tout cours qui n'en déclare pas d'autre. `course_fiche` (objectifs et prérequis), `cartes_html` et
  `course_foot` reprennent ce que les cours du dépôt source écrivaient chacun pour soi ; les couleurs des cartes
  deviennent `bleu`, `orange` et `vert` (elles désignaient la chaîne d'information et la chaîne d'énergie).
- **Consignes** : `consignes(…)` assemble les paragraphes utiles à un exercice (`C_SAISIE`, `C_GROUPE`,
  `C_ETIQUETTES`, `C_SCHEMA`, `C_DOCUMENTS`), entre les modes et le barème.
- **Contrôles à la génération** : adresses et préfixes uniques, adresse d'un cours en `cours-…`, repères des cases
  présents sur le schéma de la partie, documents des barres de documents présents dans l'exercice.

## Page modèle (`modele.html`, non publiée)

`python3 src/generer.py --modele` écrit `modele.html` à partir de `src/modele.py` : un cours et un exercice sur le
réseau local, qui servent de référence pour écrire les contenus et de banc d'essai aux tests. Le fichier n'est pas
suivi par git (`.gitignore`), donc pas publié.
- **Cours modèle** « Les matériels du réseau local » : en-tête, objectifs et prérequis, sommaire, quatre cartes à
  retourner (commutateur, routeur, point d'accès, serveur), un élément interactif propre au cours (une adresse IPv4
  écrite en binaire, octet par octet), un jeu « Commutateur ou routeur ? », un quiz de trois questions.
- **Exercice modèle** « Le réseau de la salle » (3 parties, 8 questions, 13 cases, 25 min) : documents DP1 (tableau
  d'adressage) et DT1 (adresse, masque, adresse de diffusion) ; questions à une case (mots-clés, adresse, nombre
  d'hôtes), deux cases saisies ensemble (adresse du réseau et de diffusion), un schéma à compléter (routeur,
  commutateur, serveur), des étiquettes sous l'énoncé, un QCM à réponse unique (DHCP) et un à réponses multiples
  (adresses privées).

## Images

L'illustration de l'accueil est dessinée pour le site, sans image extérieure ni question de droits
(`src/images/originaux/accueil.svg` : postes clients, serveur, imprimante, point d'accès sans fil, commutateur,
routeur, Internet) ; elle est rendue en PNG par `outils/captures.js`. `outils/preparer-images.sh` en tire
l'illustration de l'accueil (1120 × 620) et, par recadrage, les images des trois cartes « En cours d'édition »
(480 × 270), grisées par la page. Poids : `index.html` 312 Kio (186 Kio d'images).

## Vérifications effectuées

- `node --test tests/correction.test.js` : 9 tests — gabarit identique (empreinte) ; pour `index.html` et
  `modele.html`, configuration de chaque exercice (durées, points, correcteurs connus, cases présentes dans la page),
  étiquettes (chaque case en accepte au moins une, l'étiquette montrée sur un schéma corrigé est juste) ; correcteurs
  du modèle : mots-clés, faute de frappe, mot interdit, nombre, adresses (192.168.11.2 refusée pour 192.168.1.12),
  étiquettes (la bonne est la seule acceptée de sa liste, ordre alphabétique), QCM à réponse unique et multiple.
- `tests/navigateur.test.js` (Playwright, Chromium) : 9 parcours, tous réussis — accueil publié (trois rubriques,
  une carte « En cours d'édition » par rubrique vide, cartes illustrées de même taille, téléphone, aucune mention de
  diplôme ou d'épreuve) ; adresse inconnue ; chaque cours et chaque exercice proposés par l'accueil publié et par la
  page modèle s'ouvrent, en entraînement et en examen ; accueil du modèle ; cours modèle (cartes, binaire, jeu, quiz
  ★★★, impression, lien vers l'exercice) ; exercice modèle en entraînement (réponse vide refusée, réponse fausse,
  confirmation des cases vides, schéma et bandeau, liste qui refuse une case d'une autre liste, glisser-déposer,
  échange, QCM, 12,0/20 puis 20,0/20) ; en examen (rien ne filtre avant la remise, y compris à l'impression ;
  remise en deux temps ; chronomètre arrêté ; 16,1/20) ; documents et téléphone.
- Aucune erreur JavaScript dans aucun parcours.

## À faire

- La publication GitHub Pages se déclenche sur la branche `main` : le dépôt ne l'avait pas encore à la livraison.
- Ajouter les cours et les exercices à mesure qu'ils arrivent, avec l'image de leur carte.
