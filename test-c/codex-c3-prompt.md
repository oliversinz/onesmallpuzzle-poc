You are the visual puzzle specialist, called by Claude Code as a separate process. This is a targeted revision after Claude's clue-by-clue QA of your Test C composition.

Files in your working directory (test-c/): `compose.svg` (your SVG, unchanged), `handoff.json` (v2), `codex-c1.json`, `codex-c2.json`, `brief.md`. The attached image is your SVG rendered by CairoSVG 2.9 to the final 1080 × 1080 PNG. Do not read `.env` or anything outside this project; no network.

QA results: F1–F3, C2, C3, C5–C10 pass. Softened vs sharp tracks read very clearly. Two findings must be fixed:

1. **C4 (blocking: competing reading).** The handoff requires the lamp post "just inside the entrance, beside the entrance lane", and fact F2 says "the lamp post by the entrance". In the render the lamp stands deep in the yard between bays 2 and 3 (about x=437–500, y=520–710), far from the bottom-left entrance, and it reads as sitting in bay 3's slot. Bay 4's sharp tracks pass right at its base, while bay 5's softened tracks pass nowhere near it. A reader can then argue "only tracks that touch the post can belong to the culprit", which points away from the intended answer. Move the lamp to just inside the entrance opening, beside the lane, so that **all three track pairs pass it at a similar, close distance**. Proximity must not discriminate between bays 2, 4 and 5. Keep the yellow scrape (same yellow as the cars) and the dent facing the lane, readable at 360 px.
2. **C1 (clarity).** The single entrance is only an unmarked gap in a thin boundary line, and the tracks run off into the text block. Make the entrance unmistakable as the one way in and out (for example gate pillars or wall ends with the lane continuing out of the courtyard), with all three pairs passing through it. Keep the text clear of the tracks.

Change nothing else unless the fix requires it, and keep all clue states exactly as they are. CairoSVG constraints as before (no filters, `<style>`, masks, foreignObject or external files except source-image.png). Update `clue_locations` for anything that moved.

Return only JSON matching the schema, with the complete revised SVG in `svg`.
