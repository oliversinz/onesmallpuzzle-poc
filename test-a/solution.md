# Test A — "The Workshop Cabinet" (private solution)

**Type 2:** Illustrated observation and error spotting · **Target:** Medium or Hard (Codex chose Medium) · **Puzzle constructed and art-directed by:** Codex CLI (`gpt-6-astra`, xhigh) · **Background illustration:** OpenAI Images API (`gpt-image-2.6-flare`, high) · **Final composition:** SVG authored by Codex, rendered by Claude Code with CairoSVG · **Independent QA:** Claude Code (claude-opus-5-5).

## Public post

- **Image:** `test-a/puzzle.png`
- **On the image:** "Which padlock isn't keeping things shut?" and "Drawers slide straight out; only the locks hold them shut. No unlocking, damage or dismantling. The frame is fixed."
- **X caption (Codex):** A, B or C? Name the padlock that isn't doing its job—and explain why.

## Answer

**Padlock B.** Its hasp joins drawer 2 to drawer 3, two moving parts, and neither end is anchored to the fixed frame. Pull the two middle drawers out together and nothing in B's hasp or padlock has to move relative to anything else, so B does not keep them shut.

## Explanation (how a reader gets there)

1. Each lock is a hasp. A hinged strap is screwed to one surface, its slot fits over a staple screwed to the other surface, and the padlock through the staple stops the strap lifting off. A hasp holds two parts in place *relative to each other*.
2. Trace both mounting plates of each hasp:
   - **A:** the hinge plate is on the fixed top of the olive frame, and the staple and padlock are on drawer 1. Drawer 1 cannot slide away from the frame.
   - **C:** the hinge plate is on drawer 4, and the staple and padlock are on the fixed bottom of the frame. Drawer 4 cannot slide.
   - **B:** the hinge plate is on drawer 2 and the staple and padlock are on drawer 3. Neither touches the frame.
3. B stops either middle drawer from opening on its own, which is why it looks effective. But the two drawers can slide out *together*, and pulling one handle drags the other along. B is the padlock that isn't doing its job.

## Competing answers checked

| Candidate | Why it fails |
|---|---|
| A | Its hinge plate sits on the continuous olive frame (the rules say the frame is fixed). Opening drawer 1 would have to separate the strap from its anchor, and the closed padlock prevents that. |
| C | Same logic with the frame at the bottom. In the first render the bottom rail was oak-coloured and could pass for a fifth, handle-less drawer, which would have made C a second answer. After Claude's QA, Codex repainted the whole frame one continuous colour (see `qa-report.md`). |
| "Unscrew the hasp" / "cut the shackle" | Excluded on the image: "No unlocking, damage or dismantling." |
| "A hinged strap can swing out, so A and C also fail" | The strap end is held by the staple at a fixed height on the moving part. Swinging forward would need the end to rise along an arc around the hinge, which the staple prevents (beyond a few millimetres of slot play). This is how hasps on drawers work. Claude judged this objection weak but listed it as one a pedantic reader might raise. |
| "B keeps drawers 2 and 3 shut against each other" | The question asks what keeps things shut. Both drawers still open. |

## Editorial notes

- **Decisive step:** asking what each lock is actually attached to, then imagining the two middle drawers moving as one.
- **Difficulty:** Codex assessed Medium. Claude's independent assessment is **Medium (lower end)**. The insight is a genuine reframing, but once the reader asks "attached to what?", the colour difference between frame and drawers (added for uniqueness) makes the check quick. See the blind solve in `qa-report.md`.
- **What to check in the finished image:** four drawer fronts and one continuous frame; every mounting plate wholly on one surface; three identical, visibly closed hasps; labels A/B/C; no highlight on B.
