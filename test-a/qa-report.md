# Test A — QA report ("The Workshop Cabinet", Type 2, Codex-led)

**Overall: CONDITIONAL.**
- The delegation, image generation, correctness, uniqueness and visual evidence pass.
- **Difficulty misses the target.** Codex claimed Medium; Claude assessed Medium (lower end); the blind solve rated it Easy. Under the project's difficulty gate this puzzle should be reclassified as **Easy** or revised before publication. It is not a full pass.

Evidence class: **[P]** programmatic · **[M]** model-based assessment · **[H]** needs human inspection.

## Delegation evidence

| Step | What happened | Evidence |
|---|---|---|
| Brief | Claude wrote the brief (production standard with the Type 2 paragraph replacing Type 12) and the technical contract. It specified no idea, answer or scene | `brief.md`, `codex-a1-prompt.md` |
| Construction (Codex call a1) | A real `codex exec` subprocess (gpt-6-astra, xhigh, read-only sandbox, 575 s). Codex invented the cabinet/hasp mechanism, answer, alternatives, art direction and image prompt | `codex-a1.json`, `logs/codex-a1-construct-events.jsonl`, `logs/codex-execution.log` |
| Image (paid request 1 of 2) | Codex's prompt was sent verbatim to `gpt-image-2.6-flare`, quality high, 1088×1088, in 9.2 s. Codex chose to generate only the workshop setting and to draw every solution-critical element deterministically | `source-image.png`, `image-prompt.txt`, `logs/image-api-usage.json` |
| Composition (Codex call a2) | Codex received the real image, reviewed it, and authored the full 1080×1080 SVG (614 s) | `codex-a2.json`, `compose.svg` (now the revised version), `qa/compose-v1.svg` |
| Claude QA → revision (Codex call a3) | Claude found a uniqueness risk (below). Codex repainted the frame as one continuous piece (301 s) | `codex-a3-prompt.md`, `codex-a3.json`, `qa/puzzle-v1.png` → `puzzle.png` |
| Blind solve (Codex call a-blind) | A fresh session saw only `puzzle.png` and read no files. It ran 0 shell commands | `qa/blind-solve-codex.json` |

## Checks

| # | Check | Method and artifact | Result |
|---|---|---|---|
| 1 | Correct, complete solution | [M] Claude traced all six mounting plates in `puzzle.png` and the 2× crops (`qa/hasps-2x.png`): A = frame/drawer 1, B = drawer 2/drawer 3, C = drawer 4/frame | PASS |
| 2 | Uniqueness | [M] In v1 the oak bottom rail could read as a fifth drawer, making C a second answer. **Blocking risk → fixed in v2.** The frame is now continuous olive and the drawers oak. Re-inspected at 1080 and 360 px. The blind solver found no defensible alternative | PASS (after revision) |
| 3 | Logical / physical consistency | [M] The rules exclude unlocking, damage, dismantling and a moving frame. The hinged-strap objection is weak and documented in `solution.md` | PASS |
| 4 | Final visible evidence | [M] Exactly 4 drawers, 4 handles, 3 identical closed hasps and padlocks, labels A/B/C. Each plate sits wholly on one surface. Coordinates in Codex's SVG match its stated plan. No programmatic pixel decode was written for this test (the shapes are vector-drawn from a single SVG Claude inspected) | PASS |
| 5 | Generated image vs. requirements | [M] No text, cabinets, hardware, people or answer cues. The floor is larger than requested (about 19% vs 12%) and there is a faint wall-tone band at y≈212. Neither affects the puzzle | PASS |
| 6 | Readability 1080 / 360 px | [M] The question and labels are clear at 360 px. The rules text (30 px → 10 px) and the mounting plates are small but legible; the blind solver noted they may need zooming | PASS (minor) |
| 7 | No answer leakage | [M] The hardware styling is identical, with no highlight or arrows. The caption names all three options | PASS |
| 8 | Composition | [M] Front-on illustrated workshop with a vector cabinet. The flat vector foreground is a little "clip-art" against the painterly background, and a human should judge whether that is acceptable for publication [H] | REVIEW_REQUIRED |
| 9 | Difficulty (adult-oriented) | [M] Codex: Medium · Claude: Medium (lower end) · blind solve: **Easy** ("one insight"). The colour separation added to secure uniqueness also makes the decisive check faster | **Below target (Medium/Hard)** |
| 10 | Originality | [M] No lock/hasp puzzle exists in the Type 1 or Type 2 reference packages. The general gag of a lock fastened only to moving parts (a gate chained to itself) is widely known, so the idea is familiar even though the instance is original | PASS (familiar gag noted) |

## Handoff / process findings

- Codex followed the technical contract, wrote no files and stayed in the read-only sandbox. Credential scan of all outputs: clean.
- Codex could not render its own SVG (CairoSVG wasn't available in its sandbox), so every raster check fell to Claude. This worked, but it means Codex designs blind to its final pixels unless Claude returns a render.
- The difficulty calibration weakness noted in the project concept (§6) reproduced here: the author model rated its own puzzle above what the reviewer and blind solver found.
