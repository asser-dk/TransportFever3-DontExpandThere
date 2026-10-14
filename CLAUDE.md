# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

TF3 mod (modId `fenris_dont_build_there_1`): Invisible road add-on. Town buildings won't spawn on that side.

## Checks

- Type check from the repo root: `~/.luarocks/bin/tl check <file>.tl`. The `tf3` plugin's hook also runs it, and
  schema validation of `src/mod.json`, `src/_metadata/modinfo.json` and `src/strings.json`, after every edit.
- `tlconfig.lua` and `all_def.tl` are copies of the workspace (`..`) masters; keep them in sync.
- No automated tests. Verification is in-game by the user; afterwards grep the game log for `fenris_dont_build_there`.
- After adding, removing or renaming files under `src/content/`, run `/tf3:stage-mod` to regenerate
  `src/_content.json`.
- `APPLIED_WORKAROUNDS.md` lists the undocumented game internals the mod relies on. Add an entry (with its
  fallback and in-game re-test) when introducing one; after a game update, have the user re-test every entry.

## Releases

- Commit straight to `main`; no feature branches.
- Each published update: bump `revision` in `src/mod.json` and add a changelog entry to the
  `description` in `src/_metadata/modinfo.json`.
