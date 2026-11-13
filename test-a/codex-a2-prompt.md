You are the visual puzzle specialist in an attended production pipeline, called by Claude Code as a separate process. This is step 3 of the contract you designed earlier.

Your earlier construction is in `codex-a1.json` and the production brief in `brief.md` (both in your working directory, test-a/). Read them. Do not read `.env` or anything outside this project; do not use the network.

The attached image is the actual output of the one authorised Images API request (gpt-image-2.6-flare, quality high), saved as `source-image.png`. It is **1088 × 1088**; the final canvas is 1080 × 1080, so place it with `<image href="source-image.png" x="-4" y="-4" width="1088" height="1088"/>` unless you have a better reason (say so). No further image generation is possible.

Your tasks:

1. Inspect the generated image. Report anything that differs from your `must_appear` / `must_not_appear` lists and anything that could create an unintended clue or competing answer once your foreground is added. Note where the floor line and props actually are; adapt your coordinates to the real image.
2. Author the complete final composition as one standalone SVG (width="1080" height="1080", viewBox="0 0 1080 1080") that embeds `source-image.png` and draws every deterministic element: cabinet, drawers, handles, hasps, padlocks, labels, question and rules. You may refine the public wording, caption or layout if the real image warrants it; report any change.
3. The SVG is rendered with CairoSVG 2.9. Use plain SVG 1.1 elements and presentation attributes (rect, path, line, circle, ellipse, polygon, g, text/tspan, linearGradient, radialGradient, opacity). Do **not** use filters (no blur/drop-shadow), CSS stylesheets, `<style>`, masks, clipPath on text, foreignObject, textPath, external fonts or any external file other than `source-image.png`. Fonts available: DejaVu Sans/Serif, Liberation Sans/Serif, Ubuntu (weights via font-weight), Ubuntu Sans, Quicksand, Nimbus Sans, Nimbus Roman, C059, P052, URW Bookman, URW Gothic.
4. Keep solution-critical relationships exact and unambiguous at 360 px wide. The public image must contain no answer, highlighting, motion arrows or difficulty label.

Return only JSON matching the schema. Put the full SVG source in `svg`.
