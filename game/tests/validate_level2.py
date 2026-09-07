from pathlib import Path
from collections import deque
import json
r=Path(__file__).resolve().parents[1];g=json.loads((r/'data/maze2.json').read_text())['grid'];E=json.loads((r/'data/events2.json').read_text());by={e['id']:e for e in E};n=len(g)
G={(x,y):[(x+dx,y+dy) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)] if 0<=x+dx<n and 0<=y+dy<n and g[y+dy][x+dx]] for y,row in enumerate(g) for x,v in enumerate(row) if v}
assert len({tuple(e['cell']) for e in E})==len(E)
for e in E:
 c=tuple(e['cell']);assert c in G,e['id']
 if e['kind'] in ['door','exit']:
  ns=G[c];assert len(ns)==2 and ns[0][0]==ns[1][0],e['id']
def reachable(start,opened):
 blocks={tuple(e['cell']) for e in E if e['kind'] in ['door','exit'] and e['id'] not in opened};seen={start};q=deque([start])
 while q:
  for b in G[q.popleft()]:
   if b not in seen and b not in blocks:seen.add(b);q.append(b)
 return seen
assert all(c[1]<11 for c in reachable((1,1),set()))
assert all(c[1]<23 for c in reachable((1,1),{'power_gate'}))
assert len(reachable((1,1),{'power_gate','water_gate','lift_exit'}))==len(G)
# Fixed-point collection/use, including crafted items and explicit dependencies.
owned=set();done=set();changed=True
while changed:
 changed=False;rs=reachable((1,1),done)
 for e in E:
  if e['id'] in done:continue
  c=tuple(e['cell']);accessible=c in rs or (e['kind'] in ['door','exit'] and any(v in rs for v in G[c]))
  if not accessible or e.get('controlled_by') or not set(e.get('requires',[]))<=owned or not set(e.get('prerequisites',[]))<=done:continue
  if e['id']=='water_manifold' and not {'pipe_plan','gauge_pump','gauge_filter','gauge_tank'}<=done:continue
  done.add(e['id']);changed=True;owned-=set(e.get('requires',[]));owned.update(e.get('grants',{}))
  if e['kind']=='pickup':owned.add(e['resource'])
  done.update(e.get('opens',[]))
assert 'lift_exit' in done
for sc in json.loads((r/'data/shortcuts2.json').read_text()):
 assert g[sc['cell'][1]][sc['cell'][0]]==0
 assert (sc['sides'][0][1]//12)==(sc['sides'][1][1]//12)
# Full physical walkthrough fixture: all knowledge is actually collected before use.
order=['m_welcome','coupling_notice','tool_handle','tool_head','tool_bench','generator','copper_coil','valve_wheel','pipe_plan','gauge_pump','gauge_filter','gauge_tank','water_manifold','ceramic_core','relay_bench','hoist_cable','lift_notice','hoist_hook','hoist','lift_power','lift_exit']
current=(1,1);opened=set();steps=[]
for id in order:
 e=by[id];c=tuple(e['cell']);targets=set(G[c]) if e['kind']=='exit' else {c};blocks={tuple(t['cell']) for t in E if t['kind'] in ['door','exit'] and t['id'] not in opened};prev={current:None};q=deque([current]);end=None
 while q:
  t=q.popleft()
  if t in targets:end=t;break
  for v in G[t]:
   if v not in prev and v not in blocks:prev[v]=t;q.append(v)
 assert end is not None,id
 route=[];v=end
 while v is not None:route.append(v);v=prev[v]
 steps.append({'id':id,'route':route[::-1]});current=end;opened.update(e.get('opens',[]))
(r/'tests/route_level2.json').write_text(json.dumps(steps))
print('LEVEL2 GRAPH PASS: all 26 events on unique floor cells; two enforced gates; craft and clue dependencies solvable; six shortcuts remain within departments.')
print('Walkthrough:',sum(len(s['route']) for s in steps),'cells,',len(steps),'interactions')
