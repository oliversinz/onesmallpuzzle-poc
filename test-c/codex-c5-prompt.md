You are the visual puzzle specialist, called by Claude Code as a separate process. Final, text-only revision of your Test C composition.

Files in your working directory (test-c/): `compose.svg` (current, revision c4), `handoff.json` (now **version 4**: see the last `revision_log` entry). The attached image is the current render. Do not read `.env` or anything outside this project; no network.

1. F3 must now say that the tracks are all still visible. Exact wording (you may only reflow lines): "Every drive since 1 am left its own separate pair of tyre tracks, all still visible: softened by fresh snow if made while it was snowing, sharp if made after it stopped. Anything older is buried." Keep the existing bold emphasis on "own separate pair", "softened" and "sharp".
2. The fact block (F1–F3, y≈840–1065) is uneven: F2 is set tighter and smaller than F1 and F3. Reflow F1–F3 with consistent size and leading so that everything fits above y=1068 and stays clear of the courtyard artwork (which ends at about y=836). A slightly smaller common size is acceptable if needed; keep it readable at 360 px.

Change nothing else. CairoSVG constraints as before. Update `clue_locations` for F1–F3.

Return only JSON matching the schema, with the complete revised SVG in `svg`.
