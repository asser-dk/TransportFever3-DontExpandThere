#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
art="$root/art/icon"
out="$root/src/content/infrastructure/edge_addons/fenris_dont_expand_there"
command -v magick >/dev/null || { echo "magick not found; install ImageMagick" >&2; exit 1; }
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

python3 -I "$root/scripts/icon/build_icon.py" new "$art/alley.png" "$art/player_owned.png" "$tmp/icon.png"
python3 -I "$root/scripts/icon/build_icon.py" old "$art/player_owned_old.png" "$art/player_owned.png" "$tmp/icon_old.png"

# The game reads TGA rows bottom-up; -orient only sets the header flag, so pre-flip the rows.
magick "$tmp/icon.png" -flip -type TrueColorAlpha -orient BottomLeft -compress None "$out/icon@2x.tga"
magick "$tmp/icon_old.png" -flip -type TrueColorAlpha -orient BottomLeft -compress None "$out/icon_old@2x.tga"
magick "$art/preview.png" -flip -alpha off -type TrueColor -orient BottomLeft -compress None "$out/icon_preview@2x.tga"
magick "$art/preview_old.png" -flip -alpha off -type TrueColor -orient BottomLeft -compress None "$out/icon_old_preview@2x.tga"
echo "rendered icon@2x.tga, icon_old@2x.tga and their previews"
