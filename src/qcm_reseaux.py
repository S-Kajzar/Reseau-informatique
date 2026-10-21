"""QCM 1.1 — Réseaux informatiques (Niveau 1) : le premier exercice, sur le cours 1.

Six parties qui suivent le plan du cours (liaison point-à-point, mise en réseau, WAN et Internet, adressage IP et
LAN, communication entre logiciels, modèle OSI), pondérées par leur durée. Questions à réponse unique (repères A,
B, C…) ou multiple (repères numériques, il faut toutes les bonnes et elles seules) ; chaque question vaut un point,
l'explication s'affiche à la correction. Les adresses et les exemples sont ceux du cours.

exercice(g) reçoit le module generer : pas d'import circulaire.
"""
import qcm

Q = qcm.QCM


def _bus():
    """Schéma de la question sur la topologie en bus : quatre postes branchés sur une même ligne."""
    postes = "".join(
        f'<g transform="translate({40 + 110 * i} 14)"><rect width="46" height="32" rx="3" fill="#1C2530"/>'
        f'<rect x="4" y="4" width="38" height="22" fill="#4F8FDB"/><line x1="23" y1="32" x2="23" y2="74" '
        f'stroke="#5A6670" stroke-width="2.5"/><circle cx="23" cy="74" r="4" fill="#1C2530"/></g>' for i in range(4))
    return ('<figure class="fig" style="max-width:480px"><svg viewBox="0 0 480 110" role="img" aria-label="Quatre '
            'postes reliés à une même ligne de transmission" style="display:block;width:100%;height:auto">'
            '<line x1="20" y1="88" x2="440" y2="88" stroke="#5A6670" stroke-width="3"/>' + postes + "</svg></figure>")


def parties():
    return [
        {"title": "Liaison point-à-point", "minutes": 9, "blocks": [
            Q("Une liaison point-à-point relie…",
              [("A", "deux machines, directement"), ("B", "toutes les machines d'un réseau local"),
               ("C", "un réseau local à Internet")], ["A"],
              "C'est une liaison directe entre deux machines (ordinateur, smartphone, objet connecté…)."),
            Q("Par quel composant une machine se connecte-t-elle à une liaison point-à-point ?",
              [("A", "Son processeur"), ("B", "Sa carte-réseau"), ("C", "Son écran")], ["B"],
              "La carte-réseau relie la machine au support de communication."),
            Q("Sur quoi une liaison point-à-point est-elle basée ?",
              [(1, "Un support de communication"), (2, "Un protocole de communication"), (3, "Un routeur"),
               (4, "Une adresse IP publique")], [1, 2],
              "Le support (câble, fibre, air) transporte le signal ; le protocole fixe les règles de communication."),
            Q("Avec un talkie-walkie, on ne peut pas parler en même temps que son interlocuteur : la liaison est…",
              [("A", "full-duplex"), ("B", "half-duplex")], ["B"],
              "Half-duplex : un seul sens à la fois. Full-duplex : les deux sens en même temps, comme au téléphone."),
            Q("Dans un câble en cuivre à paires torsadées, les données circulent sous forme de…",
              [("A", "signal électrique"), ("B", "signal lumineux"), ("C", "ondes radio")], ["A"],
              "Le cuivre transporte un signal électrique ; la fibre optique, un signal lumineux."),
            Q("Par rapport au câble en cuivre, la fibre optique est…",
              [("A", "plus performante, mais plus chère"), ("B", "moins performante et moins chère"),
               ("C", "aussi performante et aussi chère")], ["A"],
              "La fibre optique est plus performante, mais plus chère."),
            Q("Quel est le protocole de communication filaire le plus utilisé ?",
              [("A", "Bluetooth"), ("B", "Ethernet"), ("C", "Wi-Fi")], ["B"],
              "Ethernet est le protocole filaire le plus utilisé ; Bluetooth et Wi-Fi sont des protocoles sans fil."),
            Q("Comparé au Bluetooth, le Wi-Fi…",
              [(1, "est plus performant"), (2, "offre une meilleure portée"), (3, "consomme moins d'énergie"),
               (4, "consomme plus d'énergie")], [1, 2, 4],
              "Le Wi-Fi est plus performant et porte plus loin, mais il consomme plus d'énergie que le Bluetooth."),
            Q("Un fichier de 20 Mo est transmis en 4 s. Le débit de la liaison vaut…",
              [(1, "5 Mo/s"), (2, "80 Mo/s"), (3, "40 Mbit/s"), (4, "0,2 Mo/s")], [1, 3],
              "Débit = quantité de données / durée = 20 Mo / 4 s = 5 Mo/s ; un octet vaut 8 bits : 5 × 8 = 40 Mbit/s."),
            Q("1 Mo/s correspond à…",
              [("A", "1 000 octets/s"), ("B", "1 000 000 octets/s"), ("C", "1 000 000 bit/s")], ["B"],
              "Le préfixe M (méga) vaut un million : 1 Mo/s = 1 000 000 octets/s, soit 8 000 000 bit/s."),
        ]},
        {"title": "Mise en réseau", "minutes": 9, "blocks": [
            Q("Quel est le rôle d'un dispositif d'interconnexion (switch, point d'accès) ?",
              [("A", "Faire passer les trames d'une liaison point-à-point vers une autre"),
               ("B", "Stocker les pages des sites web"), ("C", "Attribuer une adresse MAC aux machines")], ["A"],
              "Il relie plusieurs liaisons point-à-point et fait passer les trames de l'une à l'autre."),
            Q("Le commutateur (switch) interconnecte des liaisons…",
              [("A", "filaires"), ("B", "non-filaires"), ("C", "intercontinentales")], ["A"],
              "Le switch interconnecte les liaisons filaires ; le point d'accès sans fil, les liaisons non-filaires."),
            Q("Des machines interconnectées par des switchs et des points d'accès sans fil forment…",
              [("A", "un réseau local (LAN)"), ("B", "un WAN"), ("C", "une dorsale")], ["A"],
              "LAN : Local Area Network, le réseau local."),
            Q("Tous les équipements sont reliés à une même ligne de transmission : quelle est cette topologie ?",
              [("A", "En étoile"), ("B", "En bus"), ("C", "Maillée"), ("D", "En anneau")], ["B"],
              "La ligne commune s'appelle le bus ; ces réseaux, simples à mettre en œuvre, sont très utilisés en "
              "domotique.", fig=_bus()),
            Q("Quelle topologie offre des chemins différents pour relier deux points, ce qui évite les problèmes en cas "
              "de rupture d'une liaison ?", [("A", "En bus"), ("B", "En étoile"), ("C", "Maillée")], ["C"],
              "La topologie maillée, très utilisée dans les très grands réseaux, propose plusieurs chemins."),
            Q("Le réseau d'une maison, organisé autour de la box internet, a une topologie…",
              [("A", "en étoile"), ("B", "en anneau"), ("C", "en bus")], ["A"],
              "Toutes les machines sont reliées à un nœud central, la box : c'est une étoile, comme la plupart des LAN."),
            Q("Une adresse MAC se compose de…",
              [("A", "4 nombres décimaux de 0 à 255"), ("B", "6 couples de chiffres hexadécimaux"),
               ("C", "8 chiffres binaires")], ["B"],
              "Exemple : 28:87:a5:ef:18:5d, soit 6 octets (48 bits)."),
            Q("Lesquelles de ces écritures sont des adresses MAC ?",
              [(1, "28:87:a5:ef:18:5d"), (2, "192.168.1.10"), (3, "00-40-05-A9-AA-71"), (4, "28:87:G5:EF:18")],
              [1, 3],
              "Six couples de chiffres hexadécimaux, séparés par « : » ou « - ». 192.168.1.10 est une adresse IP ; "
              "28:87:G5:EF:18 n'a que 5 couples, et G n'est pas un chiffre hexadécimal."),
            Q("Qui lit l'adresse MAC du destinataire pour aiguiller une trame dans le réseau local ?",
              [("A", "Le switch"), ("B", "Le modem"), ("C", "Le serveur web")], ["A"],
              "Les switchs et les points d'accès lisent les adresses MAC pour envoyer la trame dans la bonne direction."),
            Q("Pourquoi dit-on que l'adresse MAC est l'adresse physique de la machine ?",
              [("A", "Elle est gravée sur la carte-réseau par son fabricant"),
               ("B", "Elle dépend du lieu où se trouve la machine"), ("C", "Elle change à chaque connexion")], ["A"],
              "Elle est inscrite dans la carte-réseau ; l'adresse IP, elle, peut changer : c'est l'adresse logique."),
        ]},
        {"title": "WAN et Internet", "minutes": 10, "blocks": [
            Q("Plusieurs réseaux locaux interconnectés forment…",
              [("A", "un WAN"), ("B", "un switch"), ("C", "un sous-réseau logique")], ["A"],
              "WAN : Wide Area Network. Internet est le principal WAN mondial."),
            Q("Le routeur qui relie un réseau local au WAN sert de…",
              [("A", "passerelle"), ("B", "point d'accès sans fil"), ("C", "dorsale")], ["A"],
              "Le routeur passerelle fait passer les trames du LAN vers le WAN, et inversement."),
            Q("Que contient une box internet ?",
              [(1, "Un routeur"), (2, "Un switch"), (3, "Un hotspot Wi-Fi"), (4, "Un modem"),
               (5, "Le serveur web des sites visités")], [1, 2, 3, 4],
              "La box réunit un routeur (la passerelle), un switch, un hotspot Wi-Fi et un modem, qui la relie au "
              "réseau du fournisseur d'accès (FAI)."),
            Q("Quand une trame circule dans un internet, on l'appelle…",
              [("A", "un segment"), ("B", "un paquet"), ("C", "un bit")], ["B"],
              "Dans un internet, la trame est appelée paquet ; c'est l'unité de la couche réseau."),
            Q("Comment s'appellent les mécanismes qui aiguillent les paquets à travers Internet ?",
              [("A", "Le routage"), ("B", "La segmentation"), ("C", "L'encapsulation")], ["A"],
              "Le routage est assuré par les routeurs, qui choisissent une route parmi toutes celles du maillage."),
            Q("Les grandes liaisons en fibre optique qui relient les zones géographiques d'Internet s'appellent…",
              [("A", "des dorsales (backbones)"), ("B", "des bus"), ("C", "des passerelles")], ["A"],
              "Entre les continents, les dorsales sont des câbles sous-marins."),
            Q("Laquelle de ces écritures est une adresse IP ?",
              [("A", "89.234.17.105"), ("B", "89.234.17"), ("C", "89.256.17.105")], ["A"],
              "Quatre nombres décimaux, chacun compris entre 0 et 255 : 89.234.17 n'en a que trois, 256 dépasse 255."),
            Q("Pourquoi dit-on que l'adresse IP est l'adresse logique de la machine ?",
              [("A", "Elle peut être changée à tout moment"), ("B", "Elle est gravée sur la carte-réseau"),
               ("C", "Elle est lue par les switchs")], ["A"],
              "L'adresse IP peut changer ; l'adresse MAC, gravée sur la carte, est l'adresse physique."),
            Q("Avec le masque 255.255.255.0, quel est le net-ID de l'adresse 102.122.201.17 ?",
              [("A", "102.122"), ("B", "102.122.201"), ("C", "17")], ["B"],
              "Les trois nombres situés au-dessus des 255 forment le net-ID : 102.122.201 ; le host-ID est 17."),
            Q("Avec le masque 255.0.0.0, quel est le host-ID de l'adresse 19.102.12.193 ?",
              [("A", "19"), ("B", "102.12.193"), ("C", "12.193")], ["B"],
              "Seul le premier nombre est au-dessus d'un 255 : net-ID 19, host-ID 102.12.193."),
            Q("Avec le masque 255.255.255.0, combien de machines peut-on connecter ?",
              [("A", "254"), ("B", "256"), ("C", "65 534")], ["A"],
              "Le host-ID tient sur un octet : 256 valeurs, dont deux réservées (réseau et diffusion), soit 254 "
              "machines. Avec 255.255.0.0, c'est 65 534."),
        ]},
        {"title": "Adressage IP et LAN", "minutes": 7, "blocks": [
            Q("Sur Internet, un ordinateur d'un réseau local est vu avec…",
              [("A", "son adresse IP privée"), ("B", "l'adresse IP publique de son routeur passerelle"),
               ("C", "son adresse MAC")], ["B"],
              "L'adresse publique n'est pas la véritable adresse de l'ordinateur : c'est celle de son routeur passerelle."),
            Q("Quelles adresses sont des adresses privées, réservées aux réseaux locaux ?",
              [(1, "10.12.0.3"), (2, "172.20.5.1"), (3, "172.32.0.1"), (4, "192.168.1.5"), (5, "92.169.148.17")],
              [1, 2, 4],
              "Plages réservées : 10.0.0.0 à 10.255.255.255, 172.16.0.0 à 172.31.255.255, 192.168.0.0 à "
              "192.168.255.255. 172.32.0.1 et 92.169.148.17 sont publiques."),
            Q("Toutes les machines d'un même réseau local ont…",
              [("A", "la même adresse IP publique"), ("B", "la même adresse IP privée"),
               ("C", "la même adresse MAC")], ["A"],
              "Elles passent toutes par le même routeur passerelle : elles ont la même adresse IP publique."),
            Q("PC1 a l'adresse 192.168.0.54, avec le masque 255.255.255.0. Avec quelles machines de son LAN peut-il "
              "communiquer ?",
              [(1, "192.168.0.17"), (2, "192.168.1.38"), (3, "192.168.0.200"), (4, "192.168.1.11")], [1, 3],
              "Dans un LAN, deux machines communiquent seulement si elles ont le même net-ID : ici 192.168.0."),
            Q("Pour créer deux sous-réseaux logiques dans un même LAN, il suffit de…",
              [("A", "modifier le câblage"), ("B", "bien choisir les adresses IP"), ("C", "ajouter un modem")], ["B"],
              "Les sous-réseaux logiques ne dépendent que des net-ID : le câblage ne change pas."),
        ]},
        {"title": "Communication entre logiciels", "minutes": 5, "blocks": [
            Q("Dans le modèle client-serveur, le logiciel qui cherche à accéder à des ressources en ligne est…",
              [("A", "le client"), ("B", "le serveur")], ["A"],
              "Le client accède aux ressources ; le serveur met des services à disposition."),
            Q("Les messages envoyés par le client s'appellent…",
              [("A", "des réponses"), ("B", "des requêtes"), ("C", "des trames")], ["B"],
              "Le client envoie des requêtes ; le serveur renvoie des réponses."),
            Q("Que contient la réponse HTTP d'un serveur web à la demande d'une page ?",
              [("A", "Le code HTML et CSS de la page"), ("B", "L'adresse MAC du navigateur"),
               ("C", "Le mot de passe de l'utilisateur")], ["A"],
              "Le serveur cherche la page sur son disque dur et renvoie son code HTML et CSS ; le navigateur l'affiche."),
            Q("Que fait le protocole TCP ?",
              [(1, "Il segmente les gros messages"), (2, "Il fait envoyer un accusé de réception pour chaque segment reçu"),
               (3, "Il détecte les erreurs dans les messages"), (4, "Il attribue les adresses MAC")], [1, 2, 3],
              "TCP fiabilise l'échange : segmentation, accusés de réception, détection des erreurs. L'adresse MAC est "
              "gravée sur la carte-réseau."),
        ]},
        {"title": "Modèle OSI", "minutes": 7, "blocks": [
            Q("Combien de couches compte le modèle OSI ?", [("A", "4"), ("B", "7"), ("C", "9")], ["B"],
              "Physique, liaison de données, réseau, transport, session, présentation, application."),
            Q("À quelle couche du modèle OSI appartient le protocole IP ?",
              [("A", "2 — Liaison de données"), ("B", "3 — Réseau"), ("C", "4 — Transport")], ["B"],
              "La couche réseau identifie et localise les machines d'un internet, et route les paquets."),
            Q("Quelle couche gère la segmentation des messages ?",
              [("A", "4 — Transport"), ("B", "3 — Réseau"), ("C", "1 — Physique")], ["A"],
              "La couche transport (TCP) segmente les messages et fiabilise la transmission."),
            Q("Dans la couche liaison de données, le message s'appelle…",
              [("A", "un paquet"), ("B", "une trame"), ("C", "un segment")], ["B"],
              "Bits (couche 1), trame (2), paquet (3), segment (4), requête ou réponse (5 à 7)."),
            Q("Encapsuler un message, c'est…",
              [("A", "lui ajouter un en-tête"), ("B", "le chiffrer"), ("C", "le compresser")], ["A"],
              "Chaque couche prend en charge le message et lui ajoute son en-tête (TCP, IP, Ethernet…)."),
            Q("Un routeur met en œuvre les couches…", [("A", "1 et 2"), ("B", "1 à 3"), ("C", "1 à 7")], ["B"],
              "Il remonte jusqu'à la couche 3 pour lire l'adresse IP ; les switchs et les hotspots s'arrêtent à la "
              "couche 2."),
            Q("Quels appareils mettent en œuvre les sept couches ?",
              [(1, "Les ordinateurs"), (2, "Les smartphones"), (3, "Les switchs"), (4, "Les routeurs")], [1, 2],
              "Ordinateurs et smartphones mettent en œuvre toutes les couches ; routeurs : 1 à 3 ; switchs : 1 et 2."),
        ]},
    ]


def exercice(g):
    return {"key": "qcm-reseaux", "prefix": "q", "tag": "QCM 1.1", "level": "Niveau 1", "qcm": True,
            "title": "QCM : réseaux informatiques", "parts": parties(), "docs": [], "consignes": qcm.CONSIGNES,
            "hero": ("carte-qcm", "Le réseau d'une maison : la box, le Wi-Fi et les postes",
                     "Liaisons, réseaux locaux, Internet, adresses MAC et IP, client-serveur, modèle OSI."),
            "mots": ["Liaisons", "MAC et IP", "Routage", "Modèle OSI"], "vign": "carte-qcm",
            "valt": "Topologie d'un réseau maillé",
            "sub": "Un questionnaire à choix multiples sur le cours 1 : liaison point-à-point et débit, mise en réseau "
                   "et adresse MAC, WAN et Internet, découpage des adresses IP, adresses privées et publiques, "
                   "client-serveur et TCP, modèle OSI."}
