# Applied workarounds

Undocumented game internals this mod relies on. They can break with any game update: re-test each one
in-game after every game update, before the next release. Add an entry whenever the mod starts relying on
another one.

- `preventParcels` in `street.edge.lua`: used by the base noise barriers but missing from the
  `EdgeDecoration` tealdef. Re-test: no town buildings on the marked side, and existing ones are removed.
