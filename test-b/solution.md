# Test B — "Lights out" (private solution)

**Type 10:** Switches, adjacency and valid paths · **Target:** Hard · **Constructed, rendered and verified by:** Claude Code (claude-opus-5-5); no generative image.

## Public post

- **Image:** `test-b/puzzle.png`
- **X caption:** Every room you walk into flips its light. How few doorways does it take to leave by the back door with the whole house dark?

## Answer

**13 doorways.**

One shortest route (the loop through the Studio, Bathroom and Bedroom can be run in either direction; these are the only two shortest routes):

Hall → Office → Library → Studio → Bathroom → Bedroom → Library → Office → Hall → Dining room → Kitchen → Boot room → Kitchen → Boot room → out of the back door.

## Why 13 is enough

Follow the route and flip each light on entry. The Office goes on, the Library goes on, and the Studio, Bathroom and Bedroom go off. Re-entering the Library turns it off, then the Office goes off and the Hall goes off. The Dining room goes off and the Kitchen and Boot room come on. The Kitchen and Boot room are then each entered a second time and go off. Every light is now off and you are in the Boot room.

## Why fewer is impossible

1. Every doorway puts you into exactly one room and flips that room's light. **Doorways walked = total room entries.**
2. A room that starts lit must be entered an odd number of times (at least once) to end dark. A dark room must be entered an even number of times (none, or at least twice).
3. **Lit rooms: Hall, Studio, Bedroom, Bathroom, Dining room — at least 5 entries.** The Hall counts. You start inside it with its light on, and stepping out changes nothing, so you must come back into it.
4. **Dark rooms you cannot avoid:** the Office is the only way from the Hall to the north wing, the Library is the only way on from the Office, and the Kitchen is the only way to the Boot room. One entry would leave each of them on, so **each needs at least 2 → 6.**
5. **The Boot room** is dark and you must finish in it. You enter it at least once, and once would leave it on: **at least 2.**

Total ≥ 5 + 6 + 2 = **13**. The route meets the bound exactly. Each lit room is entered once, and each unavoidable dark room twice.

## The ordering trap

The north wing has to come first. Its loop visits each lit room once and brings you back into the Library for its second entry, then through the Office (second entry) into the Hall (its single entry). If you go south first, you must cross the Dining room and the Hall twice each on the way back, and each extra entry costs two more doorways. The finish is the Kitchen ↔ Boot room shuffle: each needs two entries, and you have to end in the Boot room.

## Strongest wrong answers checked

| Claim | Why it fails |
|---|---|
| **11** (Hall → Office → Library → loop → Library → Office → Hall → Dining room → Kitchen → Boot room) | Leaves the Kitchen and Boot room **on**: each was entered once. Replayed by `solver.py` (`tempting_11_walk_lights_left_on`). |
| Counting only the lit rooms, or forgetting that dark rooms turn **on** when entered | Breaks rule 2 above. |
| Ignoring the Hall | You still have to pass back through it to reach the south wing, and the count above already includes that single entry. |
| Any route of 12 or fewer | Ruled out by exhaustive search (below) and by the counting bound. |
| "Step out of the back door and come back in to flip the Boot room for free" | Allowed or not, it doesn't help. You still need two Kitchen entries and must end in the Boot room after the second one. `solver.py` models free back-door trips and still finds 13. |

## Verification

- **Construction (programmatic, `test-b/solver.py` → `verification.json`):** a BFS over (room, 9 light bits) gives a minimum of 13 and exactly 2 shortest walks. A separately written depth-first enumeration of every walk up to 13 doorways finds no successful walk shorter than 13 and the same 2 walks of length 13. The counting lower bound from the graph is 13 (tight).
- **Rendered pixels (programmatic, `test-b/check_pixels.py` → `qa/pixel-check.json`):** the room light states were decoded from floor luminance in `puzzle.png` (lit 199–209, dark 57–58). The doorways were decoded from threshold-coloured runs on every shared wall (all 9 found, no false ones), and exactly one exterior opening (the back door, east wall) was found. The decoded instance matches `instance.json` and re-solves to 13.
- **Visual:** inspected at 1080 px and 360 px (`qa/puzzle-360.png`); see `qa-report.md`.
