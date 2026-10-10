#!/usr/bin/env python3
"""Genere index.html (FR) et en/index.html (EN) a partir d'un seul gabarit. Usage : python3 build.py"""
import os, re

REL = "https://github.com/le-belge/LithoShape3D-releases/releases/latest"
GUIDE = "https://le-belge.github.io/LithoShape3D-releases/guide/"
BETA = "https://le-belge.github.io/LithoShape3D-releases/beta/"
MAIL = "purenova3d@free.fr"

def pic(name, alt, w, h, cls="", lazy=True, pre="assets/img/"):
    l = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture><source srcset="{pre}{name}.webp" type="image/webp">'
            f'<img{c} src="{pre}{name}.jpg" width="{w}" height="{h}" alt="{alt}"{l}></picture>')

TXT = {
 "fr": dict(lang="fr", home="./", other="en/", other_label="EN", other_hl="en", pre="assets/", 
  title="LithoShape3D — Transformez vos photos en objets lumineux imprimés en 3D",
  desc="LithoShape3D crée des lithophanies, des sphères lumineuses et des horloges à partir de vos photos, prêtes à imprimer en 3D. Pour Windows et Mac. Tout reste sur votre ordinateur.",
  og="LithoShape3D — vos photos en objets lumineux", skip="Aller au contenu",
  nav=["Aperçu allumé", "Créations", "Comment ça marche", "Atouts", "FAQ"], nav_cta="Télécharger", menu="Menu",
  kicker="Pour Windows et Mac", h1="Vos photos, en <em>objets lumineux</em>.",
  lead="LithoShape3D transforme une photo en lithophanie, en sphère ou en horloge, prête à imprimer en 3D. Vous voyez le rendu <strong>allumé</strong> avant même de lancer l'impression.",
  cta1="Télécharger l'aperçu gratuit", cta2="Demander une licence de test",
  ticks=["Aperçu allumé avant impression", "Calculs en local, pas dans le cloud", "Exports STL et 3MF"],
  off="Éteint", on="Allumé", hero_alt_off="Lithophanie éteinte : seulement du relief", hero_alt_on="La même lithophanie allumée : la photo apparaît",
  strip="Vos fichiers s'ouvrent dans les trancheurs courants", strip_chips=["Bambu Studio", "OrcaSlicer", "PrusaSlicer", "Cura"],
  s1_eye="La magie de la lumière", s1_h="Éteinte, ce n'est qu'un relief. Allumée, c'est votre photo.",
  s1_sub="Une lithophanie est plus ou moins épaisse selon les zones de la photo. Glissez le curseur pour voir ce que la lumière change.",
  cmp_off="Éteinte", cmp_on="Allumée", cmp_lab="Curseur éteinte / allumée",
  facts=[("1", "Épaisseur variable", "Les zones sombres de la photo sont plus épaisses, les zones claires plus minces."),
         ("2", "La lumière fait le reste", "Derrière la pièce, une source de lumière traverse le plastique : l'image apparaît."),
         ("3", "Vous voyez avant d'imprimer", "Le bouton « Allumé » du logiciel simule ce rendu sur votre écran.")],
  s2_eye="Créations", s2_h="Trois créations, un seul logiciel", s2_sub="Chargez une photo, choisissez la forme, ajustez : le logiciel s'occupe de la géométrie.",
  tabs=[
   ("litho", "Lithophanie", "Le panneau lumineux classique", "Une photo sur un panneau plat ou courbe, avec un support d'éclairage si vous le souhaitez.",
    ["Plate, arc doux, arc standard, arc large ou demi-cylindre", "Cadrage, zoom et rotation de l'image", "Support d'éclairage imprimable (Bambu Lab Lamp Kit 001)"], "app-lithophanie", "lithophanie",
    "Capture du logiciel : lithophanie et aperçu 3D", "Lithophanie lumineuse"),
   ("sphere", "LithoSphere", "Une sphère qui s'allume", "Une ou plusieurs photos sur une sphère lumineuse, avec chapeau, rehausse et socle.",
    ["Placement automatique de plusieurs photos", "Chapeaux, rehausse et socle à imprimer", "Aperçu allumé et vue éclatée pour l'assemblage"], "app-lithosphere", "lithosphere",
    "Capture du logiciel : LithoSphere", "Sphère lumineuse avec une photo"),
   ("clock", "LithoClock", "Une horloge à votre image", "Une horloge réalisée à partir de votre photo : chiffres, boîtier et cadre.",
    ["Chiffres clairs ou sombres", "En relief lumineux, ou à plat en plusieurs couleurs", "Boîtier et cadre inclus"], "app-lithoclock", "lithoclock",
    "Capture du logiciel : LithoClock", "Horloge photo avec chiffres")],
  s3_eye="Simple", s3_h="De la photo au fichier d'impression", s3_sub="Trois étapes, sans réglage compliqué : le logiciel propose des valeurs recommandées.",
  steps=[("Ajoutez votre photo", "JPG, PNG ou SVG. Cadrez, zoomez, recadrez au format voulu. Le détourage automatique est disponible (modèle téléchargé une seule fois)."),
         ("Choisissez et regardez", "Forme, dimensions, épaisseur. L'aperçu 3D se met à jour, avec le bouton « Allumé » pour voir le rendu éclairé."),
         ("Créez les fichiers", "Le logiciel exporte des fichiers STL (et 3MF multicolore) que vous ouvrez dans votre trancheur.")],
  s4_eye="Atouts", s4_h="Pensé pour de vraies impressions", s4_sub="Ce qui fait la différence entre une belle image et une pièce réussie.",
  b1=("Aperçu allumé et vue éclatée", "Voyez le rendu éclairé avant d'imprimer, et comprenez l'assemblage avant de lancer la première pièce."), b1_alt="Capture du logiciel : aperçu 3D d'une lithophanie",
  b2=("Mode « À plat »", "2 à 4 couleurs imprimées à plat, un filament par couleur (jusqu'aux 4 emplacements d'un AMS), sans support."),
  b3=("Fichiers vérifiés", "Le logiciel contrôle que les maillages sont fermés et imprimables, et « Aide → Vérifier un fichier » relit un fichier exporté."),
  b4=("Chez vous, pas dans le cloud", "Les calculs se font sur votre ordinateur : vos photos ne sont jamais envoyées sur internet."),
  b5=("Windows et Mac", "Windows 10/11, macOS Apple Silicon et Intel. Interface en français et en anglais."),
  b6=("Un guide pas à pas", "Installation et mode d'emploi en ligne, toujours à jour."),
  s5_eye="Idées", s5_h="Ce que vous pouvez créer",
  ideas=[("Un cadeau qui s'allume", "Une photo transformée en objet unique, à offrir."), ("Un souvenir de famille", "Un moment à garder, sous un autre éclairage."),
         ("Une veilleuse sur mesure", "Une lumière douce, avec une image qui compte."), ("Une horloge personnalisée", "Votre photo, avec les heures dessus.")],
  s6_eye="Télécharger", s6_h="Téléchargez LithoShape3D", s6_sub="L'aperçu est libre. Pour créer les fichiers d'impression, il faut une licence : une licence de test est disponible via le programme bêta.",
  dl_btn="Télécharger", dl=[("🪟", "Windows", "Windows 10 / 11", "Sur la page, prenez le fichier « Setup….exe » (environ 220 Mo)."), ("", "Mac Apple Silicon", "M1, M2, M3, M4", "Sur la page, prenez le fichier « …macOS-AppleSilicon.zip » (environ 350 Mo)."), ("", "Mac Intel", "Processeurs Intel", "Sur la page, prenez le fichier « …macOS-Intel.zip » (environ 370 Mo).")],
  dl_note="Le logiciel n'est pas encore signé auprès de Microsoft et d'Apple : un avertissement s'affiche au premier lancement, c'est normal. <a href=\"" + GUIDE + "#installation\">Le guide explique comment l'autoriser en une minute.</a>",
  dl_beta="Demander une licence de test",
  s7_h="Questions fréquentes", s7_sub="Une autre question ? <a href=\"mailto:" + MAIL + "\">Écrivez-nous</a>.",
  faq=[("Qu'est-ce qu'une lithophanie ?", "C'est une plaque imprimée en 3D dont l'épaisseur varie selon la photo : les zones épaisses laissent passer peu de lumière, les zones fines en laissent passer beaucoup. Éclairée par derrière, la photo apparaît."),
       ("Mes photos sont-elles envoyées sur internet ?", "Non. Les calculs se font sur votre ordinateur et vos photos n'en sortent pas. Seule l'activation de la licence contacte le serveur de licences (clé et identifiant d'appareil)."),
       ("Quels fichiers produit-il, et avec quelles imprimantes ?", "Des fichiers STL, et des 3MF multicolores pour le mode « À plat ». Ils s'ouvrent dans les trancheurs courants (Bambu Studio, OrcaSlicer, PrusaSlicer, Cura). Le logiciel ne pilote pas l'imprimante : c'est votre trancheur qui prépare l'impression."),
       ("Pourquoi un avertissement à l'installation ?", "Le logiciel n'est pas encore signé auprès de Microsoft et d'Apple. Windows (« Windows a protégé votre ordinateur ») et macOS demandent une confirmation au premier lancement. Le <a href=\"" + GUIDE + "#installation\">guide d'installation</a> montre les gestes à faire."),
       ("Comment obtenir une licence ? Et si je perds ma clé ?", "Une licence de test est disponible via le <a href=\"" + BETA + "\">programme bêta</a>. Si vous perdez votre clé, la même page propose « Clé perdue ? ». Le code de support affiché dans « Aide → Licence » nous aide à retrouver votre licence."),
       ("Puis-je l'utiliser pour vendre mes créations ?", "La licence de test est réservée à un usage personnel et non commercial. Une offre pour l'usage commercial est prévue : elle n'est pas encore ouverte.")],
  band_h="Prêt à voir votre photo s'allumer ?", band_sub="Téléchargez LithoShape3D et essayez avec une de vos photos.",
  foot_links=[("Guide", GUIDE), ("Programme bêta", BETA), ("Versions", "https://github.com/le-belge/LithoShape3D-releases/releases")], contact="Contact"),
 "en": dict(lang="en", home="../", other="../", other_label="FR", other_hl="fr", pre="../assets/",
  title="LithoShape3D — Turn your photos into glowing 3D-printed objects",
  desc="LithoShape3D turns your photos into lithophanes, light spheres and clocks, ready to 3D print. For Windows and Mac. Everything stays on your computer.",
  og="LithoShape3D — your photos as glowing objects", skip="Skip to content",
  nav=["Lit preview", "Creations", "How it works", "Features", "FAQ"], nav_cta="Download", menu="Menu",
  kicker="For Windows and Mac", h1="Your photos, as <em>glowing objects</em>.",
  lead="LithoShape3D turns a photo into a lithophane, a sphere or a clock, ready to 3D print. You see the <strong>lit</strong> result before you even start printing.",
  cta1="Download the free preview", cta2="Request a test license",
  ticks=["Lit preview before printing", "Runs locally, not in the cloud", "STL and 3MF exports"],
  off="Off", on="Lit", hero_alt_off="Unlit lithophane: only relief", hero_alt_on="The same lithophane, lit: the photo appears",
  strip="Your files open in common slicers", strip_chips=["Bambu Studio", "OrcaSlicer", "PrusaSlicer", "Cura"],
  s1_eye="The magic of light", s1_h="Off, it is just relief. Lit, it is your photo.",
  s1_sub="A lithophane is thicker or thinner depending on the photo. Drag the slider to see what light changes.",
  cmp_off="Off", cmp_on="Lit", cmp_lab="Off / lit slider",
  facts=[("1", "Variable thickness", "Dark areas of the photo are thicker, light areas are thinner."),
         ("2", "Light does the rest", "A light source behind the piece shines through the plastic: the image appears."),
         ("3", "See it before printing", "The “Lit” button in the software simulates this result on your screen.")],
  s2_eye="Creations", s2_h="Three creations, one software", s2_sub="Load a photo, pick a shape, adjust: the software handles the geometry.",
  tabs=[
   ("litho", "Lithophane", "The classic glowing panel", "A photo on a flat or curved panel, with a lighting stand if you wish.",
    ["Flat, soft arc, standard arc, wide arc or half-cylinder", "Crop, zoom and rotate the image", "Printable lighting stand (Bambu Lab Lamp Kit 001)"], "app-lithophanie", "lithophanie",
    "Software screenshot: lithophane and 3D preview", "Glowing lithophane"),
   ("sphere", "LithoSphere", "A sphere that lights up", "One or several photos on a glowing sphere, with cap, riser and base.",
    ["Automatic placement of several photos", "Caps, riser and base to print", "Lit preview and exploded view for assembly"], "app-lithosphere", "lithosphere",
    "Software screenshot: LithoSphere", "Glowing sphere with a photo"),
   ("clock", "LithoClock", "A clock in your image", "A clock made from your photo: numerals, case and frame.",
    ["Light or dark numerals", "In glowing relief, or flat in several colors", "Case and frame included"], "app-lithoclock", "lithoclock",
    "Software screenshot: LithoClock", "Photo clock with numerals")],
  s3_eye="Simple", s3_h="From photo to print file", s3_sub="Three steps, no complicated settings: the software suggests recommended values.",
  steps=[("Add your photo", "JPG, PNG or SVG. Crop, zoom and reframe to the format you want. Automatic background removal is available (model downloaded once)."),
         ("Choose and look", "Shape, size, thickness. The 3D preview updates, with the “Lit” button to see the backlit result."),
         ("Create the files", "The software exports STL files (and multicolor 3MF) that you open in your slicer.")],
  s4_eye="Features", s4_h="Built for real prints", s4_sub="What makes the difference between a nice image and a successful part.",
  b1=("Lit preview and exploded view", "See the backlit result before printing, and understand the assembly before you start the first part."), b1_alt="Software screenshot: 3D preview of a lithophane",
  b2=("“Flat” mode", "2 to 4 colors printed flat, one filament per color (up to the 4 slots of an AMS), no supports."),
  b3=("Checked files", "The software checks that meshes are closed and printable, and “Help → Check a file” re-reads an exported file."),
  b4=("On your computer, not in the cloud", "Calculations run on your computer: your photos are never sent over the internet."),
  b5=("Windows and Mac", "Windows 10/11, macOS Apple Silicon and Intel. Interface in French and English."),
  b6=("A step-by-step guide", "Online installation and user guide, always up to date."),
  s5_eye="Ideas", s5_h="What you can create",
  ideas=[("A gift that lights up", "A photo turned into a one-of-a-kind object, to give."), ("A family keepsake", "A moment to keep, under a different light."),
         ("A custom night light", "A soft light, with an image that matters."), ("A personalised clock", "Your photo, with the hours on it.")],
  s6_eye="Download", s6_h="Download LithoShape3D", s6_sub="The preview is free. To create print files you need a license: a test license is available through the beta program.",
  dl_btn="Download", dl=[("🪟", "Windows", "Windows 10 / 11", "On the page, pick the “Setup….exe” file (about 220 MB)."), ("", "Mac Apple Silicon", "M1, M2, M3, M4", "On the page, pick the “…macOS-AppleSilicon.zip” file (about 350 MB)."), ("", "Mac Intel", "Intel processors", "On the page, pick the “…macOS-Intel.zip” file (about 370 MB).")],
  dl_note="The software is not yet signed with Microsoft and Apple: a warning appears on first launch, this is expected. <a href=\"" + GUIDE + "#installation-en\">The guide explains how to allow it in one minute.</a>",
  dl_beta="Request a test license",
  s7_h="Frequently asked questions", s7_sub="Another question? <a href=\"mailto:" + MAIL + "\">Write to us</a>.",
  faq=[("What is a lithophane?", "A 3D-printed plate whose thickness varies with the photo: thick areas let little light through, thin areas let a lot through. Lit from behind, the photo appears."),
       ("Are my photos sent over the internet?", "No. Calculations run on your computer and your photos never leave it. Only license activation contacts the license server (key and device identifier)."),
       ("Which files does it produce, and with which printers?", "STL files, and multicolor 3MF for the “Flat” mode. They open in common slicers (Bambu Studio, OrcaSlicer, PrusaSlicer, Cura). The software does not drive the printer: your slicer prepares the print."),
       ("Why a warning during installation?", "The software is not yet signed with Microsoft and Apple. Windows (“Windows protected your PC”) and macOS ask for confirmation on first launch. The <a href=\"" + GUIDE + "#installation-en\">installation guide</a> shows what to do."),
       ("How do I get a license? What if I lose my key?", "A test license is available through the <a href=\"" + BETA + "\">beta program</a>. If you lose your key, the same page offers “Lost your key?”. The support code shown in “Help → License” helps us find your license."),
       ("Can I sell my creations?", "The test license is for personal, non-commercial use. A commercial offer is planned: it is not open yet.")],
  band_h="Ready to see your photo light up?", band_sub="Download LithoShape3D and try it with one of your photos.",
  foot_links=[("Guide", GUIDE), ("Beta program", BETA), ("Releases", "https://github.com/le-belge/LithoShape3D-releases/releases")], contact="Contact"),
}

ICONS = ['<svg viewBox="0 0 48 48"><rect x="6" y="9" width="36" height="30" rx="5"/><circle cx="17" cy="21" r="4"/><path d="M6 33l11-9 8 6 8-8 9 9"/></svg>',
         '<svg viewBox="0 0 48 48"><path d="M24 6c-8 0-14 6-14 14 0 5 3 8 5 11v5h18v-5c2-3 5-6 5-11 0-8-6-14-14-14z"/><path d="M19 41h10M21 45h6"/><path d="M24 15v9l5 3"/></svg>',
         '<svg viewBox="0 0 48 48"><path d="M24 6v24M14 22l10 10 10-10"/><path d="M8 38h32"/></svg>']

def page(t):
    P = t["pre"]; pic_ = lambda n, alt, w, h, cls="", lazy=True: pic(n, alt, w, h, cls, lazy, P + "img/")
    nav = "".join(f'<a href="#{a}">{l}</a>' for a, l in zip(["apercu", "modules", "comment", "atouts", "faq"], t["nav"]))
    ticks = "".join(f"<li>{x}</li>" for x in t["ticks"])
    chips = "".join(f'<span class="chip">{c}</span>' for c in t["strip_chips"])
    facts = "".join(f'<li><i>{n}</i><div><b>{h}</b><p>{p}</p></div></li>' for n, h, p in t["facts"])
    tabs = "".join(f'<button class="tab" role="tab" id="t-{k}" aria-controls="p-{k}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{n}</button>' for i, (k, n, *_r) in enumerate(t["tabs"]))
    panels = ""
    for i, (k, n, h3, p, lis, shot, prod, alt1, alt2) in enumerate(t["tabs"]):
        li = "".join(f"<li>{x}</li>" for x in lis)
        panels += (f'<div class="panel{" on" if i == 0 else ""}" id="p-{k}" role="tabpanel" aria-labelledby="t-{k}"><div><h3>{h3}</h3><p>{p}</p><ul>{li}</ul>'
                   f'<a class="btn small" href="#telecharger">{t["nav_cta"]}</a></div><div class="shot"><div class="win"><div class="tb"><i></i><i></i><i></i></div>'
                   f'{pic_(shot, alt1, 1600, 1004)}</div><div class="prod">{pic_(prod, alt2, 960, 620)}</div></div></div>')
    steps = "".join(f'<div class="step rv d{i+1}" data-n="{i+1}">{ICONS[i]}<h3>{h}</h3><p>{p}</p></div>' for i, (h, p) in enumerate(t["steps"]))
    ideas = "".join(f'<div class="idea rv d{i%3+1}"><b>{h}</b><span>{p}</span></div>' for i, (h, p) in enumerate(t["ideas"]))
    dl = "".join(f'<div class="card rv d{i+1}"><div class="os">{o}</div><h3>{n}</h3><p>{s}</p><a class="btn small" href="{REL}">{t["dl_btn"]}</a><small class="hint">{h}</small></div>' for i, (o, n, s, h) in enumerate(t["dl"]))
    fq = list(t["faq"]); fq.insert(1, fq.pop(4))  # question licence en 2e position
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in fq)
    foot = " · ".join(f'<a href="{u}">{l}</a>' for l, u in t["foot_links"]) + f' · <a href="mailto:{MAIL}">{t["contact"]}</a>'
    b = lambda key, ic, cls: f'<div class="bx {cls} rv"><div class="ic">{ic}</div><h4>{t[key][0]}</h4><p>{t[key][1]}</p></div>'
    html = f'''<!doctype html>
<html lang="{t["lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t["title"]}</title>
<meta name="description" content="{t["desc"]}">
<meta name="theme-color" content="#0b0e14">
<meta property="og:type" content="website"><meta property="og:title" content="{t["og"]}"><meta property="og:description" content="{t["desc"]}">
<meta property="og:image" content="{P}img/og.jpg"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{P}img/logo.svg" type="image/svg+xml">
<link rel="alternate" hreflang="{t["other_hl"]}" href="{t["other"]}">
<link rel="preload" href="{P}fonts/Inter-Variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{P}css/site.css">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"LithoShape3D","applicationCategory":"MultimediaApplication","operatingSystem":"Windows, macOS","description":"{t["desc"]}"}}</script>
</head>
<body>
<a class="skip" href="#main">{t["skip"]}</a>
<header class="top"><div class="wrap bar">
  <a class="brand" href="#"><img src="{P}img/logo.svg" alt="" width="32" height="32"><b>Litho<span>Shape3D</span></b></a>
  <button class="burger" aria-label="{t["menu"]}" aria-expanded="false">{t["menu"]}</button>
  <nav class="main" aria-label="Navigation">{nav}<a class="nav-cta" href="#telecharger">{t["nav_cta"]}</a><a class="lang" href="{t["other"]}" hreflang="{t["other_hl"]}">{t["other_label"]}</a></nav>
</div></header>
<main id="main">
<section class="hero"><div class="wrap grid">
  <div>
    <div class="kicker">{t["kicker"]}</div>
    <h1>{t["h1"]}</h1>
    <p class="lead">{t["lead"]}</p>
    <div class="cta"><a class="btn" href="#telecharger">{t["cta1"]}</a><a class="btn ghost" href="{BETA}">{t["cta2"]}</a></div>
    <ul class="ticks">{ticks}</ul>
  </div>
  <div class="stage"><div class="halo"></div>
    <div class="frame">{pic_("avant-eteinte", t["hero_alt_off"], 1100, 1100, "", False)}<div class="lit">{pic_("apres-allumee", t["hero_alt_on"], 1100, 1100)}</div></div>
    <div class="switch" role="group" aria-label="{t["off"]} / {t["on"]}"><button data-state="off" aria-pressed="true">{t["off"]}</button><button data-state="on" aria-pressed="false">{t["on"]}</button></div>
  </div>
</div></section>
<div class="strip"><div class="wrap"><b>{t["strip"]}</b>{chips}</div></div>

<section id="apercu"><div class="wrap compare-wrap">
  <div class="rv">
    <div class="eyebrow">{t["s1_eye"]}</div><h2>{t["s1_h"]}</h2><p class="sub" style="margin-bottom:0">{t["s1_sub"]}</p>
    <ul class="facts">{facts}</ul>
  </div>
  <div class="compare rv d2" role="group" aria-label="{t["cmp_lab"]}">
    {pic_("apres-allumee", t["hero_alt_on"], 1100, 1100)}
    <div id="cmp-top" class="top">{pic_("avant-eteinte", t["hero_alt_off"], 1100, 1100)}</div>
    <div id="cmp-handle" class="handle"></div><span class="tag l">{t["cmp_off"]}</span><span class="tag r">{t["cmp_on"]}</span>
    <input id="cmp" type="range" min="0" max="100" value="50" aria-label="{t["cmp_lab"]}">
  </div>
</div></section>

<section id="modules" class="alt"><div class="wrap">
  <div class="rv"><div class="eyebrow">{t["s2_eye"]}</div><h2>{t["s2_h"]}</h2><p class="sub">{t["s2_sub"]}</p></div>
  <div class="tabs rv" role="tablist">{tabs}</div>
  <div class="rv">{panels}</div>
</div></section>

<section id="comment"><div class="wrap">
  <div class="rv center"><div class="eyebrow">{t["s3_eye"]}</div><h2>{t["s3_h"]}</h2><p class="sub">{t["s3_sub"]}</p></div>
  <div class="steps">{steps}</div>
</div></section>

<section id="atouts" class="alt"><div class="wrap">
  <div class="rv"><div class="eyebrow">{t["s4_eye"]}</div><h2>{t["s4_h"]}</h2><p class="sub">{t["s4_sub"]}</p></div>
  <div class="bento">
    <div class="bx b-lg rv"><div class="ic">◐</div><h4>{t["b1"][0]}</h4><p>{t["b1"][1]}</p>{pic_("app-lithophanie", t["b1_alt"], 1600, 1004)}</div>
    {b("b2", "▦", "b-md")}{b("b3", "✓", "b-md")}{b("b4", "⌂", "b-sm")}{b("b5", "⬚", "b-sm")}{b("b6", "?", "b-sm")}
  </div>
</div></section>

<section><div class="wrap">
  <div class="rv"><div class="eyebrow">{t["s5_eye"]}</div><h2>{t["s5_h"]}</h2></div>
  <div class="ideas" style="margin-top:34px">{ideas}</div>
</div></section>

<section id="telecharger" class="alt"><div class="wrap center">
  <div class="rv"><div class="eyebrow">{t["s6_eye"]}</div><h2>{t["s6_h"]}</h2><p class="sub">{t["s6_sub"]}</p></div>
  <div class="dl">{dl}</div>
  <p class="rv" style="color:var(--muted);font-size:15px;margin:30px auto 0;max-width:680px">{t["dl_note"]}</p>
  <p class="rv" style="margin-top:22px"><a class="btn ghost" href="{BETA}">{t["dl_beta"]}</a></p>
</div></section>

<section id="faq"><div class="wrap" style="max-width:840px">
  <div class="rv center"><h2>{t["s7_h"]}</h2><p class="sub">{t["s7_sub"]}</p></div>
  <div class="rv">{faq}</div>
</div></section>

<div class="band"><div class="rv"><h2>{t["band_h"]}</h2><p class="sub" style="margin:0 auto 30px">{t["band_sub"]}</p><a class="btn" href="#telecharger">{t["cta1"]}</a></div></div>
</main>
<footer><div class="wrap row"><div>© <span id="y">2026</span> LithoShape3D</div><div>{foot}</div></div></footer>
<div class="mbar"><a class="btn" href="#telecharger">{t["cta1"]}</a></div>
<script src="{P}js/site.js"></script>
</body>
</html>
'''
    return html

os.makedirs("en", exist_ok=True)
open("index.html", "w", encoding="utf-8").write(page(TXT["fr"]))
open("en/index.html", "w", encoding="utf-8").write(page(TXT["en"]))
print("pages generees :", os.path.getsize("index.html"), "et", os.path.getsize("en/index.html"), "octets")
