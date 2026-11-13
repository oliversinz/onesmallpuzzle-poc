# One Small Puzzle — Attended Multi-Model PoC: Final Report

**Date:** 13 November 2026 · **Branch:** `poc/attended-multimodel` · **Orchestrator:** Claude Code 2.1.323, model `claude-opus-5-5` · **Specialist:** Codex CLI 0.169.0 · **Images:** OpenAI Images API

## Recommendation: **CONDITIONAL PASS**

The attended architecture works. Claude Code invoked the real Codex CLI 14 times as a subprocess. The model, `gpt-6-astra`, is confirmed from Codex's own session records. The Codex calls used the ChatGPT login, with no text-model API key. Two paid image requests produced usable assets, and every artifact can be inspected and reproduced. Two things fell short:

- **None of the three puzzles reached its target difficulty with confidence.** A: Easy against a Medium/Hard target. B: borderline Hard. C: Easy–Medium against a Hard target.
- **Two of the three needed QA-driven correction loops.** Each loop caught a real uniqueness defect that would otherwise have shipped.

The corrections required before building the dashboard are listed under question 10.

| Test | Lead | Logic & uniqueness | Final visible evidence | Difficulty vs target | Status |
|---|---|---|---|---|---|
| A · Type 2 "The Workshop Cabinet" | Codex | PASS after 1 revision | PASS | **Easy** (target Medium/Hard) | CONDITIONAL |
| B · Type 10 "Lights out" | Claude | PASS, solver-proven | PASS, pixel read-back | Hard (lower end) vs Medium (blind) | PASS, difficulty REVIEW_REQUIRED |
| C · Type 13 "A Crunch in the Snow" | Claude logic, Codex scene | PASS, joint-history enumeration on decoded evidence | PASS after 3 correction loops | **Easy–Medium** (target Hard) | CONDITIONAL |

Evidence classes used throughout: **programmatic** (solver, enumeration, SVG structure, pixel read-back), **model-based** (Claude's inspection, Codex blind solves), **human inspection required** (publication taste, real difficulty). No human playtesting took place.

---

## Environment verification (performed first)

| Item | Finding |
|---|---|
| OS / tools | Ubuntu, Linux 6.8. Python 3.12.3. Project venv `.venv` (uv) with Pillow 13.0.0, NumPy 2.5.4, CairoSVG 2.9.1 and requests 2.34.2. No ImageMagick, Inkscape or Tesseract (no OCR). |
| Claude Code | 2.1.323; orchestrator model `claude-opus-5-5`. |
| Codex CLI | 0.169.0. `codex login status` → *Logged in using ChatGPT*. `~/.codex/config.toml` default `model = "gpt-6-astra"`, `model_reasoning_effort = "xhigh"`. `codex exec --help` checked: `-s read-only`, `--json`, `--output-schema`, `-o`, `-i`, `-C`, prompt via stdin. Smoke test passed. |
| Images API | `OPENAI_API_KEY` read from `.env` (mode 600); never printed or logged. A free `GET /v1/models` listed `gpt-image-2`, `gpt-image-2.5-{flare,sunburst}` and `gpt-image-2.6-{flare,sunburst}`. Chosen: **`gpt-image-2.6-flare`** (current; the docs describe flare as "fast, high-quality" generation), quality `high`. |
| References | Production prompt, Type 1–12 paragraphs, German type/routing notes, project concept, and `1.zip`–`12.zip` (zip N = type N; 120 PNGs). No Type 13 package exists. The approved Type 13 paragraph (`backend/prompts.py`, per concept §19) is **not in this workspace**, so Claude wrote one from the Type 13 routing row (`test-c/brief.md`). |
| **Security finding** | `.env` with the API key was **committed in the original initial commit** because the ignore file was misspelled `.gitgnore`. Fixed: renamed to `.gitignore` (which also ignores `.venv/` and the reference zips) and `.env` untracked. **History purged at the operator's request:** `git filter-branch` removed `.env` from every commit (all commit IDs changed), then the backup refs, `ORIG_HEAD` and reflog were dropped and `git gc --prune=now` was run. Verified afterwards: the `.env` blob is gone, no commit contains a `.env` path, and a scan of all 128 objects in `.git` finds the key 0 times. No git remote was ever configured. Rotating the key remains advisable because it sat in a committed file. |

## Pipeline as built (all files in this repo)

- `tools/codex_call.py`: runs `codex exec -s read-only -C <dir> --json -o <out> [--output-schema] [-i image] -` as a subprocess. It saves the JSONL events and reads the **model, effort, sandbox and approval policy from Codex's own session record** (`~/.codex/sessions/.../rollout-<thread>.jsonl`). It scans the outputs for the API key and appends one record per call to `logs/codex-execution.log`.
- `tools/gen_image.py`: one `POST /v1/images/generations` request, with no automatic retry. It records usage in `logs/image-api-usage.json` and **refuses a third request** unless `--allow-extra` is passed.
- `tools/render_svg.py`: CairoSVG → 1080×1080 PNG plus a 360 px preview. `tools/crops.py` and `tools/contact_sheet.py` support visual QA.
- Per test: brief → Codex calls (structured JSON via `--output-schema`) → image → SVG composition → Claude QA → targeted revision → blind solve by a fresh Codex session that sees only the PNG.

---

## 1. Did Claude successfully invoke and receive results from the real Codex CLI?

**Yes.** There were **14 real `codex exec` subprocess calls**, all exiting 0 with schema-valid JSON:
- **1 smoke test**, run directly from the shell before the wrapper existed; its log was not kept, but its Codex session record (thread `01a1d50c…`) confirms it.
- **13 logged calls** in `logs/codex-execution.log`, with each JSONL event stream in `logs/codex-<label>-events.jsonl`:
  - **Construction and scene:** a1, c1.
  - **Composition:** a2, c2.
  - **QA-driven revisions:** a3, c3, c4, c5.
  - **Blind solves of final images:** a-blind, b-blind, and three for C. Their labels are c-blind, c-blind-final (despite its name, this was the second of three) and c-blind-v4.

Claude sent the prompts on stdin and attached images with `-i`. It received structured results through `--output-schema` and `-o`, and acted on them: it sent Codex's image prompts verbatim to the Images API and rendered Codex's SVGs. Codex also sent results Claude did not ask for: it critiqued Claude's Type 13 handoff and found three real weaknesses. That is evidence of actual delegation, not role-play.

## 2. Which model and authentication method were actually used for Codex?

**`gpt-6-astra`, reasoning effort `xhigh`, provider `openai`, originator `codex_exec`, CLI 0.169.0. Authentication: ChatGPT login** (no OpenAI API key involved). The model comes from `turn_context.model` in each call's Codex session record, not from the config file or the model's self-report. Codex's `--json` event stream does **not** include the model name, so the session record has to be read. Every call ran with sandbox `read-only` and approval policy `never`. "GPT Astra" in the project concept corresponds to this confirmed model ID.

## 3. Did the OpenAI Images API produce actual usable assets?

**Yes: 2 of 2 requests, both used.** Both were `gpt-image-2.6-flare`, quality `high`, 1088×1088 requested and returned, HTTP 200, taking 9.2 s and 10.5 s. The originals are saved separately as `test-a/source-image.png` and `test-c/source-image.png`. Neither contained the forbidden content (vehicles, hardware, text, people). Small departures from the prompts: in Test A the floor took about 19% of the frame instead of 12%; in Test C the viewpoint came out flatter than requested.

**Both times, Codex chose to use the generated image only as the setting.** It drew every solution-critical element deterministically in SVG, as the concept requires (§7.5). The generative model therefore supplied atmosphere, not evidence. That is the robust pattern, but the pictures read as vector diagrams laid over a painted backdrop (see question 8).

## 4. Did all three puzzles pass logical and visual QA?

**No, not without qualification.**

- **A:** Correct and unique only **after** Claude's QA found that the handle-less bottom rail could pass for a fifth drawer, which would make C a second answer. Codex fixed it in revision a3 by painting the whole frame one colour. Visual evidence passes. **Difficulty fails the target:** the blind solver solved it in 52 s and rated it Easy, against a target of Medium or Hard.
- **B:** Passes every verifiable check. A BFS minimum of 13 and an independently written exhaustive search agree, and the counting lower bound is tight. The pixel read-back decodes every light and doorway from the PNG and re-solves to 13. The answer stays 13 under the blind solver's alternative back-door reading. Difficulty is borderline: Claude rates it Hard (lower end), the blind solver Medium.
- **C:** Logic and uniqueness pass. `verify_logic.py` v2 enumerates joint movement histories of all four cars: bay 5 is the only possible culprit, both on the intended evidence and on the evidence decoded from the final SVG and pixels. The final blind solve found no defensible alternative. The visual evidence passes after **three correction loops** (question 5). **Difficulty fails the target:** blind solves rated it Easy, Medium and Easy across versions, and Codex rated it Medium, against a Hard target.

## 5. Did the Type 13 cross-model handoff preserve every required clue?

**Every clue arrived, but not every clue's *meaning* arrived. It took three correction loops to get an unambiguous final image.**

All 13 clue ids (F1–F3, C1–C10) appear in the final PNG with the required state. `test-c/check_evidence.py` verifies this from the SVG structure and the rendered pixels, then re-runs the logic on what is actually drawn. Recorded handoff failures, in order:

1. **Codex → Claude (useful):** Codex's review of handoff v1 found that the track rule allowed a retracing loophole, that Claude's logic checker ignored car swaps, and that the difficulty claim was optimistic. Claude fixed the first two in handoff v2.
2. **Composition placement failure (Codex):** the lamp that the handoff placed "just inside the entrance" was drawn deep in the yard. This created a competing "whose tracks touch the post?" reading. Codex's own clue-location note described the placement as correct. Claude's QA caught it, and Codex fixed it in c3.
3. **Clue meaning lost (handoff design, Claude):** "an obvious yellow paint scrape" was drawn as a star burst. Claude's colour and position checks passed it, but a blind solver read it as an impact symbol, which makes bay 2 defensible. Fixed by stating the paint in public text (handoff v3, c4).
4. **Wording gap (Claude):** the rule did not say that the tracks are visible, so a hidden-track story for bay 1 was arguable. Fixed in handoff v4 and c5.

Lesson: a handoff has to carry each clue's *meaning* as public text whenever the drawing alone may not convey it. A blind solve of the final image is the check that catches this.

## 6. What manual intervention was required?

**No human intervention during the run.** The prerequisites already existed: Codex was logged in with ChatGPT and the API key was in `.env`. The operator added `references/` once, mid-session, at their own initiative. All corrections came from the orchestrator (Claude) as part of the designed QA loop. No SVG authored by Codex was edited by hand. Claude changed only its own artifacts: briefs, handoff and fact wording, solvers, and the Test B renderer.

- **A:** One revision request to Codex (a3) to separate the frame from the drawers.
- **B (Claude's own work):** "Corridor" renamed "Office", door swings moved off the labels, text enlarged, and walls thickened after the blind solve.
- **C:** handoff v2 after Codex's review; three revision requests to Codex (c3: lamp/entrance; c4: paint smear; c5: visibility wording and fact-block spacing); handoff v3 (paint stated in F2) and v4 (tracks "all still visible").

## 7. What API usage or costs were recorded?

- **Images API (metered):** 2 requests. Input was 341 + 455 text tokens; output was 1,836 + 1,836 image tokens (`logs/image-api-usage.json`). The fetched pricing page lists gpt-image-2.6 at $30 per million image output tokens, which gives **about $0.11 for the two images.** Text input adds well under $0.01, at the $5 per million rate the same page lists for gpt-image-2.5. This is an estimate from published rates; the billing dashboard was not checked.
- **Codex:** no metered API cost; usage counts against the ChatGPT plan. Logged calls: 1,876,853 input tokens (1,496,448 of them cached), 144,323 output tokens (80,649 of them reasoning). The smoke test added about 16k input tokens. Summed Codex runtime was 5,076 s (about 85 min), with some calls running in parallel.
- **Claude Code:** this attended session under the operator's Claude plan; not metered per call here.
- **No retries or extra variants were made.** `gen_image.py` enforces the two-request cap.

## 8. How does the quality compare with the earlier One Small Puzzle reference examples?

Compared side by side (`logs/contact-sheet.png` against the contact sheets of `2.zip` and `10.zip`):

- **B is at reference level.** It is as polished as the best Type 10 references ("Shy Buttons", "Mow It Once"), with a mechanism none of the ten uses: walking itself toggles the lights. Its verification goes further than the reference result file: two independent solvers, a tight proof, and a pixel read-back with re-solve.
- **A is below reference level on difficulty and roughly level on visuals.** GPT's Type 2 package has stronger Medium/Hard entries ("Harbour Press", "One Crate Short"). The cabinet idea is clean but familiar (a lock that fastens nothing to anything fixed), and making it unambiguous made it easy.
- **C is the richest scene of the three** and was QA'd the most heavily (13-clue inventory, joint-history logic, structural and pixel evidence check, three blind solves). Its puzzle still plays Easy to Medium, and the long fact block is heavier than any reference image.
- **Variety:** the three posts look clearly different from each other (warm front-on workshop, dark top-down plan, lilac winter scene). Both Codex scenes use the same recipe, though: a painterly generated backdrop with flat vector evidence on top. That style should be checked across more posts before it becomes a house look.
- **Calibration:** the concept's known weakness reproduced. The author model's rating was at or above the reviewer's and blind solver's in all three tests.

## 9. Can the workflow be reproduced in a normal attended Claude Code session without a separate LLM API?

**Yes.** Codex ran entirely through the ChatGPT-authenticated CLI, and Claude is the session itself. The only API key used was the Images API key, kept separate in `.env`. The steps to reproduce are scripted (`tools/*.py`), and every prompt, schema, Codex output, image prompt, SVG, solver and check is committed. Model output is not deterministic, so re-running the Codex calls will give different puzzles. The stored outputs let every downstream step be replayed and inspected.

Practical costs: **Codex at xhigh effort took 5–17 minutes per construction or composition call** (52–322 s for blind solves). The whole run took about 1 h 45 min from environment check (14:05) to final verification (15:48), mostly waiting on Codex.

## 10. What technical changes are required before implementing the full Ubuntu dashboard?

Required (each traced to a concrete finding in this PoC):
1. **Rotate the OpenAI key** (it was committed before the history purge) and keep `.gitignore` correct. (Security finding above.)
2. **Read the Codex model from the session record**, not from the event stream or config. The provenance record should store the thread id and rollout path. (Question 2.)
3. **Return the actual render to Codex.** CairoSVG wasn't available in Codex's sandbox: Codex worked blind in a1–a3 and fell back to librsvg previews in c2–c5. Neither renders exactly like the final CairoSVG output. A render step whose output goes back to Codex removes a class of defects that Claude had to catch. (A3, C3.)
4. **Make a difficulty gate mandatory before approval.** It should rely on a blind solve plus a reviewer, never on the author model's own rating. (All three tests.)
5. **Make a blind solve by a fresh session a standard QA step for Type 2 and Type 13.** It found the decisive paint/burst ambiguity in C that Claude's clue-by-clue review, including its pixel colour check, had passed. (Test C.)
6. **Clue inventories must state the meaning of each visual clue in public text when the drawing alone may not carry it.** "Yellow mark" ≠ "paint". (Test C, handoff v3.)
7. **Logic checks for Type 13 must model joint histories**, as in `verify_logic.py` v2. Per-object checks missed swap scenarios. (Codex's review of Claude's handoff.)

Recommended, not blocking: use a lower Codex effort (`high`) for revision and blind-solve calls to cut latency; keep the two-request image budget guard as the default.

Not currently relevant: no change to the website, publishing or scheduler plans was indicated by this PoC.

---

### Artifact index

```
test-a/  puzzle.png  source-image.png  puzzle.json  solution.md  qa-report.md
         brief.md  codex-a{1,2,3}-prompt.md  codex-a{1,2,3}.json  image-prompt.txt  compose.svg  qa/
test-b/  puzzle.png  puzzle.json  solution.md  qa-report.md
         instance.json  solver.py  verification.json  render.py  puzzle.svg  layout.json  check_pixels.py  qa/
test-c/  puzzle.png  source-image.png  handoff.json  puzzle.json  solution.md  qa-report.md
         brief.md  verify_logic.py  logic-verification.json  check_evidence.py  codex-c{1..5}-prompt.md
         codex-c{1..5}.json  image-prompt.txt  compose.svg  qa-boxes.json  qa/
logs/    codex-execution.log  image-api-usage.json  codex-*-events.jsonl  contact-sheet.png
tools/   codex_call.py  gen_image.py  render_svg.py  crops.py  contact_sheet.py  schema-*.json  blind-solve-prompt.md
```
