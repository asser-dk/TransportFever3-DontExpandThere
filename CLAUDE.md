# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

TF3 mod (modId `fenris_dont_expand_there_1`): an invisible road add-on (`preventParcels`). Towns don't grow
buildings on the marked side of the road, and existing town buildings there are removed. Towns can still
extend or change the road.

## Checks

- Type check from the repo root: `tf3-tl check <file>.tl`. The `tf3` plugin's hook also runs it, and
  schema validation of `src/mod.json`, `src/_metadata/modinfo.json` and `src/strings.json`, after every edit.
- `tlconfig.lua` and `all_def.tl` are copies of the workspace (`..`) masters; keep them in sync.
- No automated tests. Verification is in-game by the user; afterwards grep the game log for `fenris_dont_expand_there`.
- After adding, removing or renaming files under `src/content/`, run `/tf3:stage-mod` to regenerate
  `src/_content.json`.
- `APPLIED_WORKAROUNDS.md` lists the undocumented game internals the mod relies on. Add an entry (with its
  fallback and in-game re-test) when introducing one; after a game update, have the user re-test every entry.

## Releases

- Commit straight to `main`; no feature branches.
- Each published update: bump `revision` in `src/mod.json` and add a changelog entry to the
  `description` in `src/_metadata/modinfo.json`.
- The cover embeds `art/map.svg` (OpenStreetMap data, ODbL). Keep the line
  `Cover map © OpenStreetMap, openstreetmap.org/copyright` at the end of that `description`.
