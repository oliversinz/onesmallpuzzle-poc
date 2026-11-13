# One Small Puzzle — Comprehensive Project Concept

**Version:** 1.3 · November 13, 2026 (P1 accepted; 1.2: status after P1; 1.1: §16 revised after P0; 1.0: November 8, 2026)  
**Status:** P0 (API proof of concept) complete, see `p0/P0_REPORT.md`; P1 (core engine) complete for types 9 and 13, accepted by the operator on November 13, 2026, see `p1/P1_REPORT.md`  
**Planned primary domain:** `onesmallpuzzle.com` (confirm registration and final availability before launch)  
**Content language:** English · **Target audience:** Adults

> **Positioning:** “Original visual puzzles, numbers and logic. A little challenge for your day.”

## 1. Executive Summary

One Small Puzzle will be an independent, English-language puzzle product with a centralized AI-assisted editorial operation, human approval, a public puzzle archive, and automated distribution across six social media platforms.

The **Ubuntu Content Engine** will handle editorial planning, model-specific puzzle construction, image production, technical and editorial quality assurance, and persistent Editorial Memory. A private **dashboard** will support selection, review, revision, approval, and scheduling. The public **Astro website**, deployed on Vercel, will provide every approved puzzle at a permanent URL, with a solution that readers can choose to reveal. The **Outstand REST API** will handle cross-platform publishing to X, Threads, Instagram, Pinterest, Bluesky, and Facebook Pages.

**Guiding decision:** Puzzle quality is the core product; publishing software is reliable infrastructure. GPT and Claude will be assigned by puzzle type, without introducing an unnecessarily complex multi-agent system. The application will be developed primarily by **Claude Code using Claude Opus 5.5**, with an independent review by **Codex using GPT Astra**.

The architecture will support all six platforms from the outset. **Live channels will nevertheless be activated one at a time**, with separate acceptance testing for each.

## 2. Starting Point and Evidence from Testing

- The twelve existing ZIP packages, `1.zip` through `12.zip`, contain **120 complete 1080 × 1080 PNGs** and twelve `puzzle-results.md` files. The first five packages were produced with GPT; packages six through twelve were produced with Claude. These packages provide a basis for model routing and regression testing, **not an unreviewed pool of ready-to-publish content**.
- The qualitative evaluation so far found both models' editorial and visual output substantially better than the tested Grok Bot output. GPT was particularly strong in visual variety and types 2 and 4; Claude was particularly strong in logic/mathematics and types 6, 10, and 11. This is an internal project sample, not a general model benchmark.
- **Difficulty calibration** remains the most significant unresolved editorial weakness: GPT sometimes classifies very simple tasks as Easy; Claude shows outliers, particularly in types 8 and 12. The response will be explicit reference examples, independent checks, rejection rules, and feedback history.
- Type 13 (a detective scene with combined clues) **has not yet been integration-tested**. Its cross-model handoff will be validated in the first real API proof of concept.
- The previous ten-puzzle batches' distribution of 3 Easy / 4 Medium / 3 Hard was **part of the test design**, not a permanent publication quota.
- The variety found in the reference account `@AlexaBliz_` is a useful indication of potential format diversity, **not a template for copying individual third-party puzzles**. Originality is an editorial objective; worldwide novelty cannot be guaranteed.

## 3. Objectives, Product Principles, and Non-Goals

### Objectives

1. Continuously produce original, visually compelling, understandable, and correctly solvable puzzles for adults.
2. Establish a recognizable breadth of puzzle mechanisms and visual styles, with **no uniform puzzle-book look**.
3. Make editorial experience from approvals, rejections, mistakes, and difficulty feedback useful across many production cycles.
4. Provide a simple, efficient **final human approval** process, with full visibility into solutions, QA findings, and publication variants.
5. Make every published puzzle available on its own permanent web page with an accessible solution readers can reveal deliberately.
6. Reliably distribute a single canonical puzzle record to six social platforms, tracking status and assets separately for each network.
7. Capture quality, cost, and performance data so that routing, difficulty mix, and content selection can later be adjusted based on evidence.

### Non-goals for the initial version

No fully autonomous publishing without approval; no mandatory role for Grok Bot; no general-purpose agent framework; no user accounts, leaderboards, community features, standalone smartphone app, extensive CMS, video/Shorts pipeline, automated mass production of SEO articles, or automated comments or DMs directed at other accounts.

## 4. Audience, Brand, and Editorial Principles

- **Audience:** Adults interested in visual observation, numbers, geometry, and logical deduction. Do not assume specialist knowledge unless it is explained within the puzzle.
- **Tone:** Clear, idiomatic English questions that are friendly, precise, and intriguing, without exaggerated IQ claims or “99% fail” engagement bait.
- **Public asset:** The puzzle PNG contains the information needed to solve it, but **no answer, solution markings, or difficulty label**.
- **Visual identity:** At most a subtle, optionally recurring brand element. Subject, style, viewpoint, medium, and layout are chosen for each puzzle. A workshop scene can sit alongside a photographed-looking sheet of paper or a precise geometric diagram. Brand consistency should come primarily from quality and restrained identification, not a uniform card template.
- **Level of challenge:** Even Easy puzzles should offer adults a small moment of insight. Poor readability, tiny clues, and unnecessarily long routine work are not legitimate ways to increase difficulty.
- **Originality:** Compare each solving mechanism, visual concept, and decisive feature against the existing catalog. Do not directly reproduce puzzles from the reference account or other third parties.

## 5. Puzzle Catalog and Model Routing

Initially, routing will be an **editable configuration** derived from `one-small-puzzle-raetseltypen.md`, not an immutable product rule.

| No. | Puzzle type | Primary responsibility | Main rendering / verification method |
|---|---|---|---|
| 1 | Impossible state of an everyday object | **GPT** | Illustration/object depiction; functional and pixel-level checks |
| 2 | Illustrated observation and error spotting | **GPT** | Scene generation with precise clues; visual inspection |
| 3 | Counting overlapping shapes and object groups | **GPT** | Exact geometry/object inventory, optionally within an illustrated setting; enumeration |
| 4 | Reflection, rotation, and cube nets | **GPT** | Exact transformations, cube-net solver, visual inspection |
| 5 | Matchsticks, pencils, and other move puzzles | **GPT**; **Claude** optional for minimum/maximum problems | Explicit move rules; state-space/optimality checks |
| 6 | Area decomposition and geometric proof | **Claude** | Precise diagram and verifiable derivation |
| 7 | Numerical relationships, carries, and sums | **Claude** | Equation solving/brute force and consistent notation |
| 8 | Number machines, sequences, and symbol equations | **Claude** | Make rules transparent; explicitly eliminate ambiguity |
| 9 | Ordering, elimination, and statements | **Claude** | Constraint solver; test counterexamples |
| 10 | Switches, adjacency, and valid paths | **Claude** | State-space and path enumeration |
| 11 | Assembling pieces, reconciling views, proving a minimum | **Claude** | Exhaustive search/lower bound, exact views |
| 12 | Language, age, and everyday logic | **Claude**, subject to continued evaluation | Wording/timing constraints and alternative interpretations |
| 13 | Detective scene with combined clues | **Claude: clues/logic; GPT: scene** | Handoff contract; verify each visible clue; rule out alternatives |

**Model roles:** GPT Astra for visual/illustrative construction; Claude Opus for more complex deduction; a separate **OpenAI image model** for generative illustrations; Python/SVG for decisive, deterministic elements. The fact that GPT Astra can interpret images and invoke image tools **does not mean** the text model itself generates image pixels. Model names/IDs, reasoning effort, and image quality settings must remain configurable.

**Routing policy:** By default, use **one lead language model per puzzle**. Involve the second model only for an explicitly hybrid type, a concrete QA escalation, or a targeted A/B test. This keeps costs and failure paths manageable. Over time, approval rates and error categories by puzzle type/model can inform changes to the routing configuration.

## 6. Difficulty Model and Calibration

Four levels will be used internally and, when appropriate, displayed on the website:

- **Easy — accessible but clever:** A short, not entirely obvious insight. Not a children's puzzle or a mere look-up/spot-the-obvious task.
- **Medium — genuine reasoning:** At least one meaningful combination, elimination step, or spatial reinterpretation; not simply more visual decoration.
- **Hard — substantial reasoning:** Multi-step, surprising, or spatially demanding deduction supported by fair and fully visible evidence.
- **Very Hard — exceptional challenge:** Infrequent, especially demanding puzzles with a rigorously verified solution; never just longer arithmetic or barely visible details.

**Suggested initial mix, as a hypothesis:** Mostly Medium/Hard, a few genuinely good Easy puzzles, and occasional Very Hard puzzles (for example, 15% / 45% / 35% / 5%). This is not a rigid weekly quota; quality takes precedence over filling the calendar. The earlier 3/4/3 distribution will not automatically become the live-production standard.

**Difficulty gate:** The author model initially assigns and explains a difficulty rating. A separate review stage reassesses the **finished, unlabeled puzzle**, preferably without being anchored to the initial rating. The review considers the decisive insight, the number and dependency of reasoning steps, plausible wrong paths, permitted aids, and the fairness of the presentation. Obviously trivial candidates are rejected even if their illustrations are attractive. In case of disagreement, reclassify, revise with a specific objective, or reject the candidate.

**Calibration over time:** Store accepted and rejected reference cases for each type and difficulty level. Use human feedback and, later, optional website ratings as additional but nonrepresentative signals. Do not infer difficulty solely from comments, likes, or solving times. “Self-learning” means **versioned, controlled transfer of feedback**, not autonomous training of model weights.

## 7. Production Workflow — From Idea to Approval

1. **Planning:** Choose the type, target difficulty, and, where useful, subject matter based on the editorial mix, history, and available inventory. Allow manual production runs and scheduled batches; unattended daily production is not mandatory.
2. **Briefing:** Combine a shared production standard with the **type-specific paragraph** from the existing prompt approach, selected positive/negative Editorial Memory examples, and concrete rendering/QA rules.
3. **Construction:** The model generates a structured puzzle specification containing the public question, complete private solution, relevant geometry/scene facts, allowed transformations, answer format, and justified self-assessed difficulty.
4. **Internal preliminary checks:** Where applicable, verify mathematical/logical rules and answers programmatically before generating expensive images. Reject unsolvable or ambiguous candidates early.
5. **Image production:** Choose the appropriate method for the type: generative image, deterministic SVG/Python rendering, or a **hybrid** (illustrated background with precise clues/labels/objects overlaid deterministically). Do not entrust decisive counts, positions, or directions solely to the image model.
6. **Final image/content verification:** Inspect the actual PNG at 1080 px and 360 px; confirm that every intended clue appears in the final image; rule out unintended alternative solutions or extra errors. Vision review can help, but cannot guarantee exact pixel-level correctness.
7. **Editorial QA:** Assess uniqueness, suitability for adults, actual difficulty, mechanism diversity, originality, visual variety, X caption, and complete solution.
8. **Dashboard review:** Show the final image, caption, solution, QA findings, warnings, and platform previews together. Decision: approve, reject, request a specific correction, or generate a new variant.
9. **Immutable approved revision:** Freeze an approved revision. **Any materially relevant change requires renewed verification and approval.**
10. **Distribution:** Verify website publication first; then submit channel-specific post variants to Outstand, confirm publication status, and log the results.

**Standard artifacts per candidate:** Structured specification, source/intermediate graphics, final square PNG, optional portrait variant, exact X text, channel-specific captions, alt text, private answer and reasoning, difficulty rationale, QA report, provenance, and version metadata. The existing `puzzle-results.md` format remains available as an **exportable, human-readable view**, but is not the internal primary database.

## 8. Mandatory Quality Assurance

**Blocking criteria:** Missing or incorrect complete solution; numbers or objects in the final image that differ from the intended construction; contradictory rules; multiple valid answers despite a promise of uniqueness; missing visible clues; unreadable decisive details; an inadvertently revealed solution; or a demonstrable duplicate of an existing puzzle.

**Editorial rejection criteria:** Too trivial for adults; difficulty created only by poor readability rather than reasoning; overly similar mechanisms or visual themes; meaningless distractors; a boring or imprecise question; or an image that merely repeats a puzzle-book template.

**Verification tools as appropriate:** Arithmetic/constraint enumeration, cube rotations, graph paths, geometric shape counting, move search, optimization proof, and visual cross-checks. The solution must be verified **against the final image that will actually be published**, not merely against the intended construction. Automated image assessment can flag issues and provide supporting evidence; it is not a mathematical proof.

**QA status rules:** `PASS` (substantiated), `REVIEW_REQUIRED` (subjective/uncertain), `FAIL` (blocking). A convincing written verification report must not be presented as an actually executed solver run. Every check records the method and the specific artifact examined. Evidence requirements are especially strict for Very Hard puzzles.

**Regression testing:** Ingest the existing 120 test PNGs and their result files as a versioned reference corpus. Samples and known problematic cases become test fixtures for renderers, the difficulty gate, and prompt changes. They **must not automatically receive `approved` status**.

## 9. Editorial Memory — Real Learning Without a Black Box

The engine will store not just prompts but editorial experience that can inform future decisions:

- **Puzzle history:** Category, mechanism, central solving insight, visual style, difficulty, variants, and previously published subjects.
- **Error catalog:** What was wrong or weak? Why? For which type/model? Was the finding objective or subjective?
- **Correction decisions:** Rejected, corrected, rerouted, difficulty adjusted, or accepted after review, with rationale.
- **Reference examples:** Positive and negative examples of puzzle type, difficulty, clarity, and visual impact.
- **Version history:** Model ID, prompt/routing version, QA code version, image model, timestamp, token/image costs, and affected revision.

For each new task, retrieve **a small number of relevant** memories based on puzzle type and target difficulty; do not append an unlimited history of logs to every prompt. The system may propose new rules, but must not automatically activate them as binding policies without review. Compare versioned prompt/policy changes against regression tests.

**Measure of learning:** After an error type has been documented, do its repetitions and the number of corrections required decrease in later, comparable batches? An impressive-looking self-reflection statement is not sufficient evidence.

## 10. Dashboard — Central Editorial Workspace

The dashboard will be a **private, mobile-usable editorial application** running on Ubuntu, preferably accessed over Tailscale. It must be more than a log viewer.

| Section | Essential functions |
|---|---|
| **Overview** | Production progress, candidates awaiting review, approved puzzles, scheduled posts, failures, current costs |
| **Puzzle Library** | Thumbnail gallery with filters for type, model, difficulty, quality, and status; visual consistency/variety review across a series |
| **Puzzle Review** | Large PNG, 360 px preview, solution and QA side by side, revisions and exact provenance; approve/reject/request corrections |
| **Production** | Select type, count, target difficulty, model override; start/stop production runs; inspect errors |
| **Editorial Memory** | Historical rejections, reason codes, examples, feedback, approved rule versions |
| **Publishing Calendar** | Per-channel previews, date/time, editable captions, destination URL, approval, and individual post status |
| **Channels & Health** | Connected accounts, token/connection status, latest successes/failures, retries and pause controls by channel |
| **Analytics** | Publications, impressions/engagement where available, website visits, QA and cost trends |
| **Settings** | Model routing, prompt versions, rendering profiles, budget limits, channel feature flags, secure configuration |

Clicking “Approve” must approve **the exact revision displayed, including its platform variants**, not a version silently modified by a model afterward. Clicking “Retry” must never create duplicate posts without checking their status first. V1 does **not** require a sophisticated visual pixel editor: requesting a revision and reviewing the resulting new PNG is sufficient.

## 11. Public Website — `onesmallpuzzle.com`

**Stack:** Astro Static Site Generation, deployed through Vercel. The website is an independent, durable content channel and the preferred destination for Pinterest users seeking solutions.

**Initial pages and routes:**

- `/` — current/featured puzzles, entry points to categories and the archive.
- `/puzzles/` — filterable archive by type and difficulty.
- `/puzzles/[slug]/` — permanent puzzle page with image, question, optional hint, **expandable correct answer and understandable explanation**, plus relevant next puzzles.
- `/about/` and the required operator/legal and privacy pages.
- Category overview pages only when they provide genuine navigational value.

**Solutions:** By default, **do not reveal the answer immediately in the visible page content**. Let the reader expand an accessible “Reveal solution” section (e.g., semantic HTML `details`). The solution may exist in the static HTML; no separate login or live API is required. Social images, captions, and alt text must not inadvertently reveal the answer.

**SEO and operations:** Individual page titles and meta descriptions, canonical URLs, a sitemap, internal links, responsive images, good load times, meaningful image alt text, archive navigation, and structured data only where factually appropriate. Do **not** inflate the site with large volumes of thin, generated accompanying copy. Publish a puzzle's permanent URL before its corresponding Pinterest Pin, and verify that the URL responds correctly and shows the intended content.

**Data flow:** The approved canonical puzzle record is the single source of truth. An export/deploy step makes **only public information** available. Private QA findings, internal comments, credentials, and unapproved puzzles remain on Ubuntu. Public images need stable HTTPS URLs. For a growing collection of PNGs, one suitable object store/CDN (such as Vercel Blob or an S3-compatible service) may be preferable to committing every large image to Git indefinitely. Confirm the actual storage solution during the technical proof of concept.

## 12. Social Publishing via the Outstand REST API

**Six target channels configured from day one:** X, Threads, Instagram, Pinterest, Bluesky, and Facebook Pages. **Activate them sequentially** and perform a real test for each channel covering OAuth/account requirements, image variants, caption, URL, response status, and failure handling.

**Channel-specific variants:**

| Channel | Planned content |
|---|---|
| **X** | Original puzzle image + short question; depending on testing, link to the website preferably in the profile or selected posts |
| **Threads** | Image + brief, conversational caption; no automatic solution reply by default |
| **Instagram** | Image post with suitable composition (square or separate 4:5), caption, and profile reference; no blind cropping |
| **Pinterest** | Separate vertical Pin (typically about 2:3) + search-oriented title/description + **direct URL to the puzzle page** |
| **Bluesky** | Image, concise text and, when useful, website link; alt text |
| **Facebook Pages** | Image post to the Page, slightly adapted caption, optional website link |

**Important:** All six networks receive the same underlying puzzle, but not necessarily identical copy or crops. Portrait variants must be **recomposed**, not merely cropped. Do not adopt an automatic “solution comment four hours later” as the default. Solutions should primarily live on the website; social reply experiments require explicit approval and compliance with each platform's rules.

**Technical implementation:** Build a dedicated Outstand adapter with configurable API base URL and versioned request format. Maintain **a separate publication record for each channel**, even if Outstand offers a fan-out request. For every delivery, save the approved revision, account, caption, asset hash, scheduled time, website URL, request/idempotency key, provider ID, external post ID/URL, status, and errors. Provider acceptance of a request is **not confirmation that the post is live**. Reconcile status through the API and, if needed later, signed webhooks. No blind POST retries after timeouts. Prevent duplicates using local state checks and provider idempotency wherever available.

**Scheduling:** Show editorial dates/times in `Europe/Berlin` in the dashboard, but store unambiguous UTC timestamps internally. Schedule through the provider only after approval and successful website deployment. Make partial cross-channel failures visible. One channel must be pausable or reschedulable without resending posts already successfully published to other channels.

**Outstand note:** The official documentation covers posts, media, scheduling, and status/analytics functionality. At implementation time, recheck API base URLs, limits, platform restrictions, pricing, and idempotency windows against the actual Outstand environment in use. The planned integration uses the REST API, **not MCP or Grok Bot**.

## 13. Technical Architecture and Data Storage

**Pragmatic recommendation for a solo-operated system:**

- **Ubuntu backend:** Python, FastAPI, provider Python SDKs, type-specific validators/renderers, SQLite in WAL mode, and persistent local artifact storage.
- **Worker/scheduler:** One concurrency-limited background worker for production jobs; systemd services/timers. Redis, Celery, and Kubernetes are not mandatory. Adjust if future parallelism requires them.
- **Dashboard:** React/TypeScript with a simple, usable interface; private access over Tailscale (additional authentication if exposed publicly).
- **Public website:** Astro SSG on Vercel; deployments based on explicitly approved exports; publicly accessible optimized image assets.
- **Publishing:** Separate Outstand REST adapter; translate provider events and polling results cleanly into local statuses.
- **Repository:** A lean monorepo with clearly separated `backend`, `dashboard`, `site`, `contracts`, `tests`, and `docs` modules. Do not introduce a second authoritative puzzle database within the website.

**Core data-model entities:**

| Entity | Important fields |
|---|---|
| `Puzzle` | Immutable ID, type, language, current status, target difficulty, mechanism tag, slug |
| `PuzzleRevision` | Revision number, question, rules, private solution, caption, assessed difficulty, model/prompt ID, approval |
| `Artifact` | PNG/SVG/source, dimensions, hash, storage location, public/private status, role by channel |
| `ProductionJob` / `ModelRun` | Trigger, model, parameters, prompt version, cost/usage, runtime, result, error |
| `QAReport` | Verification method, artifact hash, evidence, uniqueness, difficulty, Pass/Review/Fail |
| `EditorialFeedback` | Issue type, severity, original finding, decision, corrective action, approved example |
| `PublicationPlan` | Approved PuzzleRevision, schedule, website URL, enabled channels |
| `ChannelPost` | Network, account, text/media version, provider ID, external URL, status, attempts |
| `MetricsSnapshot` | Source, channel, measurement timestamp, available raw metrics, association with post/puzzle |

**Keep state machines separate:** A puzzle revision may follow `candidate → qa_passed → in_review → approved → archived`, while each `ChannelPost` independently follows `draft → scheduled → submitted → published | failed | cancelled`. The website also has its own deployment/live status. Partial failure on one channel must not retroactively mark the puzzle revision as failed.

**Immutability and traceability:** Freeze approved revisions using hashes; any subsequent edits create a new revision. Prompt version, model, QA, and published PNG must be documented together in a reproducible manner. Do not execute model-generated code with unrestricted Ubuntu privileges without verification. Prefer declarative specifications and owned renderers; otherwise, use isolated execution with resource limits.

## 14. Security, Operations, and Cost Control

- **Secrets:** OpenAI, Anthropic, Outstand, and storage API keys must stay server-side; never expose them in the dashboard bundle, Git, or website exports. At minimum, apply restrictive file permissions and allow for future key rotation.
- **Access:** Use Tailscale for the dashboard and minimize public exposure. If Outstand webhooks are introduced, provide a separate authenticated HTTPS endpoint with signature verification and replay protection; alternatively, begin with limited status polling.
- **Backups:** Back up SQLite, private original puzzle files, and Editorial Memory consistently, including a recovery test. Keep public media reproducible from approved artifacts.
- **Resilience:** Jobs must resume safely after restarts, with timeouts, bounded retries, and intelligible error messages. Provider outages may delay publishing but must not delete approved puzzles.
- **Costs:** Track cost per model call, image variant, revision, rejected candidate, and **accepted/published puzzle**. Set configurable monthly limits, require manual approval for expensive batches, and alert on unusual spending.
- **Platform compliance:** Use authorized accounts and official API paths only. No unsolicited mass replies, scraping, or spam automation. Verify account prerequisites and posting limits when activating each platform.
- **Website legal/privacy requirements:** Prepare the legal notice and privacy policy for the actual operator circumstances; collect only necessary technical data and configure optional analytics/feedback with data minimization. Avoid unnecessary tracking and cookie complexity.

## 15. Feedback, Analytics, and Measurable Quality Improvement

The system separates **editorial quality** from **platform reach**.

**Editorial metrics:** QA pass rate by type/model, reasons for rejection, revision cycles, difficulty-rating discrepancies, repeated visual motifs, cost per approved puzzle, and regression failures.

**Distribution metrics:** Scheduled/successful/failed posts by channel, external URLs, available impressions, reactions, website referrals, and website visits. Do not combine metrics with different definitions across networks into a misleadingly precise universal score.

**Difficulty feedback:** Later, optionally collect voluntary reactions after a reader reveals the solution (`Too easy`, `About right`, `Too hard`), supplemented by occasional genuine blind tests. Responses are self-selected and must not dominate the editorial assessment on their own.

**Learning loop:** Periodically identify specific clusters of errors → curate a rule/reference example → compare it with existing test cases → approve it as a new policy version → check future batches for recurrence. Do not treat automatic self-praise as evidence of success.

## 16. Implementation Phases and Acceptance Criteria

**Primary implementer:** Claude Code / Claude Opus 5.5 Extra High on Ubuntu. **Independent review:** Codex / GPT Astra Extra High, preferably after each substantial completed milestone and again before launch. One accountable lead implementer; no simultaneous edits to the same working state.

| Phase | Deliverable | Acceptance criterion |
|---|---|---|
| **P0 — API Proof of Concept** | GPT Astra/Claude Opus calls, image API, renderer, real puzzle artifact, hybrid type-13 test | Actual, inspectable artifacts via each API; type-13 clues match the final PNG; costs/timing known. **Met on November 13, 2026** (`p0/P0_REPORT.md`) |
| **P1 — Core Engine with Required QA** | Data model, job orchestration, type routing, type briefs (the §19 type paragraphs plus a new type-13 paragraph), production artifacts, structured solution, type-specific validators and final-PNG checks for each enabled type, cost logging per model call with an enforced budget cap | For each enabled type, candidates pass that type's required checks on the final PNG, and a candidate that fails one cannot reach approval; persistent state; defined error reporting; spending stops at the configured cap. Reproducible run: every run records its inputs, prompts, model IDs, parameters and outputs and can resume from stored stages (model output itself is not deterministic). **Met for types 9 and 13 on November 13, 2026; accepted by the operator the same day** (`p1/P1_REPORT.md`) |
| **P2 — Editorial Quality and Memory** | Difficulty gate, Editorial Memory, regression corpus from the 120 test puzzles, feedback/routing versions, recomposed portrait variants (at least for Pinterest) with their own final-image check | Overly trivial candidates cannot pass to approval without the difficulty gate; changes traceable; for each enabled type, the operator has reviewed a batch, including thumbnails side by side, with approvals and rejection reasons recorded |
| **P3 — Dashboard** | Library, review, approval, settings | Human can work from finished candidate through approval; no unintended live action |
| **P4 — Website** | Astro archive, puzzle pages, reveal solution, images/SEO, deployment, backup of SQLite, private originals and Editorial Memory | Approved record appears at stable public URL; private solution appears only in the intended reveal section of the page, not in social assets; a restore from backup has been tested before the first public deploy |
| **P5 — Outstand, Six Channels** | Adapter, variants, publishing calendar, scheduling, statuses, health, retry | Separate confirmed end-to-end test for each channel, isolated failure handling, no duplicate posts; **staged activation** |
| **P6 — Production Hardening** | Security and monthly cost limits, tests, audit, operations guide | Restart/recovery test, monthly budget, audit log, Claude Code sign-off and Codex review complete |

**Type enablement:** All 13 types remain the target, but they are enabled one at a time. A type enters the routing configuration once it has its brief and validator and meets the P1 criterion; the P2 criterion then applies to it. Later phases do not wait for all 13 types.

These phases are **technical development and acceptance milestones**, not a rationale for indefinitely deferring four channels or the website. The initial application should cover the entire agreed target architecture. A small P0 test ensures that differences between Chat/Work tests and actual API use are discovered early rather than late.

**Final launch definition:** A real, human-approved adult puzzle has been produced with a traceable solution and QA; appears correctly on `onesmallpuzzle.com`; is configured for all six networks; and has been successfully published on every activated channel, with separate status/error records and no accidental solution disclosure. Inactive channels remain prepared and testable.

## 17. Risks and Deliberate Boundaries

| Risk | Mitigation |
|---|---|
| Chat/Work results cannot be reproduced exactly through APIs | Real API PoC before full implementation; configurable model/image model versions |
| LLM rates its own puzzle too favorably | Separate difficulty gate, specific negative examples, independent reviewers, and human approval |
| Generative image changes decisive details | Precise overlay elements, final-image checks, and type-specific validators |
| Uniqueness is not actually established despite a plausible explanation | Solver/enumeration/counterexamples or explicit rejection |
| Feed reverts to a puzzle-book appearance | Per-post art direction, thumbnail gallery, visual repetition checks |
| Platform accepts a request but does not publish the post | Reconcile per-channel status through Outstand; isolate partial failures |
| Website inadvertently includes private clues or is not live when Pin is published | Explicit public export, approval/deployment gate, URL check |
| Correction loops cause costs to rise | Maximum attempts, budget caps, measure cost per accepted puzzle |
| “Self-learning” is merely written commentary | Demonstrable, versioned feedback transfer and comparison of subsequent error rates |

## 18. Decisions Already Made and Remaining Operational Checks

**Agreed:** English-language puzzles for adults; 13 categories; GPT/Claude routing; Very Hard as a rare fourth level; visual variety rather than a uniform design; Ubuntu Python engine with a human review dashboard; Astro/Vercel website with solutions; six social channels via Outstand REST; staged channel activation; no required Grok Bot role; Claude Code as primary implementer and Codex as independent reviewer.

**Verify before activation without holding up the project concept:** Register the domain; enable specific API accounts/quotas/model access; test the Outstand account and actual endpoints; meet Instagram/Facebook/Pinterest account prerequisites; choose public media storage; configure the initial posting frequency and budget caps in the dashboard; finalize operator/legal notice and privacy text.

## 19. Project Sources and Technical References

**Internal sources:**

- `one-small-puzzle-raetseltypen.md` — thirteen puzzle types, rationale for model routing, visual strategy.
- `one-small-puzzle-production-prompt.txt` — controlled single-type test standard (only the “Puzzle type” section varies).
- `one-small-puzzle-prompt-types.txt` — the “Puzzle type” paragraphs for types 1–12 used with that standard. The type-13 paragraph was written and approved in P1; the single-puzzle briefs in use are in `backend/prompts.py`.
- `1.zip` through `12.zip` — 120 PNGs and twelve result files containing captions, solutions, and verification explanations.
- Project discussions “Puzzle Test Evaluation” and the initial GPT/Claude/Grok comparisons — qualitative assessments and known weaknesses in difficulty calibration.

**Public technical documentation (current as of the concept date; recheck before implementation):**

- OpenAI GPT Astra API: https://developers.openai.com/api/docs/models/gpt-6-astra
- OpenAI Image API: https://developers.openai.com/api/docs/guides/image-generation
- Anthropic model lifecycle: https://platform.claude.com/docs/en/about-claude/model-deprecations
- Outstand API / Create a post: https://www.outstand.so/docs/create-a-post
- Outstand publishing architecture: https://www.outstand.so/docs/architecture

---

**Implementation guiding principle:** *One verifiable, original puzzle for adults, with an excellent visual presentation appropriate to its type, is worth more than ten mediocre puzzles published automatically. The software should make that quality decision visible, repeatable, and operationally reliable.*
