# Applied workarounds

Undocumented game internals this mod relies on. They can break with any game update: re-test each one
in-game after every game update, before the next release. Add an entry whenever the mod starts relying on
another one.

- `construction_react_util.forEachDefinition` (`gui.zip: gui/construction/construction_react_util.tl`),
  wrapped by `src/content/gui/fenris_dont_expand_there/era_icons.script.tl` for era icons. Fallback: the
  modern icon in every era, with a `log.warning`. Re-test: the road-tools icon is cobblestone before 1940
  and switches at 1940; the log shows `fenris_dont_expand_there: era icons enabled`.
- `preventParcels` in `street.edge.lua`: used by the base noise barriers but missing from the
  `EdgeDecoration` tealdef. Re-test: no town buildings on the marked side, and existing ones are removed.
