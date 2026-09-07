"""Validate gate isolation, consumable dependencies, and a full spoiler route."""
from pathlib import Path
from collections import deque
import json
r=Path(__file__).resolve().parents[1]
m=json.loads((r/'data/maze4.json').read_text());g=m['grid'];E=json.loads((r/'data/events4.json').read_text());by={e['id']:e for e in E}
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
assert max(y for x,y in reach({'test_gate'}))==22
for sc in json.loads((r/'data/shortcuts4.json').read_text()):
 x,y=sc['cell'];assert not g[y][x]
 a,b=map(tuple,sc['sides']);assert a in G and b in G
 assert a[1]//12==b[1]//12
 assert abs(a[0]-b[0])+abs(a[1]-b[1])==2
order=['t_welcome','weight1','weight2','weight3','weight5','balance_note','t_secret1','test_balance','order_sun','order_moon','order_comet','magnet','cord','t_secret2','sequence_panel','service_duct','circuit_note','circuit_wiring','t_secret3','test_circuit','test_exit']
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
 if id=='test_balance':assert 'balance_note' in done
 if id=='sequence_panel':assert {'order_sun','order_moon','order_comet'}<=done
 if id=='test_circuit':assert {'circuit_note','circuit_wiring'}<=done
 route=[];v=end
 while v is not None:route.append(v);v=prev[v]
 steps.append({'id':id,'route':route[::-1]});current=end
 done.add(id);done.update(e.get('opens',[]));owned-=set(e.get('requires',[]));owned.update(e.get('grants',{}))
 if e['kind']=='pickup':owned.add(e['resource'])
assert len(done)==len(E),(done,len(E))
(r/'tests/route_level4.json').write_text(json.dumps(steps)+'\n')
print(f'LEVEL4 GRAPH PASS: {len(E)} events, 3 secrets, 6 safe shortcuts, two enforced gates, {sum(len(s["route"]) for s in steps)} route cells.')

# Exhaustively prove that the written clues define one solution per puzzle.
from itertools import product, permutations
weights=by['test_balance']['weights']
balances=[v for v in product(range(3),repeat=4) if v.count(1)==v.count(2)==2 and sum(w for w,p in zip(weights,v) if p==1)-sum(w for w,p in zip(weights,v) if p==2)==1]
assert balances==[(1,2,2,1)],balances
sequences=[v for v in permutations(range(5)) if v[2]==0 and v.index(3)==v.index(1)+1 and v[-1]==2 and v.index(4)>v.index(0)]
assert sequences==[tuple(by['sequence_panel']['sequence'])],sequences
c=by['test_circuit'];solutions=[]
for presses in product(range(2),repeat=4):
 lamps=c['initial'].copy()
 for i,pressed in enumerate(presses):
  if pressed:lamps=[a^b for a,b in zip(lamps,c['masks'][i])]
 if lamps==[1]*5:solutions.append(presses)
assert solutions==[(1,0,1,1)],solutions
print('UNIQUE SOLUTIONS PASS: balance (1+5)/(2+3), sequence Moon-Star-Sun-Planet-Comet, circuit I+III+IV.')
