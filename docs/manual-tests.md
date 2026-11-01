# Manual tests

Last-resort manual checks for what the automated tests (`tests/unit/`, `tests/ingame/`) can't observe,
such as on-screen appearance or how a tool feels. Each one costs a manual run before every upload and
after every game update, so keep the list as short as possible; an empty list is fine. Hard cap: 10.

Run all of them before each upload and after each game update; after a change, run the ones that cover
it.

| ID | Test | Covers | Last passed |
|---|---|---|---|
| V1 | A marked side stays empty through the 1940 road upgrade, and regrows once unmarked | Era icons, tool feel, growth over time, era road upgrade, save/load, removal | 2026-10-24, revision 2 |

## V1. A marked side stays empty through the 1940 road upgrade, and regrows once unmarked

Covers: era icons and `preventParcels` (both `APPLIED_WORKAROUNDS.md` entries), tool feel, growth over
time, the engine's 1940 town road upgrade, save/load, removing the mark.

Why manual: what the construction menu shows, how the tool behaves under the mouse, slow and random
town growth, the engine-internal road upgrade and a full save/load cycle can't be observed or driven
through the API, and rebuilding a street from a script fails with an engine assertion
(map lookup), so a test can't place the add-on either.

Setup: new game starting in 1939, with a town; the mod enabled.

1. Open the road tools. Hover the add-on.
   Expected: Cobblestone-era icon and hover preview.
   Log: `fenris_dont_expand_there: era icons enabled`
2. Mark one side of a cobblestone town street that has buildings on both sides.
   Expected: The mark snaps to the hovered side and draws nothing; the buildings on that side
   disappear, the other side keeps its own.
3. Try to mark a railway track.
   Expected: Not allowed.
4. Run at the highest speed until a few years after 1940; open the road tools again.
   Expected: The street has been upgraded to asphalt; the marked side is still empty while the other
   side and the rest of the town grow. The tool shows the modern icon and preview.
5. Save, load the save, and look at the marked street again.
   Expected: The marked side is still empty, and the tool still highlights the mark.
6. Remove the mark with the tool. Keep the town supplied (e.g. a bus line and goods deliveries) and run
   at the highest speed until it grows.
   Expected: The mark is gone and town buildings spawn on that side again.

<!--
## V2. <What the player does and what they should see>

Covers: <feature or APPLIED_WORKAROUNDS.md entry>

Why manual: <why neither a unit test nor an in-game test can check this>

Setup: <save, map, era or game state needed; or "as V<n>">

1. <action>
   Expected: <what the user should see>
2. <action>
   Log: `<regex matched against the mod's game log lines; checked automatically>`
-->
