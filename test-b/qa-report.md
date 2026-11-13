# Test B — QA report ("Lights out", Type 10, Claude-led control case)

**Overall: PASS on every verifiable criterion; difficulty REVIEW_REQUIRED** (Claude: Hard, lower end; blind solver: Medium). The logic and rendered evidence are verified programmatically. Difficulty and originality are model-based judgements, and no human test took place.

Status key: `PASS` substantiated · `REVIEW_REQUIRED` subjective/uncertain · `FAIL` blocking. The evidence class for each check is given as **[P]** programmatic, **[M]** model-based assessment, or **[H]** needs human inspection.

| # | Check | Method and artifact examined | Result |
|---|---|---|---|
| 1 | Correct, complete solution | [P] `solver.py` BFS on `instance.json`: minimum 13, route replayed light by light | PASS |
| 2 | Uniqueness of the promised value | [P] The minimum is a single number by definition. An independent DFS of every walk up to 13 found no shorter success. Only 2 shortest routes exist (loop direction), so any reader route can be checked | PASS |
| 3 | Minimum proven | [P] Counting lower bound computed from the graph = 13 = BFS minimum. The human-readable proof is in `solution.md` | PASS |
| 4 | Logical consistency of the rules | [M] Rules state the flip-on-entry behaviour, that stepping out does nothing, free reuse, the start room, the exit and the end condition, and what counts (inside doorways, not the back door). Start-room and end-room behaviour follow from the stated rules | PASS |
| 5 | Final image matches the construction | [P] `check_pixels.py` on the final `puzzle.png` (re-run after the wall fix): 9/9 light states (luminance lit ≥ 198, dark ≤ 59), 9/9 doorways, no false doorways, exactly one exterior opening (east, back door). The decoded instance re-solves to 13 | PASS |
| 6 | Visible text matches the intended rules | [M] Text is drawn from literal strings in `render.py` and read back visually at full size. No OCR engine is installed, so there is no programmatic text check | PASS |
| 7 | Readability at 1080 px | [M] All labels, rules and the question are legible. Doorways read as wooden thresholds with door swings, and lit/dark is double-coded (floor colour + bulb icon) | PASS |
| 8 | Readability at 360 px | [M] `qa/puzzle-360.png`: light states, doorways, the YOU token and the back-door arrow are clear. Rules text is about 10 px tall and room names about 8 px: readable but small, comparable to the reference set | PASS (small text noted) |
| 9 | No answer leakage | [M] The image shows no route, counts or highlights, and the caption gives no number or insight | PASS |
| 10 | Composition / variety | [M] A night-time top-down cutaway with a lawn and window light. It differs in medium and palette from Test A (front-on illustrated cabinet). The Test C comparison is on the contact sheet (`logs/contact-sheet.png`) | PASS |
| 11 | Difficulty | [M] Claude: **Hard (lower end)**. It needs the entry-parity insight, the start-room and end-room traps, unavoidable dark rooms costing two entries, a forced order, and a proof of the minimum. Blind solver: **Medium** (but it needed 322 s at xhigh effort, against 52 s for Test A). The Hard target is plausible but unconfirmed | REVIEW_REQUIRED (borderline; needs a human test) |
| 12 | Originality vs. local references | [M] Compared with all ten Type 10 reference puzzles (`references/10.zip`): toggles there are panel switches (02, 04, 08) and routes are pure path constraints (03, 06, 07, 10). None makes movement itself the switch. "Walking into a room flips its light" is a known general puzzle mechanic, and the instance and art are original. Worldwide novelty cannot be guaranteed | PASS |

## Independent blind solve (model-based)

A fresh Codex session (`gpt-6-astra`, xhigh) received only `puzzle.png` (before the wall-thickness fix), read no files, ran 0 shell commands, and took 322 s (`qa/blind-solve-codex.json`, `logs/codex-b-blind-events.jsonl`).

- **Answer: 13, correct.** It found both shortest routes and gave the same lower-bound argument (5 lit rooms × 1 + 4 unavoidable dark rooms × 2).
- **Difficulty: Medium.** "Once noticed, both the route and its optimality are straightforward."
- **Issues raised and how they were handled:**
  1. *"Hall–Bedroom lacks a prominent solid wall"*: interior walls were thickened from 12 px to 16 px and exterior walls from 20 px to 22 px; re-rendered; pixel check re-run (PASS).
  2. *"The wording doesn't prohibit leaving and re-entering through the back door mid-route"*: modelled exactly in `solver.py` (`minimum_if_backdoor_reentry_allowed`), where back-door trips are free but flip the Boot room. The minimum is still 13, so the answer holds under either reading. No wording change was needed.
  3. *Small rules text and thin door leaves at phone width*: noted. The leaves are decorative (the doorway is the threshold gap, which the pixel check confirms), and the rules text is already enlarged to 30 px.

## Notes

- No generative image was used. This is the editorially appropriate choice: every decisive element (lights, doorways, start and exit) must be exact, and the night-garden setting is easy to draw.
- Changes during production: "Corridor" became "Office" (avoiding an "is a corridor a room?" dispute and a Study/Studio name clash). Door swings were re-sided so they don't cover labels. The dining table was moved off the wall and the rules text enlarged for 360 px.
