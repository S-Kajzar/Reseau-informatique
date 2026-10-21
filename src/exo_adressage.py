"""Exercice 1.3 — Le plan d'adressage de la maison (Niveau 1), l'entraînement direct au cours 1.

Le réseau d'une maison : une box (modem, routeur, switch, point d'accès Wi-Fi) et six appareils. Quatre parties :
le schéma du réseau (étiquettes posées sur la figure), le tableau d'adressage (net-ID, host-ID, adresses de la box,
adresses privées et publiques), des adresses à choisir (nombre de machines, adresse libre, tablette mal réglée), le
débit de la connexion (durées de téléchargement, débit d'une transmission).

exercice(g) reçoit le module generer : pas d'import circulaire. Les pictogrammes viennent du cours 1.
"""
import qcm
import cours_reseaux as cr

PUBLIQUE, BOX = "86.245.12.40", "192.168.1.1"
APPAREILS = [  # appareil, liaison avec la box, adresse IP
    ("Ordinateur fixe", "câble Ethernet", "192.168.1.10"), ("Console de jeux", "câble Ethernet", "192.168.1.11"),
    ("Imprimante", "Wi-Fi", "192.168.1.20"), ("Ordinateur portable", "Wi-Fi", "192.168.1.30"),
    ("Téléphone", "Wi-Fi", "192.168.1.31"), ("Tablette", "Wi-Fi", "192.168.2.50 (réglée à la main)")]

E_BOX = ["Modem", "Routeur", "Switch", "Point d'accès Wi-Fi", "Serveur web", "Carte-réseau"]
E_LIAISONS = ["Câble Ethernet", "Wi-Fi", "Fibre optique", "Bluetooth"]
E_ADRESSES = ["Adresse privée", "Adresse publique"]


def _console(x, y):
    return (f'<g transform="translate({x} {y})"><rect width="60" height="30" rx="14" fill="{cr.ENCRE}"/>'
            '<path d="M14 10v10M9 15h10" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>'
            '<circle cx="42" cy="12" r="3.2" fill="#E8603C"/><circle cx="49" cy="18" r="3.2" fill="#5BD08A"/></g>')


def _imprimante(x, y):
    return (f'<g transform="translate({x} {y})"><rect x="12" width="36" height="12" fill="#FFFFFF" stroke="#7D868F"/>'
            '<rect y="10" width="60" height="28" rx="5" fill="#D3D8D5" stroke="#46525C" stroke-width="1.5"/>'
            '<rect x="14" y="30" width="32" height="14" fill="#FFFFFF" stroke="#7D868F"/></g>')


def _telephone(x, y):
    return (f'<g transform="translate({x} {y})"><rect width="26" height="44" rx="5" fill="{cr.ENCRE}"/>'
            f'<rect x="3" y="5" width="20" height="32" fill="{cr.ECRAN}"/></g>')


def _picto(i, x, y):
    """Pictogramme d'un appareil de la box, en haut de sa cellule : il permet de reconnaître chaque repère."""
    if i == 0:  # modem : la liaison venant d'Internet y arrive
        return (f'<path d="M{x + 52} {y + 14}q6 -8 12 0t12 0t12 0" stroke="{cr.ORANGE}" stroke-width="2.5" fill="none"/>')
    if i == 1:
        return f'<g transform="translate({x + 75} {y + 9}) scale(.5)">{cr.routeur(0, 0)}</g>'
    if i == 2:
        return (f'<rect x="{x + 45}" y="{y + 6}" width="60" height="14" rx="2" fill="{cr.ENCRE}"/>'
                + "".join(f'<rect x="{x + 50 + 13 * k}" y="{y + 10}" width="8" height="6" fill="#0E1114" '
                          'stroke="#7D868F" stroke-width=".6"/>' for k in range(4)))
    return (f'<g fill="none" stroke="{cr.VERT}" stroke-width="2.5"><path d="M{x + 66} {y + 18}a12 12 0 0 1 18 0"/>'
            f'<path d="M{x + 60} {y + 12}a20 20 0 0 1 30 0"/></g><circle cx="{x + 75}" cy="{y + 20}" r="2.5" '
            f'fill="{cr.VERT}"/>')


def plan_maison():
    """Figure 1 : le réseau de la maison. Repères 1 à 4 : les appareils de la box, reconnaissables à leur
    pictogramme ; 5 à 8 : le type de liaison, donné par le dossier DP1 (les liaisons sont toutes dessinées pareil)."""
    W, H = 860, 400
    modules = [(316, 64), (474, 64), (316, 144), (474, 144)]
    devices = [  # nom, x du centre, dessin, cible sur la box
        ("Ordinateur fixe", 80, cr.pc(52, 272), 350), ("Console de jeux", 240, _console(210, 280), 410),
        ("Imprimante", 400, _imprimante(370, 272), 470), ("Ordinateur portable", 560, cr.portable(533, 272), 530),
        ("Téléphone", 720, _telephone(707, 268), 590)]
    lignes = "".join(f'<path class="ad-l" d="M{x} 266L{cible} 224"/>' for _n, x, _d, cible in devices)
    corps = ('<path class="ad-l" d="M176 92H316"/>' + lignes + cr.nuage(110, 78, 0.95)
             + '<rect x="300" y="30" width="340" height="194" rx="12" fill="#F4F5F2" stroke="#7D868F" stroke-width="2"/>'
             '<text x="470" y="54" text-anchor="middle" class="cr-tb">Box internet</text>'
             + "".join(f'<rect x="{x}" y="{y}" width="150" height="72" rx="6" fill="#FFFFFF" stroke="#A5ADAA"/>'
                       + _picto(i, x, y) for i, (x, y) in enumerate(modules))
             + '<path class="ad-l" d="M300 92H316"/>'
             + "".join(_d for _n, _x, _d, _c in devices)
             + "".join(f'<text x="{x}" y="340" text-anchor="middle" class="cr-t">{n}</text>' for n, x, _d, _c in devices))
    cases = {str(i + 1): (x + 6, y + 28, 138, 38, "") for i, (x, y) in enumerate(modules)}
    cases["5"] = (172, 104, 122, 36, "liaison")
    cases.update({"6": (26, 350, 108, 34, "liaison"), "7": (506, 350, 108, 34, "liaison"),
                  "8": (186, 350, 108, 34, "liaison")})
    svg = (f'<svg class="plan-svg cr-svg" viewBox="0 0 {W} {H}" role="img" aria-label="Le réseau de la maison : '
           "Internet, la box et ses quatre appareils (repères 1 à 4), cinq appareils reliés à la box ; les repères 5 "
           'à 8 désignent des liaisons">' + corps + "</svg>")
    return {"svg": svg, "w": W, "h": H, "cases": cases, "maxw": W,
            "caption": "Figure 1 — Le réseau de la maison. Les cases 1 à 4 reçoivent les appareils de la box, "
                       "reconnaissables à leur pictogramme (la liaison venant d'Internet arrive au repère 1) ; les "
                       "cases 5 à 8, le type de la liaison : entre la box et Internet (5), entre la box et "
                       "l'ordinateur fixe (6), l'ordinateur portable (7), la console de jeux (8)."}


DP1 = ('<div class="doc-text"><h3>Le réseau de la maison</h3><p>La maison est raccordée à Internet par la <b>fibre '
       "optique</b>, à 1 Gbit/s. La box contient un modem, un routeur, un switch de quatre prises Ethernet et un point "
       f"d'accès Wi-Fi. Sur Internet, son adresse publique est <b>{PUBLIQUE}</b> ; dans le réseau local, son adresse est "
       f"<b>{BOX}</b>, avec le masque de sous-réseau <b>255.255.255.0</b>.</p>"
       '<table class="t"><thead><tr><th>Appareil</th><th>Liaison avec la box</th><th>Adresse IP</th></tr></thead><tbody>'
       + "".join(f"<tr><td>{a}</td><td>{l}</td><td>{ip}</td></tr>" for a, l, ip in APPAREILS)
       + "</tbody></table><p>Débits : 1 Gbit/s par câble Ethernet (la console suit le débit de la fibre) ; environ "
       "300 Mbit/s en Wi-Fi pour l'ordinateur portable.</p></div>")

DT1 = ('<div class="doc-text"><h3>Adresses IP et masques</h3><ul><li>Une adresse IP compte 4 nombres de 0 à 255. On '
       "superpose l'adresse et le masque : la partie au-dessus des 255 est le <b>net-ID</b> (le réseau), la partie "
       "au-dessus des 0 est le <b>host-ID</b> (la machine). Exemple : 192.168.1.10 avec 255.255.255.0 → net-ID "
       "192.168.1, host-ID 10.</li><li>Nombre de machines : 255.0.0.0 → 16 777 214 ; 255.255.0.0 → 65 534 ; "
       "255.255.255.0 → 254.</li><li>Dans un LAN, deux machines communiquent seulement si elles ont le même net-ID."
       "</li><li>Adresses privées, réservées aux LAN : de 10.0.0.0 à 10.255.255.255, de 172.16.0.0 à 172.31.255.255, de "
       "192.168.0.0 à 192.168.255.255. Sur Internet, les machines d'un LAN sont vues avec l'adresse publique de leur "
       "routeur passerelle.</li></ul><h3>Débit</h3><p>Débit = quantité de données / durée de transmission ; "
       "1 octet = 8 bits ; 1 Go = 1 000 Mo = 1 000 000 000 octets ; 1 Gbit/s = 1 000 Mbit/s.</p></div>")

AD_CSS = """
/* ---------- exercice 1.3 : liaisons du schéma de la maison, toutes dessinées pareil ---------- */
.ad-l{fill:none; stroke:#7D868F; stroke-width:2.5; stroke-dasharray:7 5}
"""
S = ["s", "seconde", "secondes", "sec"]
MBITS = ["mbit/s", "mbits/s", "mbits", "mbps", "megabit/s", "megabits/s"]


def parties(g):
    P, KW, IP, NUM, GRP, Q, QBAR = g.P, g.KW, g.IP, g.NUM, g.GRP, g.Q, g.QBAR
    return [
        {"title": "Le schéma du réseau", "minutes": 10, "plan": plan_maison(), "intro": [
            "<p>La figure 1 représente le réseau de la maison ; le dossier DP1 décrit chaque appareil et sa liaison "
            "avec la box.</p>"], "blocks": [
            QBAR(["DP1"], "sur la figure 1"),
            GRP("Nomme les quatre appareils que contient la box (repères 1 à 4).", "Aide-toi des pictogrammes : la "
                "liaison venant d'Internet arrive au repère 1.", [
                    ("Repère 1", KW(P("modem")), "Modem"), ("Repère 2", KW(P("routeur")), "Routeur"),
                    ("Repère 3", KW(P("switch")), "Switch"),
                    ("Repère 4", KW(P("acces"), forbid="switch"), "Point d'accès Wi-Fi")],
                "<p>La box réunit un <strong>modem</strong> (le lien avec le réseau du fournisseur d'accès), un "
                "<strong>routeur</strong> (la passerelle vers Internet), un <strong>switch</strong> (les prises "
                "Ethernet, ses ports dessinés au repère 3) et un <strong>point d'accès Wi-Fi</strong> (les liaisons "
                "sans fil, les ondes du repère 4).</p>",
                etiquettes=E_BOX, liste="Appareils", reperes=["1", "2", "3", "4"]),
            GRP("Indique le type de chaque liaison repérée 5 à 8.", "Lis le dossier DP1.", [
                    ("Repère 5 — box et Internet", KW(P("fibre")), "Fibre optique"),
                    ("Repère 6 — ordinateur fixe", KW(P("ethernet|cable"), forbid="fibre"), "Câble Ethernet"),
                    ("Repère 7 — ordinateur portable", KW(P("wi", "fi"), P("wifi")), "Wi-Fi"),
                    ("Repère 8 — console de jeux", KW(P("ethernet|cable"), forbid="fibre"), "Câble Ethernet")],
                "<p>La box est raccordée à Internet par la <strong>fibre optique</strong> ; l'ordinateur fixe et la "
                "console sont branchés au switch par un <strong>câble Ethernet</strong> (liaison filaire) ; "
                "l'ordinateur portable passe par le point d'accès, en <strong>Wi-Fi</strong>.</p>",
                etiquettes=E_LIAISONS, liste="Liaisons", reperes=["5", "6", "7", "8"]),
            qcm.QCM("Quelle est la topologie physique du réseau de la maison ?",
                    [("A", "En étoile"), ("B", "En bus"), ("C", "En anneau"), ("D", "Maillée")], ["A"],
                    "Tous les appareils sont reliés à un nœud central, la box : c'est une étoile, la topologie de la "
                    "plupart des réseaux locaux."),
        ]},
        {"title": "Le tableau d'adressage", "minutes": 12, "intro": [
            "<p>Le masque de sous-réseau de la maison est <b>255.255.255.0</b>.</p>"], "blocks": [
            QBAR(["DP1", "DT1"]),
            GRP("Découpe les adresses de l'ordinateur fixe et du téléphone.",
                "Écris seulement les nombres, séparés par des points.", [
                    ("net-ID de l'ordinateur fixe", IP("192.168.1"), "192.168.1"),
                    ("host-ID de l'ordinateur fixe", IP("10"), "10"),
                    ("host-ID du téléphone", IP("31"), "31")],
                "<p>Le masque 255.255.255.0 garde les trois premiers nombres pour le net-ID : "
                + g.calc("192.168.1.10 → net-ID 192.168.1, host-ID 10 ; 192.168.1.31 → host-ID 31") + "</p>"
                "<p>Tous les appareils de la maison ont le même net-ID, 192.168.1 : seul le host-ID change.</p>"),
            Q("Quelle adresse IP la box utilise-t-elle à l'intérieur du réseau local ?",
              "Écris l'adresse seule, en notation pointée.", IP(BOX), BOX,
              "<p>C'est l'adresse privée du routeur de la box, la passerelle des appareils de la maison (DP1).</p>"),
            Q("Avec quelle adresse IP tous les appareils de la maison sont-ils vus sur Internet ?",
              "Écris l'adresse seule, en notation pointée.", IP(PUBLIQUE), PUBLIQUE,
              "<p>Sur Internet, les appareils sont vus avec l'adresse publique de leur routeur passerelle, la box : "
              f"{PUBLIQUE}. Ils ont tous la même adresse publique.</p>"),
            GRP("Classe chaque adresse : privée ou publique.", "Les plages réservées aux LAN sont rappelées dans DT1.", [
                    ("192.168.1.31", KW(P("privee")), "Adresse privée"),
                    (PUBLIQUE, KW(P("publique")), "Adresse publique"),
                    ("10.0.0.8", KW(P("privee")), "Adresse privée"),
                    ("172.30.1.2", KW(P("privee")), "Adresse privée"),
                    ("172.40.1.2", KW(P("publique")), "Adresse publique")],
                "<p>Sont privées les adresses de 10.0.0.0 à 10.255.255.255, de 172.16.0.0 à 172.31.255.255 et de "
                "192.168.0.0 à 192.168.255.255. 172.40.1.2 n'est pas dans la deuxième plage (40 dépasse 31) : elle est "
                "publique.</p>", etiquettes=E_ADRESSES),
        ]},
        {"title": "Des adresses à choisir", "minutes": 12, "blocks": [
            QBAR(["DP1", "DT1"]),
            Q("Avec le masque 255.255.255.0, combien de machines peut-on connecter, au plus, au réseau de la maison ?",
              "Un nombre.", NUM(254), "254",
              "<p>Le host-ID tient sur un seul nombre : 256 valeurs, dont deux réservées (l'adresse du réseau et "
              "celle de diffusion), soit " + g.calc("256 − 2 = 254") + " machines, box comprise.</p>"),
            Q("Un nouvel appareil reçoit l'adresse qui suit celle du téléphone. Quelle est cette adresse ?",
              "Écris l'adresse seule, en notation pointée.", IP("192.168.1.32"), "192.168.1.32",
              "<p>Le net-ID reste 192.168.1 ; le host-ID suit celui du téléphone : 31 + 1 = 32.</p>"),
            qcm.QCM("La tablette a été réglée à la main avec l'adresse 192.168.2.50 et le masque 255.255.255.0. "
                    "Que se passe-t-il ?",
                    [(1, "Elle ne peut pas communiquer avec les autres appareils de la maison"),
                     (2, "Son net-ID, 192.168.2, n'est pas celui du réseau, 192.168.1"),
                     (3, "Il faut la brancher par un câble"),
                     (4, "Elle est vue sur Internet avec l'adresse 192.168.2.50")], [1, 2],
                    "Dans un LAN, deux machines ne communiquent que si elles ont le même net-ID : celui de la tablette "
                    "est 192.168.2. Le câblage n'y change rien, et une adresse privée n'est jamais vue sur Internet."),
            Q("Corrige l'adresse de la tablette en ne changeant qu'un seul des quatre nombres.",
              "Écris l'adresse seule, en notation pointée.", IP("192.168.1.50"), "192.168.1.50",
              "<p>On remet le net-ID du réseau, 192.168.1, en gardant le host-ID 50, libre : 192.168.1.50.</p>"),
            qcm.QCM("Si la box utilisait le masque 255.255.0.0, combien de machines pourrait-on connecter ?",
                    [("A", "254"), ("B", "65 534"), ("C", "16 777 214")], ["B"],
                    "Avec 255.255.0.0, le host-ID compte deux nombres : 65 534 machines."),
        ]},
        {"title": "Le débit de la connexion", "minutes": 11, "blocks": [
            QBAR(["DP1", "DT1"]),
            Q("La console télécharge un jeu de 50 Go par son câble Ethernet, à 1 Gbit/s. Quelle est la durée du "
              "téléchargement ?", "Donne la durée en secondes, avec son unité.", NUM(400, 0.5, "s", S), "400 s",
              "<p>Quantité : 50 Go = 50 × 8 = 400 Gbit. Durée = quantité / débit : "
              + g.calc("400 Gbit ÷ 1 Gbit/s = 400 s") + ", soit 6 min 40 s.</p>"),
            Q("Le même jeu est téléchargé par l'ordinateur portable, en Wi-Fi, à 300 Mbit/s. Quelle est la durée ?",
              "En secondes, avec son unité, arrondie à la seconde.", NUM(1333, 1.5, "s", S), "1 333 s",
              "<p>300 Mbit/s = 0,3 Gbit/s : " + g.calc("400 Gbit ÷ 0,3 Gbit/s ≈ 1 333 s") + ", soit environ "
              "22 min 13 s.</p>"),
            Q("Un fichier de 12 Mo est transmis en 2 s. Quel est le débit de la transmission ?",
              "En Mbit/s, avec son unité.", NUM(48, 0.05, "Mbit/s", MBITS), "48 Mbit/s",
              "<p>12 Mo = 12 × 8 = 96 Mbit ; " + g.calc("96 Mbit ÷ 2 s = 48 Mbit/s") + " (6 Mo/s).</p>"),
            qcm.QCM("Pourquoi l'ordinateur portable télécharge-t-il plus lentement que la console ?",
                    [("A", "Le Wi-Fi a un débit plus faible que le câble Ethernet"),
                     ("B", "Son adresse IP est privée"), ("C", "Il est plus loin d'Internet que la console")], ["A"],
                    "Les deux passent par la même fibre ; la différence vient de la dernière liaison : environ "
                    "300 Mbit/s en Wi-Fi, 1 Gbit/s par câble. Les deux adresses sont privées."),
        ]},
    ]


def exercice(g):
    return {"key": "adressage-maison", "prefix": "a", "tag": "Exercice 1.3", "level": "Niveau 1",
            "title": "Le plan d'adressage de la maison", "parts": parties(g),
            "docs": [g.DOC("DP1", "Le réseau de la maison", DP1), g.DOC("DT1", "Adresses IP, masques et débit", DT1)],
            "consignes": g.consignes(g.C_SCHEMA, g.C_ETIQUETTES, g.C_SAISIE, g.C_GROUPE, qcm.C_QCM, g.C_DOCUMENTS),
            "hero": ("carte-ex13", "Le réseau d'une maison : la box et les appareils qui lui sont reliés",
                     "Une box, six appareils, leurs adresses IP."),
            "mots": ["Box", "Adresses IP", "Masque", "Débit"], "vign": "carte-ex13", "css": AD_CSS,
            "valt": "Le schéma du réseau d'une maison",
            "sub": "Le réseau d'une maison, de la box aux appareils : compléter son schéma, découper les adresses avec "
                   "le masque, distinguer adresses privées et publiques, choisir des adresses, calculer des durées de "
                   "téléchargement."}
