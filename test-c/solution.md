# Test C — "A Crunch in the Snow" (private solution)

**Type 13:** Detective scene with multiple interacting clues · **Target:** Hard
**Case, answer, clue inventory, alternatives and logic check:** Claude Code (claude-opus-5-5)
**Scene, image prompt, art direction, title, caption and final composition:** Codex CLI (`gpt-6-astra`, xhigh)
**Backdrop illustration:** OpenAI Images API (`gpt-image-2.6-flare`, high) · **QA:** Claude Code

## Public post

- **Image:** `test-c/puzzle.png`
- **X caption (Codex):** Which bay holds the car that clipped the lamp post? Reply with the bay number and the clues that rule out the others.

## Answer

**Bay 5**, the yellow car with snow on its roof and softened tyre tracks.

## How the clues combine

1. **Paint.** The car left a smear of its paint on the lamp post (stated in the facts), and the smear is yellow. The culprit is one of the yellow cars in bays 1, 4 or 5; the car in bay 2 is red.
2. **Timing.** The crunch came at 2 am, while it was snowing, and the car is still here. So it was driving at 2 am, and that drive left its own pair of tracks, softened by the snow that fell afterwards.
3. **Bay 1:** snow on the roof and no tracks at all. It was parked before 1 am and never moved. A 2 am drive would have left a softened pair.
4. **Bay 4:** a clear roof and sharp tracks, so it arrived after 3 am. It is the most suspicious-looking car, but could it have hit the post at 2 am, left, and come back after the snow? That 2 am departure would have left its own softened pair, and the only softened pairs belong to bays 2 and 5. Could it have started in bay 5 and left at 2 am along bay 5's softened pair? Then the car now in bay 5 would have needed a second pair to arrive, and there is only one. So bay 4 was not here at 2 am.
5. **Bay 5:** softened tracks, so it drove in while it was snowing. It is the only yellow car that can have been driving at 2 am. **Answer: bay 5.**
6. **Bay 2** also drove in during the snowfall, but it is red, so the paint rules it out.

Neither clue is enough on its own. Paint alone leaves bays 1, 4 and 5; tracks alone leave bays 2 and 5.

## Strongest wrong answers

| Answer | Why tempting | Why wrong |
|---|---|---|
| Bay 4 | Yellow, the only clear roof and the freshest tracks: it "looks guilty" | Sharp tracks mean it arrived after 3 am. Any 2 am drive would have left its own softened pair, and none is available (see step 4) |
| Bay 2 | Its softened tracks put it on the move during the snowfall | Red, not yellow |
| Bay 1 | Yellow, and parked right next to the lamp post | No tracks: parked before the snow and never moved |
| "Bay 5 can't be guilty, its roof is as snowy as bay 1's" | The two roofs look alike | Roof snow only shows the car stood still for part of the snowfall. The softened tracks date its arrival to the snowfall |

## Verification

- **Logic (programmatic, `test-c/verify_logic.py` v2 → `logic-verification.json`):** enumerates joint movement histories of all four cars (0–2 drives each, before/during/after the snow), matches the visible track pairs as a multiset, and enforces bay occupancy. It found 4,509 consistent histories. In all of them only bay 5 can be a yellow car driving at 2 am, with or without the roof-snow assumption. Without the paint clue the result is {2, 5}; without the track clue it is {1, 4, 5}.
- **Final image against the clue inventory:** see `qa-report.md`.

## Scene notes (from Codex's composition, confirmed by Claude)

- A painted inn backdrop (generated) with a deterministic courtyard. The single gateway is at lower left between snow-capped wall ends, and the lamp stands just inside it.
- All three track pairs enter through the gateway, pass the lamp at a similar distance, then fan out to bays 2, 4 and 5. Where bay 4's sharp pair crosses the softened pairs, it is drawn on top: newer over older, as it should be.
- The paint smear uses exactly the cars' yellow (#f1ce35).
