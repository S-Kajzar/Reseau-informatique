"""QCM aux normes du gabarit (repris du QCM 2.1 du dépôt « Chaîne fonctionnelle »).

Chaque question est une question du gabarit à une seule case (mécanisme « fast-q ») : la case, masquée, reçoit le
repère de la ou des propositions choisies ; le moteur Grading la corrige (« code » pour une réponse unique,
« intset » pour plusieurs réponses). Modes entraînement et examen, note, récapitulatif et impression sont ceux du
gabarit. Une partie de QCM est une partie d'exercice ordinaire dont les blocs sont des QCM(…) ; l'exercice porte
"qcm": True (cartouche et accueil comptent alors des questions, et non des cases) et les consignes CONSIGNES.

Les images des questions ne sont écrites qu'une fois dans la page (images_js), même si plusieurs questions les
partagent.
"""
import json


def QCM(stem, opts, correct, explain, multi=None, img=None, hint=None, fig=None):
    """Une question à propositions.
    stem, explain : énoncé et explication (HTML) ; opts : [(repère, texte HTML)] ; correct : repères justes.
    multi : plusieurs réponses à sélectionner (par défaut, s'il y a plusieurs repères justes) ; leurs repères sont
    alors des nombres (« 1 », « 2 »…). img : (image de src/images, texte alternatif, largeur maximale) ;
    fig : figure HTML (un schéma SVG, par exemple), placée sous l'énoncé."""
    correct = [str(k) for k in correct]
    keys = [str(k) for k, _t in opts]
    assert correct and all(k in keys for k in correct), (stem, correct)
    multi = len(correct) > 1 if multi is None else multi
    if multi:
        assert all(k.isdigit() for k in keys), f"réponses multiples : repères numériques ({stem})"
        grader = {"type": "intset", "value": sorted(int(k) for k in correct)}
    else:
        grader = {"type": "code", "equals": [k.lower() for k in correct]}
    sep = " ; " if multi else " ou "
    attendu = sep.join(f"{k}) {t}" for k, t in opts if str(k) in correct)
    if hint is None:
        hint = "Plusieurs réponses : sélectionne toutes les bonnes." if multi else "Une seule réponse."
    return {"kind": "grp", "qcm": True, "stem": stem, "hint": hint, "fields": [("Réponse", grader, attendu)],
            "why": explain, "opts": [(str(k), t) for k, t in opts], "multi": multi, "img": img, "fig": fig}


def render_qcm(b, h):
    """Une question : énoncé, image éventuelle, propositions ; la case du gabarit est masquée."""
    gid, label, fid = b["id"], b["label"], b["fids"][0]
    img = ""
    if b["img"]:  # l'image n'est écrite qu'une fois dans la page (images_js) : plusieurs questions la partagent
        name, alt, maxw = b["img"]
        _src, w, hh = h.image(name)
        img = (f'<figure class="fig" style="max-width:{maxw}px"><img data-qimg="{name}" alt="{h.esc(alt)}" '
               f'width="{w}" height="{hh}"></figure>')
    if b.get("fig"):
        img += b["fig"]
    role = "group" if b["multi"] else "radiogroup"
    opts = "".join(f'<button type="button" class="qcm-o" data-k="{h.esc(k)}" role="{"checkbox" if b["multi"] else "radio"}" '
                   f'aria-checked="false"><span class="qcm-k">{h.esc(k)}</span><span class="qcm-t">{t}</span></button>'
                   for k, t in b["opts"])
    return f"""
        <div class="fast-q grp qcm" id="{gid}" data-multi="{1 if b['multi'] else 0}">
          <p class="q-stem"><span class="q-num">{label}</span> <strong>{b['stem']}</strong></p>
          <p class="q-hint">{b['hint']}</p>{img}
          <div class="qcm-opts" role="{role}" aria-label="Propositions de la question {label}">{opts}</div>
          <div class="sol qcm-sol"><input type="hidden" id="in-{fid}" data-q="{fid}"><span class="mark" aria-live="polite"></span></div>
          <div class="fast-foot"><button type="button" class="btn btn-fast" disabled>Valider</button>
            <span class="q-status" aria-live="polite"></span></div>
          <p class="q-msg" role="alert"></p>
          <div class="q-expl" hidden>
            <p class="qcm-rep"><b>Réponse attendue :</b> {b['fields'][0][2]}</p>
            <div class="q-why"><p class="why-t">Explication</p><p>{b['why']}</p></div>
          </div>
        </div>"""


CONSIGNES = """<p class="only-training"><strong>Mode entraînement.</strong> Choisis ta réponse puis clique sur « Valider » : une réponse validée est définitive, sa correction et son explication s'affichent aussitôt.</p>
    <p class="only-exam"><strong>Mode examen.</strong> Réponds à tout le questionnaire sans correction ni note : tes choix restent modifiables jusqu'au bout. Le bouton « J'ai fini, je fais corriger ma copie », en fin de sujet, dévoile d'un coup les corrections et la note.</p>
    <p><strong>Une ou plusieurs réponses.</strong> La plupart des questions n'ont qu'une bonne réponse ; quand il y en a plusieurs, l'énoncé le précise et il faut toutes les sélectionner. Certaines questions s'appuient sur une figure.</p>
    <p><strong>Barème pondéré par la durée conseillée</strong> : chaque question vaut un point, chaque partie est notée sur 20, puis pèse au prorata de son temps.</p>"""

# paragraphe des consignes d'un exercice qui mêle des QCM à d'autres questions (generer.consignes)
C_QCM = """<p><strong>Questions à propositions.</strong> Choisis une proposition, ou toutes les bonnes quand l'énoncé en annonce plusieurs, puis clique sur « Valider ».</p>"""

QCM_CSS = """
/* ---------- QCM (questions à propositions) ---------- */
.qcm .fig{margin:8px 0}
.qcm-opts{display:flex; flex-direction:column; gap:6px; margin:8px 0 4px; max-width:820px}
.qcm-o{display:flex; align-items:flex-start; gap:10px; width:100%; text-align:left; background:#fff; border:1.5px solid var(--trait); border-radius:3px; padding:8px 12px; font:inherit; font-size:.97rem; color:var(--encre); cursor:pointer}
.qcm-o:hover:not(:disabled){border-color:var(--encre); background:var(--jaune-pale)}
.qcm-o:focus-visible{outline:3px solid var(--jaune); outline-offset:1px}
.qcm-k{flex:0 0 auto; min-width:1.9em; height:1.9em; display:inline-flex; align-items:center; justify-content:center; border:1.5px solid var(--bleu); color:var(--bleu); font:700 .85rem var(--f-titre); border-radius:3px}
.qcm[data-multi="1"] .qcm-k{border-radius:3px} .qcm[data-multi="0"] .qcm-k{border-radius:50%}
.qcm-o[aria-checked="true"]{border-color:var(--bleu); background:var(--bleu-pale); box-shadow:inset 0 0 0 1px var(--bleu)}
.qcm-o[aria-checked="true"] .qcm-k{background:var(--bleu); color:#fff}
.qcm-o:disabled{cursor:default}
.qcm-o.ok{border-color:var(--vert); background:var(--vert-pale)} .qcm-o.ok .qcm-k{border-color:var(--vert); background:var(--vert); color:#fff}
.qcm-o.ko{border-color:var(--rouge); background:var(--rouge-pale)} .qcm-o.ko .qcm-k{border-color:var(--rouge); background:var(--rouge); color:#fff}
.qcm-o .qcm-tag{margin-left:auto; flex:0 0 auto; font:700 .75rem var(--f-titre); padding:1px 7px; color:#fff}
.qcm-o.ok .qcm-tag{background:var(--vert)} .qcm-o.ko .qcm-tag{background:var(--rouge)}
.qcm-sol{min-height:0}
.qcm-sol .mark{flex:0 0 auto}
.qcm-rep{margin:0 0 6px}
@media print{ .qcm-o{padding:2px 8px; font-size:9pt; break-inside:avoid} .qcm{break-inside:avoid} }
"""


def images_js(exos, h):
    """Les images des QCM, une seule fois chacune, posées dans les questions à l'ouverture de la page."""
    data = {}
    for e in exos:
        for p in e["parts"]:
            for b in p["blocks"]:
                if b.get("qcm") and b.get("img"):
                    data[b["img"][0]] = h.image(b["img"][0])[0]
    if not data:
        return ""
    return ("<script>(function () { var I = " + json.dumps(data) + ";\n"
            "  Array.prototype.forEach.call(document.querySelectorAll(\"img[data-qimg]\"), function (im) { "
            "im.src = I[im.getAttribute(\"data-qimg\")]; }); })();</script>")


QCM_JS = r"""<script>/* QCM : un clic choisit une proposition (ou plusieurs) ; le repère va dans la case masquée du gabarit */
(function () {
  "use strict";
  var parts = document.getElementById("parts");
  if (!parts || !parts.querySelector(".qcm")) return;
  function inp(q) { return q.querySelector(".sol input"); }
  function choisis(q) { return Array.prototype.filter.call(q.querySelectorAll(".qcm-o"), function (o) { return o.getAttribute("aria-checked") === "true"; }); }
  function maj(q) {
    var i = inp(q), v = choisis(q).map(function (o) { return o.getAttribute("data-k"); }).join(",");
    i.value = v;
    var b = q.querySelector(".btn-fast");
    if (!i.disabled) b.disabled = !v;
    i.dispatchEvent(new Event("input", { bubbles: true }));
  }
  parts.addEventListener("click", function (e) {
    var o = e.target.closest(".qcm-o");
    if (!o || o.disabled) return;
    var q = o.closest(".qcm"), multi = q.getAttribute("data-multi") === "1";
    if (inp(q).disabled) return;
    if (multi) o.setAttribute("aria-checked", o.getAttribute("aria-checked") === "true" ? "false" : "true");
    else Array.prototype.forEach.call(q.querySelectorAll(".qcm-o"), function (x) { x.setAttribute("aria-checked", x === o ? "true" : "false"); });
    maj(q);
  });
  // flèches du clavier dans une question à réponse unique
  parts.addEventListener("keydown", function (e) {
    var o = e.target.closest && e.target.closest(".qcm-o");
    if (!o || (e.key !== "ArrowDown" && e.key !== "ArrowUp")) return;
    var all = Array.prototype.slice.call(o.parentNode.querySelectorAll(".qcm-o")), k = all.indexOf(o) + (e.key === "ArrowDown" ? 1 : -1);
    if (all[k]) { e.preventDefault(); all[k].focus(); }
  });
  // une fois la question corrigée par le moteur (champ verrouillé) : propositions justes et fausses marquées
  function corriger(q) {
    var id = inp(q).getAttribute("data-q"), g = (window.__QCFG__[id] || {}).grader || {}, bons = {};
    (g.equals || []).forEach(function (k) { bons[k] = 1; });
    (g.value || []).forEach(function (k) { bons[String(k)] = 1; });
    Array.prototype.forEach.call(q.querySelectorAll(".qcm-o"), function (o) {
      var k = o.getAttribute("data-k").toLowerCase(), sel = o.getAttribute("aria-checked") === "true", tag;
      o.disabled = true;
      if (bons[k] || (sel && !bons[k])) {
        o.classList.add(bons[k] ? "ok" : "ko");
        tag = document.createElement("span"); tag.className = "qcm-tag";
        tag.textContent = bons[k] ? (sel ? "✔ ta réponse" : "✔ bonne réponse") : "✘ ta réponse";
        o.appendChild(tag);
      }
    });
    var juste = q.querySelector(".sol").classList.contains("is-ok");
    q.querySelector(".q-status").textContent = juste ? "Bonne réponse" : (inp(q).value ? "Réponse fausse" : "Pas de réponse");
  }
  new MutationObserver(function (ms) {
    ms.forEach(function (m) {
      var i = m.target;
      if (i.tagName !== "INPUT" || !i.disabled) return;
      var q = i.closest(".qcm");
      if (q && !q.classList.contains("corrigee")) { q.classList.add("corrigee"); corriger(q); }
    });
  }).observe(parts, { subtree: true, attributes: true, attributeFilter: ["disabled"] });
})();
</script>"""
