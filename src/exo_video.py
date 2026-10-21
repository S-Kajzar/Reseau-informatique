"""Exercice 1.4 — Le voyage d'une vidéo YouTube (Niveau 1), du serveur au smartphone.

Léa regarde une vidéo sur son smartphone 5G. La vidéo vient d'un serveur cache installé chez son opérateur (une vidéo
populaire) ou d'un centre de données aux États-Unis, par le câble sous-marin Dunant (une vidéo rare) ; un bateau la
reçoit par satellite. Quatre parties : le chemin de la vidéo (schéma), débit et qualité, le temps de trajet, l'antenne
relais 4G/5G. Une animation, la course des paquets, compare les durées de trajet une fois la partie 3 corrigée.

Les données sont sourcées et datées dans les documents (DT1, DT2) : débits recommandés par YouTube, Google Global
Cache, câble Dunant, TeleGeography, Arcep, ANFR. Les distances et durées dérivées sont calculées ici, une seule fois.

exercice(g) reçoit le module generer : pas d'import circulaire. Les pictogrammes viennent du cours 1 et de
l'exercice 1.3.
"""
import json

import qcm
import cours_reseaux as cr
import exo_adressage as ad

# ------------------------------------------------------------ données (voir les sources dans DT1 et DT2)
C, N_VERRE = 300_000, 1.5               # km/s ; indice du verre de la fibre
V_FIBRE = C / N_VERRE                   # 200 000 km/s
DUNANT_KM, GEO_KM, LEO_KM, CACHE_KM = 6400, 35_786, 550, 20
QUALITES = [("4K", 20), ("HD 1080p", 5), ("HD 720p", 2.5), ("SD 480p", 1.1), ("SD 360p", 0.7)]   # Mbit/s
SITES_5G, SITES_35 = 52_069, 35_798     # ANFR, sites 5G autorisés au 1er août 2025, dont bande 3,5 GHz


def _ms(km, v):
    return km / v * 1000


COURSE = [  # trajet, durée de propagation (ms)
    (f"Serveur cache, {CACHE_KM} km de fibre", _ms(CACHE_KM, V_FIBRE)),
    (f"Satellite en orbite basse ({LEO_KM} km)", _ms(2 * LEO_KM, C)),
    (f"Câble Dunant ({DUNANT_KM:,} km)".replace(",", " "), _ms(DUNANT_KM, V_FIBRE)),
    ("Satellite géostationnaire", _ms(2 * GEO_KM, C))]


def fr(x, d=1):
    """Nombre écrit à la française : virgule décimale, espace des milliers, zéros inutiles retirés."""
    s = f"{x:,.{d}f}".replace(",", " ").replace(".", ",")
    return s.rstrip("0").rstrip(",") if "," in s else s


E_EQ = ["Centre de données", "Serveur cache", "Routeur", "Antenne relais", "Satellite", "Switch"]
E_SUP = ["Fibre optique", "Ondes radio", "Câble Ethernet", "Bluetooth"]
S_MS = ["ms", "milliseconde", "millisecondes"]
MBITS = ad.MBITS
MO = ["mo", "megaoctet", "megaoctets", "mega-octet", "mega-octets"]
MIN = ["min", "minute", "minutes", "mn"]
KMS = ["km/s", "kms", "km.s-1"]


# ------------------------------------------------------------ pictogrammes
def _centre(x, y):
    """Centre de données : un bâtiment et trois baies de serveurs ; (x, y) : coin haut gauche (130 × 110)."""
    return (f'<g transform="translate({x} {y})"><rect width="130" height="110" rx="6" fill="#F4F5F2" stroke="#7D868F" '
            'stroke-width="2"/><path d="M0 18H130" stroke="#7D868F" stroke-width="2"/>'
            + "".join(f'<g transform="translate({12 + 38 * k} 34) scale(.75)">{cr.serveur(0, 0)}</g>' for k in range(3))
            + "</g>")


def _antenne(x, y):
    """Antenne relais : pylône et panneaux ; (x, y) : sommet du pylône, haut de 170."""
    return (f'<g transform="translate({x} {y})" fill="none" stroke="#46525C" stroke-width="3" stroke-linecap="round">'
            '<path d="M0 8L-26 170M0 8L26 170M-20 130H20M-14 90H14M-8 50H8M-20 130L14 90M20 130L-14 90M-14 90L8 50'
            'M14 90L-8 50"/><rect x="-17" y="0" width="9" height="28" rx="2" fill="#E9ECEF" stroke-width="1.5"/>'
            '<rect x="8" y="0" width="9" height="28" rx="2" fill="#E9ECEF" stroke-width="1.5"/></g>')


def _ondes(cx, cy):
    return "".join(f'<path d="M{cx} {cy - r}a{r} {r} 0 0 1 0 {2 * r}" fill="none" stroke="{cr.VERT}" '
                   'stroke-width="2.5" stroke-linecap="round"/>' for r in (12, 22, 32))


def plan_chemin():
    """Figure 1 : le chemin de la vidéo. Repères 1 à 4 : un équipement ; 5 à 7 : un support de transmission."""
    W, H = 930, 300
    fibre = 'stroke="#B26A00" stroke-width="4" fill="none"'
    corps = (
        '<text x="95" y="24" text-anchor="middle" class="cr-tb">Virginie (États-Unis)</text>'
        '<rect x="190" y="34" width="250" height="230" rx="10" fill="#DCEBF7"/>'
        '<path d="M206 230q12 -8 24 0t24 0t24 0M300 252q12 -8 24 0t24 0t24 0M220 70q12 -8 24 0t24 0t24 0" '
        'stroke="#9DB6D6" stroke-width="2" fill="none"/>'
        '<text x="315" y="58" text-anchor="middle" class="cr-ts">Océan Atlantique</text>'
        '<rect x="452" y="34" width="470" height="258" rx="10" fill="#F6F7F4" stroke="#A5ADAA" stroke-dasharray="5 4"/>'
        '<text x="912" y="24" text-anchor="end" class="cr-tb">France</text>'
        f'<path d="M160 150H492" {fibre}/>'
        '<text x="315" y="138" text-anchor="middle" class="cr-ts">câble sous-marin Dunant, 6 400 km</text>'
        '<path class="cr-cable" d="M520 102V136"/>'
        f'<path d="M548 150H738" {fibre}/>'
        + _centre(30, 70) + cr.serveur(500, 40) + cr.routeur(520, 144) + _antenne(750, 60) + _ondes(767, 76)
        + ad._telephone(852, 150)
        + '<text x="865" y="212" text-anchor="middle" class="cr-ts">smartphone</text>'
        '<text x="865" y="226" text-anchor="middle" class="cr-ts">de Léa</text>')
    cases = {"1": (20, 196, 150, 36, "équipement"), "2": (458, 188, 140, 36, "équipement"),
             "3": (552, 48, 140, 36, "équipement"), "4": (690, 244, 120, 36, "équipement"),
             "5": (240, 166, 150, 36, "support"), "6": (600, 166, 120, 36, "support"),
             "7": (802, 100, 120, 36, "support")}
    svg = (f'<svg class="plan-svg cr-svg" viewBox="0 0 {W} {H}" role="img" aria-label="Le chemin de la vidéo : un '
           "centre de données en Virginie, le câble sous-marin Dunant sous l'océan Atlantique, puis en France un "
           "routeur et un serveur de l'opérateur, une antenne relais et le smartphone de Léa ; quatre équipements "
           'repérés 1 à 4, trois liaisons repérées 5 à 7">' + corps + "</svg>")
    return {"svg": svg, "w": W, "h": H, "cases": cases, "maxw": W,
            "caption": "Figure 1 — Le chemin de la vidéo. Les cases 1 à 4 reçoivent un équipement : le bâtiment qui "
                       "stocke toutes les vidéos, aux États-Unis (1), l'appareil qui aiguille les paquets dans le "
                       "réseau de l'opérateur (2), le serveur de l'opérateur qui garde une copie des vidéos populaires "
                       "(3), le pylône qui couvre le quartier de Léa (4). Les cases 5 à 7 reçoivent un support : la "
                       "liaison sous l'océan (5), la liaison entre le routeur et l'antenne (6), la liaison entre "
                       "l'antenne et le smartphone (7). Les liaisons en orange sont celles du dossier DP1."}


# ------------------------------------------------------------ figure 2 : la course des paquets
RALENTI = 25
Y_PISTES = [64, 112, 160, 208]


def _duree(ms):
    """Durée affichée comme dans les réponses : au dixième sous 10 ms, à la milliseconde au-delà."""
    return f"{fr(ms) if ms < 10 else fr(round(ms))} ms"


def figure_course():
    pistes = "".join(
        f'<text x="10" y="{y + 5}" class="cr-t">{nom}</text>'
        f'<path d="M270 {y}H800" stroke="#D3D8D5" stroke-width="8" stroke-linecap="round"/>'
        f'<path d="M806 {y - 12}V{y + 12}" stroke="{cr.ENCRE}" stroke-width="2.5"/>'
        f'<text x="822" y="{y + 5}" class="cr-tb vi-t" id="vi-t{i}" opacity="0">{_duree(ms)}</text>'
        f'<g class="vi-p" id="vi-p{i}" transform="translate(270 {y})"><rect x="-14" y="-10" width="28" height="20" '
        'rx="4"/><path d="M-4 -5L6 0L-4 5z" fill="#FFFFFF"/></g>'
        for i, ((nom, ms), y) in enumerate(zip(COURSE, Y_PISTES)))
    corps = ('<text x="270" y="26" class="cr-ts">Temps réel écoulé depuis le départ :</text>'
             '<text x="520" y="26" class="cr-tb" id="vi-chrono">0 ms</text>' + pistes)
    return ('<figure class="cr-fig vi-fig" id="vi-course" data-grp="v3_1 v3_2 v3_3 v3_4 v3_5">'
            '<div class="cr-ctrl"><button type="button" class="btn" id="vi-go" disabled>Lancer la course des paquets'
            f'</button><span class="small" id="vi-verrou">Disponible une fois la partie 3 corrigée : la course montre '
            "les durées calculées.</span></div>"
            '<svg class="cr-svg" viewBox="0 0 900 230" role="img" aria-label="La course des paquets : quatre paquets '
            "partent au même instant, du serveur cache, d'un satellite en orbite basse, du câble Dunant et d'un "
            'satellite géostationnaire ; chacun arrive au bout de la durée de son trajet">' + corps
            + f"</svg><figcaption>Figure 2 — La course des paquets, au ralenti ({RALENTI} fois plus lent) : les quatre "
            "paquets partent au même instant ; chacun met la durée de propagation de son trajet.</figcaption>"
            '<p class="cr-cap" id="vi-cap" aria-live="polite"></p></figure>')


# ------------------------------------------------------------ documents
def _source(*liens):
    return ('<p class="small">Sources : ' + " ; ".join(f'<a href="{u}" target="_blank" rel="noopener">{t}</a>'
                                                     for t, u in liens) + ".</p>")


DP1 = ('<div class="doc-text"><h3>La vidéo de Léa</h3><p>À Lyon, Léa regarde une vidéo YouTube sur son smartphone '
       "5G. La vidéo représente l'essentiel de ce que transportent les réseaux mobiles : environ les trois quarts de "
       "leur trafic de données dans le monde, fin 2024.</p><ul>"
       "<li>YouTube stocke ses vidéos dans des <b>centres de données</b>, par exemple en Virginie, aux États-Unis.</li>"
       "<li>Google installe aussi des <b>serveurs cache</b> dans les réseaux des opérateurs : ils gardent une copie des "
       "vidéos les plus regardées. Selon Google, ils servent en général <b>70 à 90 %</b> du trafic qui peut être mis "
       f"en cache. Dans cet exercice, le serveur cache de l'opérateur de Léa est à {CACHE_KM} km d'elle, par fibre "
       "optique.</li>"
       "<li>Une vidéo rare vient des États-Unis par le <b>câble sous-marin Dunant</b>, en fibre optique : il relie "
       "Virginia Beach à Saint-Hilaire-de-Riez (Vendée), mesure 6 400 km et transporte jusqu'à 250 Tbit/s. Les "
       "câbles sous-marins portent plus de 99 % du trafic entre les continents.</li>"
       "<li>En France, la vidéo traverse le réseau de l'opérateur (fibres optiques et routeurs) jusqu'à l'<b>antenne "
       "relais</b> du quartier, raccordée par une fibre optique ; l'antenne l'envoie au smartphone par <b>ondes "
       "radio</b> (4G ou 5G).</li>"
       "<li>Un bateau en mer, loin des antennes, reçoit la vidéo par <b>satellite</b>.</li></ul>"
       "<p>Dans les calculs de durée, on ne compte que la propagation du signal, sans le temps de traitement des "
       "appareils.</p>"
       + _source(("Google, Google Global Cache", "https://support.google.com/interconnect/answer/9058809"),
                 ("DCD, mise en service du câble Dunant (2021)",
                  "https://www.datacenterdynamics.com/en/news/googles-virginia-to-france-dunant-cable-goes-live"),
                 ("TeleGeography (2023)", "https://blog.telegeography.com/2023-mythbusting-part-3"),
                 ("ComCom, d'après l'Ericsson Mobility Report de novembre 2024",
                  "https://www.comcom.admin.ch/en/mobile-data-traffic"))
       + "</div>")

DT1 = ('<div class="doc-text"><h3>Débits recommandés par YouTube</h3><p>Débit à maintenir pendant toute la vidéo '
       "pour la regarder sans coupure.</p>"
       '<table class="t"><thead><tr><th>Qualité</th><th>Débit recommandé</th></tr></thead><tbody>'
       + "".join(f"<tr><td>{q}</td><td>{fr(d)} Mbit/s</td></tr>" for q, d in QUALITES)
       + "</tbody></table><p>L'application choisit d'elle-même la qualité : la vidéo est découpée en courts morceaux, "
       "préparés en plusieurs qualités, et chaque morceau est demandé dans la meilleure qualité que le débit du moment "
       "permet (diffusion adaptative).</p>"
       "<h3>Consommation et mesures en France</h3><ul><li>Au premier trimestre 2024, un utilisateur de mobile "
       "consommait en moyenne <b>15 Go</b> de données par mois (Arcep).</li><li>Pour mesurer l'internet mobile, "
       "l'Arcep compte la part des mesures qui dépassent <b>3, 8 et 30 Mbit/s</b> (campagne 2024).</li></ul>"
       "<h3>Débit</h3><p>Débit = quantité de données / durée ; 1 octet = 8 bits ; 1 Go = 1 000 Mo.</p>"
       + _source(("YouTube, configuration requise", "https://support.google.com/youtube/answer/78358"),
                 ("Arcep, observatoire du 1er trimestre 2024",
                  "https://www.arcep.fr/cartes-et-donnees/nos-publications-chiffrees/observatoire-des-marches-des-"
                  "communications-electroniques-en-france/t1-2024.html"),
                 ("Arcep, qualité des services mobiles 2024",
                  "https://www.arcep.fr/actualites/actualites-et-communiques/detail/n/qualite-des-services-mobiles-en-"
                  "metropole-260625.html"))
       + "</div>")

DT2 = ('<div class="doc-text"><h3>Distances et vitesses</h3><ul>'
       f"<li>Vitesse de la lumière dans le vide (et dans l'air) : c = {fr(C)} km/s.</li>"
       f"<li>Dans une fibre optique, la lumière va moins vite : v = c / n, où n est l'indice du verre, n ≈ "
       f"{fr(N_VERRE)}.</li><li>Câble Dunant : {fr(DUNANT_KM)} km.</li>"
       f"<li>Satellite géostationnaire : {fr(GEO_KM)} km d'altitude, au-dessus de l'équateur ; il paraît immobile dans "
       "le ciel.</li>"
       f"<li>Satellites en orbite basse (par exemple Starlink) : environ {LEO_KM} km d'altitude.</li>"
       "<li>Pour un satellite, le signal monte jusqu'à lui puis redescend : il parcourt deux fois l'altitude (on "
       "néglige l'écart dû à la position du bateau).</li><li>Durée = distance / vitesse.</li></ul>"
       "<h3>Les antennes relais 5G</h3><ul>"
       f"<li>Au 1er août 2025, l'ANFR compte {fr(SITES_5G)} sites 5G autorisés en France, dont {fr(SITES_35)} dans la "
       "bande 3,5 GHz et 34 215 dans la bande 700 MHz (un même site peut utiliser plusieurs bandes).</li>"
       "<li>L'Arcep impose qu'au moins 75 % des sites 5G offrent un débit d'au moins 240 Mbit/s, partagé entre les "
       "utilisateurs de l'antenne.</li>"
       "<li>Les fréquences basses (700 MHz) portent loin et traversent bien les murs ; la bande 3,5 GHz offre des "
       "débits plus élevés mais porte moins loin : il faut plus d'antennes pour couvrir la même surface.</li></ul>"
       + _source(("Futura-Sciences, orbite géostationnaire",
                  "https://www.futura-sciences.com/sciences/definitions/univers-orbite-geostationnaire-2438/"),
                 ("GeekWire, orbite des satellites Starlink",
                  "https://www.geekwire.com/2018/spacex-sets-sights-lower-orbit-starlink-broadband-networks-first-"
                  "satellites/"),
                 ("ANFR, observatoire au 1er août 2025",
                  "https://www.anfr.fr/fileadmin/mediatheque/documents/Observatoire/0825/CP_observatoire_aout_2025.pdf"),
                 ("Arcep, obligations des opérateurs 5G",
                  "https://www.arcep.fr/fileadmin/user_upload/espace_collectivites/rapport-TC-2021/chapitre-01/"
                  "ARC-RA2021-TOME2-Chapitre1-Fiche2.pdf"))
       + "</div>")

VI_CSS = """
/* ---------- exercice 1.4 : la course des paquets ---------- */
.vi-p rect{fill:#B26A00}
.vi-fig #vi-verrou:empty{display:none}
"""

VI_JS = r"""<script>/* Exercice 1.4 : la course des paquets, une fois la partie 3 corrigée */
(function () {
  "use strict";
  var f = document.getElementById("vi-course");
  if (!f) return;
  var go = document.getElementById("vi-go"), verrou = document.getElementById("vi-verrou");
  var chrono = document.getElementById("vi-chrono"), cap = document.getElementById("vi-cap");
  var D = __DUREES__, R = __RALENTI__, Y = __Y__, ids = f.getAttribute("data-grp").split(" "), n = 0;
  var fin = Math.max.apply(null, D);
  var calme = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  // une question est corrigée quand ses cases sont verrouillées (question à une case ou à plusieurs, QCM)
  function corrige() {
    return document.body.classList.contains("graded") || ids.every(function (id) {
      var g = document.getElementById(id), c = g ? g.querySelectorAll("input") : [];
      return c.length > 0 && [].every.call(c, function (i) { return i.disabled; });
    });
  }
  setInterval(function () { if (go.disabled && corrige()) { go.disabled = false; verrou.textContent = ""; } }, 500);
  function ms(v) { return (v < 10 ? v.toFixed(1) : Math.round(v).toString()).replace(".", ",") + " ms"; }
  function poser(t) {
    D.forEach(function (d, i) {
      var a = Math.min(1, t / d);
      document.getElementById("vi-p" + i).setAttribute("transform", "translate(" + (270 + 530 * a).toFixed(1) + " " + Y[i] + ")");
      document.getElementById("vi-t" + i).setAttribute("opacity", a >= 1 ? "1" : "0");
    });
    chrono.textContent = ms(Math.min(t, fin));
  }
  go.addEventListener("click", function () {
    var id = ++n, t0 = null;
    cap.textContent = "";
    (function pas(tm) {
      if (id !== n) return;
      if (t0 === null) t0 = tm;
      var t = calme ? fin : (tm - t0) / R;
      poser(t);
      if (t < fin) requestAnimationFrame(pas);
      else cap.textContent = "Arrivée : le paquet du satellite géostationnaire met " + ms(fin) + ", plus de sept fois "
        + "la durée du câble transatlantique ; celui du serveur cache, voisin, arrive presque aussitôt.";
    })(performance.now());
  });
})();
</script>"""


def parties(g):
    P, KW, NUM, GRP, Q, QBAR = g.P, g.KW, g.NUM, g.GRP, g.Q, g.QBAR
    (_, t_cache), (_, t_leo), (_, t_dunant), (_, t_geo) = COURSE
    volume = 5 * 600 / 8                                 # Mo : 10 min de vidéo en 1080p
    minutes = 15 * 1000 * 8 / 5 / 60                      # min : 15 Go en 1080p
    part = SITES_35 / SITES_5G * 100
    return [
        {"title": "Le chemin de la vidéo", "minutes": 10, "plan": plan_chemin(), "intro": [
            "<p>La figure 1 suit la vidéo depuis le centre de données jusqu'au smartphone de Léa ; le dossier DP1 "
            "décrit chaque étape.</p>"], "blocks": [
            QBAR(["DP1"], "sur la figure 1"),
            GRP("Nomme les équipements repérés 1 à 4.", "La légende de la figure dit le rôle de chacun.", [
                    ("Repère 1 — aux États-Unis", KW(P("donnees")), "Centre de données"),
                    ("Repère 2 — réseau de l'opérateur", KW(P("routeur")), "Routeur"),
                    ("Repère 3 — copie des vidéos populaires", KW(P("cache")), "Serveur cache"),
                    ("Repère 4 — pylône du quartier", KW(P("antenne")), "Antenne relais")],
                "<p>Les vidéos sont stockées dans des <strong>centres de données</strong> ; dans le réseau de "
                "l'opérateur, des <strong>routeurs</strong> aiguillent les paquets, et un <strong>serveur cache</strong> "
                "garde une copie des vidéos populaires. L'<strong>antenne relais</strong> couvre le quartier de "
                "Léa.</p>", etiquettes=E_EQ, liste="Équipements", reperes=["1", "2", "3", "4"]),
            GRP("Indique le support des liaisons repérées 5 à 7.", "Lis le dossier DP1.", [
                    ("Repère 5 — sous l'océan", KW(P("fibre")), "Fibre optique"),
                    ("Repère 6 — routeur et antenne", KW(P("fibre")), "Fibre optique"),
                    ("Repère 7 — antenne et smartphone", KW(P("onde|radio")), "Ondes radio")],
                "<p>Le câble Dunant et la liaison de l'antenne sont en <strong>fibre optique</strong> ; seule la "
                "dernière liaison, de l'antenne au smartphone, passe par des <strong>ondes radio</strong> (4G ou "
                "5G).</p>", etiquettes=E_SUP, liste="Supports", reperes=["5", "6", "7"]),
            qcm.QCM("Par où passe la plupart des données échangées entre l'Amérique et l'Europe ?",
                    [("A", "Par des câbles sous-marins en fibre optique"), ("B", "Par des satellites"),
                     ("C", "Par les ondes radio des antennes relais"), ("D", "Par des câbles électriques en cuivre")],
                    ["A"],
                    "Les câbles sous-marins portent plus de 99 % du trafic entre les continents (TeleGeography) : une "
                    "fibre transporte bien plus de données qu'un satellite, avec une durée de trajet plus courte."),
            qcm.QCM("La vidéo que regarde Léa est très populaire. D'où vient-elle le plus probablement ?",
                    [("A", "Du serveur cache de son opérateur"), ("B", "Du centre de données de Virginie"),
                     ("C", "D'un satellite")], ["A"],
                    "Les vidéos populaires sont copiées sur les serveurs cache des opérateurs, qui servent en général 70 "
                    "à 90 % du trafic pouvant être mis en cache (Google) : la vidéo ne traverse pas l'océan."),
        ]},
        {"title": "Débit et qualité de la vidéo", "minutes": 10, "blocks": [
            QBAR(["DT1"]),
            Q("Quel débit YouTube recommande-t-il pour regarder une vidéo en 1080p ?", "En Mbit/s, avec son unité.",
              NUM(5, 0.01, "Mbit/s", MBITS), "5 Mbit/s",
              "<p>Le tableau du dossier DT1 donne 5 Mbit/s, à maintenir pendant toute la vidéo.</p>"),
            qcm.QCM("Dans le train, le débit du smartphone de Léa tombe à 3 Mbit/s. Quelle est la meilleure qualité "
                    "qu'elle peut regarder sans coupure ?",
                    [("A", "4K"), ("B", "HD 1080p"), ("C", "HD 720p"), ("D", "SD 360p")], ["C"],
                    "Il faut 5 Mbit/s pour le 1080p, 2,5 Mbit/s pour le 720p : avec 3 Mbit/s, le 720p est la meilleure "
                    "qualité possible. Le 360p passe aussi, mais en moins bonne qualité."),
            Q("Quelle quantité de données représente une vidéo de 10 minutes regardée en 1080p ?",
              "En mégaoctets (Mo), avec son unité.", NUM(volume, 0.5, "Mo", MO), f"{fr(volume)} Mo",
              "<p>10 min = 600 s ; " + g.calc("5 Mbit/s × 600 s = 3 000 Mbit") + ", et 1 octet = 8 bits : "
              + g.calc(f"3 000 Mbit ÷ 8 = {fr(volume)} Mo") + ".</p>"),
            Q("Le forfait de Léa compte 15 Go par mois, la consommation moyenne d'un utilisateur de mobile (DT1). "
              "Combien de minutes de vidéo en 1080p peut-elle regarder avec ?", "En minutes, avec son unité.",
              NUM(minutes, 0.5, "min", MIN), f"{fr(minutes)} min",
              "<p>15 Go = 15 000 Mo = 120 000 Mbit ; à 5 Mbit/s : " + g.calc("120 000 ÷ 5 = 24 000 s")
              + f", soit {fr(minutes)} min (6 h 40 min). En 4K, à 20 Mbit/s, le forfait ne dure que 100 min.</p>"),
            qcm.QCM("Pendant la vidéo, le débit baisse. Que fait l'application YouTube ?",
                    [("A", "Elle baisse la qualité de l'image, sans arrêter la vidéo"),
                     ("B", "Elle arrête la vidéo jusqu'au retour du débit"),
                     ("C", "Elle passe en 4K pour compenser"), ("D", "Elle fait passer la vidéo par satellite")], ["A"],
                    "La vidéo est découpée en courts morceaux préparés en plusieurs qualités : l'application demande "
                    "chaque morceau dans la meilleure qualité que le débit permet (diffusion adaptative, DT1)."),
        ]},
        {"title": "Le temps de trajet", "minutes": 12, "intro": [
            "<p>On calcule la durée de propagation du signal sur chaque trajet (dossier DT2).</p>"], "blocks": [
            QBAR(["DP1", "DT2"]),
            Q("Calcule la vitesse de la lumière dans la fibre optique.", "v = c / n ; en km/s, avec son unité.",
              NUM(V_FIBRE, 1, "km/s", KMS), f"{fr(V_FIBRE)} km/s",
              "<p>" + g.calc(f"v = {fr(C)} ÷ {fr(N_VERRE)} = {fr(V_FIBRE)} km/s") + " : un tiers de moins que dans "
              "le vide.</p>"),
            Q("Combien de temps la vidéo met-elle pour traverser le câble Dunant ?",
              "En millisecondes (ms), avec son unité.", NUM(t_dunant, 0.5, "ms", S_MS), f"{fr(t_dunant)} ms",
              "<p>Durée = distance / vitesse : " + g.calc(f"{fr(DUNANT_KM)} ÷ {fr(V_FIBRE)} = 0,032 s")
              + f", soit {fr(t_dunant)} ms pour traverser l'Atlantique.</p>"),
            Q("Le bateau reçoit la vidéo par un satellite géostationnaire : le signal monte jusqu'au satellite, puis "
              "redescend. Quelle est la durée de ce trajet ?", "Le signal va à la vitesse c ; en ms, avec son unité, "
              "arrondie à la milliseconde.", NUM(round(t_geo), 1.5, "ms", S_MS), f"{fr(round(t_geo))} ms",
              "<p>Le signal parcourt deux fois l'altitude : " + g.calc(f"2 × {fr(GEO_KM)} = {fr(2 * GEO_KM)} km")
              + " ; " + g.calc(f"{fr(2 * GEO_KM)} ÷ {fr(C)} ≈ 0,239 s") + f", soit environ {fr(round(t_geo))} ms. "
              "Une question et sa réponse font l'aller-retour : près d'une demi-seconde.</p>"),
            Q("Même calcul pour un satellite en orbite basse, à 550 km d'altitude.",
              "En ms, avec son unité, au dixième.", NUM(round(t_leo, 1), 0.1, "ms", S_MS), f"{fr(t_leo)} ms",
              "<p>" + g.calc(f"2 × {LEO_KM} = {fr(2 * LEO_KM)} km") + " ; "
              + g.calc(f"{fr(2 * LEO_KM)} ÷ {fr(C)} ≈ 0,0037 s") + f", soit environ {fr(t_leo)} ms : 65 fois "
              "moins qu'avec un satellite géostationnaire, car le satellite est 65 fois plus bas.</p>"),
            qcm.QCM("Pour un appel vidéo ou un jeu en ligne, quel trajet est le plus gênant ?",
                    [("A", "Le satellite géostationnaire"), ("B", "Le câble sous-marin"),
                     ("C", "Le satellite en orbite basse"), ("D", "Le serveur cache")], ["A"],
                    f"Avec environ {fr(round(t_geo))} ms à chaque trajet, une question et sa réponse prennent près "
                    "d'une demi-seconde : le décalage s'entend dans une conversation. Une vidéo enregistrée, elle, "
                    "supporte ce délai : elle démarre un peu plus tard, puis se lit normalement."),
            g.HTML(figure_course()),
        ]},
        {"title": "L'antenne relais 4G/5G", "minutes": 8, "blocks": [
            QBAR(["DT1", "DT2"]),
            Q("Quelle part des sites 5G autorisés utilise la bande 3,5 GHz ?", "En %, arrondie à l'unité.",
              NUM(round(part), 0.5), f"{round(part)} %",
              "<p>" + g.calc(f"{fr(SITES_35)} ÷ {fr(SITES_5G)} × 100 ≈ {fr(part)} %") + f", soit environ "
              f"{round(part)} % des sites (ANFR, au 1er août 2025).</p>"),
            Q("Une antenne 5G offre 240 Mbit/s, partagés entre ses utilisateurs. Combien de personnes peuvent, au plus, "
              "y regarder en même temps une vidéo en 1080p ?", "Un nombre.", NUM(48), "48",
              "<p>Chaque vidéo en 1080p demande 5 Mbit/s : " + g.calc("240 ÷ 5 = 48") + " personnes, et seulement "
              "12 en 4K (240 ÷ 20). Le débit d'une antenne se partage.</p>"),
            qcm.QCM("Pourquoi faut-il plus d'antennes pour couvrir une ville dans la bande 3,5 GHz que dans la bande "
                    "700 MHz ?",
                    [("A", "Les ondes à 3,5 GHz portent moins loin et traversent moins bien les murs"),
                     ("B", "Les ondes à 3,5 GHz vont moins vite"),
                     ("C", "La bande 3,5 GHz est réservée à la 4G"),
                     ("D", "Une antenne 3,5 GHz ne relie qu'un seul smartphone")], ["A"],
                    "Toutes les ondes radio vont à la vitesse de la lumière ; les fréquences hautes offrent plus de "
                    "débit mais portent moins loin (DT2)."),
            qcm.QCM("Quelles liaisons du trajet de la vidéo sont sans fil ?",
                    [(1, "Entre l'antenne relais et le smartphone"), (2, "Entre le satellite et le bateau"),
                     (3, "Entre le routeur et l'antenne relais"), (4, "Le câble Dunant")], [1, 2],
                    "Seules les dernières liaisons, vers le smartphone ou le bateau, passent par des ondes radio ; "
                    "l'antenne est raccordée par fibre optique, comme le câble sous l'océan."),
        ]},
    ]


def exercice(g):
    js = (VI_JS.replace("__DUREES__", json.dumps([round(ms, 3) for _n, ms in COURSE]))
          .replace("__RALENTI__", str(RALENTI)).replace("__Y__", json.dumps(Y_PISTES)))
    return {"key": "video-youtube", "prefix": "v", "tag": "Exercice 1.4", "level": "Niveau 1",
            "title": "Le voyage d'une vidéo YouTube", "parts": parties(g),
            "docs": [g.DOC("DP1", "La vidéo de Léa", DP1), g.DOC("DT1", "Débits et consommation", DT1),
                     g.DOC("DT2", "Distances, vitesses et antennes", DT2)],
            "consignes": g.consignes(g.C_SCHEMA, g.C_ETIQUETTES, g.C_SAISIE, g.C_GROUPE, qcm.C_QCM, g.C_DOCUMENTS),
            "hero": ("carte-ex14", "Le chemin d'une vidéo : centre de données, câble sous-marin, antenne relais",
                     "Du centre de données au smartphone."),
            "mots": ["Streaming", "Câble sous-marin", "Satellite", "4G et 5G", "Débit"], "vign": "carte-ex14",
            "valt": "Le chemin d'une vidéo, du centre de données au smartphone", "css": VI_CSS, "js": js,
            "sub": "Une vidéo YouTube suivie du serveur au smartphone : le chemin et ses supports, le débit qu'il faut "
                   "pour chaque qualité, la durée du trajet par câble sous-marin ou par satellite, le partage d'une "
                   "antenne relais 4G/5G. Données sourcées : YouTube, Google, Arcep, ANFR."}
