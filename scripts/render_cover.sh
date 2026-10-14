#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
command -v rsvg-convert >/dev/null || { echo "rsvg-convert not found; install librsvg" >&2; exit 1; }
rsvg-convert -w 1920 -h 1080 "$root/art/cover.svg" -o "$root/src/_metadata/0.png"
echo "rendered src/_metadata/0.png"
