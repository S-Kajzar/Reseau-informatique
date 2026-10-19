"""Cours et exercice modèles : chaque élément disponible pour les contenus à venir, sur un petit exemple.

    python3 src/generer.py --modele   # écrit modele.html (non suivi par git, non publié)

La page modèle n'est pas l'accueil publié : elle sert de référence pour écrire un cours ou un exercice (on recopie
un bloc dans src/generer.py, où les mêmes fonctions s'écrivent sans le préfixe « g. ») et de banc d'essai aux tests
(tests/correction.test.js, tests/navigateur.test.js). On y trouve :
  - le cours : en-tête, objectifs et prérequis, sommaire, sections, cartes à retourner, un script propre au cours
    (clés js, init, css), un jeu de classement, un quiz noté, le pied de cours ;
  - l'exercice : documents DP et DT, barre de documents, questions à une case (mots-clés, adresse, nombre),
    question à plusieurs cases saisies, question à étiquettes, schéma à compléter avec son bandeau, QCM à réponse
    unique et à réponses multiples.
"""
import qcm


def plan_reseau(g):
    """Schéma à compléter de la partie 2 : Internet, le routeur (1), le commutateur (2), le serveur (3), deux postes.
    Chaque équipement est un bloc : son pictogramme en haut, sa case en bas (repère → x, y, largeur, hauteur,
    indication, dans le repère du viewBox)."""
    W, H = 800, 340
    encre, bleu, orange = "#1C2530", "#1F5FA8", "#B26A00"

    def bloc(x, y, picto):
        return (f'<rect x="{x}" y="{y}" width="150" height="100" rx="8" fill="#FFFFFF" stroke="{encre}" '
                f'stroke-width="1.5"/>' + picto)
    routeur = (f'<g fill="{encre}"><path d="M248 144l-6-20M302 144l6-20" stroke="{encre}" stroke-width="4" '
               'stroke-linecap="round"/><rect x="236" y="142" width="78" height="18" rx="4"/></g>'
               '<g fill="#5BD08A"><circle cx="248" cy="151" r="2.6"/><circle cx="257" cy="151" r="2.6"/></g>')
    commutateur = (f'<rect x="452" y="134" width="86" height="20" rx="3" fill="{encre}"/>' +
                   "".join(f'<rect x="{458 + 10 * i}" y="142" width="7" height="7" fill="#0E1114" stroke="#7D868F" '
                           'stroke-width=".8"/>' for i in range(8)))
    serveur = (f'<rect x="484" y="241" width="22" height="34" rx="3" fill="#46525C"/>'
               '<path d="M488 249h14M488 256h14M488 263h14" stroke="#1C2530" stroke-width="3"/>')

    def poste(x, y, nom, ip):
        return (f'<rect x="{x}" y="{y}" width="46" height="32" rx="3" fill="{encre}"/><rect x="{x + 4}" y="{y + 4}" '
                f'width="38" height="22" fill="#4F8FDB"/><rect x="{x + 19}" y="{y + 32}" width="8" height="7" '
                f'fill="#46525C"/><rect x="{x + 10}" y="{y + 39}" width="26" height="4" rx="2" fill="#46525C"/>'
                f'<text x="{x + 58}" y="{y + 16}" font-size="14" font-weight="700" fill="{encre}">{nom}</text>'
                f'<text x="{x + 58}" y="{y + 34}" font-size="13" font-family="ui-monospace,Consolas,monospace" '
                f'fill="{bleu}">{ip}</text>')
    svg = (f'<svg class="plan-svg" viewBox="0 0 {W} {H}" role="img" aria-label="Réseau de la salle : Internet, '
           'le routeur (repère 1), le commutateur (repère 2), le serveur (repère 3) et deux postes clients">'
           # liaisons : Internet (tirets orange), câbles Ethernet (bleu)
           f'<path d="M150 150H200" stroke="{orange}" stroke-width="4" stroke-dasharray="9 6" fill="none"/>'
           f'<g stroke="{bleu}" stroke-width="4" fill="none" stroke-linejoin="round">'
           '<path d="M350 150H420"/><path d="M495 200V230"/><path d="M570 150H596V86H620"/>'
           '<path d="M596 150V226H620"/></g>'
           f'<path d="M48 168c-26 0-30-34-6-40c-2-26 34-34 46-14c12-26 60-22 64 6c24 2 30 34 6 48z" fill="#FFFFFF" '
           f'stroke="#9DB6D6" stroke-width="2.5"/><text x="96" y="160" text-anchor="middle" font-size="17" '
           f'font-weight="700" fill="{bleu}">Internet</text>'
           + bloc(200, 100, routeur) + bloc(420, 100, commutateur) + bloc(420, 230, serveur)
           + poste(622, 64, "Poste 1", "192.168.1.11") + poste(622, 204, "Poste 2", "192.168.1.12")
           + "</svg>")
    cases = {"1": (210, 166, 130, 26, ""), "2": (430, 166, 130, 26, ""), "3": (430, 290, 130, 30, "")}
    return {"svg": svg, "w": W, "h": H, "cases": cases, "maxw": W,
            "caption": "Figure 1 — Le réseau de la salle : les trois cases repérées en rouge reçoivent les étiquettes."}


DP1 = ("""<div class="doc-text"><h3>Le réseau de la salle</h3><p>Les postes de la salle, le serveur et le routeur sont
reliés au même commutateur par des câbles Ethernet. Le routeur relie le réseau local à Internet : c'est la
passerelle des postes.</p>
<table class="t"><thead><tr><th>Équipement</th><th>Adresse IP</th><th>Adresse MAC</th></tr></thead><tbody>
<tr><td>Routeur (passerelle)</td><td>192.168.1.1</td><td>00:1A:2B:3C:4D:01</td></tr>
<tr><td>Serveur</td><td>192.168.1.2</td><td>00:1A:2B:3C:4D:02</td></tr>
<tr><td>Poste 1</td><td>192.168.1.11</td><td>00:1A:2B:3C:4D:11</td></tr>
<tr><td>Poste 2</td><td>192.168.1.12</td><td>00:1A:2B:3C:4D:12</td></tr></tbody></table>
<p>Masque de sous-réseau de tous les équipements : <b>255.255.255.0</b>, soit <b>/24</b>.</p></div>""")

DT1 = ("""<div class="doc-text"><h3>Adresse IPv4 et masque</h3><ul>
<li>Une adresse <b>IPv4</b> compte 32 bits, soit 4 octets ; on l'écrit en notation pointée, chaque octet en décimal
(de 0 à 255) : 192.168.1.12.</li>
<li>Le <b>masque</b> désigne la partie réseau de l'adresse : avec /24 (255.255.255.0), les 24 premiers bits
désignent le réseau, les 8 derniers l'hôte.</li>
<li>L'<b>adresse du réseau</b> a tous ses bits d'hôte à 0 ; l'<b>adresse de diffusion</b> (broadcast), tous à 1.
Aucune des deux ne peut être donnée à un équipement : un réseau /n offre 2<sup>32 − n</sup> − 2 adresses
d'hôtes.</li>
<li>Une adresse <b>MAC</b> compte 48 bits ; elle identifie la carte réseau d'un équipement.</li></ul></div>""")

E_EQUIPEMENTS = ["Le routeur", "Le commutateur", "Le serveur", "Le point d'accès Wi-Fi", "Le poste client"]
E_DONNEES = ["Adresse IP", "Adresse MAC", "Masque de sous-réseau", "Nom de domaine"]

CARTES = [
    ("bleu", "COMMUTATEUR", "Relie les équipements d'un même réseau local. Il envoie chaque trame vers le seul port "
     "où se trouve son destinataire, repéré par son adresse MAC.", "Dans la salle : il relie les postes, le serveur "
     "et le routeur."),
    ("orange", "ROUTEUR", "Relie des réseaux différents, par exemple le réseau local et Internet. Il choisit la route "
     "de chaque paquet d'après son adresse IP de destination.", "C'est la passerelle des postes : 192.168.1.1."),
    ("vert", "POINT D'ACCÈS", "Relie au réseau local les appareils sans fil (Wi-Fi).",
     "Ordinateurs portables, tablettes, téléphones."),
    ("bleu", "SERVEUR", "Fournit un service aux postes clients : partage de fichiers, impression, attribution des "
     "adresses…", "Dans la salle : 192.168.1.2."),
]
JEU = [("Relier les postes d'une même salle", "com"), ("Relier le réseau local à Internet", "rou"),
       ("Lire l'adresse MAC de destination d'une trame", "com"),
       ("Choisir la route d'un paquet d'après son adresse IP", "rou")]
QUIZ = [
    ("Combien de bits compte une adresse IPv4 ?", ["16", "32", "48"], 1,
     "Quatre octets de 8 bits : 4 × 8 = 32 bits. Une adresse MAC en compte 48."),
    ("Une adresse MAC identifie…", ["une carte réseau", "un réseau entier", "un site web"], 0,
     "Elle est inscrite dans la carte réseau par son fabricant ; le commutateur s'en sert pour acheminer les trames."),
    ("Quel matériel relie le réseau local à Internet ?", ["Le commutateur", "Le routeur", "Le point d'accès"], 1,
     "Le routeur relie des réseaux différents : il est la passerelle des postes vers Internet."),
]

# script propre au cours : une adresse IPv4 écrite en binaire, octet par octet
COURS_JS = r"""
  function initCoursModele(home) {
    initCours(home);
    var champ = home.querySelector("#cm-ip"), sortie = home.querySelector("#cm-bin");
    function maj() {
      var o = champ.value.trim().split(".");
      var ok = o.length === 4 && o.every(function (x) { return /^\d{1,3}$/.test(x) && +x <= 255; });
      sortie.textContent = ok ? o.map(function (x) { return ("0000000" + (+x).toString(2)).slice(-8); }).join(" . ")
        : "Adresse incomplète ou invalide : quatre nombres de 0 à 255, séparés par des points.";
      sortie.classList.toggle("ko", !ok);
    }
    champ.addEventListener("input", maj);
    maj();
  }
"""
COURS_CSS = """
/* ---------- cours modèle : adresse IPv4 en binaire ---------- */
.cm-ip{display:flex; flex-wrap:wrap; gap:8px 14px; align-items:center}
.cm-ip input{font:600 1.05rem ui-monospace,Consolas,monospace; padding:6px 10px; border:1.5px solid var(--encre-2); width:12em}
.cm-bin{font:700 1.05rem ui-monospace,Consolas,monospace; color:var(--bleu); margin:10px 0 0; overflow-wrap:anywhere}
.cm-bin.ko{font:600 .92rem var(--f-texte); color:var(--rouge)}
"""


def contenu(g):
    """Le cours et l'exercice modèles ; g : le module generer (ses blocs, correcteurs et éléments de cours)."""
    P, KW, IP, NUM, GRP, Q, QBAR, DOC = g.P, g.KW, g.IP, g.NUM, g.GRP, g.Q, g.QBAR, g.DOC

    def render_cours():
        s1 = g.course_section(1, "cm-materiels", "Les matériels du réseau local",
                              "<p>Un réseau local relie les équipements d'un même lieu : postes, serveur, imprimante. "
                              "Chaque matériel y joue un rôle précis.</p><p class=\"cours-defi\">À toi : retourne "
                              "chaque carte pour lire le rôle du matériel.</p>" + g.cartes_html(CARTES))
        s2 = g.course_section(2, "cm-binaire", "Une adresse IPv4 en binaire",
                              "<p>Une adresse IPv4 compte 32 bits, rangés en quatre octets ; on l'écrit en décimal, "
                              "octet par octet, séparés par des points.</p>"
                              '<div class="simu"><h3>Écris une adresse</h3><div class="cm-ip"><label for="cm-ip">'
                              'Adresse IPv4</label><input id="cm-ip" type="text" value="192.168.1.12" '
                              'autocomplete="off" spellcheck="false"></div><p class="cm-bin" id="cm-bin" '
                              'aria-live="polite"></p></div>')
        s3 = g.course_section(3, "cm-jeu", "Jeu : commutateur ou routeur ?",
                              "<p>Pour chaque tâche, indique le matériel qui la réalise.</p>"
                              + g.jeu_html(JEU, [("com", "Commutateur"), ("rou", "Routeur")], "jeu-materiel"))
        s4 = g.quiz_section(4, "cm-quiz", QUIZ, "qm_")
        return f"""<div class="cours" id="cours-modele">
{g.course_head("Cours modèle", "Niveau 1", "Les matériels du réseau local",
               "Page modèle d'un cours : en-tête, objectifs et prérequis, sommaire, sections, cartes à retourner, "
               "élément interactif propre au cours, jeu et quiz. Environ 10 minutes.")}
{g.course_fiche(["Citer les matériels d'un réseau local et leur rôle.",
                 "Lire une adresse IPv4 en notation pointée et en binaire."], ["Numération binaire : bit, octet."])}
{g.course_nav([("cm-materiels", "Les matériels"), ("cm-binaire", "En binaire"), ("cm-jeu", "Jeu"), ("cm-quiz", "Quiz")])}
{s1}{s2}{s3}{s4}
{g.course_foot(("?ex=exercice-modele", "S'entraîner : exercice modèle"))}
</div>"""

    cours = [{"key": "cours-modele", "tag": "Cours modèle", "level": "Niveau 1",
              "title": "Les matériels du réseau local", "mots": ["Commutateur", "Routeur", "Binaire", "Jeu", "Quiz"],
              "vign": "carte-cours", "alt": "Point d'accès sans fil, ordinateur portable et téléphone",
              "render": render_cours, "js": COURS_JS, "init": "initCoursModele", "css": COURS_CSS}]

    parts = [
        {"title": "Adresses du réseau", "minutes": 12, "intro": [
            "<p>Le réseau de la salle est décrit dans le dossier de présentation DP1 ; le dossier technique DT1 "
            "rappelle l'écriture des adresses.</p>"], "blocks": [
            QBAR(["DP1", "DT1"]),
            Q("Quel matériel relie entre eux les postes de la salle, au sein du réseau local ?", "Un ou deux mots.",
              KW(P("commutateur|switch"), forbid="routeur"), "Le commutateur (switch)",
              "<p>Le <strong>commutateur</strong> relie les équipements d'un même réseau local ; le routeur relie le "
              "réseau local à un autre réseau (Internet).</p>"),
            Q("Quelle est l'adresse IP du poste 2 ?", "Écris l'adresse seule, en notation pointée.",
              IP("192.168.1.12"), "192.168.1.12", "<p>Elle se lit dans le tableau du DP1.</p>"),
            Q("Combien d'adresses d'hôtes utilisables compte le réseau 192.168.1.0/24 ?", "Un nombre.",
              NUM(254), "254",
              "<p>Avec /24, il reste 32 − 24 = 8 bits d'hôte : " + g.calc("2⁸ − 2 = 256 − 2 = 254") + "</p><p>On "
              "retire l'adresse du réseau et l'adresse de diffusion, qui ne peuvent pas être données à un "
              "équipement.</p>"),
            GRP("Donne l'adresse du réseau de la salle et son adresse de diffusion.",
                "Une adresse par case, en notation pointée.", [
                    ("Adresse du réseau", IP("192.168.1.0"), "192.168.1.0"),
                    ("Adresse de diffusion", IP("192.168.1.255"), "192.168.1.255")],
                "<p>Le masque /24 garde les trois premiers octets pour le réseau : 192.168.1. Le dernier octet "
                "désigne l'hôte : tous ses bits à 0 donnent l'<strong>adresse du réseau</strong> (192.168.1.0), "
                "tous à 1 l'<strong>adresse de diffusion</strong> (192.168.1.255).</p>"),
        ]},
        {"title": "Les équipements de la salle", "minutes": 8, "plan": plan_reseau(g), "intro": [
            "<p>La figure 1 représente le réseau de la salle.</p>"], "blocks": [
            GRP("Nomme les équipements repérés 1, 2 et 3 sur la figure 1.", "Un équipement par case.", [
                ("Repère 1", KW(P("routeur")), "Le routeur"),
                ("Repère 2", KW(P("commutateur|switch")), "Le commutateur"),
                ("Repère 3", KW(P("serveur")), "Le serveur")],
                "<ul><li><strong>Repère 1 — le routeur</strong> : il relie le réseau local à Internet.</li>"
                "<li><strong>Repère 2 — le commutateur</strong> : tous les équipements de la salle y sont "
                "reliés.</li><li><strong>Repère 3 — le serveur</strong> : il fournit ses services aux postes.</li>"
                "</ul>", etiquettes=E_EQUIPEMENTS, liste="Équipements", reperes=["1", "2", "3"]),
            GRP("Indique la nature de chacune de ces données, relevées sur le poste 2.",
                "Une étiquette par case ; une étiquette ne sert pas.", [
                    ("192.168.1.12", KW(P("ip"), forbid="mac|masque"), "Adresse IP"),
                    ("00:1A:2B:3C:4D:12", KW(P("mac")), "Adresse MAC"),
                    ("255.255.255.0", KW(P("masque")), "Masque de sous-réseau")],
                "<p>Quatre nombres de 0 à 255 : une <strong>adresse IP</strong> ou un <strong>masque</strong> ; le "
                "masque se reconnaît à ses bits à 1 suivis de bits à 0 (255.255.255.0). Six octets en hexadécimal : "
                "une <strong>adresse MAC</strong>.</p>", etiquettes=E_DONNEES),
        ]},
        {"title": "Questions à propositions", "minutes": 5, "blocks": [
            qcm.QCM("Quel protocole attribue automatiquement une adresse IP à un poste qui se connecte au réseau ?",
                    [("A", "DNS"), ("B", "DHCP"), ("C", "HTTP")], ["B"],
                    "Le serveur DHCP fournit au poste son adresse IP, son masque, sa passerelle et l'adresse du "
                    "serveur DNS. Le DNS traduit un nom de domaine en adresse IP ; HTTP sert à échanger des pages "
                    "web."),
            qcm.QCM("Quelles adresses sont des adresses IPv4 privées, réservées aux réseaux locaux ?",
                    [(1, "192.168.1.12"), (2, "10.0.0.5"), (3, "8.8.8.8"), (4, "172.16.4.1")], [1, 2, 4],
                    "Les plages privées sont 10.0.0.0/8, 172.16.0.0/12 (de 172.16 à 172.31) et 192.168.0.0/16 ; "
                    "8.8.8.8 est une adresse publique."),
        ]},
    ]
    exos = [{"key": "exercice-modele", "prefix": "m", "tag": "Exercice modèle", "level": "Niveau 1",
             "title": "Le réseau de la salle", "parts": parts,
             "docs": [DOC("DP1", "Le réseau de la salle", DP1), DOC("DT1", "Adresse IPv4 et masque", DT1)],
             "consignes": g.consignes(g.C_SAISIE, g.C_GROUPE, g.C_ETIQUETTES, g.C_SCHEMA, qcm.C_QCM,
                                      g.C_DOCUMENTS),
             "hero": ("accueil", "Un réseau local relié à Internet par un routeur",
                      "Postes, serveur, commutateur et routeur."),
             "mots": ["Adressage", "Étiquettes", "Schéma", "QCM"], "vign": "carte-exercice",
             "valt": "Commutateur relié aux postes clients",
             "sub": "Page modèle d'un exercice : questions à saisir (mots-clés, adresse, nombre), cases à remplir "
                    "ensemble, étiquettes à glisser, schéma à compléter et questions à propositions, avec les "
                    "documents du sujet."}]
    return cours, exos
