# Tech stack

Update this file when the stack changes.

| Component | Version / detail |
|---|---|
| Transport Fever 3 | Steam app 3493540; type defs from the install's `api/tealdef/` and `base/tealdef/` |
| Teal | `tl` 0.24.8 on Lua 5.4, run as `tf3-tl` (`tf3` plugin `bin/`, pins the versions); scripts are `.tl`, Lua 5.2 semantics at runtime |
| Teal config | `tlconfig.lua` + `all_def.tl` in the repo root, copied from the workspace (`..`) |
| teal-language-server | 0.2.1, connected by the `tf3` plugin; reads the repo's `tlconfig.lua` |
| Cover image | `art/cover.svg` → `src/_metadata/0.png` via `scripts/render_cover.sh` (`rsvg-convert`, librsvg) |
| Add-on icons | `art/icon/*.png` → `icon@2x.tga`, `icon_old@2x.tga` and their `_preview` variants in `src/content/infrastructure/edge_addons/fenris_dont_expand_there/` via `scripts/icon/build.sh` (Python 3 + numpy + Pillow, ImageMagick) |
| JSON validation | `npx ajv-cli@5` against `~/Documents/documentation/references/transport-fever-3/schemas/` |
| Claude Code | `tf3` plugin (local `transport-fever-3-modding` marketplace, `..`): skills and the edit-check hook |
| VCS | Git |
