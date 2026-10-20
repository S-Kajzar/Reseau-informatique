"""Exercice 2.1 — Suivre une requête HTTP à travers le réseau (Niveau 2), l'approfondissement du modèle OSI.

Un ordinateur portable de la maison demande la page www.example.org/index.html à un serveur web, dans un centre de
données : il passe par la box, les routeurs d'Internet, le routeur du centre de données et un switch. Quatre
parties : les couches de chaque appareil, l'encapsulation de la requête (et ses segments TCP), les adresses de la
trame dans la maison, les adresses de la trame au centre de données et la réponse. Une animation rejoue le trajet de
la requête et de la réponse, une fois les parties 3 et 4 corrigées (elle montre les réponses).

Ce que l'exercice ajoute au cours (dossier DT1) : l'adresse MAC identifie les machines d'un même LAN, donc
l'en-tête Ethernet est refait sur chaque réseau traversé, alors que les adresses IP restent celles des deux
extrémités — sauf à la box, qui remplace l'adresse privée par son adresse publique.

exercice(g) reçoit le module generer : pas d'import circulaire. Les pictogrammes viennent du cours 1.
"""
import json

import qcm
import cours_reseaux as cr

# adresses : (adresse MAC, adresse IP) ; le premier octet des adresses MAC est multiple de 4 (adresse individuelle)
PORTABLE = ("28:87:A5:EF:18:5D", "192.168.1.30")
BOX = ("3C:52:A1:10:20:01", "192.168.1.1")
PUBLIQUE = "86.245.12.40"
ROUTEUR_C = ("00:1B:44:22:00:01", "203.0.113.1")
SERVEUR = ("00:1B:44:11:3A:B7", "203.0.113.80")

# les étiquettes des adresses (parties 3 et 4) : l'adresse, puis l'appareil auquel elle appartient
E_ADRESSES = [f"{PORTABLE[0]} (ordinateur portable)", f"{BOX[0]} (box)", f"{ROUTEUR_C[0]} (routeur du centre)",
              f"{SERVEUR[0]} (serveur web)", f"{PORTABLE[1]} (ordinateur portable)", f"{BOX[1]} (box, côté maison)",
              f"{PUBLIQUE} (box, adresse publique)", f"{SERVEUR[1]} (serveur web)"]
E_COUCHES = ["Couches 1 à 7", "Couches 1 à 3", "Couches 1 et 2", "Couche 1 seulement"]
E_TRAME = ["En-tête Ethernet", "En-tête IP", "En-tête TCP", "Requête HTTP", "Remorque Ethernet", "Accusé de réception"]
E_ROLES = ["Application (couches 5 à 7)", "Transport (couche 4)", "Réseau (couche 3)", "Liaison de données (couche 2)",
           "Physique (couche 1)"]


def _compact(s):
    return "".join(c for c in s.lower() if c.isalnum())


def ADR(adresse):
    """Correcteur d'une case d'adresse : l'étiquette doit contenir cette adresse (comparée sans sa ponctuation)."""
    return {"type": "code", "contains": [_compact(adresse)]}


def _etq(adresse):
    return next(e for e in E_ADRESSES if e.startswith(adresse + " "))


def _box(x, y):
    return (f'<g transform="translate({x} {y})"><rect width="76" height="40" rx="8" fill="#F4F5F2" stroke="#7D868F" '
            'stroke-width="2"/><circle cx="14" cy="12" r="3" fill="#5BD08A"/><circle cx="24" cy="12" r="3" '
            'fill="#5BD08A"/><rect x="10" y="26" width="56" height="5" rx="2" fill="#1C2530"/></g>')


# ------------------------------------------------------------ figure 1 : le chemin et ses appareils
POS = [("Ordinateur portable", 70), ("Box", 210), ("Routeur d'Internet", 380), ("Routeur du centre|de données", 560),
       ("Switch", 700), ("Serveur web", 830)]


def _appareils(y=60, noms=True):
    d = [cr.portable(43, y + 2), _box(172, y), cr.routeur(380, y + 14), cr.routeur(560, y + 14),
         cr.switch(655, y + 6, 90, 4, ""), cr.serveur(810, y - 10)]
    t = "".join(f'<text x="{x}" y="{y + 70}" text-anchor="middle" class="cr-t">'
                + "".join(f'<tspan x="{x}" dy="{15 * (i > 0)}">{l}</tspan>' for i, l in enumerate(n.split("|")))
                + "</text>" for n, x in POS) if noms else ""
    return "".join(d) + t


def plan_chemin():
    W, H = 900, 250
    corps = ('<rect x="300" y="20" width="160" height="108" rx="40" fill="#EAF3FA" stroke="#9DB6D6" stroke-dasharray="5 4"/>'
             '<text x="380" y="40" text-anchor="middle" class="cr-ts">Internet</text>'
             '<rect x="490" y="20" width="400" height="108" rx="10" fill="#F6F7F4" stroke="#A5ADAA" stroke-dasharray="5 4"/>'
             '<text x="690" y="40" text-anchor="middle" class="cr-ts">centre de données</text>'
             '<path class="cr-cable" d="M100 82H172M248 82H352M408 82H532M588 82H655M745 82H810"/>'
             + _appareils() + "")
    cases = {"1": (12, 150, 116, 36, "couches"), "2": (322, 150, 116, 36, "couches"),
             "3": (642, 150, 116, 36, "couches"), "4": (772, 150, 116, 36, "couches")}
    svg = (f'<svg class="plan-svg cr-svg" viewBox="0 0 {W} {H}" role="img" aria-label="Le chemin de la requête : '
           "ordinateur portable, box, routeur d'Internet, routeur du centre de données, switch, serveur web ; quatre "
           'appareils repérés de 1 à 4">' + corps + "</svg>")
    return {"svg": svg, "w": W, "h": H, "cases": cases, "maxw": W,
            "caption": "Figure 1 — Le chemin de la requête. Les cases 1 à 4 reçoivent les couches du modèle OSI que met "
                       "en œuvre l'appareil placé au-dessus : l'ordinateur portable (1), un routeur d'Internet (2), le "
                       "switch (3), le serveur web (4)."}


# ------------------------------------------------------------ figures 2 et 3 : une trame et ses adresses
def plan_trame(num, titre, de, vers):
    W, H = 900, 250
    def champ(x, y, nom):
        return f'<text x="{x + 24}" y="{y}" class="cr-t">{nom}</text>'
    corps = (f'<text x="450" y="22" text-anchor="middle" class="cr-tb">{titre}</text>'
             f'<text x="450" y="42" text-anchor="middle" class="cr-ts">de : {de} — vers : {vers}</text>'
             '<rect x="10" y="54" width="880" height="176" rx="8" fill="#FFFFFF" stroke="#1C2530" stroke-width="2"/>'
             '<rect x="20" y="64" width="316" height="156" rx="5" fill="#E9ECEF"/>'
             '<rect x="346" y="64" width="316" height="156" rx="5" fill="#EEF2CF"/>'
             '<text x="30" y="84" class="cr-tb">En-tête Ethernet</text><text x="356" y="84" class="cr-tb">En-tête IP</text>'
             + champ(30, 106, "adresse MAC de destination") + champ(30, 164, "adresse MAC source")
             + champ(356, 106, "adresse IP source") + champ(356, 164, "adresse IP de destination")
             + '<rect x="672" y="64" width="208" height="44" rx="5" fill="#FBE45A"/><text x="776" y="91" '
             'text-anchor="middle" class="cr-t">En-tête TCP</text>'
             '<rect x="672" y="114" width="208" height="52" rx="5" fill="#8FD0EE"/><text x="776" y="137" '
             'text-anchor="middle" class="cr-t">Requête HTTP</text><text x="776" y="155" text-anchor="middle" '
             'class="cr-tmono">GET /index.html</text>'
             '<rect x="672" y="172" width="208" height="48" rx="5" fill="#E9ECEF"/><text x="776" y="200" '
             'text-anchor="middle" class="cr-t">Remorque Ethernet</text>')
    cases = {"1": (30, 114, 296, 36, ""), "2": (30, 172, 296, 36, ""), "3": (356, 114, 296, 36, ""),
             "4": (356, 172, 296, 36, "")}
    svg = (f'<svg class="plan-svg cr-svg" viewBox="0 0 {W} {H}" role="img" aria-label="{titre} : en-tête Ethernet '
           "(adresses MAC de destination et source, repères 1 et 2), en-tête IP (adresses IP source et de destination, "
           'repères 3 et 4), en-tête TCP, requête HTTP, remorque">' + corps + "</svg>")
    return {"svg": svg, "w": W, "h": H, "cases": cases, "maxw": W,
            "caption": f"Figure {num} — {titre}. Les cases 1 à 4 reçoivent les adresses de la trame."}


# ------------------------------------------------------------ figure 4 : le trajet animé
def figure_trajet():
    corps = ('<path class="cr-cable" d="M100 152H172M248 152H352M408 152H532M588 152H655M745 152H810"/>'
             + _appareils(130)
             + '<g id="rq-j" class="rq-jeton" opacity="0"><rect x="-118" y="-32" width="236" height="56" rx="6"/>'
             '<text y="-12" text-anchor="middle" class="cr-tj" id="rq-mac"></text>'
             '<text y="8" text-anchor="middle" class="cr-tj" id="rq-ip"></text></g>')
    return ('<figure class="cr-fig rq-fig" id="rq-trajet" data-grp="r3_1 r3_2 r4_1 r4_2 r4_3 r4_4">'
            '<div class="cr-ctrl"><button type="button" class="btn" id="rq-go" disabled>Rejouer le trajet de la '
            'requête et de la réponse</button><span class="small" id="rq-verrou">Disponible une fois les parties 3 et 4 '
            "corrigées : l'animation montre les réponses.</span></div>"
            '<svg class="cr-svg" viewBox="0 0 900 230" role="img" aria-label="Le trajet de la requête, de l\'ordinateur '
            'portable au serveur web, et de la réponse ; les adresses inscrites sur le message changent en route">'
            + corps + "</svg><figcaption>Figure 4 — Le trajet de la requête, puis de la réponse : les adresses MAC "
            "changent sur chaque réseau, les adresses IP restent celles des extrémités, sauf à la box.</figcaption>"
            '<p class="cr-cap" id="rq-t" aria-live="polite"></p></figure>')


DP1 = ('<div class="doc-text"><h3>La requête à suivre</h3><p>Dans la maison, l\'ordinateur portable ouvre la page '
       "<code>www.example.org/index.html</code>. Son navigateur envoie une requête HTTP au serveur web, installé dans un "
       "centre de données. La requête passe par la box (routeur passerelle de la maison), par des routeurs d'Internet, "
       "par le routeur du centre de données, puis par un switch.</p>"
       '<table class="t"><thead><tr><th>Appareil</th><th>Adresse MAC</th><th>Adresse IP</th></tr></thead><tbody>'
       f"<tr><td>Ordinateur portable</td><td>{PORTABLE[0]}</td><td>{PORTABLE[1]}</td></tr>"
       f"<tr><td>Box, côté maison</td><td>{BOX[0]}</td><td>{BOX[1]}</td></tr>"
       f"<tr><td>Box, côté Internet</td><td>—</td><td>{PUBLIQUE} (adresse publique)</td></tr>"
       f"<tr><td>Routeur du centre de données, côté centre</td><td>{ROUTEUR_C[0]}</td><td>{ROUTEUR_C[1]}</td></tr>"
       f"<tr><td>Serveur web</td><td>{SERVEUR[0]}</td><td>{SERVEUR[1]}</td></tr></tbody></table>"
       "<p>La page <code>index.html</code> et ses images représentent 6 000 octets ; TCP envoie au plus 1 500 octets de "
       "données par segment.</p></div>")

DT1 = ('<div class="doc-text"><h3>Couches, adresses et encapsulation</h3><ul><li>Les ordinateurs, les téléphones et '
       "les serveurs mettent en œuvre les sept couches du modèle OSI ; les routeurs, les couches 1 à 3 ; les switchs et "
       "les points d'accès, les couches 1 et 2.</li><li>Pour envoyer un message, chaque couche ajoute son en-tête : la "
       "requête HTTP (couches 5 à 7), puis l'en-tête TCP (couche 4), l'en-tête IP (couche 3), enfin l'en-tête Ethernet "
       "et la remorque (couche 2). La trame commence par l'en-tête ajouté en dernier.</li><li><b>Adresses MAC</b> : "
       "elles identifient les machines d'un même LAN. Sur chaque réseau traversé, la trame porte l'adresse MAC de "
       "l'appareil qui l'envoie sur ce réseau et celle de l'appareil qui la reçoit sur ce réseau ; chaque routeur "
       "refait l'en-tête Ethernet. Un switch, lui, transmet la trame sans la modifier.</li><li><b>Adresses IP</b> : "
       "elles restent celles de l'émetteur et du destinataire d'un bout à l'autre, sauf à la box : elle remplace "
       "l'adresse privée de l'émetteur par son adresse publique, et fait l'inverse pour la réponse (traduction "
       "d'adresses, NAT).</li><li>TCP découpe les données en segments numérotés ; le destinataire acquitte chaque "
       "segment reçu, un segment non acquitté est renvoyé.</li></ul></div>")


def parties(g):
    P, KW, NUM, GRP, Q, QBAR, IP = g.P, g.KW, g.NUM, g.GRP, g.Q, g.QBAR, g.IP
    return [
        {"title": "Les appareils et leurs couches", "minutes": 9, "plan": plan_chemin(), "intro": [
            "<p>La figure 1 montre le chemin de la requête ; le dossier DP1 la décrit, le dossier DT1 rappelle les "
            "couches que gère chaque appareil.</p>"], "blocks": [
            QBAR(["DP1", "DT1"], "sur la figure 1"),
            GRP("Indique les couches du modèle OSI que met en œuvre chaque appareil repéré (1 à 4).",
                "Une étiquette par case.", [
                    ("Repère 1 — ordinateur portable", KW(P("7")), "Couches 1 à 7"),
                    ("Repère 2 — routeur d'Internet", KW(P("3")), "Couches 1 à 3"),
                    ("Repère 3 — switch", KW(P("et", "2")), "Couches 1 et 2"),
                    ("Repère 4 — serveur web", KW(P("7")), "Couches 1 à 7")],
                "<p>Le client et le serveur, qui font tourner les logiciels, mettent en œuvre les sept couches ; le "
                "routeur remonte jusqu'à la couche 3 pour lire l'adresse IP ; le switch s'arrête à la couche 2 : il "
                "lit l'adresse MAC.</p>", etiquettes=E_COUCHES, liste="Couches", reperes=["1", "2", "3", "4"]),
            qcm.QCM("Quel appareil lit l'adresse IP de destination pour choisir la route du paquet ?",
                    [("A", "Le switch"), ("B", "Le routeur"), ("C", "Le point d'accès Wi-Fi")], ["B"],
                    "Le routeur travaille jusqu'à la couche 3 : il lit l'adresse IP de destination et choisit la route."),
            qcm.QCM("Quel appareil transmet la trame vers le bon port d'après l'adresse MAC, sans la modifier ?",
                    [("A", "Le switch"), ("B", "Le routeur"), ("C", "Le serveur web")], ["A"],
                    "Le switch lit l'adresse MAC de destination et aiguille la trame ; il ne refait pas l'en-tête."),
        ]},
        {"title": "L'encapsulation de la requête", "minutes": 11, "blocks": [
            QBAR(["DP1", "DT1"]),
            GRP("Remets dans l'ordre les éléments de la trame envoyée par l'ordinateur portable, du début à la fin.",
                "Une étiquette ne sert pas.", [
                    ("1er élément", KW(P("ethernet"), forbid="remorque"), "En-tête Ethernet"),
                    ("2e élément", KW(P("ip")), "En-tête IP"),
                    ("3e élément", KW(P("tcp")), "En-tête TCP"),
                    ("4e élément", KW(P("http")), "Requête HTTP"),
                    ("5e élément", KW(P("remorque")), "Remorque Ethernet")],
                "<p>Chaque couche ajoute son en-tête devant le message qu'elle reçoit : la trame commence par "
                "l'en-tête ajouté en dernier, celui de la couche 2.</p>"
                + g.calc("Ethernet | IP | TCP | requête HTTP | remorque"), etiquettes=E_TRAME),
            GRP("Quelle couche ajoute chacun de ces éléments ?", "Une étiquette ne sert pas.", [
                    ("La requête HTTP", KW(P("application")), "Application (couches 5 à 7)"),
                    ("L'en-tête TCP", KW(P("transport")), "Transport (couche 4)"),
                    ("L'en-tête IP", KW(P("reseau")), "Réseau (couche 3)"),
                    ("L'en-tête Ethernet", KW(P("liaison")), "Liaison de données (couche 2)")],
                "<p>HTTP appartient aux couches applications ; TCP à la couche transport, qui segmente ; IP à la couche "
                "réseau, qui route ; Ethernet à la couche liaison de données, qui identifie les machines du LAN.</p>",
                etiquettes=E_ROLES),
            Q("La réponse du serveur — la page et ses images — représente 6 000 octets. En combien de segments TCP "
              "est-elle découpée ?", "Un nombre.", NUM(4), "4",
              "<p>Au plus 1 500 octets de données par segment : " + g.calc("6 000 ÷ 1 500 = 4") + " segments.</p>"),
            qcm.QCM("Le segment 3 de la réponse se perd en route. Que se passe-t-il ?",
                    [(1, "Le navigateur n'envoie pas d'accusé de réception pour ce segment"),
                     (2, "Le serveur renvoie le segment 3"), (3, "Le navigateur affiche la page sans ce morceau"),
                     (4, "Le serveur renvoie toute la page")], [1, 2],
                    "Le destinataire, ici le navigateur, acquitte chaque segment reçu ; le segment 3, jamais acquitté, "
                    "est renvoyé par le serveur. Les autres segments, acquittés, ne sont pas renvoyés."),
        ]},
        {"title": "Les adresses dans la maison", "minutes": 12,
         "plan": plan_trame(2, "La trame de l'ordinateur portable à la box", "l'ordinateur portable", "la box"),
         "intro": ["<p>Dans la maison, la requête circule dans une trame Ethernet (ou Wi-Fi), de l'ordinateur portable "
                   "jusqu'à la box.</p>"], "blocks": [
            QBAR(["DP1", "DT1"], "sur la figure 2"),
            GRP("Complète les adresses de la trame qui va de l'ordinateur portable à la box (repères 1 à 4).",
                "Lis le principe des adresses MAC et IP dans DT1.", [
                    ("Repère 1 — adresse MAC de destination", ADR(BOX[0]), _etq(BOX[0])),
                    ("Repère 2 — adresse MAC source", ADR(PORTABLE[0]), _etq(PORTABLE[0])),
                    ("Repère 3 — adresse IP source", ADR(PORTABLE[1]), _etq(PORTABLE[1])),
                    ("Repère 4 — adresse IP de destination", ADR(SERVEUR[1]), _etq(SERVEUR[1]))],
                "<p>Dans la maison, la trame va de l'ordinateur à la box : adresses MAC de la box (destination) et de "
                "l'ordinateur (source). Les adresses IP sont celles des extrémités : l'ordinateur (source) et le "
                "serveur web (destination).</p>", etiquettes=E_ADRESSES, liste="Adresses",
                reperes=["1", "2", "3", "4"]),
            qcm.QCM("Pourquoi l'adresse MAC de destination n'est-elle pas celle du serveur web ?",
                    [("A", "L'adresse MAC identifie les machines d'un même LAN : dans la maison, la trame va jusqu'à la box"),
                     ("B", "Le serveur web n'a pas d'adresse MAC"),
                     ("C", "L'adresse MAC du serveur change à chaque requête")], ["A"],
                    "Le serveur n'est pas dans le réseau de la maison : la trame est adressée à la box, la passerelle, "
                    "qui la fera suivre. Le serveur a bien une adresse MAC, utilisée dans le LAN du centre de données."),
        ]},
        {"title": "Au centre de données, puis la réponse", "minutes": 13,
         "plan": plan_trame(3, "La trame du routeur du centre de données au serveur", "le routeur du centre de données",
                            "le serveur web"),
         "intro": ["<p>Arrivée au centre de données, la requête est remise au serveur web par le routeur du centre, à "
                   "travers un switch.</p>"], "blocks": [
            QBAR(["DP1", "DT1"], "sur la figure 3"),
            GRP("Complète les adresses de la trame qui va du routeur du centre de données au serveur (repères 1 à 4).",
                "Pense à ce que la box a changé.", [
                    ("Repère 1 — adresse MAC de destination", ADR(SERVEUR[0]), _etq(SERVEUR[0])),
                    ("Repère 2 — adresse MAC source", ADR(ROUTEUR_C[0]), _etq(ROUTEUR_C[0])),
                    ("Repère 3 — adresse IP source", ADR(PUBLIQUE), _etq(PUBLIQUE)),
                    ("Repère 4 — adresse IP de destination", ADR(SERVEUR[1]), _etq(SERVEUR[1]))],
                "<p>Dans le LAN du centre, la trame va du routeur au serveur : adresses MAC du serveur (destination) et "
                "du routeur (source) ; le switch ne les modifie pas. L'adresse IP source est l'adresse publique de la "
                "box, qui a remplacé l'adresse privée de l'ordinateur ; l'adresse IP de destination n'a pas changé.</p>",
                etiquettes=E_ADRESSES, liste="Adresses", reperes=["1", "2", "3", "4"]),
            qcm.QCM("Entre la trame de la maison et celle du centre de données, qu'est-ce qui a changé ?",
                    [(1, "Les adresses MAC"), (2, "L'adresse IP source, remplacée par l'adresse publique de la box"),
                     (3, "L'adresse IP de destination"), (4, "La requête HTTP")], [1, 2],
                    "L'en-tête Ethernet est refait sur chaque réseau ; la box a traduit l'adresse IP source. Le "
                    "destinataire et la requête, eux, restent les mêmes."),
            GRP("Le serveur répond. Écris les adresses IP de sa réponse, au départ du serveur.",
                "Une adresse par case, en notation pointée.", [
                    ("Adresse IP source", IP(SERVEUR[1]), SERVEUR[1]),
                    ("Adresse IP de destination", IP(PUBLIQUE), PUBLIQUE)],
                "<p>Le serveur répond à l'adresse d'où la requête lui semble venir : l'adresse publique de la box.</p>"),
            Q("Arrivée à la box, la réponse doit être remise à l'ordinateur portable : quelle adresse IP de destination "
              "la box y inscrit-elle ?", "Écris l'adresse seule, en notation pointée.", IP(PORTABLE[1]), PORTABLE[1],
              "<p>La box retrouve l'ordinateur qui attendait cette réponse et remet son adresse privée : c'est "
              "l'inverse de la traduction faite à l'aller.</p>"),
            g.HTML(figure_trajet()),
        ]},
    ]


RQ_CSS = """
/* ---------- exercice 2.1 : le trajet animé ---------- */
.rq-jeton rect{fill:var(--jaune); stroke:var(--encre); stroke-width:1.5}
.rq-fig #rq-verrou:empty{display:none}
"""

RQ_JS = r"""<script>/* Exercice 2.1 : le trajet de la requête et de la réponse, rejoué une fois les parties 3 et 4 corrigées */
(function () {
  "use strict";
  var f = document.getElementById("rq-trajet");
  if (!f) return;
  var go = document.getElementById("rq-go"), verrou = document.getElementById("rq-verrou"), t = document.getElementById("rq-t");
  var j = document.getElementById("rq-j"), mac = document.getElementById("rq-mac"), ip = document.getElementById("rq-ip");
  var A = __ADR__, ids = f.getAttribute("data-grp").split(" "), n = 0, demi = 118, r = j.querySelector("rect");
  var calme = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  // une question est corrigée quand ses cases sont verrouillées (question à une case ou à plusieurs, QCM)
  function corrige() {
    return document.body.classList.contains("graded") || ids.every(function (id) {
      var g = document.getElementById(id), c = g ? g.querySelectorAll("input") : [];
      return c.length > 0 && [].every.call(c, function (i) { return i.disabled; });
    });
  }
  setInterval(function () { if (go.disabled && corrige()) { go.disabled = false; verrou.textContent = ""; } }, 500);
  function trajet(pts, fin, id) {
    var L = [0], k;
    for (k = 1; k < pts.length; k++) L.push(L[k - 1] + Math.hypot(pts[k][0] - pts[k - 1][0], pts[k][1] - pts[k - 1][1]));
    var tot = L[L.length - 1], dur = calme ? 1 : tot / 260 * 1000, t0 = null;
    (function pas(tm) {
      if (id !== n) return;
      if (t0 === null) t0 = tm;
      var a = Math.min(1, (tm - t0) / dur), d = a * tot, i = 1;
      while (i < pts.length - 1 && d > L[i]) i++;
      var u = (d - L[i - 1]) / ((L[i] - L[i - 1]) || 1);
      var x = Math.max(demi + 4, Math.min(896 - demi, pts[i - 1][0] + u * (pts[i][0] - pts[i - 1][0])));
      j.setAttribute("transform", "translate(" + x.toFixed(1) + " " + (pts[i - 1][1] + u * (pts[i][1] - pts[i - 1][1])).toFixed(1) + ")");
      if (a < 1) requestAnimationFrame(pas); else fin();
    })(performance.now());
  }
  var Y = 82, X = { pc: 70, box: 210, net: 380, rc: 560, sw: 700, srv: 830 };
  var ETAPES = [
    [X.pc, X.box, "MAC : " + A.pc[0] + " → " + A.box[0], "IP : " + A.pc[1] + " → " + A.srv[1],
     "Dans la maison, la trame va de l'ordinateur à la box : adresses MAC de l'ordinateur et de la box ; adresses IP de l'ordinateur et du serveur."],
    [X.box, X.rc, "MAC : refaites sur chaque liaison", "IP : " + A.pub + " → " + A.srv[1],
     "La box remplace l'adresse IP privée de l'ordinateur par son adresse publique (NAT). Sur chaque liaison d'Internet, un routeur refait l'en-tête Ethernet."],
    [X.rc, X.srv, "MAC : " + A.rc[0] + " → " + A.srv[0], "IP : " + A.pub + " → " + A.srv[1],
     "Le routeur du centre envoie la trame au serveur : adresses MAC du routeur et du serveur. Le switch la transmet sans la modifier."],
    [X.srv, X.rc, "MAC : " + A.srv[0] + " → " + A.rc[0], "IP : " + A.srv[1] + " → " + A.pub,
     "Le serveur répond à l'adresse publique de la box, dans une nouvelle trame adressée au routeur du centre."],
    [X.rc, X.box, "MAC : refaites sur chaque liaison", "IP : " + A.srv[1] + " → " + A.pub,
     "La réponse traverse Internet de routeur en routeur jusqu'à la box."],
    [X.box, X.pc, "MAC : " + A.box[0] + " → " + A.pc[0], "IP : " + A.srv[1] + " → " + A.pc[1],
     "La box remet l'adresse privée de l'ordinateur et lui envoie la trame : réponse reçue, le navigateur affiche la page."]
  ];
  go.addEventListener("click", function () {
    var id = ++n;
    j.setAttribute("opacity", "1");
    (function suite(i) {
      if (id !== n) return;
      if (i >= ETAPES.length) { t.textContent = "Trajet terminé : les adresses MAC ont changé sur chaque réseau, les adresses IP seulement à la box."; return; }
      var e = ETAPES[i];
      mac.textContent = e[2]; ip.textContent = e[3]; t.textContent = e[4];
      // le jeton s'ajuste à ses adresses et reste dans la figure
      demi = Math.ceil(Math.max(mac.getComputedTextLength(), ip.getComputedTextLength()) / 2) + 12;
      r.setAttribute("x", -demi); r.setAttribute("width", 2 * demi);
      trajet([[e[0], Y - 30], [e[1], Y - 30]], function () { setTimeout(function () { suite(i + 1); }, calme ? 0 : 700); }, id);
    })(0);
  });
})();
</script>"""


def exercice(g):
    adr = {"pc": PORTABLE, "box": BOX, "pub": PUBLIQUE, "rc": ROUTEUR_C, "srv": SERVEUR}
    return {"key": "requete-http", "prefix": "r", "tag": "Exercice 2.1", "level": "Niveau 2",
            "title": "Suivre une requête à travers le réseau", "parts": parties(g),
            "docs": [g.DOC("DP1", "La requête à suivre", DP1), g.DOC("DT1", "Couches, adresses et encapsulation", DT1)],
            "consignes": g.consignes(g.C_SCHEMA, g.C_ETIQUETTES, g.C_SAISIE, g.C_GROUPE, qcm.C_QCM, g.C_DOCUMENTS),
            "hero": ("carte-ex21", "La trame d'une requête HTTP : en-têtes Ethernet, IP et TCP",
                     "Une requête HTTP, de l'ordinateur portable au serveur web."),
            "mots": ["HTTP", "Encapsulation", "MAC et IP", "NAT", "TCP"], "vign": "carte-ex21",
            "valt": "Une trame et ses en-têtes", "css": RQ_CSS, "js": RQ_JS.replace("__ADR__", json.dumps(adr)),
            "sub": "Une requête HTTP suivie de bout en bout : les couches de chaque appareil, l'encapsulation et les "
                   "segments TCP, les adresses MAC et IP de chaque trame, la traduction d'adresses à la box, la "
                   "réponse du serveur."}
