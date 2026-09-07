"""Validate gate isolation, consumable dependencies, and a full spoiler route."""
from pathlib import Path
from collections import deque
import json
r=Path(__file__).resolve().parents[1]
m=json.loads((r/'data/maze3.json').read_text());g=m['grid'];E=json.loads((r/'data/events3.json').read_text());by={e['id']:e for e in E}
G={(x,y):[(x+dx,y+dy) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)] if 0<=x+dx<35 and 0<=y+dy<35 and g[y+dy][x+dx]] for y,row in enumerate(g) for x,v in enumerate(row) if v}
assert len({tuple(e['cell']) for e in E})==len(E)
assert all(tuple(e['cell']) in G for e in E)
def reach(opened):
 blocked={tuple(e['cell']) for e in E if e['kind'] in ['door','exit'] and e['id'] not in opened};seen={tuple(m['start'])};q=deque(seen)
 while q:
  for v in G[q.popleft()]:
   if v not in seen and v not in blocked:seen.add(v);q.append(v)
 return seen
assert max(y for x,y in reach(set()))==10
assert max(y for x,y in reach({'optics_gate'}))==22
for sc in json.loads((r/'data/shortcuts3.json').read_text()):
 x,y=sc['cell'];assert not g[y][x]
 a,b=map(tuple,sc['sides']);assert a in G and b in G
 assert a[1]//12==b[1]//12
 assert abs(a[0]-b[0])+abs(a[1]-b[1])==2
order=['o_welcome','lens','lens_mount','optical_bench','o_secret1','projector','prism','beam_plan','beam_triangle','beam_circle','beam_square','o_secret2','archive_order','beam_router','plate_dawn','plate_zenith','plate_dusk','reader_rule','o_secret3','archive_reader','observation_exit']
current=tuple(m['start']);done=set();owned=set();steps=[]
for id in order:
 e=by[id];c=tuple(e['cell']);targets=set(G[c]) if e['kind']=='exit' else {c};blocks={tuple(t['cell']) for t in E if t['kind'] in ['door','exit'] and t['id'] not in done};prev={current:None};q=deque([current]);end=None
 while q:
  t=q.popleft()
  if t in targets:end=t;break
  for v in G[t]:
   if v not in prev and v not in blocks:prev[v]=t;q.append(v)
 assert end is not None,id
 assert set(e.get('requires',[]))<=owned,id
 assert set(e.get('prerequisites',[]))<=done,id
 if id=='beam_router':assert {'beam_plan','beam_triangle','beam_circle','beam_square'}<=done
 if id=='archive_reader':assert {'archive_order','reader_rule','plate_dawn','plate_zenith','plate_dusk'}<=done
 route=[];v=end
 while v is not None:route.append(v);v=prev[v]
 steps.append({'id':id,'route':route[::-1]});current=end
 done.add(id);done.update(e.get('opens',[]));owned-=set(e.get('requires',[]));owned.update(e.get('grants',{}))
 if e['kind']=='pickup':owned.add(e['resource'])
assert len(done)==len(E),(done,len(E))
(r/'tests/route_level3.json').write_text(json.dumps(steps)+'\n')
print(f'LEVEL3 GRAPH PASS: {len(E)} events, 3 secrets, 6 safe shortcuts, two enforced gates, {sum(len(s["route"]) for s in steps)} route cells.')
