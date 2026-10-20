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

## Cours 1 — Réseaux informatiques (Niveau 1, `?ex=cours-reseaux`)

**Source** : le cours Word « Séquence 5 — Réseaux informatiques : de la liaison point-à-point au modèle OSI »
(environ 2 h). Son texte est repris section par section (liaison point-à-point, mise en réseau, WAN et Internet,
adressage IP et LAN, communication entre logiciels, modèle OSI), avec la problématique, les objectifs et les
prérequis ; viennent s'y ajouter une synthèse en six cartes à retourner, deux jeux (« Adresse MAC ou adresse IP ? »,
8 lignes ; « À quelle couche du modèle OSI ? », 8 lignes) et un quiz de 10 questions. Liens en pied de page vers le
QCM 1.1, les exercices 1.2, 1.3 et 2.1 et l'étude 1.

Les 18 figures du Word sont des captures de manuel : aucune n'est reprise, toutes sont **redessinées en SVG** et
rendues interactives (`src/cours_reseaux.py`), numérotées de 1 à 18 :
- **liaison point-à-point** : full-duplex ou half-duplex (les données circulent dans les deux sens, ou à tour de
  rôle) ; câble à paires torsadées et fibre optique, parties montrées depuis la légende, signal électrique et lumière
  qui se réfléchit dans le cœur ; portée du Bluetooth et du Wi-Fi (on déplace l'ordinateur) ; simulateur de débit
  (fichier, liaison, quantité en Mbit, durée, calcul détaillé, transfert animé) ;
- **mise en réseau** : quatre machines reliées à un switch — on choisit l'émetteur et le destinataire, la trame porte
  l'adresse MAC du destinataire, le switch lit sa table et ne l'envoie que vers le bon port ; les quatre topologies
  (étoile, anneau, bus, maillé), dont on coupe les liaisons ou le nœud central : le texte dit quelles machines
  communiquent encore, les groupes isolés prennent une couleur ; carte-réseau et adresse MAC, octet par octet en
  binaire (48 bits, trois octets du fabricant) ;
- **WAN et Internet** : un message de A1 à B3, trame dans les LAN, paquet sur le WAN ; une box qu'on ouvre (modem,
  routeur, switch, hotspot) ; un maillage de 17 routeurs (passerelles et « ronds-points ») : on choisit deux
  passerelles, la route s'affiche et le paquet la suit, on coupe une liaison et la route change, ou disparaît ; les
  dorsales intercontinentales en schéma ; « est-ce une adresse IP ? » ; découpage net-ID / host-ID par le masque,
  avec les trois exemples du Word et le nombre de machines ;
- **adressage IP et LAN** : traduction d'adresses — l'adresse privée de l'émetteur, inscrite sur le paquet, devient
  l'adresse publique de la box au passage du routeur, et l'inverse au retour ; « adresse privée ou publique ? » ;
  sous-réseaux logiques : les quatre PC du Word, adresses modifiables, couleurs par net-ID, tableau de qui peut
  communiquer avec qui, message envoyé ou refusé ;
- **communication entre logiciels** : un navigateur demande une page à un serveur (requête, recherche sur le disque,
  réponse 200 avec le code HTML, ou 404), les messages HTTP s'affichent ; TCP découpe « Bonjour, comment ça va ? »
  en quatre segments numérotés qui n'arrivent pas dans l'ordre, chacun est acquitté, un segment perdu est renvoyé ;
- **modèle OSI** : les sept couches de l'émetteur et du destinataire alignées sur le tableau (rôle, unité,
  technologies), un message qui descend puis remonte les couches ; l'encapsulation étape par étape, puis la
  désencapsulation, chaque en-tête cliquable ; le parcours PC1 → SW1 → R1 → SW2 → PC2 à travers les couches, d'un
  trait ou appareil par appareil.

Graphismes : textes des schémas sur un halo blanc (lisibles quand un câble les croise) ; animations suspendues si le
système demande de réduire les mouvements ; à l'impression, les contenus des onglets et de la box sont imprimés.

Corrections et décisions :
- **Non repris** : les champs « Nom, Prénom, Groupe », le tableau des compétences (intitulés « à reprendre du
  référentiel », jamais remplis), les documents ressources (pages d'un manuel, site extérieur) et les modalités
  (consignes d'enseignant), comme dans les cours du dépôt Chaîne fonctionnelle ; « le réseau local de votre lycée »
  devient « de votre établissement ».
- **Adresses MAC d'exemple** : celles du Word (29:87:a5:ef:18:5d ; 13-4F-DE-A5-65-89, 53-40-…, F3-40-… sur la figure
  du switch) ont un premier octet impair, qui désigne en réalité une adresse de groupe (multicast) et non une carte.
  Elles deviennent 28:87:a5:ef:18:5d, 10-4F-DE-A5-65-89, 10-4F-DE-D5-44-8B, 50-40-DE-C5-44-8B, F0-40-A7-15-4E-80
  (premier octet multiple de 4 : adresse individuelle, attribuée par le fabricant ; PC1 et PC2 gardent le même
  fabricant).
- **« Elle ne peut pas être changée »** (adresse MAC) devient « elle est gravée sur la carte-réseau par son fabricant »
  : un logiciel peut annoncer une autre adresse, mais celle de la carte ne change pas ; le contraste avec l'adresse IP,
  « adresse logique », est conservé.
- **IPv6** : « en cours de déploiement depuis 1998, elle couvre actuellement 10 % du trafic » devient « normalisée en
  1998, toujours en cours de déploiement, de l'ordre de 40 % du trafic des grands services en ligne » (le chiffre du
  Word était ancien).
- **HTTP** : « le protocole gérant les échanges liés à Internet » devient « qui gère les échanges du Web » (Internet
  porte bien d'autres échanges : courrier, jeux, vidéo…).
- **TCP** : « pour chaque paquet reçu, faire envoyer un accusé de réception » devient « pour chaque segment reçu »
  (l'unité de TCP, définie juste avant).
- **Encapsulation** : la figure du Word nomme la couche 3 « Internet » ; elle reprend le nom du modèle OSI, « Réseau ».
- **Fibre optique** : la légende « âme creuse » de la figure, ambiguë, n'est pas reprise ; la figure redessinée
  nomme la fibre de verre, la gaine intérieure, la décharge de traction (fibres de renfort) et la gaine extérieure.
- **Carte des dorsales** (figure 7 du Word, « source : CC BY-SA 2.0 » sans auteur) : remplacée par un schéma des
  principales dorsales entre les continents, annoncé comme tel.
- **Compléments** : analogies du téléphone et du talkie-walkie (duplex) ; tableau Bluetooth / Wi-Fi et portées en
  ordres de grandeur ; « un octet = 8 bits » sous la formule du débit ; les deux adresses réservées d'un réseau
  (2<sup>8</sup> − 2 = 254) ; la traduction d'adresses (NAT), nommée ; le rôle des quatre appareils de la box ; ce
  que contient chaque en-tête (MAC, IP, numéro de segment, contrôle d'erreur).

## QCM 1.1 — Réseaux informatiques (Niveau 1, `?ex=qcm-reseaux`)

Écrit sur le cours 1 (`src/qcm_reseaux.py`), premier exercice de la rubrique : six parties qui suivent le plan du
cours, pondérées par leur durée (9, 9, 10, 7, 5 et 7 min, soit 47 min), 47 questions d'un point, dont 9 à réponses
multiples (il faut toutes les bonnes, et elles seules). Les exemples sont ceux du cours (débit de 20 Mo en 4 s,
adresses des figures, masques, couches) ; chaque question a son explication. Une figure (la topologie en bus) est
dessinée dans la question. Pas de documents à consulter : le QCM vérifie ce qui a été retenu.

## Exercice 1.2 — Mon premier site (Niveau 1, `?ex=site-html`)

**Objectif** : réaliser un petit site depuis un éditeur intégré à la page (`src/site_html.py`). Le site « Mon
réseau » présente le réseau de la maison : une page d'accueil (`index.html`), une page « Le matériel »
(`materiel.html`, avec le tableau des appareils et de leurs adresses IP) et une feuille de style (`style.css`) ; une
image est fournie (`reseau.png`, l'illustration de l'accueil du site du cours).
- **L'éditeur** : onglets des trois fichiers, coloration du code HTML et CSS, numéros de ligne, Tab pour deux espaces
  (Échap puis Tab pour quitter l'éditeur), retrait conservé à la ligne, « Réinitialiser ce fichier », « Télécharger
  mon site (.zip) » (archive des trois fichiers et de l'image, produite dans la page). Les éditeurs des quatre parties
  partagent les mêmes fichiers.
- **L'aperçu** : il joue le rôle du navigateur, se met à jour pendant la frappe, applique la feuille de style et
  l'image ; ses liens mènent d'une page à l'autre (bouton de retour), une page absente donne une erreur 404 (lien avec
  la partie 5 du cours). L'aperçu est une iframe isolée qui n'exécute aucun script.
- **La notation** : 4 parties (le squelette de l'accueil, son contenu, la seconde page et les liens, la mise en
  forme ; 8, 14, 15 et 11 min), 8 questions, 23 critères d'un point, vérifiés dans le code (une valeur CSS fausse,
  ignorée par le navigateur, ne compte pas). Le script de l'éditeur inscrit son verdict dans la case masquée de chaque
  critère ; le moteur du gabarit corrige ces cases comme les autres : entraînement (un bouton « Faire vérifier mon
  code » par question, définitif), examen (tout est vérifié à la remise), note pondérée, impression (le code de chaque
  partie remplace l'éditeur). Tant que le fichier d'un critère n'a pas été modifié, sa case reste vide : le gabarit
  refuse alors la validation (« Complète au moins une case »).
- **Documents** : DP1, le site à réaliser (plan des pages) ; DT1, les balises HTML (squelette, tableau des balises) ;
  DT2, les règles CSS (syntaxe, propriétés, couleurs).
- Rien n'est enregistré dans le navigateur, comme pour tout le site : les consignes invitent à télécharger le site
  avant de fermer la page.

## Exercice 1.3 — Le plan d'adressage de la maison (Niveau 1, `?ex=adressage-maison`)

L'entraînement direct au cours 1 (`src/exo_adressage.py`) : le réseau d'une maison, une box (modem, routeur, switch,
point d'accès Wi-Fi) et six appareils. 4 parties (10, 12, 12 et 11 min, soit 45 min), 16 questions, 28 cases.
- **Le schéma du réseau** : les appareils de la box et le type de chaque liaison, étiquettes posées sur la figure
  (chaque appareil de la box a son pictogramme : la liaison venant d'Internet arrive au modem) ; la topologie.
- **Le tableau d'adressage** : net-ID et host-ID par le masque, adresse de la box dans le réseau local, adresse
  publique, cinq adresses à classer privées ou publiques (172.40.1.2, hors de la plage 172.16 à 172.31, est publique).
- **Des adresses à choisir** : nombre de machines (254), adresse libre suivante, une tablette réglée à la main dans
  un autre net-ID (elle ne communique plus), sa correction, le masque 255.255.0.0.
- **Le débit de la connexion** : durées de téléchargement d'un jeu de 50 Go par câble (400 s) et en Wi-Fi (1 333 s),
  débit d'une transmission (48 Mbit/s), pourquoi le Wi-Fi est plus lent.
- Documents : DP1, le réseau de la maison (appareils, liaisons, adresses, débits) ; DT1, adresses IP, masques et débit.

## Exercice 2.1 — Suivre une requête à travers le réseau (Niveau 2, `?ex=requete-http`)

L'approfondissement du modèle OSI (`src/exo_requete.py`) : l'ordinateur portable de la maison demande une page à un
serveur web, dans un centre de données, à travers la box, les routeurs d'Internet, le routeur du centre et un switch.
4 parties (9, 11, 12 et 13 min, soit 45 min), 13 questions, 30 cases, trois schémas à compléter.
- **Les appareils et leurs couches** : les couches que met en œuvre chaque appareil du chemin (1 à 7, 1 à 3, 1 et 2),
  posées sur le schéma ; qui lit l'adresse IP, qui lit l'adresse MAC.
- **L'encapsulation de la requête** : l'ordre des éléments de la trame, la couche qui ajoute chacun, le nombre de
  segments TCP de la réponse (6 000 octets en segments de 1 500), ce qui se passe quand un segment se perd.
- **Les adresses dans la maison** et **au centre de données, puis la réponse** : les adresses MAC et IP de la trame
  (étiquettes « adresse (appareil) » posées sur la trame dessinée), de l'ordinateur à la box, puis du routeur du
  centre au serveur ; ce qui a changé entre les deux (adresse IP source traduite par la box, en-tête Ethernet refait
  sur chaque réseau) ; les adresses de la réponse.
- **Le trajet animé** : une figure rejoue le trajet de la requête et de la réponse, étape par étape, avec les
  adresses inscrites sur le message. Elle montre les réponses : son bouton reste verrouillé tant que les questions
  des parties 3 et 4 ne sont pas corrigées (ou la copie d'examen remise).
- Ce que l'exercice ajoute au cours (DT1) : l'adresse MAC identifie les machines d'un même LAN, donc l'en-tête
  Ethernet est refait sur chaque réseau traversé, alors que les adresses IP restent celles des extrémités, sauf à la
  box. Les adresses MAC d'exemple ont un premier octet multiple de 4 (adresses individuelles) ; celles des serveurs
  et routeurs d'Internet sont prises dans les plages réservées à la documentation (203.0.113.0/24).
- Documents : DP1, la requête à suivre (adresses de chaque appareil) ; DT1, couches, adresses et encapsulation.

## Étude 1 — Le réseau d'une médiathèque (Niveau 2, `?ex=etude-mediatheque`)

La première étude de cas (`src/etude_mediatheque.py`) : la médiathèque rénove son réseau. Un bâtiment principal
(espace multimédia de 10 postes, accueil et Wi-Fi des visiteurs, local technique où arrive la fibre de l'opérateur)
et une annexe, à 160 m, où travaille le personnel (6 postes, serveur de fichiers, imprimante). Deux réseaux séparés
par un même routeur, qui bloque les messages du réseau public vers celui du personnel. 4 parties (15, 15, 20 et
15 min, soit 1 h 05), 20 questions, 32 cases.
- **L'architecture du réseau** : sur le plan des deux bâtiments, le matériel du local technique (un routeur : il relie
  des réseaux différents, le modem ne le fait pas), de l'espace multimédia et de l'accueil, le support de la liaison
  de 160 m (fibre : plus de 100 m de câble Ethernet) et de celle des postes ; la topologie.
- **Le plan d'adressage** : six adresses à écrire d'après les règles du dossier (routeur côté personnel et côté
  public, serveur, imprimante, postes) ; la plage Wi-Fi prévue (100 adresses) ne suffit pas pour 120 visiteurs, il
  faut en choisir une autre dans le réseau public ; ce que peut faire le téléphone d'un visiteur ; pourquoi deux
  réseaux.
- **Le choix des matériels et les débits** : le nombre de ports du switch de l'espace multimédia (12), le moins cher
  des switchs qui convient à chaque bâtiment (l'annexe a besoin d'un port fibre), le débit reçu aux heures
  d'affluence (750 Mbit/s, la fibre suffit), la durée de la sauvegarde nocturne (au débit d'émission, 1 440 s) et
  d'une copie sur le réseau du personnel (16 s).
- **Les échanges à travers le routeur** : pour cinq échanges, transmis, bloqué ou sans passer par le routeur ; ce
  que lit le switch, la couche où décide le routeur, l'adresse avec laquelle un poste est vu sur Internet, ce qui
  change quand une requête traverse le routeur.
- Documents : DP1, la médiathèque et ses besoins (plan d'adressage prévu, abonnement fibre) ; DT1, les matériels et
  les quatre switchs proposés (ports cuivre et fibre, prix) ; DT2, les supports de transmission (débit, longueur).
  L'adresse publique du routeur est prise dans une plage réservée à la documentation (198.51.100.0/24).

## Compléments du générateur

- `GRP(…, auto=True)` : critères vérifiés par le script d'un exercice (cases masquées « oui » / « non »), avec leur
  verdict ☑ / ☒ et, à la correction, un exemple de code juste.
- Un exercice peut apporter son script et son style (`js`, `css`, ajoutés une seule fois à la page) et le nom de ses
  points (`unite` : « critères » plutôt que « cases »).
- `qcm.QCM(…, fig=…)` : une figure HTML (un schéma SVG) sous l'énoncé.
- Les contenus vivent dans leurs modules et s'inscrivent dans la section « CONTENU » de `src/generer.py`.

## Images

L'illustration de l'accueil est dessinée pour le site, sans image extérieure ni question de droits
(`src/images/originaux/accueil.svg` : postes clients, serveur, imprimante, point d'accès sans fil, commutateur,
routeur, Internet) ; elle est rendue en PNG par `outils/captures.js`. `outils/preparer-images.sh` en tire
l'illustration de l'accueil (1120 × 620) et, par recadrage, les images des cartes « En cours d'édition » (480 × 270),
grisées par la page. Les cartes des contenus sont tirées de leurs figures, photographiées dans la page par
`outils/captures.js` : le parcours d'un message à travers les couches (cours 1), le maillage de routeurs (QCM 1.1),
l'éditeur du site avec son aperçu (exercice 1.2), le schéma de la maison et celui de la médiathèque, étiquettes
posées et validées (exercice 1.3, étude 1), le trajet animé de la requête au-dessus de sa trame complétée
(exercice 2.1). Poids : `index.html` 1 066 Kio (421 Kio d'images).

## Vérifications effectuées

- `node --test tests/correction.test.js` : 9 tests — gabarit identique (empreinte) ; pour `index.html` et
  `modele.html`, configuration de chaque exercice (durées, points, correcteurs connus, cases présentes dans la page),
  étiquettes (chaque case en accepte au moins une, l'étiquette montrée sur un schéma corrigé est juste ; chaque
  exercice a son gabarit, où les listes d'un schéma portent des noms communs à tous : une case est rapprochée de la
  liste de son exercice) ; correcteurs
  du modèle : mots-clés, faute de frappe, mot interdit, nombre, adresses (192.168.11.2 refusée pour 192.168.1.12),
  étiquettes (la bonne est la seule acceptée de sa liste, ordre alphabétique), QCM à réponse unique et multiple.
- `node --test tests/qcm.test.js` : 4 tests — QCM 1.1 : 6 parties, 47 questions, 47 min ; pour chaque question à
  réponse unique, la bonne proposition acceptée et toutes les autres refusées ; réponses multiples exigées complètes
  et sans intrus ; réponses vérifiées sur le cours (débit, adresses privées, net-ID, box, couches) ; une explication
  par question.
- `tests/navigateur.test.js` (Playwright, Chromium) : 9 parcours — accueil publié (trois rubriques, cartes illustrées
  de même taille, « En cours d'édition » pour une rubrique vide, téléphone, aucune mention de diplôme ou d'épreuve) ;
  adresse inconnue ; chaque cours et chaque exercice de l'accueil publié et de la page modèle s'ouvrent, en
  entraînement et en examen ; page modèle (cours, exercice en entraînement 12,0/20 puis 20,0/20, en examen 16,1/20,
  documents, téléphone).
- `tests/reseaux.test.js` (Playwright, Chromium) : 12 parcours — cours 1 (sections, figures numérotées de 1 à 18,
  aucune image du Word, corrections, téléphone ; chaque figure manipulée et son résultat vérifié : duplex, supports,
  portée, débit, switch, topologies coupées, adresse MAC, WAN, box, routage et route coupée, dorsales, adresse IP,
  découpage, NAT, adresses privées, sous-réseaux, HTTP 200 et 404, TCP avec segment perdu, OSI, encapsulation,
  parcours ; jeux, quiz ★★★, impression) ; QCM 1.1 (réponse fausse expliquée, 20,0/20, examen sur la première partie
  3,8/20) ; exercice 1.2 (critères vides au départ et validation refusée, un titre faux, éditeurs synchronisés,
  aperçu avec l'image et la feuille de style, liens et retour, couleur CSS mal écrite refusée, 18,9/20, critère validé
  figé ; erreur 404, clavier, coloration, réinitialisation, archive .zip, impression du code, téléphone ; examen
  3,3/20).
- `tests/exercices.test.js` : 11 tests, correcteurs (Node) puis parcours (Playwright) — exercices 1.3 et 2.1, étude 1 :
  parties, durées et cases ; une copie juste dont chaque réponse est acceptée ; pour chaque case à étiquette, la bonne
  est la seule acceptée de sa liste ; formes admises (unités, espaces) et erreurs courantes refusées (adresse voisine,
  mauvais réseau, durée au mauvais débit) ; dans le navigateur, la copie juste vaut 20,0/20 pour chacun ; exercice
  1.3 : mauvaise étiquette corrigée sur le schéma ; exercice 2.1 : animation verrouillée jusqu'à la correction de la
  dernière question de la partie 4, puis trajet complet et adresses de la dernière étape ; en examen, déverrouillée à
  la remise ; étude 1 : carte de la rubrique « Études de cas », documents, examen sur la première partie 4,6/20
  (15 min sur 65).
- Aucune erreur JavaScript dans aucun parcours.

## À faire

- La publication GitHub Pages se déclenche sur la branche `main` : elle aura lieu à la fusion de la demande de fusion
  qui apporte ces contenus.
