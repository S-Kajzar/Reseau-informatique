"""Cours 1 — Réseaux informatiques : de la liaison point-à-point au modèle OSI (Niveau 1).

Source : le cours Word « Séquence 5 — Réseaux informatiques » (environ 2 h). Son texte est repris section par
section (liaison point-à-point, mise en réseau, WAN et Internet, adressage IP et LAN, communication entre logiciels,
modèle OSI) ; ses figures, des captures de manuel, ne sont pas reprises telles quelles : toutes sont redessinées en
SVG et rendues interactives — liaison full ou half-duplex, supports filaires, portée du Wi-Fi et du Bluetooth,
simulateur de débit, switch qui aiguille les trames d'après l'adresse MAC, topologies dont on coupe les liaisons,
adresse MAC octet par octet, deux réseaux locaux reliés par leurs routeurs, contenu d'une box, routage dans un
maillage de routeurs, dorsales intercontinentales, découpage d'une adresse IP par le masque, adresses privée et
publique, sous-réseaux logiques, requête et réponse HTTP, segments et accusés de réception TCP, modèle OSI,
encapsulation, parcours d'un message à travers les couches. Corrections et décisions : NOTE-DE-LIVRAISON.md.

cours(g) reçoit le module generer (en-tête, sections, jeux, quiz) : pas d'import circulaire.
Classes et identifiants propres au cours : préfixe « cr- ».
"""
import html
import json
import math

ENCRE, BLEU, ORANGE, VERT, ROUGE, JAUNE = "#1C2530", "#1F5FA8", "#B26A00", "#1B7A43", "#B42318", "#F2B705"
GRIS, ECRAN, CIEL = "#46525C", "#4F8FDB", "#9DB6D6"

OBJECTIFS = [
    "Caractériser une liaison point-à-point : support, protocole, mode (full/half-duplex) et débit.",
    "Identifier les dispositifs d'interconnexion et les topologies physiques d'un réseau local (LAN).",
    "Distinguer adresse MAC et adresse IP ; découper une adresse IP à l'aide d'un masque de sous-réseau.",
    "Expliquer le modèle client-serveur, le routage et l'organisation en couches du modèle OSI.",
]
PREREQUIS = ["Unités de quantité d'information : bit et octet.", "Numération binaire et hexadécimale (notions)."]

# adresses MAC des quatre machines du switch (figure 4) : PC1 et PC2 viennent du même fabricant (mêmes trois
# premiers octets) ; le premier octet est multiple de 4 (adresse individuelle, attribuée par le fabricant)
MACS = ["10-4F-DE-A5-65-89", "10-4F-DE-D5-44-8B", "50-40-DE-C5-44-8B", "F0-40-A7-15-4E-80"]

CARTES = [
    ("bleu", "LIAISON POINT-À-POINT", "Liaison directe entre deux cartes-réseau : un support (cuivre, fibre, air) et "
     "un protocole (Ethernet, Wi-Fi, Bluetooth).", "Full-duplex : les deux sens en même temps. Débit = quantité de "
     "données / durée."),
    ("bleu", "RÉSEAU LOCAL (LAN)", "Machines reliées par des switchs (filaire) et des points d'accès (sans fil).",
     "Topologie la plus courante : l'étoile. Adresse MAC : physique, 6 couples hexadécimaux."),
    ("orange", "WAN ET INTERNET", "Des LAN reliés entre eux par des routeurs passerelles ; Internet est le principal "
     "WAN.", "Structure maillée : les routeurs choisissent la route des paquets (routage)."),
    ("orange", "ADRESSE IP", "Adresse logique, routable : 4 nombres de 0 à 255. Le masque la découpe en net-ID "
     "(réseau) et host-ID (machine).", "Adresse privée dans le LAN, adresse publique du routeur sur Internet."),
    ("vert", "CLIENT-SERVEUR", "Le client envoie des requêtes, le serveur renvoie des réponses (HTTP pour le Web).",
     "TCP segmente les messages, fait acquitter chaque segment et détecte les erreurs."),
    ("vert", "MODÈLE OSI", "Sept couches, de la couche physique (bits) à la couche application (requêtes, "
     "réponses).", "Chaque couche encapsule le message en lui ajoutant un en-tête."),
]

ADRESSES = [("mac", "Adresse MAC"), ("ip", "Adresse IP")]
JEU_ADRESSES = [("Gravée sur la carte-réseau par le fabricant", "mac"), ("Peut être changée à tout moment", "ip"),
                ("Lue par les switchs et les points d'accès", "mac"), ("Lue par les routeurs", "ip"),
                ("Six couples de chiffres hexadécimaux", "mac"), ("Quatre nombres décimaux de 0 à 255", "ip"),
                ("Adresse physique de la machine", "mac"), ("Adresse logique, routable", "ip")]
COUCHES = [("1", "1 · Physique"), ("2", "2 · Liaison"), ("3", "3 · Réseau"), ("4", "4 · Transport"),
           ("app", "5 à 7 · Applications")]
JEU_COUCHES = [("La transmission des bits sur la fibre optique", "1"), ("L'adresse MAC", "2"),
               ("L'aiguillage des trames par le switch", "2"), ("L'adresse IP", "3"),
               ("Le routage des paquets par les routeurs", "3"), ("La segmentation des messages (TCP)", "4"),
               ("Les accusés de réception (TCP)", "4"), ("Les requêtes et réponses HTTP", "app")]

QUIZ = [
    ("Une liaison où les données circulent dans les deux sens en même temps est…",
     ["half-duplex", "full-duplex", "point-à-multipoint"], 1,
     "Full-duplex : les deux sens en même temps, comme une conversation téléphonique ; half-duplex : un sens à la "
     "fois, comme un talkie-walkie."),
    ("Un fichier de 40 Mo est transmis en 8 s. Le débit est de…", ["5 Mo/s", "320 Mo/s", "0,2 Mo/s"], 0,
     "Débit = quantité de données / durée = 40 Mo / 8 s = 5 Mo/s, soit 40 Mbit/s."),
    ("Quel dispositif interconnecte des liaisons filaires dans un LAN ?",
     ["Le switch", "Le point d'accès sans fil", "Le modem"], 0,
     "Le commutateur (switch) relie des liaisons filaires ; le point d'accès relie des liaisons sans fil."),
    ("La topologie de la plupart des réseaux locaux actuels est…", ["en bus", "en anneau", "en étoile"], 2,
     "Le réseau de la maison est centré sur la box, celui d'un établissement sur des switchs : c'est une étoile."),
    ("Une adresse MAC…", ["est gravée sur la carte-réseau", "change à chaque connexion", "s'écrit avec 4 nombres de "
                          "0 à 255"], 0,
     "C'est l'adresse physique de la carte : 6 couples de chiffres hexadécimaux, attribués par le fabricant."),
    ("Quel matériel relie un LAN au WAN ?", ["Le switch", "Le routeur passerelle", "La carte-réseau"], 1,
     "Le routeur sert de passerelle : il fait passer les trames du LAN vers le WAN, et inversement."),
    ("Avec le masque 255.255.0.0, le net-ID de l'adresse 82.162.240.19 est…", ["82", "82.162", "82.162.240"], 1,
     "Les deux nombres situés au-dessus des 255 du masque forment le net-ID : 82.162 ; le host-ID est 240.19."),
    ("Laquelle de ces adresses est une adresse IP privée ?", ["8.8.8.8", "92.169.148.17", "192.168.1.10"], 2,
     "Les adresses de 192.168.0.0 à 192.168.255.255 sont réservées aux réseaux locaux."),
    ("Dans le modèle client-serveur, le navigateur Web…", ["envoie des réponses", "envoie des requêtes",
                                                         "stocke les pages du site"], 1,
     "Le navigateur est le client : il envoie une requête HTTP ; le serveur renvoie la réponse (le code HTML et CSS)."),
    ("Un routeur met en œuvre les couches…", ["1 et 2", "1 à 3", "1 à 7"], 1,
     "Il lit l'adresse IP (couche 3, réseau) pour router les paquets ; les switchs s'arrêtent à la couche 2."),
]


def e(s):
    return html.escape(s, quote=True)


# ============================================================ pictogrammes SVG
def pc(x, y, nom="", sous="", cls="", ident="", sous_cls="cr-ts"):
    """Poste fixe ; (x, y) : coin haut gauche de l'écran (56 × 40), nom et adresse dessous."""
    i = f' id="{ident}"' if ident else ""
    return (f'<g class="cr-pc {cls}"{i} transform="translate({x} {y})">'
            f'<rect width="56" height="40" rx="4" fill="{ENCRE}"/><rect class="cr-ecran" x="4" y="4" width="48" '
            f'height="30" rx="1" fill="{ECRAN}"/><rect x="24" y="40" width="8" height="7" fill="{GRIS}"/>'
            f'<rect x="14" y="47" width="28" height="4" rx="2" fill="{GRIS}"/>'
            + (f'<text x="28" y="67" text-anchor="middle" class="cr-t">{nom}</text>' if nom else "")
            + (f'<text x="28" y="82" text-anchor="middle" class="{sous_cls}">{sous}</text>' if sous else "") + "</g>")


def portable(x, y, nom="", sous="", cls="", ident=""):
    """Ordinateur portable ; (x, y) : coin haut gauche de l'écran (54 × 36)."""
    i = f' id="{ident}"' if ident else ""
    return (f'<g class="cr-pc {cls}"{i} transform="translate({x} {y})">'
            f'<rect width="54" height="36" rx="4" fill="{ENCRE}"/><rect class="cr-ecran" x="4" y="4" width="46" '
            f'height="28" rx="1" fill="{ECRAN}"/><path d="M-6 36H60l6 8H-12z" fill="#A5ADAA" stroke="#7D868F"/>'
            + (f'<text x="27" y="60" text-anchor="middle" class="cr-t">{nom}</text>' if nom else "")
            + (f'<text x="27" y="75" text-anchor="middle" class="cr-ts">{sous}</text>' if sous else "") + "</g>")


def switch(x, y, w=110, ports=4, nom="Switch", ident=""):
    i = f' id="{ident}"' if ident else ""
    pas = (w - 20) / ports
    p = "".join(f'<rect class="cr-port" x="{10 + k * pas + pas / 2 - 7:.1f}" y="13" width="14" height="10" rx="1.5" '
                f'fill="#0E1114" stroke="#7D868F" stroke-width=".8"/>' for k in range(ports))
    return (f'<g class="cr-sw"{i} transform="translate({x} {y})"><rect width="{w}" height="32" rx="5" fill="{ENCRE}"/>'
            f'{p}<circle cx="{w - 8}" cy="7" r="2.6" fill="#5BD08A"/>'
            + (f'<text x="{w / 2}" y="48" text-anchor="middle" class="cr-t">{nom}</text>' if nom else "") + "</g>")


def routeur(x, y, nom="", sous="", ident="", cls=""):
    """Routeur (cylindre et ses quatre flèches) ; (x, y) : centre du disque supérieur."""
    i = f' id="{ident}"' if ident else ""
    fl = ('<path d="M-17 -1l9 0m-3 -3l3 3l-3 3M17 1l-9 0m3 3l-3-3l3-3M-2 -7l4 0M-2 7l4 0" stroke="#FFFFFF" '
          'stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    return (f'<g class="cr-rt {cls}"{i} transform="translate({x} {y})">'
            f'<path d="M-28 0v14a28 9 0 0 0 56 0V0" fill="#2E5E8E"/><ellipse rx="28" ry="9" fill="#3D7BB8"/>{fl}'
            + (f'<text y="40" text-anchor="middle" class="cr-t">{nom}</text>' if nom else "")
            + (f'<text y="55" text-anchor="middle" class="cr-ts">{sous}</text>' if sous else "") + "</g>")


def serveur(x, y, nom="", ident=""):
    i = f' id="{ident}"' if ident else ""
    return (f'<g class="cr-srv"{i} transform="translate({x} {y})"><rect width="40" height="62" rx="5" fill="{GRIS}"/>'
            '<g fill="#1C2530"><rect x="6" y="8" width="28" height="9" rx="2"/><rect x="6" y="21" width="28" height="9" '
            'rx="2"/><rect x="6" y="34" width="28" height="9" rx="2"/></g><g fill="#5BD08A"><circle cx="29" cy="12.5" '
            'r="2"/><circle cx="29" cy="25.5" r="2"/><circle cx="29" cy="38.5" r="2"/></g>'
            + (f'<text x="20" y="80" text-anchor="middle" class="cr-t">{nom}</text>' if nom else "") + "</g>")


def nuage(cx, cy, s=1.0, texte="Internet"):
    return (f'<g transform="translate({cx} {cy}) scale({s})"><path d="M-62 30c-30 0-34-40-8-46c-4-30 38-44 56-20'
            'c12-30 66-26 72 8c28 0 36 38 10 52z" fill="#FFFFFF" stroke="#9DB6D6" stroke-width="2.5"/>'
            f'<text y="12" text-anchor="middle" class="cr-tb" fill="{BLEU}">{texte}</text></g>')


def fig(ident, svg, caption, avant="", apres="", cls=""):
    """Figure du cours : commandes (avant), dessin, légende, puis texte qui suit l'animation (apres)."""
    return (f'<figure class="cr-fig {cls}" id="{ident}">{avant}{svg}<figcaption>{caption}</figcaption>{apres}'
            "</figure>")


def svg(w, h, corps, aria, ident="", cls="cr-svg"):
    i = f' id="{ident}"' if ident else ""
    return f'<svg class="{cls}"{i} viewBox="0 0 {w} {h}" role="img" aria-label="{e(aria)}">{corps}</svg>'


def boutons(groupe, items, actif=None, label=""):
    """Groupe de boutons à bascule : items = [(valeur, texte)]."""
    return (f'<div class="cr-ctrl" role="group" aria-label="{e(label)}">' + "".join(
        f'<button type="button" class="btn ghost" data-{groupe}="{v}" aria-pressed="{"true" if v == actif else "false"}">'
        f"{t}</button>" for v, t in items) + "</div>")


def options(n, choisi, prefixe="PC"):
    return "".join(f'<option value="{i}"{" selected" if i == choisi else ""}>{prefixe}{i}</option>' for i in range(1, n + 1))


def cap(ident, texte=""):
    return f'<p class="cr-cap" id="{ident}" aria-live="polite">{texte}</p>'


# ============================================================ 1. liaison point-à-point
def figure_duplex():
    corps = (pc(40, 42, "Machine A") + pc(664, 42, "Machine B")
             + f'<line x1="100" y1="72" x2="660" y2="72" stroke="{CIEL}" stroke-width="34" stroke-linecap="round" '
             'opacity=".45"/><line class="cr-dx-ab" x1="112" y1="64" x2="648" y2="64"/>'
             '<line class="cr-dx-ba" x1="648" y1="80" x2="112" y2="80"/>'
             '<text id="cr-dx-lab" x="380" y="122" text-anchor="middle" class="cr-tb"></text>')
    return fig("cr-duplex", svg(760, 140, corps, "Deux machines reliées par une liaison point-à-point ; les données "
                                 "circulent dans les deux sens"),
               "Figure 1 — Une liaison point-à-point entre deux machines. Choisis le mode : en <i>full-duplex</i>, les "
               "deux sens en même temps ; en <i>half-duplex</i>, un sens à la fois.",
               avant=boutons("dx", [("full", "Full-duplex"), ("half", "Half-duplex")], "full", "Mode de la liaison"),
               apres=cap("cr-dx-t"))


def _paire(y, c1, c2, x0=470, x1=740, ph=0):
    """Une paire torsadée : deux conducteurs enroulés en hélice (deux sinusoïdes en opposition)."""
    def onde(sgn):
        pts = []
        for k in range(0, int((x1 - x0) / 3) + 1):
            x = x0 + 3 * k
            pts.append(f"{x:.0f} {y + sgn * 5 * math.sin((x - x0) / 7 + ph):.1f}")
        return "M" + " L".join(pts)
    return (f'<path d="{onde(1)}" stroke="{c1}" stroke-width="5" fill="none" stroke-linecap="round"/>'
            f'<path d="{onde(-1)}" stroke="{c2}" stroke-width="5" fill="none" stroke-linecap="round"/>')


def _repere(x, y, lettre, cle, x2, y2):
    return (f'<g class="cr-rep" data-part="{cle}"><line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{ROUGE}" '
            f'stroke-width="2"/><circle cx="{x}" cy="{y}" r="11" fill="{ROUGE}"/><text x="{x}" y="{y + 4.5}" '
            f'text-anchor="middle" class="cr-tw">{lettre}</text></g>')


def figure_supports():
    defs = ('<defs><pattern id="cr-tresse" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            '<rect width="8" height="8" fill="#C9874A"/><path d="M0 4H8M4 0V8" stroke="#8A5523" stroke-width="1.6"/>'
            '</pattern><clipPath id="cr-clip-sig"><rect x="20" y="146" width="720" height="40"/></clipPath>'
            '<clipPath id="cr-clip-loupe"><circle cx="640" cy="92" r="74"/></clipPath></defs>')
    carre = "M-40 176" + "".join(f"h20v-22h20v22" for _ in range(22))
    cuivre = (defs
              + '<g class="cr-part" data-part="gaine"><rect x="20" y="70" width="370" height="46" rx="23" fill="#4BA3D9"/>'
              '<rect x="30" y="76" width="350" height="8" rx="4" fill="#FFFFFF" opacity=".35"/></g>'
              '<g class="cr-part" data-part="blindage"><rect x="372" y="75" width="110" height="36" rx="6" '
              'fill="url(#cr-tresse)"/></g>'
              '<g class="cr-part" data-part="paires">'
              + _paire(58, "#E07B1F", "#F4F5F2", ph=0) + _paire(82, "#2E9E4F", "#F4F5F2", ph=1)
              + _paire(106, "#2D6FC2", "#F4F5F2", ph=2) + _paire(130, "#7A4A21", "#F4F5F2", ph=3) + "</g>"
              + _repere(70, 38, "a", "gaine", 90, 70) + _repere(430, 38, "b", "blindage", 430, 75)
              + _repere(700, 30, "c", "paires", 690, 52)
              + f'<g clip-path="url(#cr-clip-sig)"><g class="cr-sig-el"><path d="{carre}" stroke="{BLEU}" stroke-width="3" '
              'fill="none"/></g></g><text x="24" y="143" class="cr-ts">signal électrique (tensions qui changent au rythme '
              'des bits)</text>')
    fibre = (defs
             + '<g class="cr-part" data-part="fgaine"><rect x="20" y="70" width="270" height="44" rx="22" fill="#2E9E4F"/>'
             '<text x="150" y="98" text-anchor="middle" class="cr-tw">FIBRE OPTIQUE</text></g>'
             '<g class="cr-part" data-part="renfort">' + "".join(
                 f'<path d="M270 {76 + 4 * k}q30 {(-1) ** k * 4} 70 {(-1) ** k * 2}" stroke="#E8C84A" stroke-width="2" '
                 'fill="none"/>' for k in range(9)) + "</g>"
             '<g class="cr-part" data-part="interieure"><rect x="320" y="82" width="120" height="20" rx="10" '
             'fill="#E07B1F"/></g>'
             '<g class="cr-part" data-part="verre"><rect x="430" y="88" width="120" height="8" rx="4" fill="#D9EEF7" '
             'stroke="#7FB6CF"/></g>'
             f'<line x1="550" y1="92" x2="572" y2="92" stroke="{CIEL}" stroke-dasharray="3 3"/>'
             '<circle cx="640" cy="92" r="76" fill="#FFFFFF" stroke="#7FB6CF" stroke-width="3"/>'
             '<g clip-path="url(#cr-clip-loupe)"><rect x="560" y="58" width="160" height="68" fill="#BFE3F2"/>'
             '<rect x="560" y="72" width="160" height="40" fill="#E9F6FB"/>'
             '<path class="cr-rayon" d="M560 108L590 76L620 108L650 76L680 108L710 76L740 108" stroke="#F2B705" '
             'stroke-width="4" fill="none"/></g>'
             '<text x="640" y="190" text-anchor="middle" class="cr-ts">vue agrandie du cœur : la lumière s\'y réfléchit</text>'
             + _repere(490, 38, "a", "verre", 490, 88) + _repere(380, 38, "b", "interieure", 380, 82)
             + _repere(305, 38, "c", "renfort", 305, 74) + _repere(150, 38, "d", "fgaine", 150, 70))
    legende_c = [("gaine", "a", "Gaine extérieure en plastique"), ("blindage", "b", "Blindage en cuivre"),
                 ("paires", "c", "Paires torsadées : conducteurs enroulés en hélice deux par deux")]
    legende_f = [("verre", "a", "Fibre de verre : la lumière y est guidée par réflexions successives"),
                 ("interieure", "b", "Gaine intérieure : elle protège la fibre"),
                 ("renfort", "c", "Décharge de traction : fibres de renfort qui encaissent les efforts"),
                 ("fgaine", "d", "Gaine extérieure")]

    def legende(items):
        return '<ul class="cr-leg">' + "".join(
            f'<li><button type="button" class="cr-leg-b" data-part="{k}"><b>{l}</b> {t}</button></li>'
            for k, l, t in items) + "</ul>"
    panes = (f'<div class="cr-pane" data-pane="cuivre">{svg(760, 196, cuivre, "Câble en cuivre à paires torsadées : gaine, blindage, quatre paires ; signal électrique")}'
             f'{legende(legende_c)}</div>'
             f'<div class="cr-pane" data-pane="fibre" hidden>{svg(760, 200, fibre, "Fibre optique : gaine extérieure, fibres de renfort, gaine intérieure, fibre de verre ; la lumière se réfléchit dans le cœur")}'
             f'{legende(legende_f)}</div>')
    return fig("cr-supports", panes, "Figure 2 — Les deux supports filaires. Touche un repère ou une ligne de la légende "
               "pour montrer la partie du câble.",
               avant=boutons("sup", [("cuivre", "Câble en cuivre à paires torsadées"), ("fibre", "Fibre optique")],
                             "cuivre", "Support"))


def figure_portee():
    x0, k = 90, 12.6  # 0 m à x0, k pixels par mètre (jusqu'à 50 m)
    graduations = "".join(
        f'<line x1="{x0 + k * m}" y1="150" x2="{x0 + k * m}" y2="156" stroke="{GRIS}"/><text x="{x0 + k * m}" y="170" '
        f'text-anchor="middle" class="cr-ts">{m} m</text>' for m in range(0, 51, 10))
    corps = (f'<g transform="translate(26 72)"><rect width="40" height="58" rx="7" fill="{ENCRE}"/><rect x="4" y="7" '
             f'width="32" height="42" rx="2" fill="{ECRAN}"/></g>'
             '<g class="cr-ondes"><path d="M74 88a18 18 0 0 1 0 26M80 80a28 28 0 0 1 0 42M86 72a38 38 0 0 1 0 58" '
             f'stroke="{VERT}" stroke-width="3" fill="none"/></g>'
             f'<rect x="{x0}" y="62" width="{k * 10}" height="26" rx="4" fill="#E2F1E7" stroke="{VERT}"/>'
             f'<text x="{x0 + 8}" y="80" class="cr-t" fill="{VERT}">Bluetooth</text>'
             f'<rect x="{x0}" y="100" width="{k * 40}" height="26" rx="4" fill="#E6EEF8" stroke="{BLEU}"/>'
             f'<text x="{x0 + 8}" y="118" class="cr-t" fill="{BLEU}">Wi-Fi</text>'
             f'<line x1="{x0}" y1="150" x2="{x0 + k * 50}" y2="150" stroke="{GRIS}" stroke-width="1.5"/>{graduations}'
             '<g id="cr-pt-app" transform="translate(240 40)"><line x1="0" y1="10" x2="0" y2="110" stroke="#B42318" '
             'stroke-dasharray="4 3"/><path d="M-22 0h44v26h-44z" fill="#1C2530"/><rect x="-18" y="4" width="36" '
             'height="18" fill="#4F8FDB"/><path d="M-27 26h54l5 6h-64z" fill="#A5ADAA"/></g>')
    ctrl = ('<div class="cr-ctrl"><label for="cr-portee">Distance de l\'ordinateur : <output id="cr-portee-o">12 m'
            '</output></label><input type="range" id="cr-portee" min="1" max="50" value="12"></div>')
    return fig("cr-portee-f", svg(760, 180, corps, "Portées comparées du Bluetooth et du Wi-Fi"),
               "Figure 3 — Portée du Bluetooth et du Wi-Fi (ordres de grandeur, à l'intérieur d'une maison). Déplace "
               "l'ordinateur.", avant=ctrl, apres=cap("cr-portee-t"))


FICHIERS = [("photo", "Une photo", 4, "Mo"), ("musique", "Un morceau de musique", 8, "Mo"),
            ("video", "Une vidéo de 10 minutes", 500, "Mo"), ("film", "Un film en haute définition", 4, "Go")]
LIAISONS_D = [("bt", "Bluetooth (≈ 2 Mbit/s)", 2e6), ("wifi", "Wi-Fi (≈ 300 Mbit/s)", 300e6),
              ("eth", "Ethernet, câble en cuivre (1 Gbit/s)", 1e9), ("fo", "Fibre optique (10 Gbit/s)", 10e9)]


def simu_debit():
    f_opts = "".join(f'<option value="{k}" data-q="{q}" data-u="{u}">{t} ({q} {u})</option>' for k, t, q, u in FICHIERS)
    l_opts = "".join(f'<option value="{k}" data-d="{d:.0f}"{" selected" if k == "wifi" else ""}>{t}</option>'
                     for k, t, d in LIAISONS_D)
    return ('<div class="simu" id="cr-debit"><h3>Simulateur : combien de temps pour transférer un fichier ?</h3>'
            '<div class="simu-grid"><label>Fichier<select id="cr-deb-f">' + f_opts + '</select></label>'
            '<label>Liaison<select id="cr-deb-l">' + l_opts + '</select></label></div>'
            '<div class="simu-out"><div><span>Quantité de données</span><b id="cr-deb-q"></b></div>'
            '<div><span>Débit</span><b id="cr-deb-d"></b></div><div><span>Durée de transmission</span>'
            '<b id="cr-deb-t"></b></div></div>'
            '<p class="cr-calc" id="cr-deb-calc"></p>'
            '<div class="cr-barre" role="progressbar" aria-label="Transfert" aria-valuemin="0" aria-valuemax="100" '
            'aria-valuenow="0"><span id="cr-deb-bar"></span></div>'
            '<p class="cr-ctrl"><button type="button" class="btn" id="cr-deb-go">Lancer le transfert</button> '
            '<span class="small" id="cr-deb-note"></span></p>'
            '<details class="simu-defi"><summary>Défi : un fichier de 20 Mo est transmis en 4 s. Quel est le débit, en '
            'Mo/s puis en Mbit/s ?</summary><p>Débit = 20 Mo / 4 s = <b>5 Mo/s</b> ; un octet vaut 8 bits : 5 × 8 = '
            '<b>40 Mbit/s</b>.</p></details></div>')


# ============================================================ 2. mise en réseau
POS_SW = [(40, 30), (40, 190), (664, 190), (664, 30)]  # PC1 haut gauche, PC2 bas gauche, PC3 bas droite, PC4 haut droite


def figure_switch():
    sx, sy = 325, 128
    ports = [sx + 10 + k * 22.5 + 11.25 for k in range(4)]
    cables, machines = [], []
    for i, ((x, y), mac) in enumerate(zip(POS_SW, MACS)):
        px = ports[i]
        cx, cy = x + 28, y + 24
        d = (f"M{cx} {cy}H{px}V{sy}" if y < sy else f"M{cx} {cy}H{px}V{sy + 32}")
        cables.append(f'<path class="cr-cable" id="cr-swc-{i + 1}" d="{d}" data-pts="{cx},{cy} {px},{cy} {px},{sy + (0 if y < sy else 32)}"/>')
        machines.append(portable(x, y, f"PC{i + 1}", mac, ident=f"cr-swp-{i + 1}"))
    port_num = "".join(f'<text x="{px + 5}" y="{sy - 6 if i in (0, 3) else sy + 46}" class="cr-ts">{i + 1}</text>'
                       for i, px in enumerate(ports))
    corps = ("".join(cables) + switch(sx, sy, 110, 4, "", "cr-sw-sw") + port_num
             + '<text x="380" y="98" text-anchor="middle" class="cr-tb">Switch</text>'
             '<text x="380" y="114" text-anchor="middle" class="cr-ts">ports 1 à 4</text>' + "".join(machines)
             + '<g id="cr-sw-trame" class="cr-jeton" opacity="0"><rect x="-46" y="-13" width="92" height="26" rx="5"/>'
             '<text y="5" text-anchor="middle" class="cr-tj">trame</text></g>')
    table = ('<table class="t cr-swtab" id="cr-sw-tab"><caption>Table du switch</caption><thead><tr><th>Port</th>'
             '<th>Adresse MAC de la machine branchée</th></tr></thead><tbody>' + "".join(
                 f'<tr data-port="{i + 1}"><td>{i + 1}</td><td><code>{m}</code></td></tr>' for i, m in enumerate(MACS))
             + "</tbody></table>")
    ctrl = (f'<div class="cr-ctrl"><label>Émetteur <select id="cr-sw-de">{options(4, 1)}</select></label>'
            f'<label>Destinataire <select id="cr-sw-a">{options(4, 4)}</select></label>'
            '<button type="button" class="btn" id="cr-sw-go">Envoyer une trame</button></div>')
    return fig("cr-switch", '<div class="cr-sw-grid">' + svg(760, 290, corps, "Quatre ordinateurs reliés aux ports "
                                                                            "d'un switch, avec leurs adresses MAC")
               + table + "</div>",
               "Figure 4 — Quatre machines reliées par un switch. Choisis l'émetteur et le destinataire : le switch lit "
               "l'adresse MAC du destinataire inscrite dans la trame et ne l'envoie que vers le bon port.",
               avant=ctrl, apres=cap("cr-sw-t", "Choisis deux machines, puis envoie une trame."))


TOPOS = [("etoile", "Étoile"), ("anneau", "Anneau"), ("bus", "Bus"), ("maille", "Maillé")]
TOPO_TXT = {
    "etoile": "Tous les équipements du réseau sont reliés à un nœud central (<i>switch</i>, <i>hotspot</i>) qui assure "
              "la communication entre tous les matériels.",
    "anneau": "Tous les ordinateurs du réseau sont situés sur une boucle et communiquent chacun à leur tour.",
    "bus": "Tous les équipements du réseau sont reliés à une même ligne de transmission appelée bus. Simples et faciles "
           "à mettre en œuvre, ces réseaux sont très utilisés en domotique.",
    "maille": "La topologie maillée est une évolution de la topologie en étoile. Très utilisée dans les très grands "
              "réseaux, elle permet d'offrir des chemins différents pour relier deux points, ce qui évite les "
              "problèmes en cas de rupture d'une liaison.",
}


def figure_topologies():
    textes = "".join(f'<p class="cr-topo-txt" data-topo-txt="{k}"{"" if k == "etoile" else " hidden"}><b>{n}</b> — '
                     f"{TOPO_TXT[k]}</p>" for k, n in TOPOS)
    return fig("cr-topo", '<svg class="cr-svg" id="cr-topo-svg" viewBox="0 0 760 300" role="img" '
               'aria-label="Topologie physique du réseau ; chaque liaison peut être coupée"></svg>',
               "Figure 5 — Les quatre topologies physiques. Clique sur une liaison pour la couper (ou sur le nœud "
               "central de l'étoile pour le mettre en panne) : quelles machines communiquent encore ?",
               avant=boutons("topo", TOPOS, "etoile", "Topologie") + textes,
               apres=cap("cr-topo-t") + '<p class="cr-ctrl"><button type="button" class="btn ghost" id="cr-topo-reset">'
               "Rétablir toutes les liaisons</button></p>")


def figure_mac():
    puces = ('<rect x="40" y="30" width="420" height="150" rx="6" fill="#2E8B57" stroke="#1E6B40" stroke-width="2"/>'
             '<path d="M70 180v22h330v-22" fill="#D4A82A" stroke="#A8841F"/>'
             + "".join(f'<rect x="{78 + 12 * i}" y="182" width="7" height="18" fill="#F2D06B"/>' for i in range(27))
             + '<rect x="12" y="62" width="34" height="56" rx="3" fill="#B8BDC2" stroke="#7D868F"/>'
             '<rect x="18" y="74" width="22" height="30" fill="#2E3B47"/>'
             '<rect x="160" y="62" width="70" height="60" rx="3" fill="#1C2530"/><text x="195" y="96" '
             'text-anchor="middle" class="cr-tw" font-size="10">contrôleur</text>'
             '<rect x="260" y="56" width="110" height="34" rx="3" fill="#1C2530"/>'
             '<rect x="90" y="132" width="40" height="26" rx="2" fill="#1C2530"/>'
             + "".join(f'<rect x="{150 + 18 * i}" y="140" width="10" height="16" rx="2" fill="#7A4A21"/>' for i in range(5))
             + '<g id="cr-mac-etq"><rect x="270" y="132" width="176" height="34" rx="4" fill="#FFFFFF" '
             f'stroke="{ORANGE}" stroke-width="2.5"/><text x="358" y="154" text-anchor="middle" class="cr-tmono" '
             'id="cr-mac-etq-t">28:87:A5:EF:18:5D</text></g>'
             f'<text x="480" y="60" class="cr-tb" fill="{ORANGE}">Carte-réseau</text>'
             f'<text x="480" y="80" class="cr-ts">son adresse MAC est inscrite</text><text x="480" y="96" '
             'class="cr-ts">sur l\'étiquette et dans le contrôleur</text>'
             f'<path d="M448 150C500 150 500 120 540 108" stroke="{ORANGE}" stroke-width="2" fill="none"/>')
    ctrl = ('<div class="cr-ctrl"><label for="cr-mac">Adresse MAC</label><input type="text" id="cr-mac" '
            'class="cr-in" value="28:87:a5:ef:18:5d" spellcheck="false" autocomplete="off"></div>')
    return fig("cr-mac-f", svg(760, 215, puces, "Carte-réseau : son adresse MAC est inscrite sur une étiquette"),
               "Figure 6 — Une carte-réseau et son adresse MAC. Écris une adresse, puis touche un octet pour le voir en "
               "binaire.", avant="",
               apres=ctrl + '<div class="cr-octets" id="cr-mac-oct"></div>' + cap("cr-mac-t"))


# ============================================================ 3. WAN et Internet
def figure_wan():
    def lan(x0, nom, cle):
        return (f'<rect x="{x0}" y="22" width="340" height="206" fill="#FFFFFF" stroke="{ORANGE}" stroke-width="1.5"/>'
                f'<text x="{x0 + 170}" y="16" text-anchor="middle" class="cr-tb" fill="{ORANGE}">{nom}</text>'
                + "".join(pc(x0 + 28 + 110 * i, 34, f"{cle}{i + 1}", ident=f"cr-wan-{cle}{i + 1}") for i in range(3))
                + switch(x0 + 115, 140, 110, 6, "Switch", f"cr-wan-sw{cle}")
                + routeur(x0 + 290, 200, "", "", f"cr-wan-r{cle}"))
    liens = ("".join(f'<path class="cr-cable" d="M{x0 + 56 + 110 * i} 106L{x0 + 145 + 20 * i} 140"/>'
                     for x0 in (20, 400) for i in range(3))
             + '<path class="cr-cable" d="M245 158H310V200"/><path class="cr-cable" d="M625 158H690V200"/>'
             '<path class="cr-cable cr-wanl" d="M310 223V262M690 223V262M120 262H740"/>'
             '<path class="cr-cable cr-wanl" d="M200 262v12M520 262v12M740 262v12"/>')
    corps = (lan(20, "Réseau local 1", "A") + lan(400, "Réseau local 2", "B") + liens
             + '<text x="300" y="246" text-anchor="end" class="cr-ts">routeur passerelle</text>'
             '<text x="680" y="246" text-anchor="end" class="cr-ts">routeur passerelle</text>'
             '<text x="430" y="292" text-anchor="middle" class="cr-ts">WAN : vers d\'autres réseaux locaux ou d\'autres '
             'parties d\'Internet</text>'
             '<g id="cr-wan-j" class="cr-jeton" opacity="0"><rect x="-34" y="-12" width="68" height="24" rx="5"/>'
             '<text y="5" text-anchor="middle" class="cr-tj">trame</text></g>')
    ctrl = ('<div class="cr-ctrl"><button type="button" class="btn" id="cr-wan-go">Envoyer un message de A1 à B3</button>'
            '</div>')
    return fig("cr-wan", svg(760, 300, corps, "Deux réseaux locaux reliés au WAN par leurs routeurs passerelles"),
               "Figure 7 — Deux réseaux locaux reliés par leurs routeurs passerelles. Suis le message de A1 à B3.",
               avant=ctrl, apres=cap("cr-wan-t"))


BOX = [("modem", "Modem", "Il fait le lien entre ton réseau domestique et le réseau de ton FAI (fournisseur d'accès à "
        "Internet) : ces deux réseaux ne sont pas forcément compatibles."),
       ("routeur", "Routeur", "C'est le routeur passerelle : il fait passer les trames du réseau local vers Internet, et "
        "inversement."),
       ("switch", "Switch", "Il interconnecte les liaisons filaires : les prises Ethernet de la box."),
       ("hotspot", "Hotspot Wi-Fi", "Il interconnecte les liaisons sans fil : ordinateurs portables, téléphones, "
        "tablettes.")]


def figure_box():
    def module(i, cle, nom):
        x = 40 + 180 * i
        picto = {"modem": f'<path d="M{x + 40} 120h80" stroke="{ORANGE}" stroke-width="3" stroke-dasharray="6 4"/>'
                          f'<circle cx="{x + 80}" cy="120" r="6" fill="{ORANGE}"/>',
                 "routeur": routeur(x + 80, 112),
                 "switch": switch(x + 25, 104, 110, 6, ""),
                 "hotspot": f'<g fill="none" stroke="{VERT}" stroke-width="3"><path d="M{x + 62} 118a26 26 0 0 1 36 0"/>'
                            f'<path d="M{x + 52} 108a40 40 0 0 1 56 0"/></g><circle cx="{x + 80}" cy="126" r="4" '
                            f'fill="{VERT}"/>'}[cle]
        return (f'<g class="cr-bx-m" data-mod="{cle}" tabindex="0" role="button" aria-label="{nom}" '
                f'style="--dx:{260 - 180 * i}px"><rect x="{x}" y="80" width="160" height="80" rx="8" fill="#FFFFFF" '
                f'stroke="{GRIS}" stroke-width="1.5"/>{picto}<text x="{x + 80}" y="152" text-anchor="middle" '
                f'class="cr-t">{nom}</text></g>')
    corps = ("".join(module(i, k, n) for i, (k, n, _t) in enumerate(BOX))
             + '<g class="cr-bx-capot"><rect x="230" y="60" width="300" height="120" rx="18" fill="#F4F5F2" '
             'stroke="#7D868F" stroke-width="2"/><rect x="250" y="150" width="260" height="10" rx="5" fill="#1C2530"/>'
             '<circle cx="270" cy="84" r="5" fill="#5BD08A"/><circle cx="288" cy="84" r="5" fill="#5BD08A"/>'
             '<circle cx="306" cy="84" r="5" fill="#F2B705"/><text x="380" y="124" text-anchor="middle" '
             'class="cr-tb">Box internet</text></g>')
    textes = "".join(f'<p class="cr-bx-txt" data-mod-txt="{k}" hidden><b>{n}</b> — {t}</p>' for k, n, t in BOX)
    return fig("cr-box", svg(760, 200, corps, "Une box internet et les quatre appareils qu'elle contient"),
               "Figure 8 — Que contient une box ? Ouvre-la, puis touche chaque appareil.",
               avant='<div class="cr-ctrl"><button type="button" class="btn" id="cr-box-go" aria-pressed="false">'
                     "Ouvrir la box</button></div>",
               apres=textes + cap("cr-box-t"))


def figure_routage():
    return fig("cr-rt", '<svg class="cr-svg" id="cr-rt-svg" viewBox="0 0 760 400" role="img" aria-label="Maillage de '
               'routeurs : la route d\'un paquet entre deux routeurs passerelles"></svg>',
               "Figure 9 — Un maillage de routeurs (les LAN, derrière les routeurs passerelles, ne sont pas représentés). "
               "Touche deux passerelles (orange) pour choisir le départ et l'arrivée ; touche une liaison pour la couper.",
               avant='<p class="cr-leg-l"><span class="cr-pt cr-pt-p"></span> routeur passerelle d\'un LAN '
                     '<span class="cr-pt cr-pt-r"></span> routeur « rond-point »</p>',
               apres=cap("cr-rt-t") + '<p class="cr-ctrl"><button type="button" class="btn ghost" id="cr-rt-reset">'
               "Rétablir les liaisons</button></p>")


ZONES = {"amn": ("Amérique du Nord", 150, 105, 80, 42), "ams": ("Amérique du Sud", 228, 252, 56, 52),
         "eur": ("Europe", 385, 92, 48, 30), "afr": ("Afrique", 405, 225, 48, 58),
         "asi": ("Asie", 590, 115, 90, 48), "oce": ("Océanie", 650, 290, 52, 28)}
DORSALES = [("amn", "eur", "Transatlantique Nord", "M240 95C290 70 320 75 335 88"),
            ("amn", "ams", "Amériques", "M180 158C195 185 205 200 215 196"),
            ("ams", "afr", "Atlantique Sud", "M278 245C310 235 330 230 350 226"),
            ("eur", "afr", "Europe – Afrique", "M380 128C372 150 370 165 368 178"),
            ("eur", "asi", "Europe – Asie (Méditerranée, mer Rouge, océan Indien)", "M438 105C470 140 500 150 520 140"),
            ("afr", "asi", "Afrique – Asie (océan Indien)", "M460 220C500 205 520 185 540 170"),
            ("asi", "oce", "Asie – Océanie", "M620 175C640 205 650 230 650 250"),
            ("amn", "asi", "Transpacifique", "M60 120C30 120 20 118 4 118M756 125C730 125 710 122 695 120")]


def figure_dorsales():
    zones = "".join(f'<g class="cr-zone"><ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}"/><text x="{x}" y="{y + 5}" '
                    f'text-anchor="middle" class="cr-t">{n}</text></g>' for n, x, y, rx, ry in ZONES.values())
    cables = "".join(f'<g class="cr-dors" data-nom="{e(n)}" tabindex="0" role="button" aria-label="{e(n)}">'
                     f'<path class="cr-dors-hit" d="{d}"/><path class="cr-dors-l" d="{d}"/><path class="cr-dors-p" d="{d}"/></g>'
                     for _a, _b, n, d in DORSALES)
    corps = ('<rect width="760" height="340" fill="#EAF3FA"/>' + cables + zones
             + '<text x="8" y="140" class="cr-ts">← Pacifique</text><text x="752" y="146" text-anchor="end" '
             'class="cr-ts">Pacifique →</text>')
    return fig("cr-dorsales", svg(760, 340, corps, "Schéma des principales dorsales intercontinentales"),
               "Figure 10 — Les principales dorsales intercontinentales, en schéma (continents ni à l'échelle ni à leur "
               "forme réelle ; le Pacifique est coupé aux deux bords). Touche une dorsale pour la nommer.",
               apres=cap("cr-dors-t", "Les impulsions lumineuses qui parcourent les dorsales représentent les données."))


def figure_ip_valide():
    return ('<div class="simu" id="cr-ipv"><h3>Est-ce une adresse IP ?</h3><div class="cr-ctrl"><label for="cr-ipv-in">'
            'Adresse</label><input type="text" id="cr-ipv-in" class="cr-in" value="89.234.17.105" spellcheck="false" '
            'autocomplete="off"></div>' + cap("cr-ipv-t") + "</div>")


MASQUES = ["255.0.0.0", "255.255.0.0", "255.255.255.0"]
EXEMPLES_DEC = [("82.162.240.19", "255.255.0.0"), ("102.122.201.17", "255.255.255.0"), ("19.102.12.193", "255.0.0.0")]


def figure_decoupage():
    corps = (f'<text x="380" y="22" text-anchor="middle" class="cr-t">Adresse IPv4</text>'
             f'<rect x="230" y="32" width="150" height="34" fill="#DDF0E2" stroke="{VERT}"/><text x="305" y="54" '
             f'text-anchor="middle" class="cr-tb" fill="{VERT}">net-ID</text>'
             f'<rect x="380" y="32" width="150" height="34" fill="#FBE3DD" stroke="{ROUGE}"/><text x="455" y="54" '
             f'text-anchor="middle" class="cr-tb" fill="{ROUGE}">host-ID</text>'
             f'<path d="M305 66v20H200" stroke="{VERT}" stroke-width="3" fill="none" marker-end="url(#cr-fl-v)"/>'
             f'<path d="M455 66v20H560" stroke="{ROUGE}" stroke-width="3" fill="none" marker-end="url(#cr-fl-r)"/>'
             f'<text x="190" y="84" text-anchor="end" class="cr-t">Le <tspan font-style="italic">net-ID</tspan> '
             '(adresse réseau)</text><text x="190" y="100" text-anchor="end" class="cr-ts">identifie le réseau.</text>'
             '<text x="570" y="84" class="cr-t">Le <tspan font-style="italic">host-ID</tspan> (adresse machine)</text>'
             '<text x="570" y="100" class="cr-ts">identifie la machine dans le réseau.</text>'
             f'<defs><marker id="cr-fl-v" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" '
             f'orient="auto"><path d="M0 0L10 5L0 10z" fill="{VERT}"/></marker><marker id="cr-fl-r" viewBox="0 0 10 10" '
             f'refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" '
             f'fill="{ROUGE}"/></marker></defs>')
    m_opts = "".join(f'<option{" selected" if m == "255.255.0.0" else ""}>{m}</option>' for m in MASQUES)
    ex = "".join(f'<button type="button" class="btn ghost" data-dec="{a}|{m}">{a} / {m}</button>' for a, m in EXEMPLES_DEC)
    simu = ('<div class="simu" id="cr-dec"><h3>Découpe une adresse avec son masque</h3><div class="simu-grid">'
            '<label>Adresse IP<input type="text" id="cr-dec-ip" class="cr-in" value="82.162.240.19" spellcheck="false" '
            f'autocomplete="off"></label><label>Masque de sous-réseau<select id="cr-dec-m">{m_opts}</select></label></div>'
            f'<p class="cr-ctrl"><span class="small">Exemples :</span> {ex}</p>'
            '<div class="cr-dec-tab" id="cr-dec-tab"></div>' + cap("cr-dec-t") + "</div>")
    return fig("cr-decoupe", svg(760, 112, corps, "Découpage d'une adresse IPv4 en net-ID et host-ID"),
               "Figure 11 — Découpage d'une adresse IPv4 : le net-ID (en vert) et le host-ID (en rouge).") + simu


# ============================================================ 4. adressage IP et LAN
SERVICES = [("ecran", "31.13.91.2", 72, 52), ("globe", "108.174.10.14", 236, 46), ("panier", "216.58.206.238", 58, 150),
            ("courrier", "199.59.148.10", 84, 250), ("arobase", "193.252.148.140", 240, 252)]
PCS_NAT = [("192.168.1.5", 590, 36), ("192.168.1.7", 670, 126), ("192.168.1.10", 590, 216)]


def figure_nat():
    def icone(cle, x, y):
        c = {"ecran": f'<rect x="-16" y="-12" width="32" height="22" rx="3" fill="none" stroke="#2BA6B5" stroke-width="3"/>'
                      '<path d="M-6 16h12M0 10v6" stroke="#2BA6B5" stroke-width="3"/>',
             "globe": f'<circle r="16" fill="none" stroke="{BLEU}" stroke-width="3"/><path d="M-16 0h32M0 -16v32M-11 -11'
                      f'q11 6 22 0M-11 11q11 -6 22 0" stroke="{BLEU}" stroke-width="2" fill="none"/>',
             "panier": f'<path d="M-16 -10h5l5 18h18l4 -13h-24" fill="none" stroke="{ORANGE}" stroke-width="3" '
                       f'stroke-linejoin="round"/><circle cx="-3" cy="13" r="3" fill="{ORANGE}"/><circle cx="10" cy="13" '
                       f'r="3" fill="{ORANGE}"/>',
             "courrier": f'<rect x="-17" y="-12" width="34" height="24" rx="2" fill="none" stroke="{VERT}" '
                         f'stroke-width="3"/><path d="M-17 -12l17 13l17 -13" fill="none" stroke="{VERT}" stroke-width="3"/>',
             "arobase": '<text y="11" text-anchor="middle" font-size="34" font-weight="700" fill="#8E3FA6">@</text>'}[cle]
        return f'<g transform="translate({x} {y})">{c}</g>'
    serv = "".join(f'<g class="cr-srvn" id="cr-nat-s{i}">{icone(k, x, y)}<text x="{x}" y="{y + 36}" '
                   f'text-anchor="middle" class="cr-tip" fill="{BLEU}">{ip}</text></g>'
                   for i, (k, ip, x, y) in enumerate(SERVICES))
    liens = ("".join(f'<path class="cr-cable cr-fin" d="M{x} {y}L150 150"/>' for _k, _ip, x, y in SERVICES)
             + '<path class="cr-cable" d="M190 150H350"/>'
             + "".join(f'<path class="cr-cable" d="M410 150L{x + 4} {y + 24}"/>' for _ip, x, y in PCS_NAT))
    corps = (liens + '<circle cx="150" cy="150" r="34" fill="#DDEBF7" stroke="#7FB6CF" stroke-width="2"/>'
             '<path d="M120 140q30 -24 60 0M120 160q30 24 60 0" stroke="#7FB6CF" fill="none"/>'
             '<line x1="380" y1="30" x2="380" y2="324" stroke="#1C2530" stroke-dasharray="5 5"/>'
             f'<text x="180" y="24" text-anchor="middle" class="cr-tb" fill="{BLEU}">INTERNET</text>'
             f'<text x="600" y="24" text-anchor="middle" class="cr-tb" fill="#8A3A1C">LAN</text>'
             + routeur(380, 142, "", "", "cr-nat-r")
             + f'<text x="372" y="196" text-anchor="end" class="cr-tip" fill="{BLEU}">92.169.148.17</text>'
             f'<text x="388" y="196" class="cr-tip" fill="{ROUGE}">192.168.1.1</text>'
             '<text x="380" y="214" text-anchor="middle" class="cr-ts">routeur (dans la box)</text>'
             + serv + "".join(pc(x, y, "", ip, ident=f"cr-nat-p{i}", sous_cls="cr-tip cr-rouge")
                              for i, (ip, x, y) in enumerate(PCS_NAT))
             + '<g id="cr-nat-j" class="cr-jeton cr-jeton-l" opacity="0"><rect x="-92" y="-13" width="184" height="26" '
             'rx="5"/><text y="5" text-anchor="middle" class="cr-tj"></text></g>'
             f'<rect x="20" y="332" width="22" height="8" fill="{BLEU}"/><text x="48" y="340" class="cr-ts">adresses '
             f'IP publiques</text><rect x="560" y="332" width="22" height="8" fill="{ROUGE}"/><text x="588" y="340" '
             'class="cr-ts">adresses IP privées</text>')
    p_opts = "".join(f'<option value="{i}">{ip}</option>' for i, (ip, _x, _y) in enumerate(PCS_NAT))
    s_opts = "".join(f'<option value="{i}"{" selected" if i == 2 else ""}>{ip}</option>'
                     for i, (_k, ip, _x, _y) in enumerate(SERVICES))
    ctrl = (f'<div class="cr-ctrl"><label>Ordinateur du LAN <select id="cr-nat-p">{p_opts}</select></label>'
            f'<label>Serveur sur Internet <select id="cr-nat-s">{s_opts}</select></label>'
            '<button type="button" class="btn" id="cr-nat-go">Envoyer une requête</button></div>')
    return fig("cr-nat", svg(760, 348, corps, "Adresses IP publiques côté Internet, privées côté LAN, et le routeur "
                                              "entre les deux"),
               "Figure 12 — Adresses IP publiques (côté Internet) et privées (côté LAN). Seule l'adresse publique de la "
               "box est visible sur Internet : suis les adresses inscrites sur le paquet.",
               avant=ctrl, apres=cap("cr-nat-t"))


def figure_privee():
    return ('<div class="simu" id="cr-priv"><h3>Adresse privée ou publique ?</h3><div class="cr-ctrl">'
            '<label for="cr-priv-in">Adresse IP</label><input type="text" id="cr-priv-in" class="cr-in" '
            'value="172.20.5.1" spellcheck="false" autocomplete="off"></div>' + cap("cr-priv-t") + "</div>")


SR_PCS = [("192.168.0.54", 40), ("192.168.1.38", 230), ("192.168.1.11", 420), ("192.168.0.17", 610)]


def figure_sousreseaux():
    corps = ("".join(f'<path class="cr-cable" id="cr-sr-c{i + 1}" d="M{x + 58} 126L{350 + 20 * i} 196"/>'
                     for i, (_ip, x) in enumerate(SR_PCS))
             + switch(325, 196, 110, 6, "Switch")
             + "".join(f'<g id="cr-sr-p{i + 1}">{pc(x + 30, 54, f"PC{i + 1}")}<rect class="cr-sr-net" x="{x - 12}" y="10" '
                       f'width="140" height="40" rx="6"/><text x="{x + 58}" y="27" text-anchor="middle" class="cr-tip" '
                       f'id="cr-sr-ip{i + 1}">{ip}</text><text x="{x + 58}" y="43" text-anchor="middle" class="cr-ts">'
                       'masque 255.255.255.0</text></g>' for i, (ip, x) in enumerate(SR_PCS))
             + '<g id="cr-sr-j" class="cr-jeton" opacity="0"><rect x="-30" y="-11" width="60" height="22" rx="5"/>'
             '<text y="4" text-anchor="middle" class="cr-tj">message</text></g>')
    champs = "".join(f'<label>PC{i + 1}<input type="text" class="cr-in" id="cr-sr-in{i + 1}" value="{ip}" '
                     'spellcheck="false" autocomplete="off"></label>' for i, (ip, _x) in enumerate(SR_PCS))
    ctrl = (f'<div class="cr-sr-in">{champs}</div><div class="cr-ctrl"><label>De <select id="cr-sr-de">{options(4, 1)}'
            f'</select></label><label>vers <select id="cr-sr-a">{options(4, 2)}</select></label>'
            '<button type="button" class="btn" id="cr-sr-go">Envoyer un message</button></div>')
    return fig("cr-sr", svg(760, 250, corps, "Un réseau local physique de quatre ordinateurs reliés au même switch"),
               "Figure 13 — Un LAN physique, des sous-réseaux logiques : les machines de même couleur ont le même "
               "net-ID. Modifie les adresses et observe qui peut communiquer.",
               avant="", apres=ctrl + cap("cr-sr-t") + '<table class="t cr-sr-mat" id="cr-sr-mat"></table>')


# ============================================================ 5. communication entre logiciels
PAGES_HTTP = [("/index.html", "Accueil"), ("/contact.html", "Contact"), ("/photos.html", "Photos")]


def figure_http():
    corps = ('<g transform="translate(30 40)"><rect width="150" height="104" rx="6" fill="#FFFFFF" stroke="#1C2530" '
             'stroke-width="2"/><rect width="150" height="20" rx="6" fill="#D3D8D5"/><circle cx="12" cy="10" r="4" '
             'fill="#B42318"/><circle cx="24" cy="10" r="4" fill="#F2B705"/><circle cx="36" cy="10" r="4" '
             'fill="#1B7A43"/><rect x="12" y="34" width="90" height="8" rx="3" fill="#9DB6D6"/><rect x="12" y="50" '
             'width="124" height="6" rx="3" fill="#D3D8D5"/><rect x="12" y="62" width="110" height="6" rx="3" '
             'fill="#D3D8D5"/><text x="75" y="128" text-anchor="middle" class="cr-tb">Navigateur web</text>'
             '<text x="75" y="144" text-anchor="middle" class="cr-ts">le client</text></g>'
             + serveur(600, 52, "")
             + '<text x="620" y="150" text-anchor="middle" class="cr-tb">Serveur web</text>'
             '<text x="620" y="166" text-anchor="middle" class="cr-ts">le serveur</text>'
             '<g id="cr-http-disque"><rect x="652" y="44" width="104" height="84" rx="5" fill="#F4F5F2" stroke="#A5ADAA"/>'
             '<text x="704" y="60" text-anchor="middle" class="cr-ts">disque</text>'
             '<text x="660" y="80" class="cr-tmono" data-f="/index.html">index.html</text>'
             '<text x="660" y="98" class="cr-tmono" data-f="/contact.html">contact.html</text>'
             '<text x="660" y="116" class="cr-tmono" data-f="/style.css">style.css</text></g>'
             f'<path d="M200 80H580" stroke="{BLEU}" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#cr-fl-b)"/>'
             f'<path d="M580 124H200" stroke="{VERT}" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#cr-fl-g)"/>'
             f'<text x="390" y="70" text-anchor="middle" class="cr-tb" fill="{BLEU}">requête</text>'
             f'<text x="390" y="146" text-anchor="middle" class="cr-tb" fill="{VERT}">réponse</text>'
             f'<defs><marker id="cr-fl-b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
             f'orient="auto"><path d="M0 0L10 5L0 10z" fill="{BLEU}"/></marker><marker id="cr-fl-g" viewBox="0 0 10 10" '
             f'refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" '
             f'fill="{VERT}"/></marker></defs>'
             '<g id="cr-http-j" class="cr-jeton" opacity="0"><rect x="-70" y="-13" width="140" height="26" rx="5"/>'
             '<text y="5" text-anchor="middle" class="cr-tj"></text></g>')
    opts = "".join(f'<option value="{p}">www.example.org{p}</option>' for p, _t in PAGES_HTTP)
    ctrl = (f'<div class="cr-ctrl"><label>Adresse <select id="cr-http-url">{opts}</select></label>'
            '<button type="button" class="btn" id="cr-http-go">Charger la page</button></div>')
    vues = ('<div class="cr-http-vues"><div class="cr-nav"><div class="cr-nav-barre"><span id="cr-http-barre">'
            'www.example.org</span></div><div class="cr-nav-page" id="cr-http-page"><p class="small">La page '
            'apparaîtra ici.</p></div></div><div class="cr-http-msg"><p class="cr-msg-t">Messages échangés</p>'
            '<pre id="cr-http-req" class="cr-pre"></pre><pre id="cr-http-rep" class="cr-pre"></pre></div></div>')
    return fig("cr-http", svg(760, 196, corps, "Un navigateur web (client) et un serveur web : requête et réponse "
                                              "HTTP"),
               "Figure 14 — Requête et réponse HTTP : le navigateur (client) demande une page, le serveur cherche la "
               "ressource sur son disque, puis répond avec son code HTML et CSS.", avant=ctrl,
               apres=cap("cr-http-t") + vues)


SEGMENTS = ["Bonjour, ", "comment ", "ça ", "va ?"]


def figure_tcp():
    corps = (pc(20, 70, "Émetteur") + pc(684, 70, "Destinataire")
             + f'<path class="cr-cable" d="M90 96H670"/><path class="cr-cable cr-fin" d="M670 128H90"/>'
             '<text x="380" y="88" text-anchor="middle" class="cr-ts">segments →</text>'
             '<text x="380" y="146" text-anchor="middle" class="cr-ts">← accusés de réception</text>'
             '<text x="20" y="30" class="cr-t">Message : « Bonjour, comment ça va ? »</text>'
             '<text x="740" y="30" text-anchor="end" class="cr-t">Message reçu :</text>'
             '<text x="740" y="50" text-anchor="end" class="cr-tmono" id="cr-tcp-recu">…</text>'
             '<g id="cr-tcp-tampon">' + "".join(
                 f'<rect class="cr-tcp-case" x="{396 + 88 * i}" y="190" width="84" height="34" rx="4" data-n="{i + 1}"/>'
                 f'<text x="{438 + 88 * i}" y="242" text-anchor="middle" class="cr-ts">case {i + 1}</text>'
                 for i in range(4)) + "</g>"
             '<text x="388" y="211" text-anchor="end" class="cr-ts">remise dans l\'ordre :</text>'
             '<g id="cr-tcp-vol"></g>')
    ctrl = ('<div class="cr-ctrl"><button type="button" class="btn" id="cr-tcp-go">Envoyer le message</button>'
            '<label class="cr-chk"><input type="checkbox" id="cr-tcp-perte"> perdre le segment 3 en route</label></div>')
    return fig("cr-tcp", svg(760, 250, corps, "Le protocole TCP découpe le message en segments numérotés ; le "
                                              "destinataire acquitte chaque segment"),
               "Figure 15 — TCP découpe le message en segments numérotés. Les segments n'arrivent pas forcément dans "
               "l'ordre : le destinataire les remet en place, et acquitte chacun d'eux. Un segment perdu, jamais "
               "acquitté, est renvoyé.", avant=ctrl, apres=cap("cr-tcp-t"))


# ============================================================ 6. modèle OSI
OSI = [  # n°, nom, unité, rôle, technologies, couleur
    (7, "Application", "requête / réponse", "Préparer les requêtes et les réponses.", "HTTP", "#E8603C"),
    (6, "Présentation", "requête / réponse", "Mettre en forme les données pour permettre aux applications de les "
     "traiter.", "HTTP", "#E86AA6"),
    (5, "Session", "requête / réponse", "Organiser et synchroniser les échanges et les communications.", "HTTP",
     "#F6BE6E"),
    (4, "Transport", "segment", "Gérer la segmentation des messages ; fiabiliser la transmission.", "TCP", "#FBE45A"),
    (3, "Réseau", "paquet", "Identifier et localiser les machines d'un internet ; router les paquets dans "
     "l'Internet.", "IP, adresse IP, routeurs", "#CFD95C"),
    (2, "Liaison de données", "trame", "Identifier les machines d'un LAN ; gérer la transmission des trames dans un "
     "LAN.", "Ethernet, Wi-Fi, Bluetooth, adresse MAC, switch, hotspot", "#86C463"),
    (1, "Physique", "bits", "Transmettre physiquement les bits d'une machine à une autre, et les recevoir.",
     "Ethernet, Wi-Fi, Bluetooth (câbles, fibre, ondes)", "#4E9A7C"),
]


def figure_osi():
    tech = {7: 3, 4: 1, 3: 1, 2: 2}  # couche où commence une cellule de technologies, et le nombre de couches couvertes
    cases = ['<div class="cr-osi-h cr-osi-pt" style="grid-column:1">Émetteur</div>',
             '<div class="cr-osi-h" style="grid-column:2">Couche</div>',
             '<div class="cr-osi-h" style="grid-column:3">N°</div>',
             '<div class="cr-osi-h cr-osi-role" style="grid-column:4">Rôle</div>',
             '<div class="cr-osi-h" style="grid-column:5">Technologies, protocoles, matériels</div>',
             '<div class="cr-osi-h cr-osi-pt" style="grid-column:6">Destina&shy;taire</div>']
    for r, (n, nom, u, role, t, c) in enumerate(OSI, start=2):
        st = f"grid-row:{r};--c:{c}"
        cases += [f'<button type="button" class="cr-c" data-c="{n}" data-cote="e" style="grid-column:1;{st}" '
                  f'aria-label="Émetteur, couche {n}">{n}</button>',
                  f'<div class="cr-osi-d cr-osi-nom" data-c="{n}" style="grid-column:2;{st}"><b>{nom}</b>'
                  f'<span class="small">({u})</span></div>',
                  f'<div class="cr-osi-d cr-osi-n" data-c="{n}" style="grid-column:3;{st}">{n}</div>',
                  f'<div class="cr-osi-d cr-osi-role" data-c="{n}" style="grid-column:4;{st}">{role}</div>',
                  f'<button type="button" class="cr-c" data-c="{n}" data-cote="d" style="grid-column:6;{st}" '
                  f'aria-label="Destinataire, couche {n}">{n}</button>']
        if n in tech:
            cases.append(f'<div class="cr-osi-tech" style="grid-column:5;grid-row:{r} / span {tech[n]}">{t}</div>')
    corps = ('<div class="cr-osi" id="cr-osi-g">' + "".join(cases) + "</div>"
             '<p class="cr-osi-grp"><span>Couches 5 à 7 : couches applications</span><span>Couches 1 à 4 : couches '
             "réseau</span></p>"
             '<div class="cr-flux" id="cr-osi-flux" aria-hidden="true">↓ émetteur · 1001101001100100 … flux binaire … '
             "1001010000000101 · destinataire ↑</div>")
    ctrl = '<div class="cr-ctrl"><button type="button" class="btn" id="cr-osi-go">Envoyer un message</button></div>'
    return fig("cr-osi-f", corps, "Figure 16 — Les sept couches du modèle OSI. Touche une couche pour la mettre en "
               "évidence, ou envoie un message : il descend les couches de l'émetteur, circule sous forme de bits, puis "
               "remonte les couches du destinataire.", avant=ctrl, apres=cap("cr-osi-t"))


ENCAPS = [  # étape : (couche, nom de l'unité, blocs ajoutés, explication)
    ("7 à 5", "Données", "Le logiciel de messagerie prépare le message : « Bonjour, comment ça va ? »."),
    ("7 à 5", "Données", "Les couches applications ajoutent l'en-tête applicatif : il dépend du protocole utilisé (ici "
     "SMTP, celui du courrier électronique)."),
    ("4", "Segment", "La couche transport (TCP) ajoute son en-tête : numéro du segment, contrôle d'erreur. Le message "
     "devient un segment."),
    ("3", "Paquet", "La couche réseau (IP) ajoute son en-tête : adresses IP de l'émetteur et du destinataire. Le segment "
     "devient un paquet."),
    ("2", "Trame", "La couche liaison de données (Ethernet) ajoute son en-tête — adresses MAC du destinataire et de "
     "l'émetteur, type — et une remorque (contrôle d'erreur). Le paquet devient une trame."),
    ("1", "Bits", "La couche physique transmet la trame bit après bit, sous forme de signal."),
]


def figure_encapsulation():
    ctrl = ('<div class="cr-ctrl"><button type="button" class="btn ghost" id="cr-enc-prec">◀ Étape précédente</button>'
            '<button type="button" class="btn" id="cr-enc-suiv">Étape suivante ▶</button>'
            '<button type="button" class="btn ghost" id="cr-enc-dec" aria-pressed="false">Côté destinataire : '
            'désencapsuler</button></div>')
    corps = ('<div class="cr-enc"><div class="cr-enc-zone"><p class="cr-enc-et" id="cr-enc-et"></p>'
             '<div class="cr-enc-blocs" id="cr-enc-blocs"></div><p class="cr-enc-det" id="cr-enc-det"></p></div>'
             '<ol class="cr-enc-pile" id="cr-enc-pile" reversed>' + "".join(
                 f'<li data-c="{c}"><b>{n}</b><span>{u}</span></li>' for c, n, u in
                 [("app", "Application", "Données"), ("4", "Transport", "Segment"), ("3", "Réseau", "Paquet"),
                  ("2", "Liaison de données", "Trame"), ("1", "Physique", "Bits")]) + "</ol></div>")
    return fig("cr-encaps", corps, "Figure 17 — Encapsulation : chaque couche prend en charge le message et lui ajoute "
               "un en-tête. Touche un en-tête pour lire ce qu'il contient.", avant=ctrl, apres=cap("cr-enc-t"))


PARCOURS = [("PC1", 7), ("SW1", 2), ("R1", 3), ("SW2", 2), ("PC2", 7)]


def figure_parcours():
    cx = [70, 235, 380, 525, 690]
    noms = {7: "Application", 6: "Présentation", 5: "Session", 4: "Transport", 3: "Réseau", 2: "Liaison de données",
            1: "Physique"}
    coul = {n: c for n, _nom, _u, _r, _t, c in OSI}
    H, B = 26, 214  # hauteur d'une couche, bas de la couche 1
    piles = ""
    for i, ((nom, nc), x) in enumerate(zip(PARCOURS, cx)):
        w = 128 if nc == 7 else 120
        for n in range(1, nc + 1):
            y = B - n * H
            piles += (f'<rect class="cr-pc-c" data-app="{i}" data-c="{n}" x="{x - w / 2}" y="{y}" width="{w}" height="{H}" '
                      f'fill="{coul[n]}"/><text x="{x}" y="{y + 17.5}" text-anchor="middle" class="cr-tcouche'
                      f'{" cr-tw" if n == 1 else ""}">{noms[n]}</text>')
        if nom.startswith("PC"):
            piles += pc(x - 28, 228, nom)
        elif nom.startswith("SW"):
            piles += switch(x - 45, 236, 90, 4, nom)
        else:
            piles += routeur(x, 236, nom)
    corps = (piles + '<line x1="98" y1="252" x2="662" y2="252" stroke="#A5ADAA" stroke-width="2"/>'
             '<polyline id="cr-par-l" fill="none" stroke="#1C2530" stroke-width="3.5" stroke-linejoin="round" points=""/>'
             '<circle id="cr-par-p" r="7" fill="#F2B705" stroke="#1C2530" stroke-width="2" opacity="0"/>')
    ctrl = ('<div class="cr-ctrl"><button type="button" class="btn" id="cr-par-go">Lancer le message</button>'
            '<button type="button" class="btn ghost" id="cr-par-pas">Pas à pas</button></div>')
    return fig("cr-parcours", svg(760, 300, corps, "Liaison entre deux postes de deux réseaux différents reliés par un "
                                                   "routeur : le message traverse les couches de chaque appareil",
                                  "cr-par-svg"),
               "Figure 18 — Liaison entre deux postes de deux réseaux différents reliés par un routeur ; dans chaque "
               "réseau, les postes sont reliés à un switch. Le message monte et descend les couches de chaque appareil.",
               avant=ctrl, apres=cap("cr-par-t"))


# ============================================================ le cours
def _remarque(texte):
    return f'<div class="remarque"><p><b>Remarque :</b> {texte}</p></div>'


def _exemple(texte):
    return f'<div class="exemple"><p><b><i>Exemple :</i></b> <i>{texte}</i></p></div>'


def render(g):
    s1 = g.course_section(1, "cr-liaison", "Liaison point-à-point",
        "<p>Une <b>liaison point-à-point</b> est une liaison directe entre deux machines (ordinateur, smartphone, objet "
        "connecté, etc.). Une machine se connecte à une liaison point-à-point grâce à sa <b>carte-réseau</b>. Une liaison "
        "point-à-point est basée sur :</p><ul><li>un <b>support de communication</b>, dans lequel les données circulent "
        "sous forme de signal ;</li><li>un <b>protocole de communication</b>, qui précise les règles de communication "
        "utilisées.</li></ul><p>Une liaison point-à-point sera dite <b><i>full-duplex</i></b> si des données peuvent "
        "circuler dans les deux sens en même temps, ou <b><i>half-duplex</i></b> si elles ne peuvent circuler que dans un "
        "sens à la fois.</p>" + figure_duplex()
        + "<h3>1.1 Liaison filaire</h3><p>Une liaison point-à-point peut être réalisée à l'aide d'une technologie de "
        "transmission filaire. Les supports de communication filaires les plus courants sont :</p><ul><li>les câbles en "
        "<b>cuivre à paires torsadées</b> (signal électrique) ;</li><li>la <b>fibre optique</b> (signal lumineux). La "
        "fibre optique est plus performante, mais plus chère.</li></ul>" + figure_supports()
        + "<p>Le protocole de communication filaire le plus utilisé est <b>Ethernet</b>.</p>"
        "<h3>1.2 Liaison non-filaire</h3><p>Une connexion point-à-point peut aussi être réalisée à l'aide d'une "
        "technologie de transmission non-filaire. Dans ce cas, le support de communication devient l'air, dans lequel "
        "des <b>ondes</b> radioélectriques transportent les données.</p><p>Dans le cadre des réseaux informatiques, les "
        "protocoles des normes <b>Bluetooth</b> et <b>Wi-Fi</b> sont les plus courants. Le Wi-Fi est plus performant et "
        "offre une meilleure portée, mais il consomme plus d'énergie que le Bluetooth.</p>" + figure_portee()
        + '<table class="t cr-comp"><thead><tr><th></th><th>Bluetooth</th><th>Wi-Fi</th></tr></thead><tbody>'
        "<tr><th scope=\"row\">Débit</th><td>quelques Mbit/s</td><td>plusieurs centaines de Mbit/s</td></tr>"
        "<tr><th scope=\"row\">Portée</th><td>une dizaine de mètres</td><td>quelques dizaines de mètres</td></tr>"
        "<tr><th scope=\"row\">Consommation d'énergie</th><td>faible</td><td>plus élevée</td></tr>"
        "<tr><th scope=\"row\">Exemples</th><td>écouteurs, montre, enceinte</td><td>box, ordinateur, téléphone</td>"
        "</tr></tbody></table>"
        "<h3>1.3 Débit</h3><p>Une caractéristique importante d'une liaison point-à-point est son <b>débit</b>, aussi "
        "nommé vitesse de transmission. Le débit s'exprime en bit/s ou en octets/s, et vaut :</p>"
        '<div class="formule"><span class="f-main">Débit = ' + g.frac("Quantité de données", "Durée de transmission")
        + '</span><span class="f-units">débit en bit/s (ou octets/s), quantité en bits (ou octets), durée en s ; '
        "1 octet = 8 bits</span></div>"
        + _remarque("Les préfixes du système international sont utilisés pour les débits importants. On a, par exemple, "
                    "1 kbit/s = 1 000 bit/s, ou 1 Mo/s = 1 000 000 octets/s.") + simu_debit())

    s2 = g.course_section(2, "cr-mise", "Mise en réseau",
        "<h3>2.1 Dispositif d'interconnexion et réseau local (LAN)</h3><p>Il existe des dispositifs d'interconnexion qui "
        "sont capables de relier plusieurs liaisons point-à-point simultanément. Leur rôle est de faire passer les trames "
        "venant d'une liaison point-à-point vers une autre liaison point-à-point.</p><p>Les deux principaux dispositifs "
        "d'interconnexion sont :</p><ul><li>le <b>commutateur</b>, ou <b><i>switch</i></b> en anglais, qui "
        "interconnecte des liaisons filaires ;</li><li>le <b>point d'accès sans fil</b>, ou "
        "<b><i>hotspot/access point</i></b> en anglais, qui interconnecte des liaisons non-filaires.</li></ul>"
        + figure_switch()
        + _remarque("Un commutateur ne possède pas une carte-réseau pour chacun de ses ports : à la place, il a ce qu'on "
                    "appelle des contrôleurs réseau, qui sont des puces électroniques capables d'utiliser le protocole "
                    "Ethernet.")
        + "<p>Lorsque plusieurs machines sont interconnectées grâce à un ou plusieurs commutateurs et/ou points d'accès "
        "sans fil, on dit qu'elles forment un <b>réseau local</b>, ou <b>LAN</b> (<i>Local Area Network</i> en "
        "anglais).</p><h3>2.2 Topologie physique</h3><p>Les LAN peuvent être structurés de plusieurs manières. La "
        "structure du LAN s'appelle sa <b>topologie physique</b>. On distingue notamment les réseaux structurés en "
        "<b>étoile</b> (<i>star</i>), en <b>anneau</b> (<i>ring</i>), en <b>bus</b> et les réseaux <b>maillés</b> "
        "(<i>mesh</i>).</p>" + figure_topologies()
        + '<div class="remarque"><p><b>Remarque :</b> La majorité des réseaux locaux actuels suivent une structure de '
        "type étoile. C'est le cas du réseau local de votre domicile, qui est centré autour d'une box internet, ou du "
        "réseau local de votre établissement.</p><p>Pour avoir une topologie maillée, il n'est pas nécessaire que chaque "
        "machine ait une liaison point-à-point avec 100 % des autres machines.</p></div>"
        "<h3>2.3 Adresse MAC</h3><p>Avoir plusieurs machines dans un même réseau local pose un problème : il est "
        "impossible de savoir qui est l'émetteur d'une trame, et qui en est le destinataire. Les protocoles de "
        "communication des LAN (Ethernet, Wi-Fi, Bluetooth) résolvent ce problème grâce à un <b>système "
        "d'adressage</b>.</p><p>Chaque machine connectée au LAN possède une adresse : l'<b>adresse MAC</b>, <i>Media "
        "Access Control</i>. Toutes les trames envoyées sur le réseau sont étiquetées avec l'adresse MAC de "
        "l'expéditeur et l'adresse MAC du destinataire. Les <i>switchs</i> et <i>hotspots</i> lisent les adresses MAC "
        "pour savoir comment aiguiller les messages dans la bonne direction.</p><p>Une adresse MAC se compose de 6 "
        "couples de chiffres hexadécimaux. Exemple : 28:87:a5:ef:18:5d. Elle est gravée sur la carte-réseau de la "
        "machine par son fabricant : on dit que c'est son <b>adresse physique</b>.</p>" + figure_mac())

    s3 = g.course_section(3, "cr-wan-s", "Au-delà du réseau local : WAN et Internet",
        "<h3>3.1 WAN, passerelle et Internet</h3><p>Plusieurs LAN peuvent être interconnectés, de manière à créer un "
        "<b>WAN</b>, <i>Wide Area Network</i>.</p><p>Chaque LAN faisant partie d'un WAN est relié au WAN par "
        "l'intermédiaire d'un <b>routeur</b>. Le routeur sert de <b>passerelle</b> vers le WAN : il fait passer les "
        "trames du LAN vers le WAN, et inversement.</p><p><b>Internet</b> est le principal WAN mondial.</p>"
        + figure_wan()
        + _remarque("Chez vous, le routeur passerelle se trouve dans votre box. Votre box comporte en fait un routeur, un "
                    "<i>switch</i> et un <i>hotspot</i> Wi-Fi. Elle comporte aussi un modem, qui fait le lien entre "
                    "votre réseau domestique et le réseau de votre FAI, Fournisseur d'Accès Internet : ces deux réseaux "
                    "ne sont pas forcément compatibles.") + figure_box()
        + "<p>Quand une trame circule dans un internet, elle est appelée <b>paquet</b>.</p>"
        "<h3>3.2 Structure d'Internet et routage</h3><p>Internet est très vaste, et il possède une structure complexe, "
        "qui est globalement maillée. Il y a de nombreuses routes différentes pour passer d'un point A à un point B. "
        "Des mécanismes spécifiques sont donc à l'œuvre pour aiguiller les paquets, de leurs émetteurs jusqu'à leurs "
        "destinataires, le plus rapidement possible. Ces mécanismes sont appelés <b>routage</b>. Ce sont, de nouveau, "
        "les <b>routeurs</b> qui se chargent du routage.</p>"
        + _remarque("L'avantage de la structure maillée est qu'en cas de coupure d'un câble sur Internet, il y a "
                    "toujours d'autres routes qui peuvent être utilisées pour acheminer les paquets au destinataire.")
        + "<p>Sur l'illustration ci-dessous, on peut voir un exemple de structure qu'on retrouve sur Internet. Chaque "
        "dispositif est un routeur, qui peut être, au choix :</p><ul><li>un routeur servant de passerelle à un LAN (les "
        "LAN ne sont pas représentés sur le schéma) ;</li><li>un routeur servant de « rond-point », dont le rôle est "
        "d'aiguiller les messages au travers d'Internet.</li></ul>" + figure_routage()
        + "<p>Entre certains des routeurs « rond-point », on trouve de grandes liaisons en fibre optique, qu'on appelle "
        "des <b>dorsales</b>, ou <b><i>backbones</i></b> en anglais. Elles permettent de relier les différentes zones "
        "géographiques connectées à Internet ; entre les continents, ce sont des câbles sous-marins.</p>"
        + figure_dorsales()
        + "<h3>3.3 Adresse IP</h3><p>Le routage est grandement facilité par le système d'adressage utilisé sur Internet : "
        "l'<b>adressage IP</b>, <b><i>Internet Protocol</i></b>. Chaque machine connectée à un internet possède une "
        "adresse IP.</p><p>Tous les paquets sont étiquetés avec l'adresse IP de l'émetteur et l'adresse IP du "
        "destinataire. Les routeurs lisent les adresses IP pour savoir comment aiguiller les messages dans la bonne "
        "direction.</p><p>Une adresse IP se compose de 4 nombres décimaux, compris entre 0 et 255. Exemple : "
        "89.234.17.105.</p>" + figure_ip_valide()
        + "<p>Comme pour l'adresse MAC, chaque carte-réseau possède une adresse IP. En revanche, l'adresse IP peut être "
        "changée à tout moment : on dit que c'est l'<b>adresse logique</b> de la machine.</p><p>Les adresses IP sont "
        "dites <b>routables</b>, du fait qu'elles facilitent le routage, comme nous allons le voir.</p>"
        "<h3>3.4 Découpage des adresses IP</h3><p>Une adresse IP peut être découpée en deux parties :</p><ul><li>le "
        "<b>champ de sous-réseau</b>, <i>net-ID</i> en anglais ;</li><li>le <b>champ hôte</b>, <b><i>host-ID</i></b> "
        "en anglais.</li></ul>"
        + _remarque("Dans ce cours, nous présentons la version 4 du protocole IP (IPv4). La version 6 (IPv6), "
                    "normalisée en 1998, est toujours en cours de déploiement : elle porte aujourd'hui une part "
                    "importante du trafic, de l'ordre de 40 % de celui des grands services en ligne.")
        + "<p>Sur Internet, le <i>net-ID</i> d'un ordinateur n'est pas choisi au hasard : il dépend de son FAI et de la "
        "région du monde dans laquelle il se trouve. Ainsi, en lisant le <i>net-ID</i> du destinataire d'un paquet, un "
        "routeur peut facilement orienter le paquet dans la bonne direction. C'est grâce à cela que les adresses IP sont "
        "rendues <b>routables</b>.</p><p>La découpe entre les deux champs de l'adresse IP se fait grâce à ce qu'on "
        "appelle un <b>masque de sous-réseau</b>, qui, lui aussi, se compose de 4 nombres décimaux. Ces quatre nombres "
        "vaudront toujours soit 0, soit 255, dans les situations que nous rencontrerons. Exemple : 255.255.0.0</p>"
        "<p>Pour découper l'adresse IP, on superpose l'adresse et le masque. La partie de l'adresse IP au-dessus des 255 "
        "est le <i>net-ID</i>, et la partie au-dessus des 0 est le <i>host-ID</i>.</p>" + figure_decoupage()
        + '<div class="remarque"><p><b>Remarque :</b> Les trois seuls masques que nous rencontrerons seront :</p><ul>'
        "<li>255.0.0.0 : dans ce cas, on peut connecter 16 777 214 machines ;</li><li>255.255.0.0 : dans ce cas, on "
        "peut connecter 65 534 machines ;</li><li>255.255.255.0 : dans ce cas, on peut connecter 254 machines.</li></ul>"
        "<p>Deux adresses de chaque réseau sont réservées (celle du réseau lui-même et celle de diffusion) : par "
        "exemple, 2<sup>8</sup> − 2 = 254.</p></div>")

    s4 = g.course_section(4, "cr-lan", "Adressage IP et LAN",
        "<h3>4.1 Adresse privée et adresse publique</h3><p>En réalité, un ordinateur qui se connecte à Internet utilise "
        "deux adresses IP :</p><ul><li>une <b>adresse IP privée</b> : c'est sa véritable adresse IP, qu'il utilise à "
        "l'intérieur de son LAN, mais elle est invisible pour les machines de l'Internet ;</li><li>une <b>adresse IP "
        "publique</b> : c'est l'adresse IP par laquelle il est vu par les machines de l'Internet.</li></ul>"
        + figure_nat()
        + "<p>L'adresse IP publique n'est pas la véritable adresse IP de l'ordinateur : c'est celle de son routeur "
        "passerelle. Le routeur remplace l'adresse privée par la sienne dans les paquets qui sortent, et fait l'inverse "
        "pour les réponses : on parle de traduction d'adresses (NAT).</p>"
        + _remarque("Toutes les machines d'un LAN utilisent le même routeur comme passerelle vers Internet : elles ont "
                    "donc toutes la même adresse IP publique.")
        + "<p>Certaines adresses IP sont <b>réservées</b> pour être utilisées exclusivement dans les LAN : il est "
        "interdit de s'en servir sur Internet. C'est le cas des adresses suivantes :</p><ul><li>les adresses allant de "
        "10.0.0.0 à 10.255.255.255 ;</li><li>les adresses allant de 172.16.0.0 à 172.31.255.255 ;</li><li>les adresses "
        "allant de 192.168.0.0 à 192.168.255.255.</li></ul>" + figure_privee()
        + "<h3>4.2 Sous-réseaux logiques dans un LAN</h3><p><b>Dans un LAN, deux machines peuvent communiquer uniquement "
        "si elles ont le même <i>net-ID</i>.</b></p><p>Cela signifie que l'on peut créer, virtuellement, plusieurs "
        "sous-réseaux dans un même LAN, sans modifier le câblage. Il suffit de bien choisir les adresses IP. On parle de "
        "<b>structure logique</b> du LAN.</p>"
        + _exemple("dans le schéma ci-dessous, les 4 PC font physiquement partie du même LAN. Cependant, PC1 ne peut "
                   "communiquer qu'avec PC4, car leur net-ID est 192.168.0. Le net-ID des deux autres PC est différent : "
                   "c'est 192.168.1. La structure logique de ce LAN comporte donc deux sous-réseaux virtuels.")
        + figure_sousreseaux())

    s5 = g.course_section(5, "cr-logiciels", "Communication entre logiciels",
        "<h3>5.1 Du logiciel à la carte-réseau</h3><p>La plupart des logiciels (logiciels ordinateur, applications "
        "mobiles, jeux vidéo, etc.) possèdent des fonctionnalités utilisant les réseaux, et notamment Internet. Pour "
        "utiliser ces fonctionnalités, les logiciels vont préparer des messages, puis transmettre ces messages à la "
        "carte-réseau. La carte-réseau enverra ensuite ces messages sur le réseau.</p>"
        + _exemple("un navigateur Internet, qui a besoin d'ouvrir une page Internet, va préparer un message. Ce message "
                   "sera ensuite remis à la carte-réseau, qui l'enverra sur le réseau.")
        + "<h3>5.2 Modèle client-serveur</h3><p>La plupart des logiciels utilisant le réseau communiquent en suivant le "
        "<b>modèle client-serveur</b> :</p><ul><li>un des logiciels est nommé <b>client</b> : ce logiciel cherche à "
        "accéder à des ressources en ligne ;</li><li>un des logiciels est nommé <b>serveur</b> : ce logiciel met à "
        "disposition des services en ligne.</li></ul><p>Deux types de messages vont être échangés entre le client et le "
        "serveur :</p><ul><li>les <b>requêtes</b> : ce sont des messages envoyés par le client ;</li><li>les "
        "<b>réponses</b> : ce sont des messages envoyés par le serveur, en réponse aux requêtes du client.</li></ul>"
        "<p>Pour mettre en œuvre le modèle client-serveur, les logiciels suivent les règles d'un protocole de "
        "communication pour logiciels. Le <b>protocole HTTP</b>, par exemple, est le protocole qui gère les échanges du "
        "Web, c'est-à-dire des pages Internet. HTTP décrit à quoi doivent ressembler les requêtes et réponses HTTP.</p>"
        + _exemple("un navigateur Internet (client), qui doit ouvrir une page Internet, va préparer un message qu'on "
                   "appelle une requête HTTP. Ce message précisera de quelle page Internet le navigateur a besoin. La "
                   "requête HTTP sera envoyée à un serveur Internet (serveur). Le serveur Internet cherchera la page "
                   "Internet dans son disque dur, puis transmettra le code HTML et CSS de cette page, sous forme d'une "
                   "réponse HTTP.") + figure_http()
        + "<h3>5.3 Gestion des messages</h3><p>Le protocole <b>TCP</b> permet de fiabiliser l'échange. Il va notamment :"
        "</p><ul><li><b>segmenter</b> les gros messages en petits morceaux, qu'on appelle des <b>segments</b> ;</li>"
        "<li>pour chaque segment reçu, faire envoyer un accusé de réception par le destinataire du message ;</li>"
        "<li>détecter les erreurs dans les messages.</li></ul>" + figure_tcp())

    s6 = g.course_section(6, "cr-osi-s", "Modèle OSI",
        "<h3>6.1 Couches réseaux</h3><p>Une communication à travers le réseau nécessite un assemblage de plusieurs "
        "technologies, protocoles et matériels. Chaque technologie, protocole ou matériel est une solution à un problème "
        "qu'il faut résoudre pour que le réseau fonctionne. Ces problèmes sont indépendants les uns des autres, et "
        "peuvent être séparés en plusieurs catégories, qu'on appelle des <b>couches réseaux</b>.</p><p>Le <b>modèle "
        "OSI</b> est le modèle standard pour décrire le fonctionnement d'un réseau. Le modèle OSI représente les réseaux "
        "avec les sept couches suivantes.</p>" + figure_osi()
        + "<h3>6.2 Trames et encapsulation</h3><p>Toutes les couches sont nécessaires pour réaliser la communication "
        "entre deux logiciels. Chaque couche est responsable d'une partie de la transmission à travers le réseau. Les "
        "couches vont, tour à tour, prendre en charge le message à transmettre, et <b>encapsuler</b> le message en lui "
        "ajoutant ce qu'on appelle un <b>en-tête</b>.</p>" + figure_encapsulation()
        + "<h3>6.3 Synthèse d'une transmission</h3><p>Lors de son trajet à travers un ordinateur, un LAN, un Internet, "
        "puis un second LAN et un second ordinateur, un message va passer entre les mains des différentes couches à "
        "plusieurs reprises.</p>" + figure_parcours()
        + _remarque("Les ordinateurs et smartphones sont capables de mettre en œuvre toutes les couches. Les routeurs sont "
                    "capables de gérer les protocoles des couches 1 à 3, les <i>switchs</i> et <i>hotspots</i> sont "
                    "capables de gérer les protocoles des couches 1 et 2."))

    s7 = g.course_section(7, "cr-essentiel", "L'essentiel à retenir",
        '<p class="cours-defi">Retourne chaque carte : elle résume une partie du cours.</p>' + g.cartes_html(CARTES))
    s8 = g.course_section(8, "cr-jeux", "Jeux : classe les notions",
        "<h3>Adresse MAC ou adresse IP ?</h3>" + g.jeu_html(JEU_ADRESSES, ADRESSES, "cr-jeu-adr")
        + "<h3>À quelle couche du modèle OSI ?</h3>" + g.jeu_html(JEU_COUCHES, COUCHES, "cr-jeu-osi"))
    s9 = g.quiz_section(9, "cr-quiz", QUIZ, "qr_")
    nav = g.course_nav([("cr-liaison", "Liaison"), ("cr-mise", "Mise en réseau"), ("cr-wan-s", "WAN et Internet"),
                        ("cr-lan", "Adressage IP et LAN"), ("cr-logiciels", "Logiciels"), ("cr-osi-s", "Modèle OSI"),
                        ("cr-essentiel", "L'essentiel"), ("cr-jeux", "Jeux"), ("cr-quiz", "Quiz")])
    return f"""<div class="cours" id="cours-reseaux">
{g.course_head("Cours 1", "Niveau 1", "Réseaux informatiques",
               "De la liaison point-à-point au modèle OSI. <b>Problématique :</b> comment des machines, reliées par des "
               "câbles ou des ondes, parviennent-elles à s'identifier et à échanger des messages de manière fiable, d'un "
               "réseau local jusqu'à l'autre bout d'Internet ? Environ 2 heures, avec dix-huit figures animées ou "
               "interactives, des simulateurs, deux jeux et un quiz.")}
{g.course_fiche(OBJECTIFS, PREREQUIS)}
{nav}
{s1}{s2}{s3}{s4}{s5}{s6}{s7}{s8}{s9}
{g.course_foot(("?ex=qcm-reseaux", "S'entraîner : QCM 1.1"), ("?ex=site-html", "Exercice 1.2 : mon premier site"),
              ("?ex=adressage-maison", "Exercice 1.3 : le plan d'adressage de la maison"),
              ("?ex=requete-http", "Exercice 2.1 : suivre une requête"),
              ("?ex=etude-mediatheque", "Étude 1 : le réseau d'une médiathèque"))}
</div>"""


def cours(g):
    """L'entrée de COURS : la carte de l'accueil, le rendu, le script et le style du cours."""
    return {"key": "cours-reseaux", "tag": "Cours 1", "level": "Niveau 1", "title": "Réseaux informatiques",
            "mots": ["Liaisons", "MAC et IP", "Routage", "Client-serveur", "Modèle OSI"], "vign": "carte-cours-1",
            "alt": "Les sept couches du modèle OSI", "render": lambda: render(g), "js": CR_JS,
            "init": "initCoursReseaux", "css": CR_CSS}




# ============================================================ comportement
CR_JS = r"""
  function initCoursReseaux(home) {
    initCours(home);
    var NS = "http://www.w3.org/2000/svg";
    var calme = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
    function q(s, r) { return (r || home).querySelector(s); }
    function qa(s, r) { return Array.prototype.slice.call((r || home).querySelectorAll(s)); }
    function mk(tag, at, parent) { var el = document.createElementNS(NS, tag); for (var k in at) el.setAttribute(k, at[k]); if (parent) parent.appendChild(el); return el; }
    function tx(parent, x, y, s, cls, anchor) { var t = mk("text", { x: x, y: y, "class": cls || "", "text-anchor": anchor || "start" }, parent); t.textContent = s; return t; }
    function pad(s, n) { s = String(s); while (s.length < n) s = "0" + s; return s; }
    function points(s) { return s.trim().split(/\s+/).map(function (p) { return p.split(",").map(Number); }); }
    function presser(groupe, b) { qa("[data-" + groupe + "]", b.closest(".cr-fig")).forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); }); }
    // une animation en cours est abandonnée dès qu'on la relance : chaque lancement reçoit sa garde
    function garde() { var n = 0; return function () { var id = ++n; return function () { return id === n; }; }; }
    function apres(ms, fin, g) { setTimeout(function () { if (!g || g()) fin(); }, calme ? 0 : ms); }
    // déplace un jeton (groupe SVG) le long d'une ligne brisée, à vitesse constante (unités du dessin par seconde)
    function trajet(el, pts, v, fin, g) {
      var L = [0], i;
      for (i = 1; i < pts.length; i++) L.push(L[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
      var tot = L[L.length - 1], dur = calme ? 1 : Math.max(1, tot / v * 1000), t0 = null;
      function pos(d) {
        for (var k = 1; k < pts.length; k++) if (d <= L[k] || k === pts.length - 1) {
          var a = Math.min(1, Math.max(0, (d - L[k - 1]) / ((L[k] - L[k - 1]) || 1)));
          return [pts[k - 1][0] + a * (pts[k][0] - pts[k - 1][0]), pts[k - 1][1] + a * (pts[k][1] - pts[k - 1][1])];
        }
        return pts[0];
      }
      function place(p) { el.setAttribute("transform", "translate(" + p[0].toFixed(1) + " " + p[1].toFixed(1) + ")"); }
      place(pts[0]);
      function pas(t) {
        if (g && !g()) return;
        if (t0 === null) t0 = t;
        var k = Math.min(1, (t - t0) / dur);
        place(pos(k * tot));
        if (k < 1) requestAnimationFrame(pas); else if (fin) fin();
      }
      requestAnimationFrame(pas);
    }
    // texte d'un jeton : le cadre s'ajuste à sa longueur
    function etiquette(j, s) {
      var t = j.querySelector("text"), r = j.querySelector("rect");
      t.textContent = s;
      var w = Math.max(40, (t.getComputedTextLength ? t.getComputedTextLength() : s.length * 7) + 18);
      r.setAttribute("x", (-w / 2).toFixed(1)); r.setAttribute("width", w.toFixed(1));
    }
    // enchaîne des étapes [points, texte de la légende, avant(), vitesse] le long d'un même jeton
    function parcours(j, etapes, cap, g, fin) {
      (function suite(i) {
        if (i >= etapes.length) { if (fin) fin(); return; }
        var e = etapes[i];
        if (e.avant) e.avant();
        if (e.t) cap.innerHTML = e.t;
        if (!e.p) { apres(e.pause || 900, function () { suite(i + 1); }, g); return; }
        trajet(j, e.p, e.v || 260, function () { apres(e.pause || 250, function () { suite(i + 1); }, g); }, g);
      })(0);
    }
    function lireIP(s) {
      var m = String(s).trim().split(".");
      if (m.length !== 4 || !m.every(function (x) { return /^\d{1,3}$/.test(x) && +x <= 255; })) return null;
      return m.map(Number);
    }
    function nb(x) { return x.toLocaleString("fr-FR"); }

    // ---------- figure 1 : full-duplex ou half-duplex ----------
    (function () {
      var f = q("#cr-duplex"), lab = q("#cr-dx-lab"), t = q("#cr-dx-t"), mode = "full", sens = 0;
      function maj() {
        f.setAttribute("data-mode", mode);
        f.classList.toggle("dx-ba", mode === "half" && sens === 1);
        lab.textContent = mode === "full" ? "A et B émettent en même temps" : (sens ? "B émet, A écoute" : "A émet, B écoute");
        t.textContent = mode === "full" ? "Full-duplex : les données circulent dans les deux sens en même temps, comme dans une conversation téléphonique."
          : "Half-duplex : les données ne circulent que dans un sens à la fois ; chaque machine émet à son tour, comme avec un talkie-walkie.";
      }
      qa("[data-dx]", f).forEach(function (b) { b.addEventListener("click", function () { mode = b.getAttribute("data-dx"); sens = 0; presser("dx", b); maj(); }); });
      setInterval(function () { if (mode === "half") { sens = 1 - sens; maj(); } }, 2600);
      maj();
    })();

    // ---------- figure 2 : les supports filaires ----------
    (function () {
      var f = q("#cr-supports");
      qa("[data-sup]", f).forEach(function (b) {
        b.addEventListener("click", function () {
          presser("sup", b);
          qa(".cr-pane", f).forEach(function (p) { p.hidden = p.getAttribute("data-pane") !== b.getAttribute("data-sup"); });
        });
      });
      qa(".cr-leg-b, .cr-rep", f).forEach(function (b) {
        b.addEventListener("click", function () {
          var k = b.getAttribute("data-part");
          qa("[data-part]", f).forEach(function (el) { el.classList.toggle("cr-hl", el.getAttribute("data-part") === k); });
        });
      });
    })();

    // ---------- figure 3 : portée du Bluetooth et du Wi-Fi ----------
    (function () {
      var r = q("#cr-portee"), o = q("#cr-portee-o"), app = q("#cr-pt-app"), t = q("#cr-portee-t");
      function etat(ok) { return ok ? '<b class="ok">✔ capté</b>' : '<b class="ko">✘ hors de portée</b>'; }
      function maj() {
        var d = +r.value;
        o.textContent = d + " m";
        app.setAttribute("transform", "translate(" + (90 + 12.6 * d).toFixed(1) + " 40)");
        t.innerHTML = "À " + d + " m : Bluetooth " + etat(d <= 10) + " — Wi-Fi " + etat(d <= 40) + ".";
      }
      r.addEventListener("input", maj);
      maj();
    })();

    // ---------- simulateur de débit ----------
    (function () {
      var f = q("#cr-deb-f"), l = q("#cr-deb-l"), bar = q("#cr-deb-bar"), go = q("#cr-deb-go"), note = q("#cr-deb-note"), g = garde(), D;
      var UNITE = { Mo: 1e6, Go: 1e9 };
      function duree(s) {
        if (s < 1) return fr(s * 1000, s < 0.01 ? 1 : 0) + " ms";
        if (s < 60) return fr(s, s < 10 ? 1 : 0) + " s";
        s = Math.round(s);
        if (s < 3600) return Math.floor(s / 60) + " min " + pad(s % 60, 2) + " s";
        return Math.floor(s / 3600) + " h " + pad(Math.round((s % 3600) / 60), 2) + " min";
      }
      function calc() {
        var of = f.selectedOptions[0], ol = l.selectedOptions[0];
        var qv = +of.getAttribute("data-q"), u = of.getAttribute("data-u"), bits = qv * UNITE[u] * 8, deb = +ol.getAttribute("data-d");
        D = { bits: bits, deb: deb, t: bits / deb };
        q("#cr-deb-q").textContent = qv + " " + u + " = " + nb(bits / 1e6) + " Mbit";
        q("#cr-deb-d").textContent = nb(deb / 1e6) + " Mbit/s";
        q("#cr-deb-t").textContent = duree(D.t);
        q("#cr-deb-calc").innerHTML = "Durée = quantité de données ÷ débit = " + nb(bits / 1e6) + " Mbit ÷ " + nb(deb / 1e6) +
          " Mbit/s ≈ <b>" + duree(D.t) + "</b> (un octet = 8 bits : " + qv + " " + u + " = " + nb(qv * UNITE[u]) + " octets).";
        g(); bar.style.width = "0%"; bar.parentNode.setAttribute("aria-valuenow", "0"); note.textContent = "";
      }
      go.addEventListener("click", function () {
        var ok = g(), anim = Math.min(D.t, 5) * 1000, t0 = null;
        note.textContent = D.t > 5 ? "Animation accélérée : le transfert réel dure " + duree(D.t) + "." : "Transfert en temps réel.";
        function pas(t) {
          if (!ok()) return;
          if (t0 === null) t0 = t;
          var k = calme ? 1 : Math.min(1, (t - t0) / Math.max(anim, 1));
          bar.style.width = (k * 100).toFixed(1) + "%";
          bar.parentNode.setAttribute("aria-valuenow", Math.round(k * 100));
          if (k < 1) requestAnimationFrame(pas); else note.textContent = "Transfert terminé en " + duree(D.t) + ".";
        }
        requestAnimationFrame(pas);
      });
      f.addEventListener("change", calc); l.addEventListener("change", calc);
      calc();
    })();

    // ---------- figure 4 : le switch aiguille les trames d'après l'adresse MAC ----------
    (function () {
      var MACS = __MACS__, de = q("#cr-sw-de"), a = q("#cr-sw-a"), j = q("#cr-sw-trame"), t = q("#cr-sw-t"), sw = q("#cr-sw-sw"), g = garde();
      function chemin(i) { return points(q("#cr-swc-" + i).getAttribute("data-pts")); }
      function eteindre() {
        qa("#cr-sw-tab tr, #cr-switch .cr-pc").forEach(function (x) { x.classList.remove("cr-on", "cr-dest"); });
        sw.classList.remove("cr-on");
      }
      q("#cr-sw-go").addEventListener("click", function () {
        var s = +de.value, d = +a.value, ok = g();
        eteindre();
        if (s === d) { j.setAttribute("opacity", "0"); t.textContent = "Choisis deux machines différentes."; return; }
        var aller = chemin(s), retour = chemin(d).reverse();
        etiquette(j, "→ " + MACS[d - 1]);
        j.setAttribute("opacity", "1");
        q("#cr-swp-" + s).classList.add("cr-on");
        parcours(j, [
          { p: aller, v: 240, t: "PC" + s + " envoie une trame étiquetée avec l'adresse MAC du destinataire, <code>" + MACS[d - 1] + "</code>, et la sienne, <code>" + MACS[s - 1] + "</code>." },
          { avant: function () { sw.classList.add("cr-on"); q('#cr-sw-tab tr[data-port="' + d + '"]').classList.add("cr-on"); },
            t: "Le switch lit l'adresse MAC du destinataire : d'après sa table, cette machine est branchée sur le port " + d + ".", pause: 1100 },
          { p: [aller[aller.length - 1], [380, 144], retour[0]].concat(retour.slice(1)), v: 240,
            t: "Il fait passer la trame vers le port " + d + " seulement." }
        ], t, ok, function () {
          q("#cr-swp-" + d).classList.add("cr-dest");
          t.innerHTML = "Trame reçue par PC" + d + ". Les autres machines ne l'ont pas reçue : le switch ne l'a envoyée que vers le port " + d + ".";
        });
      });
    })();

    // ---------- figure 5 : les topologies, et ce que devient le réseau quand on coupe une liaison ----------
    (function () {
      var svgT = q("#cr-topo-svg"), t = q("#cr-topo-t"), cur = "etoile", coupe = {}, panne = {};
      var BUSX = [110, 245, 380, 515, 650];
      var T = {
        etoile: { n: [["Switch", 380, 168, "sw"], ["PC1", 140, 62], ["PC2", 380, 40], ["PC3", 620, 62], ["PC4", 190, 240], ["PC5", 570, 240]],
                  l: [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5]] },
        anneau: { n: [["PC1", 640, 150], ["PC2", 510, 240], ["PC3", 250, 240], ["PC4", 120, 150], ["PC5", 250, 52], ["PC6", 510, 52]],
                  l: [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 0]], rond: 1 },
        bus: { n: BUSX.map(function (x, i) { return ["PC" + (i + 1), x, 70]; }).concat(BUSX.map(function (x) { return ["", x, 200, "t"]; })),
               l: BUSX.map(function (x, i) { return [i, i + 5]; }).concat([[5, 6], [6, 7], [7, 8], [8, 9]]) },
        maille: { n: [["PC1", 140, 70], ["PC2", 380, 40], ["PC3", 620, 70], ["PC4", 620, 230], ["PC5", 380, 260], ["PC6", 140, 230]],
                  l: [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 0], [0, 3], [1, 4], [2, 5]] }
      };
      function groupes() {
        var o = T[cur], par = o.n.map(function (_, i) { return i; });
        function rac(i) { while (par[i] !== i) i = par[i] = par[par[i]]; return i; }
        o.l.forEach(function (l, i) { if (!coupe[i] && !panne[l[0]] && !panne[l[1]]) par[rac(l[0])] = rac(l[1]); });
        var gr = {}, ordre = [];
        o.n.forEach(function (n, i) { if (n[3]) return; var r = rac(i); if (!gr[r]) { gr[r] = []; ordre.push(r); } gr[r].push(i); });
        return ordre.map(function (r) { return gr[r]; });
      }
      function dessin() {
        var o = T[cur];
        while (svgT.firstChild) svgT.removeChild(svgT.firstChild);
        if (cur === "bus") { tx(svgT, 54, 222, "Bus", "cr-t"); }
        o.l.forEach(function (l, i) {
          var a = o.n[l[0]], b = o.n[l[1]], gl = mk("g", { "class": "cr-tl" + (coupe[i] ? " cr-coupe" : ""), "data-l": i, tabindex: 0, role: "button", "aria-label": "Liaison " + (a[0] || "bus") + " – " + (b[0] || "bus") }, svgT);
          var y1 = a[2] + (a[3] ? 0 : 20), y2 = b[2] + (b[3] ? 0 : 20);
          mk("line", { x1: a[1], y1: y1, x2: b[1], y2: y2, "class": "cr-tl-hit" }, gl);
          mk("line", { x1: a[1], y1: y1, x2: b[1], y2: y2, "class": "cr-tl-v" }, gl);
          if (coupe[i]) { var mx = (a[1] + b[1]) / 2, my = (y1 + y2) / 2; mk("path", { d: "M" + (mx - 8) + " " + (my - 8) + "l16 16m0 -16l-16 16", "class": "cr-croix" }, gl); }
        });
        var gs = groupes(), couleur = {};
        gs.forEach(function (gr, k) { gr.forEach(function (i) { couleur[i] = gs.length > 1 ? "cr-g" + (k % 4) : ""; }); });
        o.n.forEach(function (n, i) {
          if (n[3] === "t") { mk("circle", { cx: n[1], cy: n[2], r: 5, "class": "cr-tap" }, svgT); return; }
          if (n[3] === "sw") {
            var gsw = mk("g", { "class": "cr-tsw" + (panne[i] ? " cr-panne" : ""), "data-n": i, transform: "translate(" + (n[1] - 50) + " " + (n[2] - 16) + ")", tabindex: 0, role: "button", "aria-label": "Nœud central (switch)" }, svgT);
            mk("rect", { width: 100, height: 32, rx: 5, fill: "#1C2530" }, gsw);
            for (var k = 0; k < 5; k++) mk("rect", { x: 12 + 16 * k, y: 12, width: 11, height: 9, fill: "#0E1114", stroke: "#7D868F" }, gsw);
            tx(gsw, 50, 50, panne[i] ? "Switch en panne" : "Switch", "cr-t", "middle");
            if (panne[i]) mk("path", { d: "M30 -4l40 40m0 -40l-40 40", "class": "cr-croix" }, gsw);
            return;
          }
          var gp = mk("g", { "class": "cr-pc " + (couleur[i] || ""), transform: "translate(" + (n[1] - 28) + " " + (n[2] - 20) + ")" }, svgT);
          mk("rect", { width: 56, height: 40, rx: 4, fill: "#1C2530" }, gp);
          mk("rect", { x: 4, y: 4, width: 48, height: 30, rx: 1, "class": "cr-ecran", fill: "#4F8FDB" }, gp);
          mk("rect", { x: 24, y: 40, width: 8, height: 5, fill: "#46525C" }, gp);
          tx(gp, 28, 58, n[0], "cr-t", "middle");
        });
        var noms = gs.map(function (gr) { return gr.map(function (i) { return o.n[i][0]; }); }), msg;
        var nc = Object.keys(coupe).length + Object.keys(panne).length;
        if (gs.length === 1) msg = nc ? "Toutes les machines communiquent encore : les messages passent par un autre chemin." : "Toutes les machines communiquent. Coupe une liaison pour voir ce qui se passe.";
        else if (noms.every(function (x) { return x.length === 1; })) msg = "Plus aucune machine ne communique avec une autre.";
        else msg = "Le réseau est coupé en " + gs.length + " groupes qui ne communiquent plus entre eux : " + noms.map(function (x) { return "{" + x.join(", ") + "}"; }).join(" · ") + ".";
        t.textContent = msg;
      }
      function bascule(el) {
        if (el.hasAttribute("data-l")) { var i = +el.getAttribute("data-l"); if (coupe[i]) delete coupe[i]; else coupe[i] = 1; }
        else { var n = +el.getAttribute("data-n"); if (panne[n]) delete panne[n]; else panne[n] = 1; }
        dessin();
      }
      svgT.addEventListener("click", function (e) { var el = e.target.closest(".cr-tl, .cr-tsw"); if (el) bascule(el); });
      svgT.addEventListener("keydown", function (e) { var el = e.target.closest && e.target.closest(".cr-tl, .cr-tsw"); if (el && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); bascule(el); } });
      qa("[data-topo]").forEach(function (b) {
        b.addEventListener("click", function () {
          cur = b.getAttribute("data-topo"); coupe = {}; panne = {};
          presser("topo", b);
          qa("[data-topo-txt]").forEach(function (p) { p.hidden = p.getAttribute("data-topo-txt") !== cur; });
          dessin();
        });
      });
      q("#cr-topo-reset").addEventListener("click", function () { coupe = {}; panne = {}; dessin(); });
      dessin();
    })();

    // ---------- figure 6 : l'adresse MAC, octet par octet ----------
    (function () {
      var inp = q("#cr-mac"), box = q("#cr-mac-oct"), t = q("#cr-mac-t"), etq = q("#cr-mac-etq-t");
      function maj() {
        var m = inp.value.trim().split(/[:\-]/);
        var ok = m.length === 6 && m.every(function (x) { return /^[0-9a-fA-F]{2}$/.test(x); });
        box.innerHTML = "";
        inp.setAttribute("aria-invalid", ok ? "false" : "true");
        if (!ok) { t.className = "cr-cap ko"; t.textContent = "Une adresse MAC compte 6 couples de chiffres hexadécimaux (0 à 9 et A à F), séparés par « : » ou « - »."; return; }
        etq.textContent = m.join(":").toUpperCase();
        m.forEach(function (x, i) {
          var b = document.createElement("button");
          b.type = "button"; b.className = "cr-oct" + (i < 3 ? " cr-oct-f" : ""); b.setAttribute("aria-pressed", "false");
          b.innerHTML = "<b>" + x.toUpperCase() + "</b><span>" + pad(parseInt(x, 16).toString(2), 8) + "</span>";
          b.addEventListener("click", function () { b.setAttribute("aria-pressed", b.getAttribute("aria-pressed") === "true" ? "false" : "true"); });
          box.appendChild(b);
        });
        t.className = "cr-cap";
        t.innerHTML = "6 octets, soit 6 × 8 = <b>48 bits</b>. Les trois premiers (<b>" + m.slice(0, 3).join(":").toUpperCase() + "</b>) identifient le fabricant de la carte ; les trois derniers, la carte elle-même.";
      }
      inp.addEventListener("input", maj);
      maj();
    })();

    // ---------- figure 7 : deux réseaux locaux reliés par leurs routeurs passerelles ----------
    (function () {
      var j = q("#cr-wan-j"), t = q("#cr-wan-t"), g = garde();
      function on(ids) { qa("#cr-wan .cr-on").forEach(function (x) { x.classList.remove("cr-on"); }); ids.forEach(function (i) { q("#" + i).classList.add("cr-on"); }); }
      q("#cr-wan-go").addEventListener("click", function () {
        var ok = g();
        etiquette(j, "trame"); j.setAttribute("opacity", "1");
        parcours(j, [
          { avant: function () { on(["cr-wan-A1"]); }, p: [[76, 106], [145, 140]], t: "Dans le réseau local 1, A1 envoie le message au switch, sous forme de trame." },
          { avant: function () { on(["cr-wan-swA"]); }, p: [[145, 140], [175, 150], [245, 158], [310, 158], [310, 192]], t: "Le destinataire n'est pas dans ce réseau local : le switch envoie la trame au routeur passerelle." },
          { avant: function () { on(["cr-wan-rA"]); etiquette(j, "paquet"); }, p: [[310, 192], [310, 262], [690, 262], [690, 192]], v: 330, t: "Le routeur passerelle fait passer le message vers le WAN. Quand une trame circule dans un internet, elle est appelée <b>paquet</b>." },
          { avant: function () { on(["cr-wan-rB"]); etiquette(j, "trame"); }, p: [[690, 192], [690, 158], [625, 158], [595, 150]], t: "Le routeur passerelle du réseau local 2 fait entrer le message dans son LAN." },
          { avant: function () { on(["cr-wan-swB"]); }, p: [[585, 140], [676, 106]], t: "Le switch l'aiguille vers B3." }
        ], t, ok, function () { on(["cr-wan-B3"]); t.innerHTML = "Message reçu par B3, dans le réseau local 2."; });
      });
    })();

    // ---------- figure 8 : ce que contient la box ----------
    (function () {
      var f = q("#cr-box"), b = q("#cr-box-go"), t = q("#cr-box-t");
      function montrer(k) {
        qa(".cr-bx-m", f).forEach(function (m) { m.classList.toggle("cr-on", m.getAttribute("data-mod") === k); });
        qa("[data-mod-txt]", f).forEach(function (p) { p.hidden = p.getAttribute("data-mod-txt") !== k; });
      }
      b.addEventListener("click", function () {
        var o = !f.classList.contains("ouverte");
        f.classList.toggle("ouverte", o);
        b.setAttribute("aria-pressed", o ? "true" : "false");
        b.textContent = o ? "Refermer la box" : "Ouvrir la box";
        t.textContent = o ? "La box réunit quatre appareils : touche chacun d'eux." : "";
        if (!o) montrer("");
      });
      qa(".cr-bx-m", f).forEach(function (m) {
        function choisir() { if (f.classList.contains("ouverte")) montrer(m.getAttribute("data-mod")); }
        m.addEventListener("click", choisir);
        m.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); choisir(); } });
      });
    })();

    // ---------- figure 9 : le routage dans un maillage de routeurs ----------
    (function () {
      var S = q("#cr-rt-svg"), t = q("#cr-rt-t"), g = garde();
      var N = [[60, 120, 1], [60, 290, 1], [170, 60, 0], [170, 200, 0], [170, 335, 0], [300, 120, 0], [300, 280, 0], [390, 40, 1], [410, 200, 0],
               [390, 360, 1], [510, 120, 0], [510, 280, 0], [610, 60, 0], [610, 200, 0], [610, 340, 0], [710, 120, 1], [710, 290, 1]];
      var L = [[0, 2], [0, 3], [1, 3], [1, 4], [2, 5], [2, 7], [3, 5], [3, 6], [4, 6], [4, 9], [5, 7], [5, 8], [6, 8], [6, 9], [7, 12],
               [8, 10], [8, 11], [5, 10], [6, 11], [9, 14], [10, 12], [10, 13], [11, 13], [11, 14], [12, 15], [13, 15], [13, 16], [14, 16]];
      var coupe = {}, dep = 0, arr = 16, attente = 0, route = null;
      function voisins(i) { var v = []; L.forEach(function (l, k) { if (coupe[k]) return; if (l[0] === i) v.push([l[1], k]); else if (l[1] === i) v.push([l[0], k]); }); return v; }
      function chercher() {
        var prec = {}, vu = {}, file = [dep]; vu[dep] = 1;
        while (file.length) { var i = file.shift(); if (i === arr) break; voisins(i).forEach(function (v) { if (!vu[v[0]]) { vu[v[0]] = 1; prec[v[0]] = [i, v[1]]; file.push(v[0]); } }); }
        if (!vu[arr]) return null;
        var n = [arr], l = [], c = arr;
        while (c !== dep) { l.unshift(prec[c][1]); c = prec[c][0]; n.unshift(c); }
        return { n: n, l: l };
      }
      function dessin() {
        while (S.firstChild) S.removeChild(S.firstChild);
        var surRoute = {}; if (route) route.l.forEach(function (k) { surRoute[k] = 1; });
        L.forEach(function (l, k) {
          var a = N[l[0]], b = N[l[1]], gl = mk("g", { "class": "cr-tl" + (coupe[k] ? " cr-coupe" : "") + (surRoute[k] ? " cr-route" : ""), "data-l": k, tabindex: 0, role: "button", "aria-label": "Liaison R" + (l[0] + 1) + " – R" + (l[1] + 1) }, S);
          mk("line", { x1: a[0], y1: a[1], x2: b[0], y2: b[1], "class": "cr-tl-hit" }, gl);
          mk("line", { x1: a[0], y1: a[1], x2: b[0], y2: b[1], "class": "cr-tl-v" }, gl);
          if (coupe[k]) { var mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2; mk("path", { d: "M" + (mx - 7) + " " + (my - 7) + "l14 14m0 -14l-14 14", "class": "cr-croix" }, gl); }
        });
        N.forEach(function (n, i) {
          var gr = mk("g", { "class": "cr-rtn" + (n[2] ? " cr-rtp" : "") + (i === dep ? " cr-dep" : "") + (i === arr ? " cr-arr" : ""), "data-r": i, transform: "translate(" + n[0] + " " + n[1] + ")" }, S);
          if (n[2]) { gr.setAttribute("tabindex", "0"); gr.setAttribute("role", "button"); gr.setAttribute("aria-label", "Routeur passerelle R" + (i + 1)); }
          mk("path", { d: "M-20 -4v10a20 7 0 0 0 40 0V-4", "class": "cr-rtn-c" }, gr);
          mk("ellipse", { cy: -4, rx: 20, ry: 7, "class": "cr-rtn-h" }, gr);
          tx(gr, 0, 26, "R" + (i + 1), "cr-ts cr-tb2", "middle");
          if (i === dep || i === arr) tx(gr, 0, -16, i === dep ? "départ" : "arrivée", "cr-ts cr-tb2", "middle");
        });
        var p = mk("g", { id: "cr-rt-pq", opacity: 0 }, S);
        mk("circle", { r: 7, fill: "#F2B705", stroke: "#1C2530", "stroke-width": 2 }, p);
      }
      function calculer(rejouer) {
        var avant = route;
        route = attente ? null : chercher();
        dessin();
        if (attente) { t.textContent = "Départ : R" + (dep + 1) + ". Touche maintenant la passerelle d'arrivée."; return; }
        if (!route) { t.textContent = "Aucune route ne relie R" + (dep + 1) + " à R" + (arr + 1) + " : trop de liaisons sont coupées."; return; }
        var txt = "Route : " + route.n.map(function (i) { return "R" + (i + 1); }).join(" → ") + " (" + route.l.length + " liaisons).";
        if (rejouer === "coupe" && avant && avant.n.join() !== route.n.join()) txt = "La route précédente est coupée : le paquet en emprunte une autre. " + txt;
        t.textContent = txt;
        var pq = q("#cr-rt-pq", S), ok = g();
        pq.setAttribute("opacity", "1");
        trajet(pq, route.n.map(function (i) { return [N[i][0], N[i][1]]; }), 300, null, ok);
      }
      function choisir(i) {
        if (!N[i][2]) return;
        if (!attente) { dep = i; attente = 1; } else { if (i === dep) return; arr = i; attente = 0; }
        calculer();
      }
      S.addEventListener("click", function (e) {
        var r = e.target.closest(".cr-rtn"), l = e.target.closest(".cr-tl");
        if (r) { choisir(+r.getAttribute("data-r")); return; }
        if (l) { var k = +l.getAttribute("data-l"); if (coupe[k]) delete coupe[k]; else coupe[k] = 1; calculer("coupe"); }
      });
      S.addEventListener("keydown", function (e) {
        if (e.key !== "Enter" && e.key !== " ") return;
        var el = e.target.closest && e.target.closest(".cr-rtn, .cr-tl");
        if (!el) return;
        e.preventDefault();
        el.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      });
      q("#cr-rt-reset").addEventListener("click", function () { coupe = {}; attente = 0; calculer(); });
      calculer();
    })();

    // ---------- figure 10 : les dorsales ----------
    (function () {
      var t = q("#cr-dors-t");
      qa(".cr-dors").forEach(function (d) {
        function nommer() {
          qa(".cr-dors").forEach(function (x) { x.classList.toggle("cr-on", x === d); });
          t.innerHTML = "<b>" + d.getAttribute("data-nom") + "</b> : des câbles en fibre optique, posés au fond des océans, relient ces zones géographiques.";
        }
        d.addEventListener("click", nommer);
        d.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); nommer(); } });
      });
    })();

    // ---------- est-ce une adresse IP ? ----------
    (function () {
      var inp = q("#cr-ipv-in"), t = q("#cr-ipv-t");
      function maj() {
        var s = inp.value.trim(), m = s.split("."), ip = lireIP(s), msg;
        if (ip) msg = '<b class="ok">✔ Adresse IP valide</b> : 4 nombres décimaux, chacun compris entre 0 et 255.';
        else if (m.length !== 4) msg = '<b class="ko">✘ Ce n\'est pas une adresse IP</b> : il faut 4 nombres séparés par des points (ici ' + m.length + ").";
        else {
          var x = m.filter(function (v) { return !/^\d{1,3}$/.test(v); })[0];
          msg = x !== undefined ? '<b class="ko">✘ Ce n\'est pas une adresse IP</b> : « ' + x + " » n'est pas un nombre décimal."
            : '<b class="ko">✘ Ce n\'est pas une adresse IP</b> : ' + m.filter(function (v) { return +v > 255; })[0] + " dépasse 255.";
        }
        t.innerHTML = msg;
      }
      inp.addEventListener("input", maj);
      maj();
    })();

    // ---------- figure 11 : découper une adresse avec son masque ----------
    (function () {
      var ip = q("#cr-dec-ip"), m = q("#cr-dec-m"), tab = q("#cr-dec-tab"), t = q("#cr-dec-t");
      var MACH = { "255.0.0.0": "16 777 214", "255.255.0.0": "65 534", "255.255.255.0": "254" };
      function maj() {
        var a = lireIP(ip.value), k = m.value.split(".");
        if (!a) { tab.innerHTML = ""; t.innerHTML = '<b class="ko">Écris une adresse IP valide</b> : 4 nombres de 0 à 255.'; return; }
        var net = [], host = [];
        tab.innerHTML = '<div class="cr-dec-l">' + a.map(function (x, i) { (k[i] === "255" ? net : host).push(x); return '<span class="' + (k[i] === "255" ? "cr-net" : "cr-host") + '">' + x + "</span>"; }).join("") +
          '</div><div class="cr-dec-l cr-dec-m">' + k.map(function (x) { return "<span>" + x + "</span>"; }).join("") + "</div>";
        t.innerHTML = '<span class="cr-net-t">net-ID : <b>' + net.join(".") + "</b></span> (identifie le réseau) — " +
          '<span class="cr-host-t">host-ID : <b>' + host.join(".") + "</b></span> (identifie la machine). Avec le masque " + m.value +
          ", on peut connecter " + MACH[m.value] + " machines.";
      }
      ip.addEventListener("input", maj); m.addEventListener("change", maj);
      qa("[data-dec]").forEach(function (b) { b.addEventListener("click", function () { var v = b.getAttribute("data-dec").split("|"); ip.value = v[0]; m.value = v[1]; maj(); }); });
      maj();
    })();

    // ---------- figure 12 : adresse privée, adresse publique (traduction d'adresses) ----------
    (function () {
      var PCS = __PCS_NAT__, SRV = __SERVICES__, PUB = "92.169.148.17";
      var j = q("#cr-nat-j"), t = q("#cr-nat-t"), g = garde();
      q("#cr-nat-go").addEventListener("click", function () {
        var p = PCS[+q("#cr-nat-p").value], s = SRV[+q("#cr-nat-s").value], ok = g();
        var P = [p[1] + 28, p[2] + 20], R = [380, 150], W = [150, 150], V = [s[2], s[3]];
        qa("#cr-nat .cr-on").forEach(function (x) { x.classList.remove("cr-on"); });
        etiquette(j, p[0] + " → " + s[1]); j.setAttribute("opacity", "1");
        parcours(j, [
          { p: [P, R], t: "L'ordinateur envoie sa requête. Sur le paquet : de <b class=\"cr-rouge\">" + p[0] + "</b> (son adresse privée) vers <b>" + s[1] + "</b>." },
          { avant: function () { q("#cr-nat-r").classList.add("cr-on"); etiquette(j, PUB + " → " + s[1]); }, pause: 1200,
            t: "Le routeur remplace l'adresse privée de l'émetteur par son adresse publique, <b class=\"cr-bleu\">" + PUB + "</b> : c'est la traduction d'adresses (NAT)." },
          { p: [R, W, V], t: "Sur Internet, seule l'adresse publique de la box est visible." },
          { avant: function () { etiquette(j, s[1] + " → " + PUB); }, p: [V, W, R], t: "Le serveur répond à l'adresse publique, celle du routeur." },
          { avant: function () { etiquette(j, s[1] + " → " + p[0]); }, pause: 1200,
            t: "Le routeur retrouve l'ordinateur du LAN qui attendait cette réponse et y remet son adresse privée, <b class=\"cr-rouge\">" + p[0] + "</b>." },
          { p: [R, P] }
        ], t, ok, function () { t.innerHTML = "Réponse reçue par l'ordinateur " + p[0] + ". Pour le serveur, la requête venait de " + PUB + "."; });
      });
    })();

    // ---------- adresse privée ou publique ? ----------
    (function () {
      var inp = q("#cr-priv-in"), t = q("#cr-priv-t");
      function maj() {
        var a = lireIP(inp.value), plage = null;
        if (!a) { t.innerHTML = '<b class="ko">Écris une adresse IP valide</b> : 4 nombres de 0 à 255.'; return; }
        if (a[0] === 10) plage = "10.0.0.0 à 10.255.255.255";
        else if (a[0] === 172 && a[1] >= 16 && a[1] <= 31) plage = "172.16.0.0 à 172.31.255.255";
        else if (a[0] === 192 && a[1] === 168) plage = "192.168.0.0 à 192.168.255.255";
        t.innerHTML = plage ? '<b class="cr-rouge">Adresse privée</b>, réservée aux LAN (plage ' + plage + ") : elle ne peut pas servir sur Internet."
          : '<b class="cr-bleu">Adresse publique</b> : elle n\'appartient à aucune des trois plages réservées aux LAN.';
      }
      inp.addEventListener("input", maj);
      maj();
    })();

    // ---------- figure 13 : sous-réseaux logiques dans un LAN ----------
    (function () {
      var X = [40, 230, 420, 610], j = q("#cr-sr-j"), t = q("#cr-sr-t"), mat = q("#cr-sr-mat"), g = garde();
      function ips() { return [1, 2, 3, 4].map(function (i) { return lireIP(q("#cr-sr-in" + i).value); }); }
      function net(a) { return a ? a.slice(0, 3).join(".") : null; }
      function maj() {
        var A = ips(), nets = [], h = "<thead><tr><th>Peut communiquer avec…</th>";
        A.forEach(function (a, i) {
          var n = net(a), k = nets.indexOf(n);
          if (n && k < 0) { nets.push(n); k = nets.length - 1; }
          q("#cr-sr-ip" + (i + 1)).textContent = a ? a.join(".") : "adresse invalide";
          q("#cr-sr-p" + (i + 1)).setAttribute("class", a ? "cr-g" + (k % 4) : "cr-inv");
          q("#cr-sr-in" + (i + 1)).setAttribute("aria-invalid", a ? "false" : "true");
          h += "<th>PC" + (i + 1) + "</th>";
        });
        h += "</tr></thead><tbody>";
        A.forEach(function (a, i) {
          h += '<tr><th scope="row">PC' + (i + 1) + "</th>";
          A.forEach(function (b, k) { h += i === k ? "<td>—</td>" : (a && b && net(a) === net(b) ? '<td class="ok">✔</td>' : '<td class="ko">✘</td>'); });
          h += "</tr>";
        });
        mat.innerHTML = h + "</tbody>";
        var n = nets.length;
        t.textContent = n === 1 ? "Les quatre PC ont le même net-ID : un seul sous-réseau logique." : "Ce LAN physique comporte " + n + " sous-réseaux logiques (une couleur par net-ID).";
      }
      q("#cr-sr-go").addEventListener("click", function () {
        var s = +q("#cr-sr-de").value, d = +q("#cr-sr-a").value, A = ips(), ok = g();
        if (s === d) { t.textContent = "Choisis deux PC différents."; return; }
        if (!A[s - 1] || !A[d - 1]) { t.textContent = "Corrige d'abord les adresses invalides."; return; }
        var P = function (i) { return [X[i - 1] + 58, 126]; };
        etiquette(j, "message"); j.setAttribute("opacity", "1");
        if (net(A[s - 1]) === net(A[d - 1])) {
          parcours(j, [{ p: [P(s), [380, 205], P(d)], t: "Même net-ID (" + net(A[s - 1]) + ") : le message part vers PC" + d + "." }], t, ok,
            function () { t.textContent = "PC" + s + " et PC" + d + " ont le même net-ID (" + net(A[s - 1]) + ") : ils communiquent."; });
        } else {
          parcours(j, [{ p: [P(s), [P(s)[0], 150], P(s)], v: 120, t: "PC" + s + " prépare son message…" }], t, ok, function () {
            j.setAttribute("opacity", "0");
            t.textContent = "net-ID différents (" + net(A[s - 1]) + " et " + net(A[d - 1]) + ") : PC" + s + " ne peut pas communiquer avec PC" + d + ", bien qu'ils soient reliés au même switch.";
          });
        }
      });
      qa(".cr-sr-in input").forEach(function (i) { i.addEventListener("input", maj); });
      maj();
    })();

    // ---------- figure 14 : requête et réponse HTTP ----------
    (function () {
      var PAGES = {
        "/index.html": ['<h4>Bienvenue sur mon site</h4><p>Ce site présente le réseau de la maison.</p><p><u>Contact</u></p>',
                        '<!DOCTYPE html>\n<html lang="fr">\n  <head>\n    <title>Accueil</title>\n    <link rel="stylesheet" href="style.css">\n  </head>\n  <body>\n    <h1>Bienvenue sur mon site</h1>\n    <p>Ce site présente le réseau de la maison.</p>\n    <a href="contact.html">Contact</a>\n  </body>\n</html>'],
        "/contact.html": ['<h4>Contact</h4><p>Écris-moi à l\'adresse indiquée.</p>',
                          '<!DOCTYPE html>\n<html lang="fr">\n  <head>\n    <title>Contact</title>\n    <link rel="stylesheet" href="style.css">\n  </head>\n  <body>\n    <h1>Contact</h1>\n    <p>Écris-moi à l\'adresse indiquée.</p>\n  </body>\n</html>']
      };
      var j = q("#cr-http-j"), t = q("#cr-http-t"), page = q("#cr-http-page"), g = garde();
      function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
      q("#cr-http-go").addEventListener("click", function () {
        var u = q("#cr-http-url").value, P = PAGES[u], ok = g();
        qa("#cr-http-disque text").forEach(function (x) { x.classList.remove("cr-on", "cr-ko"); });
        q("#cr-http-barre").textContent = "www.example.org" + u;
        q("#cr-http-req").textContent = "GET " + u + " HTTP/1.1\nHost: www.example.org";
        q("#cr-http-rep").textContent = "";
        page.innerHTML = '<p class="small">Chargement…</p>';
        etiquette(j, "Requête : GET " + u); j.setAttribute("opacity", "1");
        parcours(j, [
          { p: [[260, 80], [520, 80]], t: "1. Le navigateur (client) envoie une <b>requête</b> HTTP : il demande la page <code>" + u + "</code>." },
          { avant: function () { j.setAttribute("opacity", "0"); var f = q('#cr-http-disque text[data-f="' + u + '"]'); if (f) f.classList.add("cr-on"); else q("#cr-http-disque").classList.add("cr-cherche"); },
            pause: 1100, t: "2. Le serveur cherche la ressource demandée sur son disque dur…" + (P ? "" : " Elle n'y est pas.") },
          { avant: function () { q("#cr-http-disque").classList.remove("cr-cherche"); etiquette(j, P ? "Réponse : 200 OK" : "Réponse : 404 Not Found"); j.setAttribute("opacity", "1"); },
            p: [[520, 124], [260, 124]],
            t: P ? "3. Le serveur envoie sa <b>réponse</b> : le code HTML et CSS de la page." : "3. Le serveur répond que la page n'existe pas : erreur 404." }
        ], t, ok, function () {
          j.setAttribute("opacity", "0");
          q("#cr-http-rep").textContent = P ? "HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + P[1] : "HTTP/1.1 404 Not Found";
          page.innerHTML = P ? P[0] : '<h4>Erreur 404</h4><p>La page demandée est introuvable.</p>';
          t.innerHTML = P ? "4. Le navigateur affiche la page à partir du code reçu." : "4. Le navigateur affiche le message d'erreur.";
        });
      });
    })();

    // ---------- figure 15 : segments et accusés de réception (TCP) ----------
    (function () {
      var SEG = __SEGMENTS__, vol = q("#cr-tcp-vol"), t = q("#cr-tcp-t"), recu = q("#cr-tcp-recu"), g = garde();
      var VIT = [360, 280, 460, 340], DEP = [0, 300, 600, 900];
      function jeton(n, cls) {
        var j = mk("g", { "class": "cr-seg " + (cls || ""), opacity: 1 }, vol);
        mk("rect", { x: -38, y: -12, width: 76, height: 24, rx: 4 }, j);
        tx(j, 0, 4, "", "cr-tj", "middle");
        etiquette(j, cls === "cr-ack" ? "✓ reçu " + n : n + " · " + SEG[n - 1].trim());
        return j;
      }
      q("#cr-tcp-go").addEventListener("click", function () {
        var ok = g(), perte = q("#cr-tcp-perte").checked, place = {}, acq = {};
        while (vol.firstChild) vol.removeChild(vol.firstChild);
        qa("#cr-tcp .cr-tcp-case").forEach(function (c) { c.classList.remove("cr-on"); });
        recu.textContent = "…";
        t.textContent = "TCP découpe le message en " + SEG.length + " segments numérotés, envoyés l'un après l'autre.";
        function fini() {
          if (Object.keys(acq).length < SEG.length) return;
          recu.textContent = SEG.join("");
          t.innerHTML = "Message reconstitué dans l'ordre : « " + SEG.join("") + " ». Les " + SEG.length + " segments ont été acquittés." + (perte ? " Le segment 3, perdu, a été renvoyé." : "");
        }
        function arrive(n, j) {
          place[n] = 1;
          q('#cr-tcp .cr-tcp-case[data-n="' + n + '"]').classList.add("cr-on");
          trajet(j, [[660, 96], [438 + 88 * (n - 1), 207]], 500, null, ok);
          var ordre = Object.keys(place).length;
          t.textContent = "Segment " + n + " reçu (" + ordre + (ordre > 1 ? "e" : "er") + " arrivé) : rangé à sa place, case " + n + ". Le destinataire renvoie un accusé de réception.";
          var a = jeton(n, "cr-ack");
          trajet(a, [[660, 128], [100, 128]], 520, function () { acq[n] = 1; a.setAttribute("opacity", "0"); fini(); }, ok);
        }
        function envoyer(n, delai, v, perdu) {
          apres(delai, function () {
            var j = jeton(n);
            if (perdu) {
              trajet(j, [[100, 96], [380, 96]], v, function () {
                j.classList.add("cr-perdu");
                t.textContent = "Le segment " + n + " s'est perdu en route : le destinataire ne l'acquitte pas.";
                apres(2600, function () {
                  t.textContent = "Aucun accusé de réception pour le segment " + n + " : l'émetteur le renvoie.";
                  envoyer(n, 300, 420, false);
                }, ok);
              }, ok);
            } else trajet(j, [[100, 96], [660, 96]], v, function () { arrive(n, j); }, ok);
          }, ok);
        }
        SEG.forEach(function (_, i) { envoyer(i + 1, DEP[i], VIT[i], perte && i === 2); });
      });
    })();

    // ---------- figure 16 : les sept couches du modèle OSI ----------
    (function () {
      var f = q("#cr-osi-f"), t = q("#cr-osi-t"), g = garde();
      var INFO = __OSI__;
      function montrer(n, cote) {
        qa(".cr-c, .cr-osi-d", f).forEach(function (x) {
          var c = x.getAttribute("data-cote");
          x.classList.toggle("cr-on", +x.getAttribute("data-c") === n && (!cote || !c || c === cote));
        });
      }
      function choisir(n) {
        g(); f.classList.remove("cr-flux-on"); montrer(n);
        var c = INFO[n];
        t.innerHTML = "<b>Couche " + n + " — " + c[0] + "</b> (" + c[1] + ") : " + c[2] + " Technologies : " + c[3] + ".";
      }
      qa(".cr-c", f).forEach(function (b) { b.addEventListener("click", function () { choisir(+b.getAttribute("data-c")); }); });
      qa(".cr-osi-d", f).forEach(function (r) { r.addEventListener("click", function () { choisir(+r.getAttribute("data-c")); }); });
      q("#cr-osi-go").addEventListener("click", function () {
        var ok = g(), etapes = [], k;
        for (k = 7; k >= 1; k--) etapes.push(["e", k]);
        etapes.push(["flux", 0]);
        for (k = 1; k <= 7; k++) etapes.push(["d", k]);
        (function suite(i) {
          if (!ok()) return;
          if (i >= etapes.length) { montrer(0); t.textContent = "Le message a descendu les 7 couches de l'émetteur, circulé sous forme de bits, puis remonté les 7 couches du destinataire."; return; }
          var e = etapes[i];
          f.classList.toggle("cr-flux-on", e[0] === "flux");
          if (e[0] === "flux") { montrer(0); t.textContent = "Flux binaire : les bits circulent sur le support (câble, fibre ou ondes)."; }
          else { montrer(e[1], e[0]); t.textContent = (e[0] === "e" ? "Émetteur" : "Destinataire") + " — couche " + e[1] + " : " + INFO[e[1]][0] + " (" + INFO[e[1]][1] + ")."; }
          apres(e[0] === "flux" ? 1100 : 420, function () { suite(i + 1); }, ok);
        })(0);
      });
    })();

    // ---------- figure 17 : l'encapsulation ----------
    (function () {
      var BLOCS = {
        eth: ["En-tête Ethernet", "Adresse MAC du destinataire, adresse MAC de l'émetteur, type (ou longueur) de la trame."],
        ip: ["En-tête IP", "Adresse IP de l'émetteur et adresse IP du destinataire : les routeurs les lisent pour router le paquet."],
        tcp: ["En-tête TCP", "Numéro du segment, numéro d'accusé de réception, contrôle d'erreur."],
        app: ["En-tête applicatif", "Il dépend du protocole utilisé : ici SMTP, celui du courrier électronique."],
        d: ["Données", "Le message lui-même : « Bonjour, comment ça va ? »."],
        rem: ["Remorque Ethernet", "Placée à la fin de la trame : un code de contrôle qui permet de détecter les erreurs de transmission."]
      };
      var ETAPES = [["d"], ["app", "d"], ["tcp", "app", "d"], ["ip", "tcp", "app", "d"], ["eth", "ip", "tcp", "app", "d", "rem"], null];
      var COUCHE = ["app", "app", "4", "3", "2", "1"], UNITE = ["Données", "Données", "Segment", "Paquet", "Trame", "Bits"];
      var TXT = __ENCAPS__;
      var TXT_DEC = ["Le destinataire reçoit les bits : sa couche physique les rassemble en trame.",
                     "La couche liaison de données lit l'en-tête Ethernet (la trame lui est bien destinée), vérifie la remorque, puis les retire : il reste un paquet.",
                     "La couche réseau lit l'en-tête IP, puis le retire : il reste un segment.",
                     "La couche transport (TCP) lit son en-tête — numéro du segment, contrôle d'erreur —, acquitte le segment et retire l'en-tête.",
                     "Les couches applications lisent l'en-tête applicatif et le retirent.",
                     "Le logiciel de messagerie du destinataire affiche le message : « Bonjour, comment ça va ? »."];
      var et = 0, dec = false, zone = q("#cr-enc-blocs"), det = q("#cr-enc-det"), t = q("#cr-enc-t"), titre = q("#cr-enc-et");
      var bp = q("#cr-enc-prec"), bs = q("#cr-enc-suiv"), bd = q("#cr-enc-dec");
      function rendre(avance) {
        var k = dec ? 5 - et : et, blocs = ETAPES[k], prec = avance && !dec && k > 0 ? (ETAPES[k - 1] || []) : null;
        zone.innerHTML = "";
        det.textContent = "";
        if (!blocs) {
          var b = document.createElement("div");
          b.className = "cr-bits"; b.textContent = "1011010101110101010100100101010101011010101110101010001001010101011";
          zone.appendChild(b);
        } else blocs.forEach(function (c) {
          var b = document.createElement("button");
          b.type = "button"; b.className = "cr-blk cr-blk-" + c + (prec && prec.indexOf(c) < 0 ? " cr-neuf" : ""); b.textContent = BLOCS[c][0];
          b.addEventListener("click", function () {
            qa(".cr-blk", zone).forEach(function (x) { x.classList.toggle("cr-on", x === b); });
            det.innerHTML = "<b>" + BLOCS[c][0] + "</b> : " + BLOCS[c][1];
          });
          zone.appendChild(b);
        });
        qa("#cr-enc-pile li").forEach(function (li) { li.classList.toggle("cr-on", li.getAttribute("data-c") === COUCHE[k]); });
        titre.textContent = (dec ? "Destinataire" : "Émetteur") + " — étape " + (et + 1) + " / 6 : " + UNITE[k].toLowerCase();
        t.textContent = dec ? TXT_DEC[et] : TXT[k];
        bp.disabled = et === 0; bs.disabled = et === 5;
      }
      bs.addEventListener("click", function () { if (et < 5) { et++; rendre(true); } });
      bp.addEventListener("click", function () { if (et > 0) { et--; rendre(); } });
      bd.addEventListener("click", function () {
        dec = !dec; et = 0;
        bd.setAttribute("aria-pressed", dec ? "true" : "false");
        bd.textContent = dec ? "Côté émetteur : encapsuler" : "Côté destinataire : désencapsuler";
        rendre();
      });
      rendre();
    })();

    // ---------- figure 18 : le parcours du message à travers les couches ----------
    (function () {
      var CX = [70, 235, 380, 525, 690], NC = [7, 2, 3, 2, 7], H = 26, B = 214;
      function yc(n) { return B - n * H + H / 2; }
      var pts = [], etape = [];
      function ajout(x, y, e) { pts.push([x, y]); etape.push(e); }
      ajout(CX[0] + 44, yc(7), 0); ajout(CX[0] + 44, yc(1), 0);
      for (var i = 1; i < 5; i++) {
        var w = (NC[i] === 7 ? 128 : 120) / 2 - 18;
        ajout(CX[i] - w, yc(1), i); ajout(CX[i] - w, yc(NC[i]), i);
        if (i < 4) { ajout(CX[i] + w, yc(NC[i]), i); ajout(CX[i] + w, yc(1), i); }
      }
      var TXT = ["PC1 : le message descend les sept couches, de l'application jusqu'à la couche physique, qui l'envoie sous forme de bits.",
                 "SW1 : le switch remonte jusqu'à la couche 2 (liaison de données) : il lit l'adresse MAC de la trame, puis la renvoie vers le bon port.",
                 "R1 : le routeur remonte jusqu'à la couche 3 (réseau) : il lit l'adresse IP du destinataire et choisit la route vers l'autre réseau.",
                 "SW2 : le switch du second réseau remonte jusqu'à la couche 2 et aiguille la trame d'après l'adresse MAC.",
                 "PC2 : le message remonte les sept couches jusqu'au logiciel destinataire. Message reçu."];
      var ligne = q("#cr-par-l"), p = q("#cr-par-p"), t = q("#cr-par-t"), g = garde(), L = [0];
      ligne.setAttribute("points", pts.map(function (x) { return x.join(","); }).join(" "));
      for (var k = 1; k < pts.length; k++) L.push(L[k - 1] + Math.hypot(pts[k][0] - pts[k - 1][0], pts[k][1] - pts[k - 1][1]));
      var TOT = L[L.length - 1], fin = [], d0 = 0, cur = -1;
      for (var s = 0; s < 5; s++) fin.push(s < 4 ? L[etape.indexOf(s + 1)] : TOT);
      ligne.style.strokeDasharray = TOT; ligne.style.strokeDashoffset = TOT;
      function position(d) {
        for (var k = 1; k < pts.length; k++) if (d <= L[k] || k === pts.length - 1) {
          var a = Math.min(1, Math.max(0, (d - L[k - 1]) / ((L[k] - L[k - 1]) || 1)));
          return [pts[k - 1][0] + a * (pts[k][0] - pts[k - 1][0]), pts[k - 1][1] + a * (pts[k][1] - pts[k - 1][1])];
        }
      }
      function allumer(e) { qa("#cr-par-svg .cr-pc-c").forEach(function (r) { r.classList.toggle("cr-on", +r.getAttribute("data-app") === e); }); }
      function aller(dA, dB, fini) {
        var ok = g(), t0 = null, dur = calme ? 1 : Math.max(1, (dB - dA) / 170 * 1000);
        p.setAttribute("opacity", "1");
        (function pas(tm) {
          if (!ok()) return;
          if (t0 === null) t0 = tm;
          var k = Math.min(1, (tm - t0) / dur), d = dA + k * (dB - dA), pp = position(d), e = 0;
          while (e < 4 && d > fin[e]) e++;
          if (e !== cur) { cur = e; t.textContent = TXT[e]; allumer(e); }
          p.setAttribute("cx", pp[0].toFixed(1)); p.setAttribute("cy", pp[1].toFixed(1));
          ligne.style.strokeDashoffset = TOT - d;
          if (k < 1) requestAnimationFrame(pas); else { d0 = dB; if (fini) fini(); }
        })(performance.now());
      }
      q("#cr-par-go").addEventListener("click", function () { cur = -1; aller(0, TOT); });
      q("#cr-par-pas").addEventListener("click", function () {
        if (d0 >= TOT - 0.5) { d0 = 0; cur = -1; }
        var e = 0; while (e < 4 && d0 >= fin[e] - 0.5) e++;
        aller(d0, fin[e]);
      });
      t.textContent = "Lance le message, ou avance appareil par appareil avec « Pas à pas ».";
    })();
  }
"""
CR_JS = (CR_JS.replace("__MACS__", json.dumps(MACS))
         .replace("__PCS_NAT__", json.dumps(PCS_NAT))
         .replace("__SERVICES__", json.dumps(SERVICES))
         .replace("__SEGMENTS__", json.dumps(SEGMENTS, ensure_ascii=False))
         .replace("__OSI__", json.dumps({n: [nom, u, r, t] for n, nom, u, r, t, _c in OSI}, ensure_ascii=False))
         .replace("__ENCAPS__", json.dumps([x[2] for x in ENCAPS], ensure_ascii=False)))

# ============================================================ style
CR_CSS = """
/* ---------- cours 1 : réseaux informatiques (préfixe cr-) ---------- */
.cr-fig{margin:14px 0 18px; padding:10px 12px 8px; background:#fff; border:1px solid var(--trait-fin)}
.cr-fig>figcaption{font-size:.86rem; color:var(--encre-2); margin:6px 0 2px}
.cr-svg{display:block; width:100%; height:auto; max-width:900px; margin:0 auto; font-family:var(--f-texte)}
.cr-ctrl{display:flex; flex-wrap:wrap; align-items:center; gap:8px 12px; margin:4px 0 8px}
.cr-ctrl label{display:inline-flex; align-items:center; gap:6px; font-weight:600; font-size:.92rem}
.cr-ctrl select{padding:5px; border:1.5px solid var(--encre-2); background:#fff; font:inherit}
.cr-ctrl .btn{padding:6px 12px; font-size:.92rem}
.cr-ctrl .btn[aria-pressed="true"]{background:var(--encre); color:#fff}
.cr-ctrl input[type=range]{width:min(320px,100%); accent-color:var(--bleu)}
.cr-chk{font-weight:400!important}
.cr-in{font:600 1rem ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; padding:6px 10px; border:1.5px solid var(--encre-2); background:#fff; width:14em; max-width:100%}
.cr-in[aria-invalid="true"]{border-color:var(--rouge); background:var(--rouge-pale)}
.cr-cap{min-height:1.5em; margin:6px 0 2px; padding:6px 10px; border-left:4px solid var(--bleu); background:var(--bleu-pale); font-size:.95rem}
.cr-cap:empty{display:none}
.cr-cap .ok,.cr-fig .ok,.simu .ok{color:var(--vert)} .cr-cap .ko,.cr-fig .ko,.simu .ko{color:var(--rouge)}
.cr-cap.ko{border-left-color:var(--rouge); background:var(--rouge-pale)}
.cr-rouge{color:var(--rouge)} .cr-bleu{color:var(--bleu)}
.cr-t{font:700 13px var(--f-texte); fill:var(--encre)}
.cr-tb{font:700 15px var(--f-texte); fill:var(--encre)}
.cr-tb2{font-weight:700}
.cr-ts{font:400 11.5px var(--f-texte); fill:var(--encre-2)}
.cr-tw{font:700 12px var(--f-texte); fill:#fff}
.cr-tip{font:700 12px ui-monospace,Consolas,monospace}
.cr-tip.cr-rouge{fill:var(--rouge)}
.cr-tmono{font:600 11.5px ui-monospace,Consolas,monospace; fill:var(--encre)}
.cr-tj{font:700 11px ui-monospace,Consolas,monospace; fill:var(--encre)}
.cr-tcouche{font:700 11px var(--f-texte); fill:var(--encre)}
/* halo blanc sous les textes des schémas : ils restent lisibles quand un câble les traverse */
.cr-svg text:not(.cr-tw):not(.cr-tcouche):not(.cr-tj){paint-order:stroke fill; stroke:#fff; stroke-width:3.5px; stroke-linejoin:round}
.cr-cable{fill:none; stroke:#5A6670; stroke-width:2.5; stroke-linejoin:round}
.cr-cable.cr-fin{stroke-width:1.5; stroke:#9AA4AC}
.cr-jeton rect{fill:var(--jaune); stroke:var(--encre); stroke-width:1.5}
.cr-pc.cr-on .cr-ecran,.cr-pc.cr-dest .cr-ecran{fill:var(--jaune)}
.cr-sw.cr-on>rect:first-child,#cr-wan .cr-on>rect:first-child{fill:#2E5E8E}
.cr-rt.cr-on ellipse{fill:var(--jaune)}
/* figure 1 : duplex */
.cr-dx-ab,.cr-dx-ba{stroke:var(--bleu); stroke-width:9; stroke-linecap:round; stroke-dasharray:14 36; animation:cr-f50 1.1s linear infinite}
.cr-dx-ba{stroke:var(--orange)}
#cr-duplex[data-mode=half] .cr-dx-ab{transform:translateY(8px)}
#cr-duplex[data-mode=half] .cr-dx-ba{transform:translateY(-8px); display:none}
#cr-duplex.dx-ba .cr-dx-ab{display:none} #cr-duplex.dx-ba .cr-dx-ba{display:inline}
@keyframes cr-f50{to{stroke-dashoffset:-50}}
@keyframes cr-f40{to{stroke-dashoffset:-40}}
@keyframes cr-sig{from{transform:translateX(0)} to{transform:translateX(40px)}}
@keyframes cr-pulse{0%{opacity:.25} 50%{opacity:1} 100%{opacity:.25}}
/* figure 2 : supports */
.cr-sig-el{animation:cr-sig 1.4s linear infinite}
.cr-rayon{stroke-dasharray:18 22; animation:cr-f40 .9s linear infinite}
.cr-rep{cursor:pointer}
.cr-part.cr-hl{filter:drop-shadow(0 0 3px #F2B705) drop-shadow(0 0 6px #F2B705)}
.cr-rep.cr-hl circle{fill:var(--jaune)} .cr-rep.cr-hl text{fill:var(--encre)}
.cr-leg{list-style:none; margin:4px 0 0; padding:0; display:flex; flex-wrap:wrap; gap:6px}
.cr-leg-b{font:inherit; font-size:.9rem; text-align:left; background:#fff; border:1.5px solid var(--trait); padding:4px 10px; cursor:pointer}
.cr-leg-b b{display:inline-block; min-width:1.4em; color:var(--rouge)}
.cr-leg-b.cr-hl{background:var(--jaune-pale); border-color:var(--orange)}
/* figure 3 : portée */
.cr-ondes{animation:cr-pulse 1.6s ease-in-out infinite}
.cr-comp{max-width:720px; margin:6px 0 12px}
/* débit */
.cr-calc{font-size:.92rem; margin:4px 0 8px}
.cr-barre{height:16px; background:#fff; border:1.5px solid var(--bleu); margin:6px 0}
.cr-barre span{display:block; height:100%; width:0; background:var(--bleu)}
/* figure 4 : switch */
.cr-sw-grid{display:grid; grid-template-columns:minmax(0,2.2fr) minmax(220px,1fr); gap:10px 16px; align-items:center}
@media (max-width:860px){ .cr-sw-grid{grid-template-columns:1fr} }
.cr-swtab{font-size:.88rem; margin:0}
.cr-swtab caption{font-weight:700; text-align:left; padding:0 0 4px}
.cr-swtab tr.cr-on td{background:var(--jaune-pale); font-weight:700}
/* figures 5 et 9 : liaisons que l'on coupe */
.cr-tl{cursor:pointer}
.cr-tl-hit{stroke:transparent; stroke-width:18}
.cr-tl-v{stroke:#5A6670; stroke-width:3}
.cr-tl:hover .cr-tl-v,.cr-tl:focus .cr-tl-v{stroke:var(--orange); stroke-width:5}
.cr-tl:focus{outline:none}
.cr-tl.cr-coupe .cr-tl-v{stroke:var(--rouge); stroke-dasharray:6 6}
.cr-tl.cr-route .cr-tl-v{stroke:var(--jaune); stroke-width:6}
.cr-croix{stroke:var(--rouge); stroke-width:4; stroke-linecap:round; fill:none}
.cr-tap{fill:var(--encre)}
.cr-tsw{cursor:pointer}
.cr-tsw.cr-panne>rect:first-child{fill:#7A848C}
.cr-g0 .cr-ecran{fill:#4F8FDB} .cr-g1 .cr-ecran{fill:#E8A33D} .cr-g2 .cr-ecran{fill:#3FAE6A} .cr-g3 .cr-ecran{fill:#B07CC6}
.cr-g0 .cr-sr-net{fill:#E6EEF8; stroke:#4F8FDB} .cr-g1 .cr-sr-net{fill:#FCEFD8; stroke:#E8A33D}
.cr-g2 .cr-sr-net{fill:#E2F1E7; stroke:#3FAE6A} .cr-g3 .cr-sr-net{fill:#F3E8F8; stroke:#B07CC6}
.cr-inv .cr-sr-net{fill:var(--rouge-pale); stroke:var(--rouge)}
.cr-sr-net{stroke-width:2}
.cr-topo-txt{margin:2px 0 6px; font-size:.95rem}
/* figure 6 : adresse MAC */
.cr-octets{display:flex; flex-wrap:wrap; gap:6px; margin:6px 0}
.cr-oct{display:flex; flex-direction:column; align-items:center; min-width:4.6em; font:inherit; background:#fff; border:2px solid var(--bleu); padding:4px 8px; cursor:pointer}
.cr-oct b{font:700 1.15rem ui-monospace,Consolas,monospace}
.cr-oct span{display:none; font:600 .78rem ui-monospace,Consolas,monospace; color:var(--encre-2)}
.cr-oct[aria-pressed="true"] span{display:block}
.cr-oct-f{border-color:var(--orange)}
/* figure 8 : la box */
.cr-bx-m{transition:transform .6s ease, opacity .6s ease; cursor:pointer}
#cr-box:not(.ouverte) .cr-bx-m{transform:translateX(var(--dx)) scale(.6); opacity:0; pointer-events:none}
.cr-bx-m{transform-box:fill-box; transform-origin:center}
.cr-bx-capot{transition:opacity .5s ease, transform .5s ease}
#cr-box.ouverte .cr-bx-capot{opacity:0; transform:translateY(-40px); pointer-events:none}
.cr-bx-m.cr-on>rect{stroke:var(--orange); stroke-width:3; fill:var(--jaune-pale)}
.cr-bx-m:focus{outline:none} .cr-bx-m:focus>rect{stroke:var(--bleu); stroke-width:3}
.cr-bx-txt{margin:4px 0; padding:6px 10px; background:var(--jaune-pale); border-left:4px solid var(--orange)}
/* figure 9 : routage */
.cr-leg-l{font-size:.88rem; margin:2px 0 4px}
.cr-pt{display:inline-block; width:12px; height:12px; border-radius:50%; vertical-align:-1px; margin:0 4px 0 10px}
.cr-pt-p{background:#E07B1F} .cr-pt-r{background:#3D7BB8}
.cr-rtn-c{fill:#2E5E8E} .cr-rtn-h{fill:#3D7BB8}
.cr-rtp .cr-rtn-c{fill:#B05E12} .cr-rtp .cr-rtn-h{fill:#E07B1F}
.cr-rtp{cursor:pointer}
.cr-rtp:focus{outline:none} .cr-rtp:focus .cr-rtn-h{stroke:var(--encre); stroke-width:2}
.cr-dep .cr-rtn-h,.cr-arr .cr-rtn-h{fill:var(--jaune); stroke:var(--encre); stroke-width:2}
/* figure 10 : dorsales */
.cr-zone ellipse{fill:#F4F5F2; stroke:#A5ADAA; stroke-width:1.5}
.cr-dors{cursor:pointer}
.cr-dors-hit{fill:none; stroke:transparent; stroke-width:18}
.cr-dors-l{fill:none; stroke:#C24A2C; stroke-width:5; stroke-linecap:round; opacity:.55}
.cr-dors-p{fill:none; stroke:#FFFFFF; stroke-width:2.5; stroke-dasharray:6 18; animation:cr-f40 1.2s linear infinite; stroke-linecap:round}
.cr-dors:hover .cr-dors-l,.cr-dors.cr-on .cr-dors-l,.cr-dors:focus .cr-dors-l{opacity:1; stroke-width:8}
.cr-dors:focus{outline:none}
/* figure 11 : découpage */
.cr-dec-tab{display:inline-grid; gap:4px; margin:8px 0 4px}
.cr-dec-l{display:grid; grid-template-columns:repeat(4,4.6em); gap:6px}
.cr-dec-l span{display:block; text-align:center; font:700 1.25rem ui-monospace,Consolas,monospace; padding:4px 0; border:2px solid var(--trait); background:#fff}
.cr-dec-l .cr-net{border-color:var(--vert); background:#DDF0E2; color:var(--vert)}
.cr-dec-l .cr-host{border-color:var(--rouge); background:#FBE3DD; color:var(--rouge)}
.cr-dec-m span{font-size:1.05rem; color:var(--encre-2)}
.cr-net-t{color:var(--vert)} .cr-host-t{color:var(--rouge)}
/* figure 13 : sous-réseaux logiques */
.cr-sr-in{display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:8px; margin:8px 0}
.cr-sr-in label{display:flex; flex-direction:column; gap:3px; font-weight:700; font-size:.88rem}
.cr-sr-in .cr-in{width:100%; font-size:.92rem}
@media (max-width:640px){ .cr-sr-in{grid-template-columns:repeat(2,minmax(0,1fr))} }
.cr-sr-mat{max-width:520px; margin:6px 0 0; text-align:center}
.cr-sr-mat td.ok{color:var(--vert); font-weight:700} .cr-sr-mat td.ko{color:var(--rouge); font-weight:700}
/* figure 14 : HTTP */
#cr-http-disque text.cr-on{fill:var(--vert); font-weight:800}
#cr-http-disque.cr-cherche rect{stroke:var(--rouge); stroke-width:2.5}
.cr-http-vues{display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1.2fr); gap:12px; margin-top:8px}
@media (max-width:760px){ .cr-http-vues{grid-template-columns:1fr} }
.cr-nav{border:2px solid var(--encre); background:#fff; min-height:150px}
.cr-nav-barre{background:#D3D8D5; padding:4px 8px; font:600 .85rem ui-monospace,Consolas,monospace}
.cr-nav-page{padding:6px 12px}
.cr-nav-page h4{font:700 1.15rem var(--f-titre); margin:6px 0}
.cr-nav-page u{color:var(--bleu)}
.cr-msg-t{font-weight:700; margin:0 0 4px}
.cr-pre{font:500 .78rem/1.35 ui-monospace,Consolas,monospace; background:#1C2530; color:#E9ECEF; padding:6px 10px; margin:0 0 6px; white-space:pre-wrap; min-height:2.2em; max-height:220px; overflow:auto}
.cr-pre:empty{display:none}
/* figure 15 : TCP */
.cr-seg rect{fill:#FCEFD8; stroke:var(--orange); stroke-width:1.5}
.cr-seg.cr-ack rect{fill:#E2F1E7; stroke:var(--vert)}
.cr-seg.cr-perdu{opacity:0; transition:opacity .8s ease}
.cr-tcp-case{fill:#F4F5F2; stroke:#A5ADAA; stroke-dasharray:4 3}
.cr-tcp-case.cr-on{stroke:var(--vert); stroke-dasharray:none}
/* figure 16 : modèle OSI (grille : couches de l'émetteur, tableau, couches du destinataire) */
.cr-osi{display:grid; grid-template-columns:58px minmax(110px,1fr) 34px minmax(0,2fr) minmax(130px,1.2fr) 58px; gap:3px 0; font-size:.86rem}
.cr-osi-h{font-weight:700; padding:4px 8px; background:#F4F5F2; border-bottom:2px solid var(--encre); grid-row:1}
.cr-osi-pt{background:none; border-bottom:0; text-align:center; font-size:.74rem; padding:4px 0; hyphens:manual; overflow-wrap:anywhere}
.cr-osi-d{padding:5px 8px; background:color-mix(in srgb, var(--c) 40%, #fff); cursor:pointer}
.cr-osi-nom b{display:block}
.cr-osi-n{font:700 1.2rem var(--f-titre); text-align:center; padding:5px 0}
.cr-osi-d.cr-on{background:var(--c); font-weight:700}
.cr-osi-tech{display:flex; align-items:center; justify-content:center; text-align:center; font-weight:700; padding:6px 8px; background:#F6F7F4; border-left:1px solid var(--trait-fin)}
.cr-c{margin:0 8px; font:700 1.2rem var(--f-titre); border:1.5px solid rgba(0,0,0,.25); background:var(--c); color:var(--encre); cursor:pointer}
.cr-c[data-c="1"]{color:#fff}
.cr-c.cr-on{outline:4px solid var(--encre); outline-offset:-4px; transform:scale(1.08)}
.cr-osi-grp{display:flex; justify-content:space-between; gap:10px; font-size:.82rem; font-weight:700; color:var(--encre-2); margin:4px 66px 0}
.cr-flux{margin:8px auto 0; max-width:640px; text-align:center; font:600 .8rem ui-monospace,Consolas,monospace; color:var(--bleu); border:1.5px solid var(--bleu); border-radius:10px; padding:5px; background:var(--bleu-pale); opacity:.45}
.cr-flux-on .cr-flux{opacity:1; box-shadow:0 0 0 3px var(--jaune)}
@media (max-width:760px){ .cr-osi{grid-template-columns:44px minmax(0,1fr) 28px 0 minmax(0,1fr) 44px} .cr-osi-role{display:none} .cr-c{margin:0 4px} .cr-osi-grp{margin:4px 0 0} }
/* figure 17 : encapsulation */
.cr-enc{display:grid; grid-template-columns:minmax(0,1fr) 200px; gap:14px; align-items:start}
@media (max-width:760px){ .cr-enc{grid-template-columns:1fr} }
.cr-enc-et{font-weight:700; margin:2px 0 8px}
.cr-enc-blocs{display:flex; flex-wrap:wrap; gap:0; min-height:46px}
.cr-blk{font:600 .88rem var(--f-texte); border:1.5px solid var(--encre); padding:10px 10px; cursor:pointer; margin:0 -1.5px 4px 0}
.cr-blk.cr-on{outline:3px solid var(--bleu); outline-offset:-3px; position:relative}
.cr-blk-eth,.cr-blk-rem{background:#C9CED3} .cr-blk-ip{background:#CFD95C} .cr-blk-tcp{background:#FBE45A}
.cr-blk-app{background:#8FD0EE} .cr-blk-d{background:#F6BE6E}
.cr-neuf{animation:cr-entre .6s ease}
@keyframes cr-entre{from{transform:translateY(-14px); opacity:0} to{transform:none; opacity:1}}
.cr-bits{font:600 .95rem ui-monospace,Consolas,monospace; background:#1C2530; color:#fff; padding:10px 12px; overflow-wrap:anywhere; animation:cr-entre .6s ease}
.cr-enc-det{font-size:.92rem; min-height:1.4em; margin:6px 0 0}
.cr-enc-pile{list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:4px}
.cr-enc-pile li{display:flex; justify-content:space-between; gap:6px; border:1.5px solid var(--trait); padding:5px 8px; font-size:.84rem; background:#fff}
.cr-enc-pile li span{color:var(--encre-2)}
.cr-enc-pile li.cr-on{border-color:var(--encre); background:var(--jaune-pale); font-weight:700}
/* figure 18 : parcours */
.cr-pc-c{stroke:rgba(0,0,0,.2)}
.cr-pc-c.cr-on{stroke:var(--encre); stroke-width:2.5}
#cr-par-l{stroke-dasharray:0}
@media (prefers-reduced-motion:reduce){
  .cr-dx-ab,.cr-dx-ba,.cr-sig-el,.cr-rayon,.cr-ondes,.cr-dors-p,.cr-neuf,.cr-bits{animation:none}
  .cr-bx-m,.cr-bx-capot{transition:none}
}
@media print{
  .cr-ctrl,.cr-leg,.cr-sr-in{display:none!important}
  .cr-pane[hidden]{display:block!important}
  .cr-fig{break-inside:avoid}
  #cr-box .cr-bx-m{transform:none!important; opacity:1!important} #cr-box .cr-bx-capot{display:none}
  .cr-bx-txt[hidden]{display:block!important}
  .cr-topo-txt[hidden]{display:block!important}
}
"""
