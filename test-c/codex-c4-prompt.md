You are the visual puzzle specialist, called by Claude Code as a separate process. This is a second targeted revision of your Test C composition.

Files in your working directory (test-c/): `compose.svg` (your current SVG, revision c3), `handoff.json` (now **version 3**: see the last `revision_log` entry), `codex-c3.json`. The attached image is the current render. Do not read `.env` or anything outside this project; no network.

An independent blind solver (a fresh session that saw only the PNG) answered bay 5, but with medium confidence. It read the yellow star-shaped mark on the lamp post as a cartoon impact burst rather than transferred paint. Read that way, colour no longer discriminates and bay 2 becomes defensible. Claude has changed the case wording (handoff v3):

1. **F2 text** must now read (you may polish phrasing, not facts): "At 2 am the night porter heard a crunch: a car clipped the lamp post by the entrance and left a smear of its paint on it. That car is still in the car park." Keep the fact block readable; reflow lines as needed.
2. **C4 drawing:** replace the star/burst shape with a mark that reads unmistakably as a smear of transferred car paint: a scuffed, streaky band along the post at bumper height, beside a small dent. Keep exactly the same yellow as the cars (#f1ce35). It must remain visible at 360 px.

Change nothing else: lamp position, tracks, cars, roofs, numbering and other text stay as they are. CairoSVG constraints as before. Update `clue_locations` for C4 and F2.

Return only JSON matching the schema, with the complete revised SVG in `svg`.
