# Test C — QA report ("A Crunch in the Snow", Type 13, hybrid integration test)

**Overall: CONDITIONAL.**
- The integration works. Every clue in Claude's inventory is in the final PNG with the required state. The answer (bay 5) is unique, by programmatic enumeration on the evidence decoded from the final artwork and by the final blind solve (no defensible alternative, high confidence).
- **Getting there took three correction loops after the first composition:** one placement failure, one clue meaning lost in the drawing, and one wording gap.
- **Difficulty misses the Hard target.** Blind solves rated it Easy, Medium and Easy across versions, and Codex rated it Medium. Claude now assesses it as **Medium at best**.

Evidence class: **[P]** programmatic · **[M]** model-based assessment · **[H]** needs human inspection.

## Workflow trace

| Step | Who | What happened | Evidence |
|---|---|---|---|
| 1. Case, answer, clue inventory, alternatives | Claude | Snowy car park; scrape colour × track age; four tempting wrong answers | `handoff.json` (v1), `solution.md` |
| 2. Logic check | Claude | v1: per-car model → bay 5 unique | `verify_logic.py` (v1 superseded) |
| 3. Structured handoff | Claude | 13 clue ids (F1–F3, C1–C10) with exact required states, deterministic flags, must-not list, visibility rules and Codex's freedoms | `handoff.json` |
| 4. Codex scene development (c1, 563 s) | Codex | Chose a winter inn at dawn, gouache style, generated backdrop only, every clue deterministic. **Raised 4 handoff issues** (below). Wrote the image prompt | `codex-c1.json` |
| 4b. Handoff v2 | Claude | Tightened F3 ("own separate pair") and rewrote the logic check as a joint-history model; bay 5 is still unique | `handoff.json` `revision_log`, `logic-verification.json` |
| 5. Image (paid request 2 of 2) | Images API | Codex's prompt sent verbatim; 10.5 s; usable | `source-image.png`, `image-prompt.txt`, `logs/image-api-usage.json` |
| 6. Composition (c2, 1015 s) | Codex | Reviewed the real image, adapted to its flatter viewpoint, authored the SVG and returned clue bounding boxes | `codex-c2.json`, `qa/compose-v1.svg`, `qa/puzzle-v1.png` |
| 8. Claude review → revision (c3, 653 s) | Claude → Codex | **Handoff failure found and fixed** (C4/C1, below) | `codex-c3-prompt.md`, `codex-c3.json`, `qa/compose-v2.svg`, `qa/puzzle-v2.png` |
| 8b. Blind solve 1 → handoff v3 → revision (c4, 305 s) | Codex (fresh) → Claude → Codex | The star-shaped mark read as an impact burst rather than paint. F2 now states the paint; the mark was redrawn as a smear | `qa/blind-solve-codex-v2.json`, `codex-c4.json`, `qa/puzzle-v3.png` |
| 8c. Blind solve 2 → handoff v4 → revision (c5) | Codex (fresh) → Claude → Codex | Weak alternative: bay 1's tracks could be hidden under the car. F3 now says "all still visible"; the fact block was re-leaded | `qa/blind-solve-codex-v3.json`, `codex-c5.json`, `compose.svg`, `puzzle.png` |
| 9. Final verification | Claude | Clue-by-clue visual review, programmatic evidence read-back, logic re-run on the decoded evidence, independent blind solve | `check_evidence.py` → `qa/evidence-check.json`, `qa/v2/*.png`, `qa/blind-solve-codex.json` |

## Handoff findings (Claude ↔ Codex)

**Issues Codex raised against Claude's handoff (step 4), all valid:**
1. The "own pair" rule did not explicitly exclude a later drive retracing an older track, which leaves room for a bay-4 return-trip story. → F3 changed to "Every drive since 1 am left its own separate pair…".
2. Tracks don't show direction. → Accepted: the argument needs only which pairs exist and how old they are.
3. Claude's `verify_logic.py` v1 collapsed repeated tracks and never tested swaps between bays. → Rewritten as v2 (joint histories, track multisets, occupancy). 4,509 consistent histories; bay 5 is still unique, with or without the roof assumption.
4. The case is "medium with a harder return-trip objection", not securely Hard. → Recorded (see difficulty).

**Failure introduced by Codex in the composition (step 6), caught by Claude's QA (step 8):**
- **C4 lamp placement (blocking).** The handoff required the lamp "just inside the entrance, beside the entrance lane", and F2 says "by the entrance". v1 put it deep in the yard between bays 2 and 3, reading as part of bay 3's slot. Bay 4's sharp tracks passed right at its base and bay 5's tracks passed nowhere near it. That invited a competing "whose tracks touch the post?" reading pointing away from bay 5. Codex's own `clue_locations` note described it as "on the inner entrance approach", so the mismatch was not visible from its self-report.
- **C1 entrance (clarity).** The single entrance was an unmarked gap, with tracks running into the text block.
- **Fix (c3):** the lamp now stands just inside a gateway marked by snow-capped wall ends, the lane continues off-frame, and all three pairs pass the lamp at similar distance (offsets of 18 px). The re-route made the pairs interleave and cross. Claude checked that the sharp (newer) track is drawn **over** the softened ones at each crossing, which is physically consistent, and that every pair still traces to its own bay.
**Clue meaning lost between the handoff and the image, caught by the blind solve (step 8b):**
- C4 asked for "an obvious fresh yellow paint scrape". Codex drew a yellow star-shaped burst. Claude's review and `check_evidence.py` confirmed the *colour* and *position* but not that it *reads as paint*. A fresh solver read it as a cartoon impact symbol; on that reading, colour proves nothing and bay 2 is defensible. Root cause: the paint fact lived only in the drawing. **Fix:** F2 states it ("left a smear of its paint on it"), and the mark was redrawn as a streaky smear (c4).

**Residual wording gap found by the second blind solve (step 8c):** F3 guaranteed a separate pair per drive but not that every pair is visible, so a 2 am shuffle by bay 1 (next to the lamp) with tracks hidden under the car was arguable. F3 now says "all still visible" (c5).

- No clue id was lost. Every one appears in the final PNG with the required state (table below), but **two clue meanings needed explicit text** before the image was unambiguous.

## Clue inventory vs. final PNG

| Clue | Required | Final PNG | Method | Result |
|---|---|---|---|---|
| F1 | Snow 1–3 am | "It snowed from **1 am** until **3 am**, then stopped." | [M] visual; literal SVG text | PASS |
| F2 | 2 am crunch; lamp by entrance; car left its paint; car still here | Present (v3 wording) | [M] | PASS (after v3) |
| F3 | v4 rule: separate, still-visible pairs; softened/sharp/buried | Present (v4 wording), key terms bold | [M] | PASS (after v4) |
| C1 | Single entrance; all tracks through it | Gateway between wall ends (y 690–813); all 6 grooves start off-frame inside that gap | [P] SVG path starts · [M] | PASS (after c3) |
| C2 | Bays 1–5 numbered, readable at 360 | Dark boards, 36 px numerals | [M] | PASS |
| C3 | Even snow except tracks | Opaque deterministic snow over the generated ground | [M] | PASS |
| C4 | Lamp just inside entrance; yellow paint smear; dent | Lamp by the upper wall end; streaky smear in exact car yellow (#f1ce35), pixel count in `qa/evidence-check.json` | [P] fill + pixel count · [M] | PASS (after c3 and c4) |
| C5 | Bay 1 yellow, snowy roof, no tracks | Body yellow, roof white, 0 track px in front | [P] pixels | PASS |
| C6 | Bay 2 red, snowy roof, softened pair | Body red, roof white, softened pair ends in car | [P] SVG + pixels | PASS |
| C7 | Bay 3 empty, smooth snow | Snow, no car, no track px | [P] pixels | PASS |
| C8 | Bay 4 yellow, bare roof, sharp pair | Body and roof yellow, 273 sharp px in front | [P] SVG + pixels | PASS |
| C9 | Bay 5 yellow, snowy roof, softened pair | Body yellow, roof white, softened px in front, 0 sharp | [P] SVG + pixels | PASS |
| C10 | No other tracks, footprints or vehicles | SVG has exactly 3 route pairs and 4 car uses, nothing else in the field | [P] SVG structure · [M] | PASS |
| — | Logic on what is actually drawn | Decoded evidence → `verify_logic.analyse()` → {bay 5}, also without the roof rule | [P] | PASS |

## Other QA checks

| Check | Method | Result |
|---|---|---|
| Uniqueness | [P] joint-history enumeration on intended and on decoded evidence → bay 5 only; [M] blind solve (below) | PASS (final blind solve: no defensible alternative) |
| Accidental clues | [M] Generated backdrop has no vehicles, tracks, text or lamps. In the evidence field the lamp sits closest to bay 1 (intended distractor: bay 1 has no tracks). Crossing order is physically consistent | PASS |
| Readability 1080 / 360 px | [M] Bay numbers, car colours, roof states and track styles are clear at 360. The six fact lines are about 10 px at 360 (legible but text-heavy). The scrape is small but distinct | PASS (text-heavy noted) |
| No answer leakage | [M] No highlight on bay 5. The caption asks for a bay and reasons | PASS |
| Composition | [M] Painterly generated inn + flat vector cars and tracks. Coherent palette, but the foreground reads as a diagram laid over an illustration. Text block is long. Needs a human verdict for publication [H] | REVIEW_REQUIRED |
| Difficulty | [M] Claude (author) aimed for Hard, with the bay-4 return-trip objection as the hard step. Codex: Medium. Blind solves: Easy (v2), Medium (v3), Easy (final). Most solvers never raise the return-trip objection: paint × softened tracks gives the answer directly. Each wording fix that removed an ambiguity (paint, visibility) also made it easier | **Below target (Hard)**: Medium at best |
| Originality | [M] No local reference puzzle uses snow or track ageing (types 1–12 checked by title and mechanism; no Type 13 package exists). "Snow on the car / tracks in the snow" is a familiar detective trope, but the instance is original | PASS |

## Independent blind solve

Three fresh Codex sessions (`gpt-6-astra`, xhigh) each saw only the PNG of the day. None read files or ran commands.

| Image version | Answer | Confidence | Defensible alternative raised | Difficulty | Action taken |
|---|---|---|---|---|---|
| v2 (after c3; star-shaped mark, no paint wording) | Bay 5 "if the mark is paint" | medium | **Bay 2**, if the yellow mark is an impact symbol rather than paint | Easy | Handoff v3: paint stated in F2; mark redrawn as a smear (c4) |
| v3 (after c4) | Bay 5 | high | Bay 1 (weak, conditional): a 2 am shuffle with tracks hidden under the car | Medium | Handoff v4: "all still visible" in F3; fact block re-leaded (c5) |
| **v4, final** | **Bay 5** | **high** | **none** | Easy | none: final |

Remaining remarks from the final blind solve, none blocking: the track rule is "physically idealized" (it is an explicit puzzle rule); the fact paragraph is dense on a phone; the smear is small; softened tracks are low-contrast where they cross.
