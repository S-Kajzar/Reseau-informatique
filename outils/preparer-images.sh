#!/usr/bin/env bash
# Prépare les images intégrées dans la page (ImageMagick 6 requis).
#   - src/images/originaux/       : dessins du site (SVG) et leurs rendus PNG en double définition (outils/captures.js),
#                                   figures d'origine des cours et des exercices à venir
#   - src/images/accueil.png      : illustration de la page d'accueil (un réseau local)
#   - src/images/carte-*.png|jpg  : images des cartes de l'accueil, toutes au même format 480 × 270
#   outils/captures.js rend d'abord les dessins SVG : NODE_PATH=$(npm root -g) node outils/captures.js
# Usage : bash outils/preparer-images.sh   (depuis la racine du dépôt)
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=src/images/originaux
OUT=src/images

# 1. Illustration de l'accueil : le dessin accueil.svg, ramené à 1120 × 620 et quantifié (PNG 8 bits)
convert "$SRC/accueil.png" -resize 1120x620 -strip -colors 256 "PNG8:$OUT/accueil.png"

# 2. Images des cartes de l'accueil : toutes au même format 480 × 270.
#    remplir : l'image couvre la carte (recadrée) ; entiere : l'image entière sur fond blanc (figures très allongées).
#    Les cartes « En cours d'édition » (cours, exercice, étude à venir) sont des recadrages du dessin de l'accueil,
#    grisés par la page ; recadrage <géométrie> en pixels du rendu double définition (2240 × 1240).
remplir() { convert "$1" -background white -alpha remove -alpha off -resize 480x270^ -gravity "${4:-center}" \
  -extent 480x270 -strip $3 "$OUT/$2"; }
entiere() { convert "$1" -background "${3:-white}" -alpha remove -alpha off -resize 456x250 -gravity center \
  -extent 480x270 -strip -colors 256 "PNG8:$OUT/$2"; }
recadrer() {
  local tmp
  tmp=$(mktemp --suffix=.png)
  convert "$SRC/accueil.png" -crop "$1" +repage "$tmp"
  remplir "$tmp" "$2" "-colors 256"
  rm -f "$tmp"
}
recadrer 1040x585+0+170    carte-cours.png      # point d'accès et appareils sans fil
recadrer 1120x630+600+500  carte-exercice.png   # commutateur et postes clients
recadrer 1200x675+1040+40  carte-etude.png      # serveur, routeur et Internet

find "$OUT" -maxdepth 1 \( -name '*.png' -o -name '*.jpg' \) -printf '%s\n' |
  awk '{s += $1} END {print NR " images, " int(s / 1024) " Kio"}'
