You are the visual puzzle specialist, called by Claude Code as a separate process. This is the composition step of the Type 13 hybrid test.

Files in your working directory (test-c/): `brief.md`, `handoff.json` (now **version 2**: see its `revision_log`, which answers the issues you raised), `codex-c1.json` (your scene development), `logic-verification.json`. Do not read `.env` or anything outside this project; no network.

The attached image is the actual output of the one authorised Images API request for this test (your prompt, gpt-image-2.6-flare, quality high), saved as `source-image.png`, **1088 × 1088**. Place it at x=-4, y=-4 (1088 × 1088) unless you have a reason not to. No further image generation is possible.

Tasks:
1. Review the generated image against your must_appear / must_not_appear lists and note where the inn, veranda, horizon and empty snow actually are. Adapt your composition plan to the real image (the viewpoint came out flatter and the snowfield larger than planned).
2. Author the complete final 1080 × 1080 SVG. Draw every clue flagged deterministic in the handoff exactly as specified (C1–C10), plus the question and facts F1–F3. Use the **version 2** wording of F3 (meaning unchanged; you may polish phrasing without changing facts).
3. CairoSVG 2.9 constraints: plain SVG 1.1 shapes, text, gradients, clipPath on shapes/images; no filters, `<style>`, masks, foreignObject, textPath or external files other than `source-image.png`. Fonts: DejaVu Sans/Serif, Liberation Sans/Serif, Ubuntu (weights), Ubuntu Sans, Quicksand, Nimbus Sans, Nimbus Roman, C059, P052, URW Bookman, URW Gothic, Z003.
4. For Claude's clue-by-clue QA, return `clue_locations`: one entry per clue id with a bounding box [x0, y0, x1, y1] in final-canvas pixels covering where that clue is drawn (for C10 give the whole evidence field).

Return only JSON matching the schema, with the complete SVG in `svg`.
