You are the visual puzzle specialist, called by Claude Code as a separate process. This is a targeted revision after Claude's independent QA of your rendered composition.

Files in your working directory (test-a/): `compose.svg` (your SVG, unchanged), `codex-a1.json`, `codex-a2.json`, `brief.md`. The attached image is your SVG as rendered by CairoSVG to the final 1080 × 1080 PNG. Do not read `.env` or anything outside this project; no network.

QA finding to fix (blocking risk for uniqueness):
- The fixed bottom rail (y≈929–1024) has the same oak tone and similar edge treatment as the drawer fronts and no visual connection to the side stiles beyond butting against them. Without a handle it can still read as a shallow fifth drawer or plinth drawer. A reader who sees it that way would conclude that C also joins two moving parts, giving a second answer. The top rail has the same, milder risk.

Please revise with the smallest change that makes the fixed frame read unmistakably as one rigid piece (stiles + top rail + bottom rail/plinth) and distinct from the four drawer fronts, at both 1080 px and 360 px. Keep every solution-critical coordinate, the hardware, labels, wording and overall look unchanged unless a change is required for this fix. Do not add answer cues (no highlight on B, no arrows, no labels naming parts). CairoSVG constraints from before still apply (no filters, styles, masks, external files except source-image.png).

Return only JSON matching the schema, with the complete revised SVG in `svg`.
