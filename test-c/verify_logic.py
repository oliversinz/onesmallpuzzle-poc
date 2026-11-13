#!/usr/bin/env python3
"""Logic check for Test C (Claude's construction), version 2.

Version 1 checked each car on its own and treated tracks as sets. Codex's handoff review
(test-c/codex-c1.json) pointed out that this collapses repeated tracks and never tests swaps
(e.g. car X leaves bay 5 at 2 am, car Y then arrives in bay 5). This version enumerates JOINT
movement histories of all four cars and compares the resulting MULTISET of visible track pairs
with the evidence exactly.

Model
- Locations: O (outside, via the single entrance) and bays 1-5. Every drive goes from one
  location to another and leaves its own separate pair of tracks between them (public rule F3).
- Drive times: before the snow (0.5, buried = invisible), during it (1.5, 2.0, 2.5 -> softened),
  after it (3.5 -> sharp). Each car makes 0-2 drives and ends in the bay where it is drawn.
- Occupancy: no two cars in the same bay at the same time.
- Roof snow (optional constraint): snow on the roof iff the car's last drive was before 3 am.
- Culprit: a yellow car that drives at 2.0 (any drive at 2 am counts; conservative).
Run: python3 test-c/verify_logic.py
"""
import itertools
import json
import pathlib
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent
T = [0.5, 1.5, 2.0, 2.5, 3.5]
LOC = ["O", "B1", "B2", "B3", "B4", "B5"]
SCRAPE = "yellow"

# Evidence exactly as it must appear in the final image.
CARS = {  # final bay -> colour, roof snow
    "B1": ("yellow", True), "B2": ("red", True), "B4": ("yellow", False), "B5": ("yellow", True)}
TRACKS = Counter({(frozenset({"O", "B2"}), "softened"): 1,
                  (frozenset({"O", "B4"}), "sharp"): 1,
                  (frozenset({"O", "B5"}), "softened"): 1})


def look(t):
    return None if t < 1 else ("softened" if t < 3 else "sharp")


def car_histories(final, roof, use_roof):
    out = []
    for start in LOC:
        for k in range(3):
            for times in itertools.combinations(T, k):
                for mids in itertools.product(LOC, repeat=max(k - 1, 0)):
                    path = [start, *mids, final] if k else [start]
                    if path[-1] != final or any(a == b for a, b in zip(path, path[1:])):
                        continue
                    drives = list(zip(times, path, path[1:]))
                    if use_roof:
                        last = drives[-1][0] if drives else 0
                        if (last < 3) != roof:
                            continue
                    tr = Counter((frozenset({a, b}), look(t)) for t, a, b in drives if look(t))
                    if all(tr[x] <= TRACKS[x] for x in tr):
                        out.append((start, drives, tr))
    return out


def occupancy_ok(combo):
    # where is each car just after each event time; bays must not be shared
    for t in [0.0] + T:
        seen = set()
        for start, drives, _ in combo:
            pos = start
            for dt, a, b in drives:
                if dt <= t:
                    pos = b
            if pos != "O":
                if pos in seen:
                    return False
                seen.add(pos)
    return True


def analyse(use_roof=True, use_colour=True, use_tracks=True):
    keys = list(CARS)
    hist = {b: car_histories(b, CARS[b][1], use_roof) for b in keys}
    possible, n_consistent = set(), 0
    for combo in itertools.product(*(hist[b] for b in keys)):
        total = Counter()
        for _, _, tr in combo:
            total += tr
        if use_tracks and total != TRACKS:
            continue
        if not occupancy_ok(combo):
            continue
        n_consistent += 1
        for b, (_, drives, _) in zip(keys, combo):
            if (not use_colour or CARS[b][0] == SCRAPE) and any(t == 2.0 for t, _, _ in drives):
                possible.add(b)
            if not use_tracks and (not use_colour or CARS[b][0] == SCRAPE):
                possible.add(b)
    return sorted(possible), n_consistent


def main():
    r_all, n_all = analyse()
    r_noroof, n_noroof = analyse(use_roof=False)
    r_nocol, _ = analyse(use_colour=False)
    r_notr, _ = analyse(use_tracks=False)
    report = {
        "model": "joint histories of 4 cars, 0-2 drives each, multiset track match, occupancy",
        "consistent_joint_histories": n_all,
        "possible_culprit_bays": r_all,
        "possible_culprit_bays_ignoring_roof_snow": r_noroof,
        "consistent_joint_histories_ignoring_roof_snow": n_noroof,
        "possible_culprit_bays_without_paint_colour": r_nocol,
        "possible_culprit_bays_without_track_evidence": r_notr,
    }
    report["unique"] = r_all == ["B5"] and r_noroof == ["B5"]
    report["each_clue_necessary"] = len(r_nocol) > 1 and len(r_notr) > 1
    print(json.dumps(report, indent=1))
    (HERE / "logic-verification.json").write_text(json.dumps(report, indent=1) + "\n")
    print("LOGIC PASS" if report["unique"] and report["each_clue_necessary"] else "LOGIC FAIL")


if __name__ == "__main__":
    main()
