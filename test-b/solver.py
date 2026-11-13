#!/usr/bin/env python3
"""Exact verification for Test B ("Lights out, back door").

Rules: each move walks through one inside doorway into a neighbouring room and flips
that room's light. Leaving a room changes nothing. Start in `start`; finish in
`exit_room` with every light off (then leave by the back door, which is not counted).

Method 1: BFS over (room, light pattern) -> exact minimum and number of shortest walks.
Method 2: written separately, plain depth-first enumeration of every walk up to the
          bound, simulating the lights move by move (no state merging).
Method 3: the counting lower bound used in the published explanation.
Usage: python3 test-b/solver.py [instance.json]  (writes test-b/verification.json)
"""
import json
import pathlib
import sys
from collections import deque

HERE = pathlib.Path(__file__).resolve().parent


def load(path=HERE / "instance.json"):
    return json.loads(pathlib.Path(path).read_text())


def graph(inst):
    g = {r: set() for r in inst["rooms"]}
    for a, b in inst["doors"]:
        g[a].add(b)
        g[b].add(a)
    return g


def bfs(inst):
    g, rooms = graph(inst), list(inst["rooms"])
    bit = {r: 1 << i for i, r in enumerate(rooms)}
    lit = sum(bit[r] for r in rooms if inst["rooms"][r]["lit"])
    start, goal = (inst["start"], lit), (inst["exit_room"], 0)
    dist, count, preds = {start: 0}, {start: 1}, {start: []}
    q = deque([start])
    while q:
        s = q.popleft()
        for nxt in sorted(g[s[0]]):
            t = (nxt, s[1] ^ bit[nxt])
            if t not in dist:
                dist[t], count[t], preds[t] = dist[s] + 1, count[s], [s]
                q.append(t)
            elif dist[t] == dist[s] + 1:
                count[t] += count[s]
                preds[t].append(s)
    if goal not in dist:
        return None, 0, []
    walks = []

    def back(s, acc):
        if s == start:
            walks.append([start[0]] + acc[::-1])
            return
        for p in preds[s]:
            back(p, acc + [s[0]])
    back(goal, [])
    return dist[goal], count[goal], sorted(walks)


def dfs_all(inst, max_len):
    """Independent check: every walk of length <= max_len, lights simulated directly."""
    g = graph(inst)
    found = []

    def go(room, lights, walk):
        if room == inst["exit_room"] and not any(lights.values()):
            found.append(list(walk))
        if len(walk) - 1 == max_len:
            return
        for nxt in sorted(g[room]):
            lights[nxt] = not lights[nxt]
            walk.append(nxt)
            go(nxt, lights, walk)
            walk.pop()
            lights[nxt] = not lights[nxt]
    go(inst["start"], {r: v["lit"] for r, v in inst["rooms"].items()}, [inst["start"]])
    return found


def counting_bound(inst):
    """Each move enters exactly one room, so moves = total entries.
    Lit room: odd number of entries (>= 1). Dark room: even (0 or >= 2).
    A dark room is unavoidable if deleting it cuts the start off from a room that must be entered.
    The exit room must be entered at least once (you finish there), so >= 2 if dark."""
    g = graph(inst)
    must = {r for r, v in inst["rooms"].items() if v["lit"]} | {inst["exit_room"]}

    def reach(avoid):
        seen, st = {inst["start"]}, [inst["start"]]
        while st:
            x = st.pop()
            for y in g[x]:
                if y != avoid and y not in seen:
                    seen.add(y)
                    st.append(y)
        return seen
    need = {}
    for r, v in inst["rooms"].items():
        if v["lit"]:
            need[r] = 1
        elif r == inst["exit_room"]:
            need[r] = 2
        elif r != inst["start"] and (must - {r}) - reach(r):
            need[r] = 2
        else:
            need[r] = 0
    return sum(need.values()), need


def backdoor_variant(inst):
    """0-1 shortest path where leaving/re-entering via the back door is free but flips the exit room."""
    import heapq
    g, rooms = graph(inst), list(inst["rooms"])
    bit = {r: 1 << i for i, r in enumerate(rooms)}
    lit = sum(bit[r] for r in rooms if inst["rooms"][r]["lit"])
    ex = inst["exit_room"]
    start = (inst["start"], lit)
    dist, pq = {start: 0}, [(0, start)]
    while pq:
        d, (pos, m) = heapq.heappop(pq)
        if d > dist[(pos, m)]:
            continue
        if pos == ex and m == 0:
            return d
        moves = [] if pos == "outside" else [(n, m ^ bit[n], 1) for n in g[pos]]
        if pos == ex:
            moves.append(("outside", m, 0))
        if pos == "outside":
            moves.append((ex, m ^ bit[ex], 0))
        for n, nm, c in moves:
            if d + c < dist.get((n, nm), 1 << 30):
                dist[(n, nm)] = d + c
                heapq.heappush(pq, (d + c, (n, nm)))
    return None


def entries(walk):
    e = {}
    for r in walk[1:]:
        e[r] = e.get(r, 0) + 1
    return e


def main():
    inst = load(sys.argv[1]) if len(sys.argv) > 1 else load()
    d, n, walks = bfs(inst)
    lb, need = counting_bound(inst)
    dfs = dfs_all(inst, d)
    dfs_short = [w for w in dfs if len(w) - 1 < d]
    dfs_opt = sorted(w for w in dfs if len(w) - 1 == d)
    names = {r: v["name"] for r, v in inst["rooms"].items()}
    report = {
        "bfs_minimum_doorways": d,
        "bfs_number_of_shortest_walks": n,
        "bfs_shortest_walks": [[names[r] for r in w] for w in walks],
        "dfs_walks_shorter_than_minimum": len(dfs_short),
        "dfs_shortest_walks_match_bfs": dfs_opt == walks,
        "counting_lower_bound": lb,
        "counting_bound_per_room": {names[r]: k for r, k in need.items()},
        "bound_is_tight": lb == d,
        "entries_in_each_shortest_walk": [{names[r]: k for r, k in entries(w).items()} for w in walks],
    }
    # The tempting 11-doorway walk from the explanation leaves two lights on.
    w11 = ["hall", "office", "library", "studio", "bathroom", "bedroom", "library", "office",
           "hall", "dining", "kitchen", "bootroom"]
    lights = {r: v["lit"] for r, v in inst["rooms"].items()}
    for r in w11[1:]:
        lights[r] = not lights[r]
    report["tempting_11_walk_lights_left_on"] = [names[r] for r, on in lights.items() if on]
    report["all_shortest_walks_do_north_wing_first"] = all(w.index("office") < w.index("dining") for w in walks)
    # Reading raised by the blind solver: may you step out of the back door and come back in mid-route?
    # Model it as free (uncounted) moves; re-entering flips the boot room. The minimum must not drop.
    report["minimum_if_backdoor_reentry_allowed"] = backdoor_variant(inst)
    print(json.dumps(report, indent=2))
    if len(sys.argv) == 1:
        (HERE / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    ok = d == 13 and n == 2 and not dfs_short and dfs_opt == walks and lb == d \
        and report["minimum_if_backdoor_reentry_allowed"] == d
    print("ALL CHECKS PASS" if ok else "CHECK FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
