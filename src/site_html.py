"""Exercice 1.2 — Mon premier site (Niveau 1) : écrire un petit site dans un éditeur intégré à la page.

Le site « Mon réseau » présente le réseau de la maison : une page d'accueil (index.html), une page « Le matériel »
(materiel.html) et une feuille de style (style.css), plus une image fournie (reseau.png). L'élève écrit le code dans
l'éditeur (onglets des fichiers, coloration du code, numéros de ligne) ; l'aperçu affiche le site en direct et ses
liens mènent d'une page à l'autre, comme dans un navigateur (une page absente donne une erreur 404). Le site se
télécharge en .zip.

Chaque question est une liste de critères (GRP auto du générateur) : le script de l'éditeur vérifie le code et
écrit, dans la case masquée de chaque critère, « oui » ou « non » (vide tant que le fichier n'a pas été modifié) ;
le moteur du gabarit corrige ces cases comme les autres : modes entraînement et examen, note pondérée, impression.
L'aperçu n'exécute aucun script : l'iframe est isolée (sandbox), et ses liens sont relayés par la page.

exercice(g) reçoit le module generer : pas d'import circulaire. Classes et identifiants propres : préfixe « ed- ».
"""
import json

ORDRE = ["index.html", "materiel.html", "style.css"]
DEPART = {
    "index.html": "<!DOCTYPE html>\n<html>\n  <head>\n    <meta charset=\"utf-8\">\n  </head>\n  <body>\n\n  </body>\n</html>\n",
    "materiel.html": "<!-- La page « Le matériel » : écris-la ici. Tu peux recopier le squelette de index.html. -->\n",
    "style.css": "/* La feuille de style du site : les règles de mise en forme des deux pages. */\n",
}
IMAGE = "reseau.png"  # l'illustration de l'accueil du site, fournie (src/images/accueil.png)

# critère : (fichier vérifié, énoncé, exemple de code juste)
CRITERES = {
    "lang": ("index.html", "La balise <code>&lt;html&gt;</code> indique la langue de la page : <code>lang=\"fr\"</code>.",
             '<code>&lt;html lang="fr"&gt;</code>'),
    "titre": ("index.html", "L'en-tête <code>&lt;head&gt;</code> contient le titre de l'onglet, "
              "<code>&lt;title&gt;</code> : « Mon réseau ».", "<code>&lt;title&gt;Mon réseau&lt;/title&gt;</code>"),
    "h1": ("index.html", "Le corps <code>&lt;body&gt;</code> contient un grand titre <code>&lt;h1&gt;</code>.",
           "<code>&lt;h1&gt;Le réseau de la maison&lt;/h1&gt;</code>"),
    "p": ("index.html", "Un paragraphe <code>&lt;p&gt;</code> d'au moins dix mots présente le réseau.",
          "<code>&lt;p&gt;Chez moi, la box relie à Internet les ordinateurs, les téléphones et la "
          "console.&lt;/p&gt;</code>"),
    "strong": ("index.html", "Un mot important est mis en valeur avec <code>&lt;strong&gt;</code>.",
               "<code>la &lt;strong&gt;box&lt;/strong&gt;</code>"),
    "h2": ("index.html", "Un sous-titre <code>&lt;h2&gt;</code> annonce la liste.",
           "<code>&lt;h2&gt;Les équipements&lt;/h2&gt;</code>"),
    "ul": ("index.html", "Une liste à puces <code>&lt;ul&gt;</code>.", "<code>&lt;ul&gt; … &lt;/ul&gt;</code>"),
    "li": ("index.html", "La liste compte au moins trois éléments <code>&lt;li&gt;</code>.",
           "<code>&lt;li&gt;La box&lt;/li&gt; &lt;li&gt;L'ordinateur&lt;/li&gt; &lt;li&gt;Le téléphone&lt;/li&gt;</code>"),
    "img": ("index.html", "Une image <code>&lt;img&gt;</code> affiche le fichier <code>reseau.png</code>.",
            '<code>&lt;img src="reseau.png" …&gt;</code>'),
    "alt": ("index.html", "L'image a un texte alternatif <code>alt</code> qui la décrit.",
            '<code>&lt;img src="reseau.png" alt="Le réseau de la maison"&gt;</code>'),
    "squelette": ("materiel.html", "La page a un squelette complet : <code>&lt;!DOCTYPE html&gt;</code>, "
                  "<code>&lt;html lang=\"fr\"&gt;</code>, <code>&lt;head&gt;</code> avec un <code>&lt;title&gt;</code>, "
                  "<code>&lt;body&gt;</code>.", "le squelette de index.html, avec "
                  "<code>&lt;title&gt;Le matériel&lt;/title&gt;</code>"),
    "mh1": ("materiel.html", "Un grand titre <code>&lt;h1&gt;</code> : « Le matériel ».",
            "<code>&lt;h1&gt;Le matériel&lt;/h1&gt;</code>"),
    "table": ("materiel.html", "Un tableau <code>&lt;table&gt;</code> d'au moins trois lignes <code>&lt;tr&gt;</code>.",
              "<code>&lt;table&gt; &lt;tr&gt;…&lt;/tr&gt; &lt;tr&gt;…&lt;/tr&gt; &lt;tr&gt;…&lt;/tr&gt; &lt;/table&gt;</code>"),
    "th": ("materiel.html", "Une ligne d'en-tête avec des cellules <code>&lt;th&gt;</code> : « Appareil », « Adresse IP ».",
           "<code>&lt;tr&gt;&lt;th&gt;Appareil&lt;/th&gt;&lt;th&gt;Adresse IP&lt;/th&gt;&lt;/tr&gt;</code>"),
    "ip": ("materiel.html", "Une cellule <code>&lt;td&gt;</code> donne une adresse IP, par exemple 192.168.1.10.",
           "<code>&lt;td&gt;192.168.1.10&lt;/td&gt;</code>"),
    "lien1": ("index.html", "La page d'accueil a un lien vers la page du matériel : "
              "<code>&lt;a href=\"materiel.html\"&gt;</code>.",
              '<code>&lt;a href="materiel.html"&gt;Le matériel&lt;/a&gt;</code>'),
    "lien2": ("materiel.html", "La page du matériel a un lien de retour vers l'accueil, <code>index.html</code>.",
              '<code>&lt;a href="index.html"&gt;Accueil&lt;/a&gt;</code>'),
    "css1": ("index.html", "La page d'accueil utilise la feuille de style : <code>&lt;link rel=\"stylesheet\" "
             "href=\"style.css\"&gt;</code> dans le <code>&lt;head&gt;</code>.",
             '<code>&lt;link rel="stylesheet" href="style.css"&gt;</code>'),
    "css2": ("materiel.html", "La page du matériel utilise aussi <code>style.css</code>.",
             '<code>&lt;link rel="stylesheet" href="style.css"&gt;</code>'),
    "fond": ("style.css", "Une couleur de fond pour les pages : règle <code>body</code>, propriété "
             "<code>background-color</code>.", "<code>body { background-color: lightyellow; }</code>"),
    "police": ("style.css", "Une police pour le texte : règle <code>body</code>, propriété <code>font-family</code>.",
               "<code>body { font-family: Arial, sans-serif; }</code>"),
    "couleur": ("style.css", "Une couleur pour les grands titres : règle <code>h1</code>, propriété <code>color</code>.",
                "<code>h1 { color: navy; }</code>"),
    "bord": ("style.css", "Des bordures pour le tableau : règle <code>table, th, td</code>, propriété "
             "<code>border</code>.", "<code>table, th, td { border: 1px solid gray; }</code>"),
}
OUI = {"type": "yesno", "value": True}  # case remplie par le script de l'éditeur : « oui » si le critère est rempli


def editeur(fichier, page=None):
    """Un éditeur du site ; toutes les parties partagent les mêmes fichiers. fichier : l'onglet ouvert au départ ;
    page : la page affichée dans l'aperçu (par défaut, le fichier ouvert, ou l'accueil pour la feuille de style)."""
    page = page or (fichier if fichier.endswith(".html") else "index.html")
    onglets = "".join(f'<button type="button" class="ed-ong" role="tab" data-f="{f}" aria-selected="false">{f}</button>'
                      for f in ORDRE)
    return (f'<div class="ed" data-fichier="{fichier}" data-page="{page}">'
            f'<div class="ed-barre"><div class="ed-onglets" role="tablist" aria-label="Fichiers du site">{onglets}</div>'
            '<span class="ed-img small">image fournie : <code>reseau.png</code></span>'
            '<button type="button" class="btn ghost ed-reinit">Réinitialiser ce fichier</button>'
            '<button type="button" class="btn ghost ed-zip">Télécharger mon site (.zip)</button></div>'
            '<div class="ed-corps"><div class="ed-code"><pre class="ed-num" aria-hidden="true"></pre>'
            '<div class="ed-zone"><pre class="ed-hl" aria-hidden="true"><code></code></pre>'
            '<textarea class="ed-ta" wrap="off" spellcheck="false" autocomplete="off" autocapitalize="off" '
            'aria-label="Code du fichier"></textarea></div></div>'
            '<div class="ed-apercu"><div class="ed-ap-barre"><button type="button" class="ed-retour" '
            'aria-label="Page précédente" disabled>◀</button><span class="ed-url">mon-site/index.html</span></div>'
            '<iframe class="ed-if" sandbox="allow-same-origin" title="Aperçu du site"></iframe></div></div>'
            '<p class="ed-etat small" aria-live="polite">Tab insère deux espaces ; Échap puis Tab pour quitter '
            "l'éditeur. L'aperçu se met à jour pendant que tu écris.</p>"
            '<pre class="ed-print print-only"></pre></div>')


def _plan_site():
    """Plan du site (DP1) : les deux pages liées, la feuille de style et l'image."""
    def page(x, nom, lignes):
        return (f'<g transform="translate({x} 20)"><rect width="190" height="150" rx="6" fill="#FFFFFF" '
                f'stroke="#1C2530" stroke-width="2"/><rect width="190" height="24" rx="6" fill="#D3D8D5"/>'
                f'<text x="12" y="17" font-size="13" font-weight="700" font-family="ui-monospace,monospace">{nom}</text>'
                + "".join(f'<text x="14" y="{48 + 20 * i}" font-size="12.5">{t}</text>' for i, t in enumerate(lignes))
                + "</g>")
    return ('<svg class="dp-svg" viewBox="0 0 640 260" role="img" aria-label="Plan du site : la page d\'accueil et la '
            'page du matériel, liées entre elles, utilisent la même feuille de style">'
            '<defs><marker id="ed-fl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
            'orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#1F5FA8"/></marker></defs>'
            + page(30, "index.html", ["titre h1", "paragraphe, mot en valeur", "sous-titre h2 et liste",
                                      "image reseau.png", "lien vers le matériel"])
            + page(420, "materiel.html", ["titre h1 « Le matériel »", "tableau des appareils", "et de leurs adresses IP",
                                          "lien vers l'accueil"])
            + '<path d="M222 90H416" stroke="#1F5FA8" stroke-width="2.5" marker-start="url(#ed-fl)" '
            'marker-end="url(#ed-fl)"/><text x="320" y="82" text-anchor="middle" font-size="12.5" fill="#1F5FA8">liens'
            '</text><g transform="translate(250 200)"><rect width="140" height="44" rx="6" fill="#FCEFD8" '
            'stroke="#B26A00" stroke-width="2"/><text x="70" y="27" text-anchor="middle" font-size="13" '
            'font-weight="700" font-family="ui-monospace,monospace">style.css</text></g>'
            '<path d="M125 172V222H248M515 172V222H392" stroke="#B26A00" stroke-width="2" stroke-dasharray="6 4" '
            'fill="none"/><text x="320" y="192" text-anchor="middle" font-size="12" fill="#B26A00">mise en forme des '
            "deux pages</text></svg>")


DP1 = ("<div class=\"doc-text\"><h3>Le site à réaliser : « Mon réseau »</h3><p>Le site présente le réseau de ta maison. "
       "Il compte deux pages, reliées par des liens, et une feuille de style commune :</p>" + _plan_site()
       + "<ul><li><b>index.html</b>, l'accueil : un grand titre, un paragraphe qui présente le réseau, un sous-titre et "
       "la liste des équipements (box, ordinateur, téléphone…), l'image <code>reseau.png</code> et un lien vers la "
       "page du matériel ;</li><li><b>materiel.html</b>, « Le matériel » : un grand titre, un tableau des appareils et "
       "de leurs adresses IP (des adresses privées, de la forme 192.168.1.x) et un lien de retour vers l'accueil ;</li>"
       "<li><b>style.css</b> : la couleur de fond et la police des pages, la couleur des titres, les bordures du "
       "tableau.</li></ul><p>L'aperçu de l'éditeur joue le rôle du navigateur : quand tu cliques sur un lien, il "
       "affiche l'autre page, comme le ferait un navigateur après une requête HTTP. Une page qui n'existe pas donne "
       "une erreur 404.</p></div>")

DT1 = """<div class="doc-text"><h3>Le squelette d'une page HTML</h3>
<pre class="ed-doc">&lt;!DOCTYPE html&gt;
&lt;html lang="fr"&gt;
  &lt;head&gt;
    &lt;meta charset="utf-8"&gt;
    &lt;title&gt;Titre de l'onglet&lt;/title&gt;
    &lt;link rel="stylesheet" href="style.css"&gt;
  &lt;/head&gt;
  &lt;body&gt;
    … le contenu de la page …
  &lt;/body&gt;
&lt;/html&gt;</pre>
<p>Une balise s'ouvre (<code>&lt;p&gt;</code>) et se ferme (<code>&lt;/p&gt;</code>) ; certaines n'ont pas de
fermeture (<code>&lt;img&gt;</code>, <code>&lt;meta&gt;</code>, <code>&lt;link&gt;</code>). Un attribut précise une
balise : <code>nom="valeur"</code>.</p>
<table class="t"><thead><tr><th>Balise</th><th>Rôle</th><th>Exemple</th></tr></thead><tbody>
<tr><td><code>&lt;h1&gt;</code>, <code>&lt;h2&gt;</code></td><td>grand titre, sous-titre</td><td><code>&lt;h2&gt;Les équipements&lt;/h2&gt;</code></td></tr>
<tr><td><code>&lt;p&gt;</code></td><td>paragraphe</td><td><code>&lt;p&gt;Mon réseau compte trois appareils.&lt;/p&gt;</code></td></tr>
<tr><td><code>&lt;strong&gt;</code>, <code>&lt;em&gt;</code></td><td>mot important, mot accentué</td><td><code>la &lt;strong&gt;box&lt;/strong&gt;</code></td></tr>
<tr><td><code>&lt;ul&gt;</code>, <code>&lt;li&gt;</code></td><td>liste à puces, élément de la liste</td><td><code>&lt;ul&gt;&lt;li&gt;La box&lt;/li&gt;&lt;/ul&gt;</code></td></tr>
<tr><td><code>&lt;img&gt;</code></td><td>image ; <code>alt</code> la décrit (lecteurs d'écran, image absente)</td><td><code>&lt;img src="reseau.png" alt="Mon réseau"&gt;</code></td></tr>
<tr><td><code>&lt;a&gt;</code></td><td>lien vers une autre page</td><td><code>&lt;a href="materiel.html"&gt;Le matériel&lt;/a&gt;</code></td></tr>
<tr><td><code>&lt;table&gt;</code>, <code>&lt;tr&gt;</code></td><td>tableau, ligne du tableau</td><td rowspan="2"><code>&lt;table&gt;<br>&nbsp;&nbsp;&lt;tr&gt;&lt;th&gt;Appareil&lt;/th&gt;&lt;th&gt;Adresse IP&lt;/th&gt;&lt;/tr&gt;<br>&nbsp;&nbsp;&lt;tr&gt;&lt;td&gt;Box&lt;/td&gt;&lt;td&gt;192.168.1.1&lt;/td&gt;&lt;/tr&gt;<br>&lt;/table&gt;</code></td></tr>
<tr><td><code>&lt;th&gt;</code>, <code>&lt;td&gt;</code></td><td>cellule d'en-tête, cellule</td></tr>
</tbody></table></div>"""

DT2 = """<div class="doc-text"><h3>Les règles CSS</h3>
<p>Une règle choisit des éléments (le <b>sélecteur</b>) et leur donne des <b>propriétés</b> :</p>
<pre class="ed-doc">sélecteur {
  propriété: valeur;
  propriété: valeur;
}

body { background-color: lightyellow; font-family: Arial, sans-serif; }
h1 { color: navy; }
table, th, td { border: 1px solid gray; border-collapse: collapse; padding: 4px 8px; }</pre>
<table class="t"><thead><tr><th>Propriété</th><th>Effet</th><th>Exemples de valeurs</th></tr></thead><tbody>
<tr><td><code>background-color</code></td><td>couleur de fond</td><td><code>lightyellow</code>, <code>#E6EEF8</code></td></tr>
<tr><td><code>color</code></td><td>couleur du texte</td><td><code>navy</code>, <code>darkred</code>, <code>#1F5FA8</code></td></tr>
<tr><td><code>font-family</code></td><td>police</td><td><code>Arial, sans-serif</code>, <code>Verdana</code>, <code>Georgia, serif</code></td></tr>
<tr><td><code>font-size</code></td><td>taille du texte</td><td><code>18px</code>, <code>1.2em</code></td></tr>
<tr><td><code>border</code></td><td>bordure : épaisseur, style, couleur</td><td><code>1px solid gray</code>, <code>2px dashed navy</code></td></tr>
<tr><td><code>text-align</code></td><td>alignement du texte</td><td><code>center</code>, <code>left</code></td></tr>
<tr><td><code>width</code></td><td>largeur (d'une image, par exemple)</td><td><code>400px</code>, <code>50%</code></td></tr>
</tbody></table>
<p>Les couleurs s'écrivent par leur nom anglais (<code>white</code>, <code>black</code>, <code>lightblue</code>,
<code>orange</code>…) ou en hexadécimal (<code>#RRVVBB</code>) : on retrouve la notation de l'adresse MAC.</p></div>"""


def question(g, codes, stem, hint, why):
    return g.GRP(stem, hint, [(f'<span data-chk="{c}">{CRITERES[c][1]}</span>', OUI, CRITERES[c][2]) for c in codes],
                 why, auto=True)


def parties(g):
    return [
        {"title": "Le squelette de la page d'accueil", "minutes": 8, "intro": [
            "<p>Tu vas écrire le site « Mon réseau » (dossier DP1), page après page, dans l'éditeur ci-dessous ; "
            "l'aperçu, à droite, affiche le site comme un navigateur. Les quatre parties travaillent sur les mêmes "
            "fichiers : l'éditeur de chaque partie reprend ton code là où tu l'as laissé.</p><p><b>À faire</b> : dans "
            "<code>index.html</code>, indique la langue de la page dans la balise <code>&lt;html&gt;</code>, ajoute "
            "dans le <code>&lt;head&gt;</code> le titre de l'onglet, « Mon réseau », puis écris un grand titre "
            "<code>&lt;h1&gt;</code> dans le <code>&lt;body&gt;</code>. Le dossier technique DT1 donne le squelette "
            "complet.</p>"], "blocks": [
            g.QBAR(["DP1", "DT1"], "dans l'éditeur"),
            g.HTML(editeur("index.html")),
            question(g, ["lang", "titre", "h1"], "Complète le squelette de la page d'accueil, <code>index.html</code>.",
                     "Quand ton code est prêt, fais-le vérifier : chaque critère vaut un point.",
                     "<p>La balise <code>&lt;html&gt;</code> porte l'attribut <code>lang</code> ; le titre de l'onglet "
                     "se place dans l'en-tête <code>&lt;head&gt;</code>, tout ce qui s'affiche dans le corps "
                     "<code>&lt;body&gt;</code> :</p>" + g.calc("&lt;html lang=\"fr\"&gt; … &lt;title&gt;Mon "
                                                                "réseau&lt;/title&gt; … &lt;h1&gt;Le réseau de la "
                                                                "maison&lt;/h1&gt;")),
        ]},
        {"title": "Le contenu de l'accueil", "minutes": 14, "intro": [
            "<p><b>À faire</b> : toujours dans <code>index.html</code>, présente ton réseau dans un paragraphe et mets "
            "en valeur un mot important ; ajoute un sous-titre et la liste des équipements de la maison ; insère "
            "l'image fournie, <code>reseau.png</code>, avec un texte alternatif.</p>"], "blocks": [
            g.QBAR(["DP1", "DT1"], "dans l'éditeur"),
            g.HTML(editeur("index.html")),
            question(g, ["p", "strong"], "Présente ton réseau dans un paragraphe.", "Dix mots au moins.",
                     "<p>Un paragraphe s'écrit entre <code>&lt;p&gt;</code> et <code>&lt;/p&gt;</code> ; "
                     "<code>&lt;strong&gt;</code> met en valeur un mot à l'intérieur du texte.</p>"),
            question(g, ["h2", "ul", "li"], "Liste les équipements du réseau sous un sous-titre.",
                     "Une puce par équipement.",
                     "<p>La liste à puces <code>&lt;ul&gt;</code> contient un élément <code>&lt;li&gt;</code> par "
                     "équipement :</p>" + g.calc("&lt;h2&gt;Les équipements&lt;/h2&gt; &lt;ul&gt; &lt;li&gt;La box"
                                                 "&lt;/li&gt; &lt;li&gt;L'ordinateur&lt;/li&gt; &lt;li&gt;Le "
                                                 "téléphone&lt;/li&gt; &lt;/ul&gt;")),
            question(g, ["img", "alt"], "Insère l'illustration du réseau.",
                     "L'image s'appelle reseau.png ; décris-la dans l'attribut alt.",
                     "<p>La balise <code>&lt;img&gt;</code> n'a pas de fermeture ; son attribut <code>src</code> "
                     "donne le fichier, <code>alt</code> le décrit pour qui ne voit pas l'image :</p>"
                     + g.calc("&lt;img src=\"reseau.png\" alt=\"Le réseau de la maison\"&gt;")),
        ]},
        {"title": "Une deuxième page et des liens", "minutes": 15, "intro": [
            "<p><b>À faire</b> : écris la page <code>materiel.html</code> (onglet du même nom) : son squelette "
            "complet, un grand titre « Le matériel » et un tableau des appareils de la maison avec leurs adresses IP "
            "(des adresses privées, de la forme 192.168.1.x). Relie ensuite les deux pages par des liens : clique "
            "sur un lien dans l'aperçu pour changer de page.</p>"], "blocks": [
            g.QBAR(["DP1", "DT1"], "dans l'éditeur"),
            g.HTML(editeur("materiel.html")),
            question(g, ["squelette", "mh1", "table", "th", "ip"], "Écris la page du matériel, "
                     "<code>materiel.html</code>.", "Une ligne d'en-tête, puis une ligne par appareil.",
                     "<p>La page reprend le squelette de l'accueil. Dans le tableau, chaque ligne "
                     "<code>&lt;tr&gt;</code> contient ses cellules : <code>&lt;th&gt;</code> pour l'en-tête, "
                     "<code>&lt;td&gt;</code> pour les données.</p>"
                     + g.calc("&lt;tr&gt;&lt;th&gt;Appareil&lt;/th&gt;&lt;th&gt;Adresse IP&lt;/th&gt;&lt;/tr&gt; "
                              "&lt;tr&gt;&lt;td&gt;Ordinateur&lt;/td&gt;&lt;td&gt;192.168.1.10&lt;/td&gt;&lt;/tr&gt;")),
            question(g, ["lien1", "lien2"], "Relie les deux pages par des liens.",
                     "Un lien sur chaque page, vers l'autre.",
                     "<p>L'attribut <code>href</code> du lien <code>&lt;a&gt;</code> donne le nom du fichier de "
                     "l'autre page. Sur un vrai site, cliquer sur le lien fait envoyer au navigateur une requête HTTP "
                     "pour cette page.</p>"),
        ]},
        {"title": "La mise en forme", "minutes": 11, "intro": [
            "<p><b>À faire</b> : relie la feuille de style <code>style.css</code> aux deux pages (balise "
            "<code>&lt;link&gt;</code> dans chaque <code>&lt;head&gt;</code>), puis écris ses règles : couleur de "
            "fond et police des pages, couleur des grands titres, bordures du tableau. Le dossier technique DT2 "
            "donne les propriétés utiles.</p>"], "blocks": [
            g.QBAR(["DP1", "DT2"], "dans l'éditeur"),
            g.HTML(editeur("style.css", "index.html")),
            question(g, ["css1", "css2"], "Relie la feuille de style aux deux pages.",
                     "La même balise dans le head de chaque page.",
                     "<p>Une seule feuille de style met en forme tout le site : chaque page la désigne avec "
                     "<code>&lt;link rel=\"stylesheet\" href=\"style.css\"&gt;</code>.</p>"),
            question(g, ["fond", "police", "couleur", "bord"], "Écris les règles de <code>style.css</code>.",
                     "Une valeur fausse (une couleur mal écrite, par exemple) est ignorée par le navigateur.",
                     "<p>Une règle associe un sélecteur à des propriétés :</p>"
                     + g.calc("body { background-color: lightyellow; font-family: Arial, sans-serif; } h1 { color: "
                              "navy; } table, th, td { border: 1px solid gray; }")),
        ]},
    ]


EDITEUR_CSS = """
/* ---------- exercice 1.2 : l'éditeur du site (préfixe ed-) ---------- */
.ed{margin:12px 0 16px; border:2px solid var(--encre); background:#fff}
body.exo-site-html .page{max-width:1180px}
.ed-barre{display:flex; flex-wrap:wrap; align-items:center; gap:6px 10px; padding:6px 8px; background:#E9ECEF; border-bottom:1px solid var(--trait)}
.ed-onglets{display:flex; flex-wrap:wrap; gap:2px; margin-right:auto; min-width:0}
@media (max-width:520px){ .ed-ong{padding:4px 7px; font-size:.76rem} .ed-barre .btn{font-size:.78rem} }
.ed-ong{font:600 .86rem ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; padding:5px 12px; border:1px solid var(--trait); border-bottom:0; background:#F6F7F4; cursor:pointer}
.ed-ong[aria-selected="true"]{background:#1C2530; color:#fff; border-color:#1C2530}
.ed-barre .btn{padding:4px 10px; font-size:.84rem}
.ed-img code{font-size:.84rem}
.ed-corps{display:grid; grid-template-columns:minmax(0,1.15fr) minmax(0,1fr); min-height:380px}
@media (max-width:900px){ .ed-corps{grid-template-columns:1fr} .ed-apercu{min-height:300px} }
.ed-code{display:flex; background:#1C2530; min-height:380px; max-height:560px; overflow:hidden}
.ed-num{margin:0; padding:10px 6px 10px 8px; min-width:2.8em; text-align:right; color:#6C7883; background:#151C24; font:13px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; overflow:hidden; user-select:none}
.ed-zone{position:relative; flex:1; min-width:0}
.ed-hl,.ed-ta{margin:0; padding:10px 12px; border:0; font:13px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; letter-spacing:0; tab-size:2; white-space:pre; box-sizing:border-box; width:100%; height:100%}
.ed-hl{position:absolute; inset:0; overflow:hidden; pointer-events:none; color:#E9ECEF}
.ed-hl code{font:inherit}
.ed-ta{position:relative; display:block; background:transparent; color:transparent; caret-color:#FFFFFF; resize:none; overflow:auto; outline:none}
.ed-ta::selection{background:rgba(242,183,5,.35)}
.ed-zone:focus-within{box-shadow:inset 0 0 0 2px var(--jaune)}
.hl-tag{color:#7FB8F0} .hl-att{color:#F2B705} .hl-val{color:#9BD18B} .hl-com{color:#8A96A0; font-style:italic}
.hl-dt{color:#C9A0E8} .hl-sel{color:#F2B705} .hl-prop{color:#7FB8F0} .hl-vc{color:#9BD18B}
.ed-apercu{display:flex; flex-direction:column; border-left:2px solid var(--encre); background:#fff}
.ed-ap-barre{display:flex; align-items:center; gap:6px; padding:4px 8px; background:#D3D8D5; font:600 .82rem ui-monospace,Consolas,monospace}
.ed-retour{font:inherit; border:1px solid var(--trait); background:#fff; cursor:pointer; padding:0 6px}
.ed-retour:disabled{opacity:.4; cursor:default}
.ed-if{flex:1; width:100%; min-height:340px; border:0; background:#fff}
.ed-etat{margin:0; padding:5px 10px; border-top:1px solid var(--trait-fin)}
.ed-doc{font:500 .8rem/1.4 ui-monospace,Consolas,monospace; background:#1C2530; color:#E9ECEF; padding:8px 12px; white-space:pre; overflow-x:auto}
@media print{
  .ed-barre,.ed-corps,.ed-etat{display:none!important}
  .ed{border:1px solid #999}
  .ed-print{display:block!important; margin:0; padding:6px 10px; font:8.5pt/1.35 ui-monospace,Consolas,monospace; white-space:pre-wrap}
}
"""

EDITEUR_JS = r"""<script>/* Exercice 1.2 : l'éditeur du site. Les éditeurs de toutes les parties partagent les mêmes fichiers ; l'aperçu
   (iframe isolée, sans script) affiche la page et relaie ses liens ; chaque critère d'une question est vérifié dans le
   code, et son verdict (« oui », « non », ou rien tant que le fichier n'a pas été modifié) va dans la case masquée que
   corrige le moteur du gabarit. */
(function () {
  "use strict";
  var parts = document.getElementById("parts");
  var EDS = parts ? Array.prototype.slice.call(parts.querySelectorAll(".ed")) : [];
  if (!EDS.length) return;
  var CFG = __CFG__;
  var P = {}, cache = {}, minuteur = null;
  CFG.ordre.forEach(function (f) { P[f] = CFG.depart[f]; });
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function norm(s) { return String(s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/\s+/g, " ").trim(); }
  function lien(h) { return String(h || "").trim().replace(/^\.\//, "").split("#")[0]; }

  // ---------- coloration du code ----------
  function attrs(a) {
    return a.replace(/("[^"]*"?|'[^']*'?)|([\w:-]+)|([\s\S])/g, function (m, v, n) {
      return v ? '<span class="hl-val">' + esc(v) + "</span>" : n ? '<span class="hl-att">' + esc(n) + "</span>" : esc(m);
    });
  }
  function colorerHTML(s) {
    return s.replace(/(<!--[\s\S]*?(?:-->|$))|(<!doctype[^>]*>)|(<\/?)([a-zA-Z][\w-]*)([^<>]*?)(\/?>)|([^<]+|<)/gi,
      function (m, com, dt, o, nom, at, f) {
        if (com) return '<span class="hl-com">' + esc(com) + "</span>";
        if (dt) return '<span class="hl-dt">' + esc(dt) + "</span>";
        if (nom) return '<span class="hl-tag">' + esc(o) + nom + "</span>" + attrs(at) + '<span class="hl-tag">' + esc(f) + "</span>";
        return esc(m);
      });
  }
  function decl(d) {
    return d.replace(/(\/\*[\s\S]*?(?:\*\/|$))|([\w-]+)(\s*:)([^;}]*)|([\s\S])/g, function (m, com, p, c, v) {
      if (com) return '<span class="hl-com">' + esc(com) + "</span>";
      if (p) return '<span class="hl-prop">' + esc(p) + "</span>" + esc(c) + '<span class="hl-vc">' + esc(v) + "</span>";
      return esc(m);
    });
  }
  function colorerCSS(s) {
    return s.replace(/(\/\*[\s\S]*?(?:\*\/|$))|([^{}\/]+)(\{)([^{}]*)(\}?)|([\s\S])/g, function (m, com, sel, ao, d, af) {
      if (com) return '<span class="hl-com">' + esc(com) + "</span>";
      if (ao) return '<span class="hl-sel">' + esc(sel) + "</span>" + ao + decl(d) + (af || "");
      return esc(m);
    });
  }

  // ---------- vérification des critères ----------
  function doc(f) {
    if (!cache[f] || cache[f][0] !== P[f]) cache[f] = [P[f], new DOMParser().parseFromString(P[f], "text/html")];
    return cache[f][1];
  }
  function texte(el) { return el ? el.textContent.replace(/\s+/g, " ").trim() : ""; }
  function un(f, sel, test) { return $$(sel, doc(f)).some(test || function (el) { return !!texte(el); }); }
  function image() { return $$("img[src]", doc("index.html")).filter(function (i) { return lien(i.getAttribute("src")) === CFG.image; })[0]; }
  function vers(f, cible) { return $$("a[href]", doc(f)).some(function (a) { return lien(a.getAttribute("href")) === cible; }); }
  function feuille(f) { return $$("link[href]", doc(f)).some(function (l) { return /stylesheet/i.test(l.getAttribute("rel") || "") && lien(l.getAttribute("href")) === "style.css"; }); }
  function ip(s) { var m = s.match(/\b(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b/); return !!m && m.slice(1).every(function (x) { return +x <= 255; }); }
  var cssCache = [null, []];
  function regles() {
    var css = P["style.css"];
    if (cssCache[0] === css) return cssCache[1];
    var out = [];
    try {
      var sh = new CSSStyleSheet();
      sh.replaceSync(css);
      Array.prototype.forEach.call(sh.cssRules, function (r) {
        if (!r.selectorText) return;
        var p = {};
        for (var i = 0; i < r.style.length; i++) p[r.style[i]] = r.style.getPropertyValue(r.style[i]);
        out.push({ sel: r.selectorText.split(",").map(function (x) { return x.trim().toLowerCase(); }), p: p });
      });
    } catch (e) {  /* navigateur sans CSSStyleSheet() : lecture simplifiée des règles */
      css.replace(/\/\*[\s\S]*?\*\//g, "").replace(/([^{}]+)\{([^{}]*)\}/g, function (_m, sel, d) {
        var p = {};
        d.split(";").forEach(function (x) { var k = x.indexOf(":"); if (k > 0) p[x.slice(0, k).trim().toLowerCase()] = x.slice(k + 1).trim(); });
        out.push({ sel: sel.split(",").map(function (x) { return x.trim().toLowerCase(); }), p: p });
      });
    }
    cssCache = [css, out];
    return out;
  }
  function regle(sels, test) { return regles().some(function (r) { return r.sel.some(function (s) { return sels.indexOf(s) >= 0; }) && test(r.p); }); }
  function plein(v) { return !!v && !/^(initial|inherit|unset|transparent|none)$/i.test(v.trim()); }
  var CHK = {
    lang: function () { return /^fr\b/i.test(doc("index.html").documentElement.getAttribute("lang") || ""); },
    titre: function () { var t = doc("index.html").head.querySelector("title"); return !!t && norm(t.textContent).indexOf("mon reseau") >= 0; },
    h1: function () { return un("index.html", "body h1"); },
    p: function () { return un("index.html", "body p", function (p) { return texte(p).split(" ").filter(Boolean).length >= 10; }); },
    strong: function () { return un("index.html", "body strong"); },
    h2: function () { return un("index.html", "body h2"); },
    ul: function () { return !!doc("index.html").body.querySelector("ul"); },
    li: function () { return un("index.html", "body ul", function (u) { return Array.prototype.filter.call(u.children, function (li) { return li.tagName === "LI" && texte(li); }).length >= 3; }); },
    img: function () { return !!image(); },
    alt: function () { var i = image(); return !!i && (i.getAttribute("alt") || "").trim().length >= 3; },
    squelette: function () {
      var s = P["materiel.html"], d = doc("materiel.html"), t = d.head.querySelector("title");
      return /^\s*(<!--[\s\S]*?-->\s*)*<!doctype html\s*>/i.test(s) && /<html\b[^>]*\blang\s*=\s*["']?fr/i.test(s) &&
        /<head[\s>]/i.test(s) && /<body[\s>]/i.test(s) && !!t && !!texte(t);
    },
    mh1: function () { return un("materiel.html", "body h1", function (h) { return norm(texte(h)).indexOf("materiel") >= 0; }); },
    table: function () { return un("materiel.html", "table", function (t) { return t.querySelectorAll("tr").length >= 3; }); },
    th: function () { return un("materiel.html", "table", function (t) { return t.querySelectorAll("th").length >= 2; }); },
    ip: function () { return un("materiel.html", "td", function (td) { return ip(texte(td)); }); },
    lien1: function () { return vers("index.html", "materiel.html"); },
    lien2: function () { return vers("materiel.html", "index.html"); },
    css1: function () { return feuille("index.html"); },
    css2: function () { return feuille("materiel.html"); },
    fond: function () { return regle(["body", "html"], function (p) { return plein(p["background-color"]) || plein(p["background"]); }); },
    police: function () { return regle(["body", "html", "*"], function (p) { return plein(p["font-family"]); }); },
    couleur: function () { return regle(["h1"], function (p) { return plein(p["color"]); }); },
    bord: function () {
      return regle(["table", "th", "td"], function (p) {
        return Object.keys(p).some(function (k) { return /^border(-(top|right|bottom|left))?(-style)?$/.test(k) && plein(p[k]) && !/\b(none|hidden)\b/.test(p[k]); });
      });
    }
  };
  function verdict(code) { try { return !!CHK[code](); } catch (e) { return false; } }
  function evaluer() {
    $$("#parts .grp-auto .grp-l [data-chk]").forEach(function (sp) {
      var code = sp.getAttribute("data-chk"), inp = sp.closest(".grp-l").querySelector(".sol input");
      if (!inp || inp.disabled) return;
      var f = CFG.criteres[code], v = P[f] === CFG.depart[f] ? "" : (verdict(code) ? "oui" : "non");
      if (inp.value !== v) { inp.value = v; inp.dispatchEvent(new Event("input", { bubbles: true })); }
    });
  }

  // ---------- l'aperçu : la page, sa feuille de style et l'image ; ses liens sont relayés ----------
  function page(nom) {
    if (!Object.prototype.hasOwnProperty.call(P, nom) || !/\.html$/.test(nom))
      return '<!DOCTYPE html><html lang="fr"><body style="font-family:sans-serif;padding:12px"><h1>Erreur 404</h1><p>La page <b>' +
        esc(nom) + "</b> n'existe pas sur ce site : vérifie le nom du fichier dans le lien.</p></body></html>";
    return P[nom]
      .replace(/<link\b[^>]*>/gi, function (m) {
        var h = m.match(/href\s*=\s*["']?([^"'\s>]+)/i);
        return /stylesheet/i.test(m) && h && lien(h[1]) === "style.css" ? "<style>" + P["style.css"].replace(/<\/style/gi, "<\\/style") + "</style>" : m;
      })
      .replace(/(\bsrc\s*=\s*)(["']?)([^"'\s>]+)\2/gi, function (m, a, q, f) { return CFG.images[lien(f)] ? a + '"' + CFG.images[lien(f)] + '"' : m; });
  }

  // ---------- les éditeurs ----------
  var INST = EDS.map(function (ed) {
    var I = { ed: ed, f: ed.getAttribute("data-fichier"), page: ed.getAttribute("data-page"), hist: [], sortie: false };
    var ta = ed.querySelector(".ed-ta"), code = ed.querySelector(".ed-hl code"), hl = ed.querySelector(".ed-hl"), num = ed.querySelector(".ed-num");
    var ifr = ed.querySelector(".ed-if"), url = ed.querySelector(".ed-url"), retour = ed.querySelector(".ed-retour"), etat = ed.querySelector(".ed-etat");
    I.dessiner = function () {
      var s = P[I.f];
      code.innerHTML = (/\.css$/.test(I.f) ? colorerCSS(s) : colorerHTML(s)) + "\n";
      var n = s.split("\n").length, t = [];
      for (var k = 1; k <= n; k++) t.push(k);
      num.textContent = t.join("\n");
      I.defiler();
    };
    I.defiler = function () { hl.scrollTop = ta.scrollTop; hl.scrollLeft = ta.scrollLeft; num.scrollTop = ta.scrollTop; };
    I.ouvrir = function (f) {
      I.f = f;
      $$(".ed-ong", ed).forEach(function (o) { o.setAttribute("aria-selected", o.getAttribute("data-f") === f ? "true" : "false"); });
      ta.value = P[f];
      ta.setAttribute("aria-label", "Code du fichier " + f);
      I.dessiner();
    };
    I.montrer = function (nom) {
      I.page = nom;
      url.textContent = "mon-site/" + nom;
      retour.disabled = !I.hist.length;
      ifr.srcdoc = page(nom);
    };
    I.etat = function (s) { etat.textContent = s; };
    ifr.addEventListener("load", function () {
      var d;
      try { d = ifr.contentDocument; } catch (e) { return; }
      if (!d) return;
      d.addEventListener("click", function (e) {
        var a = e.target.closest && e.target.closest("a[href]");
        if (!a) return;
        var h = a.getAttribute("href").trim();
        if (/^#/.test(h)) return;
        e.preventDefault();
        if (/^(https?:)?\/\//i.test(h)) { window.open(h, "_blank", "noopener"); I.etat("Lien externe : " + h + " s'ouvre dans un nouvel onglet."); return; }
        if (/^[a-z]+:/i.test(h)) { I.etat("Lien « " + h + " » : il ne s'ouvre pas dans l'aperçu."); return; }
        I.hist.push(I.page);
        I.montrer(lien(h));
        I.etat(Object.prototype.hasOwnProperty.call(P, lien(h)) ? "Lien suivi : l'aperçu affiche " + lien(h) + "." : "Page introuvable : erreur 404.");
      });
    });
    retour.addEventListener("click", function () { if (I.hist.length) I.montrer(I.hist.pop()); });
    $$(".ed-ong", ed).forEach(function (o) { o.addEventListener("click", function () { I.ouvrir(o.getAttribute("data-f")); }); });
    function inserer(t) {
      ta.focus();
      if (!document.execCommand || !document.execCommand("insertText", false, t)) {
        var a = ta.selectionStart, b = ta.selectionEnd;
        ta.setRangeText(t, a, b, "end");
        ta.dispatchEvent(new Event("input", { bubbles: true }));
      }
    }
    ta.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { I.sortie = true; return; }
      if (e.key === "Tab" && !e.shiftKey && !I.sortie && !e.ctrlKey && !e.altKey) { e.preventDefault(); inserer("  "); return; }
      if (e.key === "Enter" && !e.shiftKey && !e.ctrlKey && !e.altKey) {
        var debut = ta.value.lastIndexOf("\n", ta.selectionStart - 1) + 1, ind = ta.value.slice(debut).match(/^[ \t]*/)[0];
        if (ind) { e.preventDefault(); inserer("\n" + ind); }
      }
      I.sortie = false;
    });
    ta.addEventListener("input", function () { P[I.f] = ta.value; changement(I); });
    ta.addEventListener("scroll", I.defiler);
    ed.querySelector(".ed-reinit").addEventListener("click", function () {
      if (P[I.f] === CFG.depart[I.f]) { I.etat(I.f + " est déjà dans son état de départ."); return; }
      if (!window.confirm("Remettre « " + I.f + " » dans son état de départ ? Ton code de ce fichier sera effacé.")) return;
      P[I.f] = CFG.depart[I.f];
      I.ouvrir(I.f);
      changement(I);
      I.etat(I.f + " est revenu à son état de départ.");
    });
    ed.querySelector(".ed-zip").addEventListener("click", function () { telecharger(); I.etat("Ton site est téléchargé : mon-site.zip (trois fichiers et l'image)."); });
    I.ouvrir(I.f);
    I.montrer(I.page);
    return I;
  });
  // une modification se reporte dans les autres éditeurs et les aperçus ; les critères sont vérifiés aussitôt
  function changement(source) {
    INST.forEach(function (I) {
      if (I !== source && I.f === source.f) { var ta = I.ed.querySelector(".ed-ta"); if (document.activeElement !== ta) ta.value = P[I.f]; }
      if (I.f === source.f) I.dessiner();
    });
    evaluer();
    clearTimeout(minuteur);
    minuteur = setTimeout(function () {
      INST.forEach(function (I) { if (I.page === source.f || source.f === "style.css") I.montrer(I.page); });
    }, 250);
  }

  // ---------- télécharger le site : une archive .zip, sans compression ----------
  function crc32(b) {
    var t = crc32.t, c, i, k;
    if (!t) { t = crc32.t = []; for (i = 0; i < 256; i++) { c = i; for (k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[i] = c >>> 0; } }
    c = 0xFFFFFFFF;
    for (i = 0; i < b.length; i++) c = t[(c ^ b[i]) & 255] ^ (c >>> 8);
    return (c ^ 0xFFFFFFFF) >>> 0;
  }
  function archive(fichiers) {
    var morceaux = [], central = [], pos = 0, enc = new TextEncoder();
    function u16(v) { return [v & 255, (v >>> 8) & 255]; }
    function u32(v) { return [v & 255, (v >>> 8) & 255, (v >>> 16) & 255, (v >>> 24) & 255]; }
    fichiers.forEach(function (f) {
      var nom = enc.encode(f.nom), crc = crc32(f.octets), n = f.octets.length;
      var tete = [].concat(u32(0x04034b50), u16(20), u16(0x0800), u16(0), u16(0), u16(0x21), u32(crc), u32(n), u32(n), u16(nom.length), u16(0));
      morceaux.push(new Uint8Array(tete), nom, f.octets);
      central.push(new Uint8Array([].concat(u32(0x02014b50), u16(20), u16(20), u16(0x0800), u16(0), u16(0), u16(0x21), u32(crc), u32(n), u32(n),
        u16(nom.length), u16(0), u16(0), u16(0), u16(0), u32(0), u32(pos))), nom);
      pos += tete.length + nom.length + n;
    });
    var taille = central.reduce(function (s, x) { return s + x.length; }, 0);
    var fin = new Uint8Array([].concat(u32(0x06054b50), u16(0), u16(0), u16(fichiers.length), u16(fichiers.length), u32(taille), u32(pos), u16(0)));
    return new Blob(morceaux.concat(central, [fin]), { type: "application/zip" });
  }
  function telecharger() {
    var enc = new TextEncoder(), fichiers = CFG.ordre.map(function (f) { return { nom: "mon-site/" + f, octets: enc.encode(P[f]) }; });
    Object.keys(CFG.images).forEach(function (f) {
      var b = atob(CFG.images[f].split(",")[1]), o = new Uint8Array(b.length);
      for (var i = 0; i < b.length; i++) o[i] = b.charCodeAt(i);
      fichiers.push({ nom: "mon-site/" + f, octets: o });
    });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(archive(fichiers));
    a.download = "mon-site.zip";
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  }

  // impression : le code du fichier de chaque partie remplace l'éditeur
  window.addEventListener("beforeprint", function () {
    INST.forEach(function (I) { var f = I.ed.getAttribute("data-fichier"); I.ed.querySelector(".ed-print").textContent = "— " + f + " —\n" + P[f]; });
  });
  window.__site__ = { fichiers: P, verifier: evaluer };
  evaluer();
})();
</script>"""


def exercice(g):
    cfg = {"ordre": ORDRE, "depart": DEPART, "image": IMAGE, "images": {IMAGE: g.png("accueil")[0]},
           "criteres": {k: v[0] for k, v in CRITERES.items()}}
    js = EDITEUR_JS.replace("__CFG__", json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/"))
    return {"key": "site-html", "prefix": "h", "tag": "Exercice 1.2", "level": "Niveau 1", "title": "Mon premier site",
            "parts": parties(g),
            "docs": [g.DOC("DP1", "Le site à réaliser", DP1), g.DOC("DT1", "Les balises HTML", DT1),
                     g.DOC("DT2", "Les règles CSS", DT2)],
            "consignes": g.consignes(
                "<p><strong>Un éditeur, un aperçu.</strong> Écris ton code dans l'éditeur, à gauche ; l'aperçu, à "
                "droite, affiche le site comme un navigateur et se met à jour pendant que tu écris. Les onglets "
                "ouvrent les trois fichiers du site ; les éditeurs des quatre parties travaillent sur les mêmes "
                "fichiers. Rien n'est enregistré : télécharge ton site (.zip) avant de fermer la page.</p>",
                "<p><strong>Des critères vérifiés.</strong> Chaque question est une liste de critères ; quand ton "
                "code est prêt, fais-le vérifier : chaque critère rempli vaut un point. En mode examen, ton code est "
                "vérifié à la remise de la copie.</p>", g.C_DOCUMENTS),
            "hero": ("carte-site", "L'éditeur du site : le code HTML à gauche, l'aperçu de la page à droite",
                     "Deux pages HTML, une feuille de style, un aperçu en direct."),
            "mots": ["HTML", "Liens", "Tableau", "CSS", "Éditeur"], "vign": "carte-site",
            "valt": "Le code HTML d'une page et son aperçu", "unite": ("critères", "critères vérifiés", "un point chacun"),
            "sub": "Réaliser un petit site depuis l'éditeur intégré : une page d'accueil, une page « Le matériel » "
                   "avec le tableau des adresses IP de la maison, des liens entre les pages et une feuille de style ; "
                   "l'aperçu affiche le site en direct.",
            "js": js, "css": EDITEUR_CSS}
