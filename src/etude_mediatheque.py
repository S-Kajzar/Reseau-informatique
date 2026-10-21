"""Étude de cas 1 — Le réseau d'une médiathèque (Niveau 2), le cours 1 appliqué à un bâtiment réel.

La médiathèque rénove son réseau : un bâtiment principal (espace multimédia, accueil et son Wi-Fi des visiteurs,
local technique où arrive la fibre de l'opérateur) et une annexe, à 160 m, où travaille le personnel. Deux réseaux
séparés par un même routeur. Quatre parties : l'architecture (matériels et supports posés sur le plan), le plan
d'adressage des deux réseaux, le choix des switchs et les débits, les échanges que le routeur transmet ou bloque.

exercice(g) reçoit le module generer : pas d'import circulaire. Les pictogrammes viennent du cours 1 et de
l'exercice 1.3.
"""
import qcm
import cours_reseaux as cr
import exo_adressage as ad

PUBLIQUE = "198.51.100.25"
PERSO, PUBLIC = "192.168.10", "192.168.20"

E_MAT = ["Routeur", "Switch", "Point d'accès Wi-Fi", "Serveur", "Modem"]
E_SUP = ["Fibre optique", "Câble Ethernet", "Wi-Fi", "Bluetooth"]
E_ROUTEUR = ["Transmise par le routeur", "Bloquée par le routeur", "Sans passer par le routeur"]
SWITCHS = [  # modèle, ports cuivre, ports fibre, prix
    ("A", 8, 0, 45), ("B", 8, 2, 130), ("C", 16, 0, 95), ("D", 24, 4, 280)]


def _pc(x, y):
    """Poste fixe réduit (31 × 28) ; (x, y) : coin haut gauche."""
    return f'<g transform="translate({x} {y}) scale(.55)">{cr.pc(0, 0)}</g>'


def _point_acces(x, y):
    """Point d'accès Wi-Fi ; (x, y) : coin haut gauche du boîtier (64 × 22), ondes au-dessus."""
    return (f'<g transform="translate({x} {y})"><rect width="64" height="22" rx="8" fill="#F4F5F2" stroke="#7D868F" '
            'stroke-width="2"/><circle cx="14" cy="11" r="3" fill="#5BD08A"/><rect x="26" y="9" width="28" height="4" '
            f'rx="2" fill="{cr.ENCRE}"/><g fill="none" stroke="{cr.VERT}" stroke-width="2.5"><path d="M23 -6a13 13 0 0 1 '
            '18 0"/><path d="M17 -13a22 22 0 0 1 30 0"/></g></g>')


def _pile(x, y):
    """Trois postes empilés : un groupe de postes reliés chacun au switch."""
    return "".join(_pc(x + 9 * k, y + 8 * k) for k in range(3))


def plan_mediatheque():
    """Figure 1 : le plan de la médiathèque. Repères 1 à 3 : un matériel ; 4 et 5 : un support de transmission."""
    W, H = 900, 412
    postes = [28 + 34 * i for i in range(10)]
    eventail = "".join(f'<path class="cr-cable" d="M202 152L{x + 15.5} 282"/>' for x in postes)
    cables = ('<path class="cr-cable" d="M492 136H264"/>'                      # routeur → switch multimédia
              '<path class="cr-cable" d="M470 316H388V146H264"/>'              # point d'accès → switch multimédia
              + eventail
              + '<path class="cr-cable" d="M803 144L751 214M803 144L846 204M803 144L803 316"/>')
    fibres = ('<path d="M520 4V120" stroke="#B26A00" stroke-width="4" fill="none"/>'
              '<path d="M548 128H743" stroke="#B26A00" stroke-width="4" fill="none"/>')
    corps = (
        # bâtiments et pièces
        '<text x="300" y="22" text-anchor="middle" class="cr-tb">Bâtiment principal</text>'
        '<rect x="10" y="30" width="590" height="374" rx="10" fill="#F6F7F4" stroke="#7D868F" stroke-width="2"/>'
        '<rect x="24" y="44" width="356" height="346" rx="6" fill="#FFFFFF" stroke="#A5ADAA"/>'
        '<text x="36" y="64" class="cr-ts">Espace multimédia</text>'
        '<rect x="396" y="44" width="190" height="186" rx="6" fill="#FFFFFF" stroke="#A5ADAA"/>'
        '<text x="406" y="64" class="cr-ts">Local technique</text>'
        '<rect x="396" y="246" width="190" height="144" rx="6" fill="#FFFFFF" stroke="#A5ADAA"/>'
        '<text x="406" y="266" class="cr-ts">Accueil</text>'
        '<text x="658" y="300" text-anchor="middle" class="cr-ts">jardin</text>'
        '<text x="803" y="22" text-anchor="middle" class="cr-tb">Annexe (bureaux)</text>'
        '<rect x="716" y="30" width="174" height="374" rx="10" fill="#F6F7F4" stroke="#7D868F" stroke-width="2"/>'
        + cables + fibres
        + '<text x="528" y="18" class="cr-ts">fibre de l\'opérateur</text>'
        '<text x="658" y="120" text-anchor="middle" class="cr-ts">160 m</text>'
        # repère 5 : le câble d'un poste multimédia
        '<path d="M128 185H161" stroke="#B42318" stroke-width="1.5" stroke-dasharray="3 3"/>'
        # matériels
        + cr.switch(140, 120, 124, 6, "") + cr.routeur(520, 128) + _point_acces(470, 300)
        + "".join(_pc(x, 282) for x in postes)
        + '<text x="196" y="334" text-anchor="middle" class="cr-t">10 postes multimédia</text>'
        + cr.switch(743, 112, 120, 6, "")
        + '<text x="803" y="100" text-anchor="middle" class="cr-t">Switch de l\'annexe</text>'
        + f'<g transform="translate(734 210) scale(.8)">{cr.serveur(0, 0)}</g>'
        '<text x="752" y="278" text-anchor="middle" class="cr-ts">serveur de</text>'
        '<text x="752" y="292" text-anchor="middle" class="cr-ts">fichiers</text>'
        + _pile(826, 200)
        + '<text x="846" y="264" text-anchor="middle" class="cr-ts">6 postes du</text>'
        '<text x="846" y="278" text-anchor="middle" class="cr-ts">personnel</text>'
        + f'<g transform="translate(773 316)">{ad._imprimante(0, 0)}</g>'
        '<text x="803" y="378" text-anchor="middle" class="cr-ts">imprimante</text>')
    cases = {"1": (460, 168, 120, 36, "matériel"), "2": (130, 76, 144, 36, "matériel"),
             "3": (426, 336, 130, 36, "matériel"), "4": (606, 142, 104, 36, "support"),
             "5": (28, 168, 100, 34, "support")}
    svg = (f'<svg class="plan-svg cr-svg" viewBox="0 0 {W} {H}" role="img" aria-label="Le plan de la médiathèque : '
           "bâtiment principal (espace multimédia et ses dix postes, local technique, accueil) et annexe des bureaux, "
           "à 160 m ; trois matériels repérés 1 à 3, deux liaisons repérées 4 et 5\">" + corps + "</svg>")
    return {"svg": svg, "w": W, "h": H, "cases": cases, "maxw": W,
            "caption": "Figure 1 — Le plan de la médiathèque. Les cases 1 à 3 reçoivent un matériel : celui du local "
                       "technique, qui relie l'opérateur et les deux réseaux (1), celui qui relie les postes de "
                       "l'espace multimédia (2), celui de l'accueil, pour les visiteurs (3). Les cases 4 et 5 reçoivent "
                       "un support : la liaison de 160 m entre le local technique et l'annexe (4), la liaison entre le "
                       "switch et chaque poste multimédia, 25 m au plus (5). Les liaisons en orange sont celles de la "
                       "fibre de l'opérateur et de l'annexe."}


DP1 = ('<div class="doc-text"><h3>La médiathèque et ses besoins</h3><p>La médiathèque de la ville rénove son réseau. '
       "Le <b>bâtiment principal</b> accueille l'espace multimédia (10 postes en libre accès), l'accueil, où les "
       "visiteurs se connectent en Wi-Fi, et le local technique, où arrive la fibre de l'opérateur. Le personnel "
       "travaille dans l'<b>annexe</b>, de l'autre côté du jardin, à <b>160 m</b> du local technique : 6 postes, le "
       "serveur de fichiers (catalogue, dossiers du personnel) et une imprimante. Dans les deux bâtiments, chaque "
       "poste a son propre câble vers le switch de sa pièce.</p><ul>"
       "<li>Deux réseaux séparés : le <b>réseau du personnel</b> (postes du personnel, serveur, imprimante) et le "
       "<b>réseau public</b> (postes multimédia, Wi-Fi des visiteurs).</li>"
       "<li>Un seul appareil, dans le local technique, relie l'opérateur et les deux réseaux. Il transmet vers Internet "
       "les messages des deux réseaux, et <b>bloque les messages du réseau public adressés au réseau du personnel</b>."
       "</li><li>Le point d'accès Wi-Fi de l'accueil est branché au switch de l'espace multimédia.</li>"
       "<li>Jusqu'à <b>120 visiteurs</b> connectés en même temps en Wi-Fi.</li></ul>"
       "<h3>Le plan d'adressage prévu</h3><p>Masque de sous-réseau des deux réseaux : <b>255.255.255.0</b>.</p>"
       '<table class="t"><thead><tr><th>Réseau</th><th>Adresse du réseau</th><th>Host-ID des machines</th></tr></thead>'
       f"<tbody><tr><td>Personnel</td><td>{PERSO}.0</td><td>routeur : 1 ; serveur : 2 ; imprimante : 3 ; postes : "
       f"11 à 16</td></tr><tr><td>Public</td><td>{PUBLIC}.0</td><td>routeur : 1 ; postes multimédia : 101 à 110 ; "
       "Wi-Fi des visiteurs : 150 à 249</td></tr></tbody></table>"
       f"<p>Adresse publique du routeur, côté opérateur : <b>{PUBLIQUE}</b>. Abonnement fibre : <b>1 Gbit/s</b> en "
       "réception, <b>500 Mbit/s</b> en émission.</p></div>")

DT1 = ('<div class="doc-text"><h3>Les matériels</h3><ul><li><b>Routeur</b> : relie des réseaux différents (ici '
       "l'opérateur, le réseau du personnel et le réseau public) ; il lit les adresses IP et peut filtrer les messages. "
       "Le routeur de la médiathèque intègre le modem de la fibre : un port WAN fibre (opérateur), un port LAN fibre, "
       "quatre ports LAN cuivre.</li><li><b>Switch</b> : relie par des câbles les machines d'un même réseau ; il lit "
       "les adresses MAC.</li><li><b>Point d'accès Wi-Fi</b> : relie au réseau les appareils sans fil.</li>"
       "<li><b>Serveur</b> : machine qui fournit un service (fichiers, pages web).</li><li><b>Modem</b> : fait le lien "
       "avec le réseau de l'opérateur, sans relier de réseaux locaux entre eux.</li></ul>"
       "<h3>Les switchs proposés</h3><p>Ports cuivre à 1 Gbit/s, pour câble Ethernet ; ports fibre à 10 Gbit/s.</p>"
       '<table class="t"><thead><tr><th>Switch</th><th>Ports cuivre</th><th>Ports fibre</th><th>Prix</th></tr></thead>'
       "<tbody>" + "".join(f"<tr><td>{m}</td><td>{c}</td><td>{f or '—'}</td><td>{p} €</td></tr>"
                           for m, c, f, p in SWITCHS) + "</tbody></table></div>")

DT2 = ('<div class="doc-text"><h3>Les supports de transmission</h3><table class="t"><thead><tr><th>Support</th>'
       "<th>Débit</th><th>Longueur, portée</th></tr></thead><tbody>"
       "<tr><td>Câble Ethernet catégorie 6 (cuivre, paires torsadées)</td><td>1 Gbit/s</td><td>100 m au plus</td></tr>"
       "<tr><td>Fibre optique multimode</td><td>10 Gbit/s</td><td>300 m au plus ; insensible aux perturbations "
       "électromagnétiques</td></tr><tr><td>Wi-Fi</td><td>environ 300 Mbit/s, partagés entre les appareils connectés"
       "</td><td>environ 30 m à l'intérieur</td></tr><tr><td>Bluetooth</td><td>environ 2 Mbit/s</td><td>environ 10 m"
       "</td></tr></tbody></table><h3>Débit</h3><p>Débit = quantité de données / durée de transmission ; 1 octet = "
       "8 bits ; 1 Go = 1 000 Mo ; 1 Gbit/s = 1 000 Mbit/s.</p></div>")

S = ad.S
MBITS = ad.MBITS


def parties(g):
    P, KW, IP, NUM, GRP, Q, QBAR = g.P, g.KW, g.IP, g.NUM, g.GRP, g.Q, g.QBAR
    return [
        {"title": "L'architecture du réseau", "minutes": 15, "plan": plan_mediatheque(), "intro": [
            "<p>La figure 1 est le plan de la médiathèque ; le dossier DP1 décrit le bâtiment et ses besoins, les "
            "dossiers DT1 et DT2 les matériels et les supports de transmission.</p>"], "blocks": [
            QBAR(["DP1", "DT1", "DT2"], "sur la figure 1"),
            GRP("Place les matériels repérés 1 à 3.", "La légende de la figure dit ce que fait chacun ; le dossier DT1 "
                "décrit les matériels.", [
                    ("Repère 1 — local technique", KW(P("routeur")), "Routeur"),
                    ("Repère 2 — espace multimédia", KW(P("switch")), "Switch"),
                    ("Repère 3 — accueil", KW(P("acces"), forbid="switch"), "Point d'accès Wi-Fi")],
                "<p>Seul un <strong>routeur</strong> relie des réseaux différents : l'opérateur, le réseau du "
                "personnel et le réseau public ; il lit les adresses IP, ce qui lui permet de filtrer. Le modem "
                "fait seulement le lien avec l'opérateur (ici, il est intégré au routeur). Les postes multimédia sont "
                "reliés par câble à un <strong>switch</strong> ; les visiteurs, sans fil, à un <strong>point d'accès "
                "Wi-Fi</strong>.</p>", etiquettes=E_MAT, liste="Matériels", reperes=["1", "2", "3"]),
            GRP("Choisis le support des liaisons repérées 4 et 5.", "Compare les longueurs aux limites du dossier DT2.",
                [("Repère 4 — local technique et annexe, 160 m", KW(P("fibre")), "Fibre optique"),
                 ("Repère 5 — switch et poste multimédia", KW(P("ethernet|cable"), forbid="fibre"), "Câble Ethernet")],
                "<p>La liaison avec l'annexe mesure 160 m : plus que les 100 m d'un câble Ethernet, moins que les "
                "300 m d'une fibre multimode, d'où la <strong>fibre optique</strong>. Les postes, à 25 m au plus du "
                "switch, ont chacun leur <strong>câble Ethernet</strong>, à 1 Gbit/s.</p>",
                etiquettes=E_SUP, liste="Supports", reperes=["4", "5"]),
            qcm.QCM("Pourquoi ne pas relier l'annexe au local technique par un câble Ethernet ?",
                    [("A", "La liaison mesure 160 m, alors qu'un câble Ethernet ne dépasse pas 100 m"),
                     ("B", "Un câble Ethernet ne peut pas être branché sur un routeur"),
                     ("C", "Un câble Ethernet coûte plus cher qu'une fibre optique"),
                     ("D", "Le Wi-Fi de l'accueil perturberait le câble")], ["A"],
                    "D'après DT2, un câble Ethernet catégorie 6 fait 100 m au plus ; la fibre multimode va jusqu'à "
                    "300 m. Les routeurs ont bien des ports cuivre, et le Wi-Fi ne gêne pas un câble."),
            qcm.QCM("Quelle est la topologie physique du réseau de l'espace multimédia ?",
                    [("A", "En étoile"), ("B", "En bus"), ("C", "En anneau"), ("D", "Maillée")], ["A"],
                    "Chaque poste a son propre câble vers le switch, le nœud central : c'est une étoile (figure 1)."),
        ]},
        {"title": "Le plan d'adressage", "minutes": 15, "intro": [
            "<p>Le dossier DP1 donne les adresses des deux réseaux, le masque et les host-ID prévus.</p>"], "blocks": [
            QBAR(["DP1"]),
            GRP("Écris les adresses IP de ces machines.", "Adresse seule, en notation pointée : net-ID du réseau, puis "
                "host-ID de la machine.", [
                    ("Routeur, côté personnel", IP(PERSO + ".1"), PERSO + ".1"),
                    ("Routeur, côté public", IP(PUBLIC + ".1"), PUBLIC + ".1"),
                    ("Serveur de fichiers", IP(PERSO + ".2"), PERSO + ".2"),
                    ("Imprimante", IP(PERSO + ".3"), PERSO + ".3"),
                    ("Premier poste du personnel", IP(PERSO + ".11"), PERSO + ".11"),
                    ("Dernier poste multimédia", IP(PUBLIC + ".110"), PUBLIC + ".110")],
                f"<p>Avec le masque 255.255.255.0, le net-ID est formé des trois premiers nombres : {PERSO} pour le "
                f"réseau du personnel, {PUBLIC} pour le réseau public. On lui ajoute le host-ID de la machine. Le "
                "routeur appartient aux deux réseaux : il a une adresse dans chacun.</p>"),
            Q("Combien d'adresses la plage prévue pour le Wi-Fi des visiteurs (host-ID 150 à 249) contient-elle ?",
              "Un nombre.", NUM(100), "100",
              "<p>De 150 à 249, bornes comprises : " + g.calc("249 − 150 + 1 = 100") + " adresses, une par "
              "appareil connecté.</p>"),
            qcm.QCM("Jusqu'à 120 visiteurs se connectent en même temps. Quelle plage de host-ID retenir pour le Wi-Fi ?",
                    [("A", "150 à 269"), ("B", "120 à 239"), ("C", "50 à 169"), ("D", "1 à 120 dans le réseau 192.168.21")],
                    ["B"],
                    "La plage prévue, 100 adresses, est trop petite. 120 à 239 donne 120 adresses, après les postes "
                    "multimédia (101 à 110). Un host-ID ne dépasse pas 254 (A), la plage C reprend les host-ID des "
                    "postes multimédia, et la plage D est dans un autre réseau, que le routeur ne relie pas."),
            qcm.QCM(f"Le téléphone d'un visiteur reçoit l'adresse {PUBLIC}.163. Quelles affirmations sont justes ?",
                    [(1, "Il fait partie du réseau public"),
                     (2, f"Pour aller sur Internet, il passe par le routeur, d'adresse {PUBLIC}.1"),
                     (3, f"Il peut ouvrir les dossiers du serveur, d'adresse {PERSO}.2"),
                     (4, f"Sur Internet, il est vu avec l'adresse {PUBLIC}.163")], [1, 2],
                    f"Son net-ID est {PUBLIC} : réseau public, dont la passerelle est le routeur ({PUBLIC}.1). Le "
                    "routeur bloque les messages du réseau public vers le réseau du personnel, où est le serveur. Sur "
                    f"Internet, le téléphone est vu avec l'adresse publique du routeur, {PUBLIQUE}."),
            qcm.QCM("Pourquoi faire deux réseaux, l'un pour le personnel, l'autre pour le public ?",
                    [("A", "Pour que les visiteurs ne puissent pas atteindre le serveur et les postes du personnel"),
                     ("B", "Pour doubler le débit de la fibre"),
                     ("C", "Parce qu'un switch ne peut pas relier plus de dix postes"),
                     ("D", "Parce que le Wi-Fi ne fonctionne qu'avec des adresses publiques")], ["A"],
                    "C'est une mesure de sécurité : le routeur relie les deux réseaux à Internet mais bloque le passage "
                    "du réseau public vers le réseau du personnel. La fibre est partagée par tous, quel que soit le "
                    "nombre de réseaux."),
        ]},
        {"title": "Le choix des matériels et les débits", "minutes": 20, "blocks": [
            QBAR(["DP1", "DT1", "DT2"]),
            Q("Combien de ports cuivre faut-il au switch de l'espace multimédia ?",
              "Un port par appareil branché, liaison avec le routeur comprise.", NUM(12), "12",
              "<p>10 postes, le point d'accès Wi-Fi de l'accueil et le câble du routeur : "
              + g.calc("10 + 1 + 1 = 12") + " ports cuivre.</p>"),
            qcm.QCM("Quel switch choisir pour l'espace multimédia ? Retiens le moins cher qui convient.",
                    [(m, f"Switch {m}") for m, *_ in SWITCHS], ["C"],
                    "Il faut 12 ports cuivre : A et B n'en ont que 8. C (16 ports, 95 €) et D (24 ports, 280 €) "
                    "conviennent ; C est le moins cher. Aucune fibre n'arrive à ce switch."),
            qcm.QCM("Quel switch choisir pour l'annexe ? Retiens le moins cher qui convient.",
                    [(m, f"Switch {m}") for m, *_ in SWITCHS], ["B"],
                    "Il faut 8 ports cuivre (6 postes, le serveur, l'imprimante) et 1 port fibre, pour la liaison avec "
                    "le local technique. A et C n'ont pas de port fibre ; B (130 €) convient, D aussi, plus cher."),
            Q("Aux heures d'affluence, les 10 postes multimédia regardent chacun une vidéo à 25 Mbit/s et 100 visiteurs "
              "une vidéo à 5 Mbit/s. Quel débit total la fibre doit-elle recevoir ?", "En Mbit/s, avec son unité.",
              NUM(750, 0.5, "Mbit/s", MBITS), "750 Mbit/s",
              "<p>" + g.calc("10 × 25 + 100 × 5 = 250 + 500 = 750 Mbit/s") + " : moins que le 1 Gbit/s (1 000 Mbit/s) "
              "de l'abonnement en réception, la fibre suffit.</p>"),
            Q("Chaque nuit, le serveur envoie sa sauvegarde, 90 Go, vers un centre de données, par la fibre. Quelle est "
              "la durée minimale de l'envoi ?", "Lis le débit d'émission dans DP1 ; donne la durée en secondes, avec son "
              "unité.", NUM(1440, 0.5, "s", S), "1 440 s",
              "<p>90 Go = 90 × 8 = 720 Gbit = 720 000 Mbit ; l'envoi utilise le débit d'émission : "
              + g.calc("720 000 Mbit ÷ 500 Mbit/s = 1 440 s") + ", soit 24 min.</p>"),
            Q("Un agent copie un dossier de 2 Go du serveur vers son poste. La liaison la plus lente du trajet est le "
              "câble Ethernet de son poste. Quelle est la durée minimale de la copie ?", "En secondes, avec son unité.",
              NUM(16, 0.5, "s", S), "16 s",
              "<p>2 Go = 16 Gbit ; le câble Ethernet transmet 1 Gbit/s (DT2) : "
              + g.calc("16 Gbit ÷ 1 Gbit/s = 16 s") + ". La copie reste dans le réseau du personnel : elle "
              "n'utilise pas la fibre de l'opérateur.</p>"),
        ]},
        {"title": "Les échanges à travers le routeur", "minutes": 15, "blocks": [
            QBAR(["DP1", "DT1"]),
            GRP("Pour chaque échange, indique ce que fait le routeur.", "Lis la règle de filtrage de DP1 ; deux machines "
                "d'un même réseau communiquent par leur switch.", [
                    ("Un poste multimédia ouvre un site web", KW(P("transmis")), "Transmise par le routeur"),
                    ("Le téléphone d'un visiteur ouvre un dossier du serveur", KW(P("bloque")), "Bloquée par le routeur"),
                    ("Un poste du personnel imprime", KW(P("sans")), "Sans passer par le routeur"),
                    ("Un poste du personnel ouvre un site web", KW(P("transmis")), "Transmise par le routeur"),
                    ("Un poste multimédia envoie un document à l'imprimante", KW(P("bloque")),
                     "Bloquée par le routeur")],
                "<p>Le routeur transmet vers Internet les messages des deux réseaux, et bloque ceux du réseau public "
                "adressés au réseau du personnel (serveur, imprimante). Un poste du personnel et l'imprimante ont le "
                "même net-ID : la trame va de l'un à l'autre par le switch de l'annexe, sans passer par le "
                "routeur.</p>", etiquettes=E_ROUTEUR, liste="Ce que fait le routeur"),
            qcm.QCM("Le switch de l'espace multimédia reçoit une trame qu'un poste envoie au routeur. Que lit-il pour "
                    "choisir le port de sortie ?",
                    [("A", "L'adresse MAC de destination"), ("B", "L'adresse IP de destination"),
                     ("C", "L'adresse IP source"), ("D", "Le nom du site demandé")], ["A"],
                    "Un switch lit les adresses MAC (couche 2) : il envoie la trame vers le port où se trouve l'adresse "
                    "MAC de destination, ici celle du routeur."),
            qcm.QCM("À quelle couche du modèle OSI le routeur décide-t-il de transmettre ou de bloquer un message ?",
                    [("A", "Couche 1, physique"), ("B", "Couche 2, liaison de données (adresses MAC)"),
                     ("C", "Couche 3, réseau (adresses IP)"), ("D", "Couche 7, application")], ["C"],
                    "Le routeur lit les adresses IP, couche 3 : le net-ID de la source et de la destination lui dit de "
                    "quel réseau vient le message et où il va."),
            Q("Avec quelle adresse IP un poste multimédia est-il vu par le serveur d'un site web ?",
              "Écris l'adresse seule, en notation pointée.", IP(PUBLIQUE), PUBLIQUE,
              "<p>Le routeur remplace l'adresse privée du poste par son adresse publique (traduction d'adresses, "
              f"NAT) : le serveur web voit {PUBLIQUE}, comme pour toutes les machines de la médiathèque.</p>"),
            qcm.QCM("Un visiteur ouvre un site web. Quand sa requête traverse le routeur, qu'est-ce qui change ?",
                    [(1, "L'adresse IP source"), (2, "Les adresses MAC de la trame"),
                     (3, "L'adresse IP de destination"), (4, "La requête HTTP")], [1, 2],
                    f"L'adresse IP source, privée ({PUBLIC}.163), devient l'adresse publique du routeur ; l'en-tête "
                    "Ethernet est refait pour la liaison suivante, avec de nouvelles adresses MAC. L'adresse de "
                    "destination, celle du serveur web, et la requête ne changent pas."),
        ]},
    ]


def exercice(g):
    return {"key": "etude-mediatheque", "prefix": "e", "tag": "Étude 1", "level": "Niveau 2", "etude": True,
            "title": "Le réseau d'une médiathèque", "parts": parties(g),
            "docs": [g.DOC("DP1", "La médiathèque et ses besoins", DP1), g.DOC("DT1", "Les matériels", DT1),
                     g.DOC("DT2", "Les supports de transmission", DT2)],
            "consignes": g.consignes(g.C_SCHEMA, g.C_ETIQUETTES, g.C_SAISIE, g.C_GROUPE, qcm.C_QCM, g.C_DOCUMENTS),
            "hero": ("carte-etude-1", "Le plan du réseau d'une médiathèque : bâtiment principal et annexe",
                     "Deux bâtiments, deux réseaux, un routeur."),
            "mots": ["Deux réseaux", "Plan d'adressage", "Choix des matériels", "Débits"], "vign": "carte-etude-1",
            "valt": "Le plan du réseau d'une médiathèque",
            "sub": "Le réseau d'une médiathèque, du local technique à l'annexe des bureaux : placer les matériels et "
                   "les supports, établir le plan d'adressage de deux réseaux, choisir les switchs, vérifier les "
                   "débits, dire ce que le routeur transmet ou bloque."}
