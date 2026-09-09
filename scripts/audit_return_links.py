"""Measure and select additive return doors; never relocate existing save IDs.

The selection uses a fully explored map, all static gates open (except one-way
airlocks), and the other shortcuts open. This is a lower bound on detours, not
a claimed first-playthrough time. Gate safety uses separate components with
every puzzle/variable barrier closed. Movable archive shelves are excluded.
"""
from collections import deque
from pathlib import Path
from copy import deepcopy
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'game/data'
REPORT = ROOT / 'game/tests/return_links_audit.json'
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
MIN_NEW = 20
MIN_OLD = 12


def read(path):
    return json.loads(path.read_text())


def neighbors(cell):
    return [(cell[0] + x, cell[1] + y) for x, y in DIRECTIONS]


def distances(cells, start):
    if start not in cells:
        return {}
    result = {start: 0}
    queue = deque([start])
    while queue:
        c = queue.popleft()
        for n in neighbors(c):
            if n in cells and n not in result:
                result[n] = result[c] + 1
                queue.append(n)
    return result


def load_level(n):
    suffix = '' if n == 1 else str(n)
    maze, events, links = [read(DATA / f'{name}{suffix}.json') for name in ['maze', 'events', 'shortcuts']]
    ending = read(DATA / 'endings.json')[str(n)]
    for e in events:
        if e['id'] == ending['id']:
            e['cell'] = ending['cell']
            if 'title' in ending:
                e['title'] = ending['title'][0]
    floors = {(x, y) for y, row in enumerate(maze['grid']) for x, v in enumerate(row) if v}
    barriers = {tuple(e['cell']) for e in events if e['kind'] in ['door', 'exit', 'oneway', 'creature']}
    barriers |= {tuple(g['cell']) for e in events for g in e.get('world_gates', [])}
    if n == 10:
        barriers |= {(x, y) for x in range(13, 22) for y in [4, 7, 10]}
    safe = floors - barriers
    open_floor = floors - {tuple(e['cell']) for e in events if e['kind'] == 'oneway'}
    components = {}
    for c in sorted(safe):
        if c not in components:
            components.update({p: len(components) for p in distances(safe, c)})
    rewards = {tuple(e['cell']) for e in read(DATA / 'collectibles.json')[str(n)]}
    # Important destinations include the actual (v0.20+) doctor position.
    destinations = [e for e in events if e['kind'] in ['mechanism', 'craft', 'exit', 'creature']
                    or (e['kind'] == 'door' and ('answer' in e or 'requires' in e))]
    anchors = [e for e in events if e['kind'] not in ['door', 'oneway']]
    return dict(n=n, suffix=suffix, maze=maze, events=events, links=links,
                floors=floors, safe=safe, open_floor=open_floor,
                components=components, rewards=rewards, destinations=destinations, anchors=anchors)


def candidates(data):
    grid = data['maze']['grid']
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[y]) - 1):
            c = (x, y)
            if c in data['floors']:
                continue
            sides = [p for p in neighbors(c) if p in data['floors']]
            if len(sides) != 2 or tuple(map(sum, zip(*sides))) != (2*x, 2*y):
                continue
            a, b = sides
            if a not in data['components'] or b not in data['components']:
                continue
            if data['components'][a] != data['components'][b] or set(sides) & data['rewards']:
                continue
            detour = distances(data['open_floor'], a).get(b, 0)
            if detour < MIN_NEW + 2:
                continue
            yield dict(cell=list(c), sides=[list(a), list(b)], axis='x' if a[1] == b[1] else 'y')


def useful_example(data, link, network):
    """Best documented return to an important event (others already open)."""
    a, b = map(tuple, link['sides'])
    da, db = distances(network, a), distances(network, b)
    best = None
    for target in data['destinations']:
        t = tuple(target['cell'])
        dt = distances(network, t)
        for origin in data['anchors']:
            p = tuple(origin['cell'])
            if p == t or p not in dt or p not in da or t not in da:
                continue
            before = dt[p]
            after = min(before, da[p] + 2 + db[t], db[p] + 2 + da[t])
            gain = before - after
            if gain >= MIN_NEW and (best is None or (gain, -after) > (best['saved'], -best['after'])):
                best = dict(origin=origin['id'], target=target['id'], origin_ref=origin['ref'], target_ref=target['ref'],
                            origin_title=origin['title'], target_title=target['title'], before=before, after=after, saved=gain)
    return best


def admissible(data, links, old_ids):
    network = data['open_floor'] | {tuple(s['cell']) for s in links}
    for s in links:
        a, b = map(tuple, s['sides'])
        gain = distances(network - {tuple(s['cell'])}, a).get(b, 0) - 2
        if gain < (MIN_OLD if s['id'] in old_ids else MIN_NEW):
            return False
    return True


def select(data, original, limit=4):
    links = deepcopy(original)
    old_ids = {s['id'] for s in original}
    pool = list(candidates(data))
    for index in range(limit):
        network = data['open_floor'] | {tuple(s['cell']) for s in links}
        options = []
        for candidate in pool:
            c = tuple(candidate['cell'])
            if any(sum(abs(a-b) for a, b in zip(c, s['cell'])) < 3 for s in links):
                continue
            s = dict(candidate, id=f'B{index+1}')
            if not admissible(data, links + [s], old_ids):
                continue
            # Preserve a useful destination for previously selected new doors too.
            trial = network | {c}
            if any(useful_example(data, old, trial-{tuple(old['cell'])}) is None for old in links if old['id'] not in old_ids):
                continue
            example = useful_example(data, s, network)
            if example:
                options.append(((example['saved'], -example['after'], -c[1], -c[0]), s))
        if not options:
            break
        links.append(max(options, key=lambda v: v[0])[1])
    full = data['open_floor'] | {tuple(s['cell']) for s in links}
    # Retain legacy safe-network metadata for the pre-existing chapter tests.
    safe = data['safe']
    if data['n'] == 10:
        safe = data['floors']
    for s in links:
        a, b = map(tuple, s['sides'])
        s['original_detour_steps'] = distances(safe, a)[b]
        s['minimum_saved_steps'] = distances(safe | {tuple(t['cell']) for t in links if t != s}, a)[b] - 2
        s['fully_open_saved_steps'] = distances(full - {tuple(s['cell'])}, a)[b] - 2
        if s['id'] not in old_ids:
            s['return_example'] = useful_example(data, s, full - {tuple(s['cell'])})
    return links, len(pool)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--reselect', action='store_true', help='Author a new selection before release; may relocate new IDs.')
    args = parser.parse_args()
    prior = read(REPORT) if REPORT.exists() else {'levels': []}
    original = {v['level']: v['before'] for v in prior['levels']}
    authored = {v['level']: v['after'] for v in prior['levels']}
    rows = []
    for n in range(1, 26):
        data = load_level(n)
        before = original.get(n, data['links'])
        if n in authored and not args.reselect:
            # Once authored, coordinates and IDs are stable for saved games.
            # Remeasure the checked-in selection instead of silently relocating it.
            after = deepcopy(authored[n])
            count = len(list(candidates(data)))
            network = data['open_floor'] | {tuple(s['cell']) for s in after}
            old_ids = {s['id'] for s in before}
            assert admissible(data, after, old_ids)
            for s in after:
                if s['id'] not in old_ids:
                    s['return_example'] = useful_example(data, s, network - {tuple(s['cell'])})
                    assert s['return_example'], (n, s['id'], 'No useful return to a permanent station')
        else:
            after, count = select(data, before)
        added = [s for s in after if s['id'] not in {s['id'] for s in before}]
        row = dict(level=n, before=before, after=after, added_ids=[s['id'] for s in added], candidate_count=count)
        rows.append(row)
        print(n, f'{len(before)} -> {len(after)}', [(s['id'], s['cell'], s['fully_open_saved_steps'], s['return_example']['target_ref']) for s in added], flush=True)
    if args.write:
        for row in rows:
            suffix = '' if row['level'] == 1 else str(row['level'])
            (DATA / f'shortcuts{suffix}.json').write_text(json.dumps(row['after'], ensure_ascii=False, indent=2)+'\n')
        REPORT.write_text(json.dumps(dict(version='0.22', minimum_new_saving=MIN_NEW, minimum_existing_saving=MIN_OLD,
            measurement='Both sides visited, other links and puzzle gates open; one-way airlocks excluded.', levels=rows), ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    main()
