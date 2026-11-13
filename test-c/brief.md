# One Small Puzzle — Test C production brief (hybrid: Claude logic, Codex scene)

Derived from `references/one-small-puzzle-production-prompt.txt`. The "Puzzle type" section is replaced by a Type 13 paragraph. `references/one-small-puzzle-prompt-types.txt` covers types 1–12 only; the approved Type 13 paragraph (P1, `backend/prompts.py`) is not in this workspace, so the paragraph below was written by Claude for this PoC from the Type 13 row of `references/one-small-puzzle-raetseltypen.md`.

## Puzzle type

Detective scene with multiple interacting clues. One original illustrated scene in which the reader works out who did something, or which account must be true, by combining several visible clues. No single clue settles the case: at least two must be combined, and the most tempting wrong answer survives one of them. State any fact the reader needs that the picture cannot show, such as times or a rule about the setting. Keep every decisive clue visible and unambiguous at phone size. In the private solution, list every clue, show how they combine to force the answer, and name the clue that eliminates each alternative. Verify the finished image against the full clue inventory and check that no incidental detail supports another answer.

**Division of labour (Type 13 routing):** Claude Code fixed the case, the answer, the complete clue inventory and the elimination of alternatives (`handoff.json`, verified by `verify_logic.py`). Codex decides how the clues become naturally visible: setting, viewpoint, medium, composition, art direction, the image-generation prompt and the final composition. Codex must not change the facts of the case; it may polish public wording, choose the title and write the caption, and must report anything in the handoff it finds ambiguous or unworkable.

## Editorial brief (production standard, adapted to one puzzle)

- Target difficulty: **Hard**, by adult standards. Difficulty must come from combining evidence, not from tiny details, poor contrast or lengthy reading.
- The puzzle must be self-contained and the answer unique under the public rules.

## Art direction

Design this post individually. Avoid a generic header/footer/card template. Give the scene the frame it needs. The look must be clearly different from a flat workbook diagram, but every decisive clue must stay exact and readable at 360 px wide. Existing posts in this test set: a warm front-on workshop cabinet (Test A) and a top-down night floor plan of a house in yellow and navy (Test B); avoid looking like either.

## Deliverables

1. One finished 1080 × 1080 PNG with the question and the necessary facts; no answer, solution marks or difficulty label.
2. One short, idiomatic English X caption that invites a specific answer without giving away the insight; no IQ bait, success-rate claims or unnecessary hashtags.
3. Private answer and explanation (Claude has drafted the logic; Codex adds scene-specific notes).
4. Editorial notes: difficulty and why, decisive step, what to check in the finished image.
