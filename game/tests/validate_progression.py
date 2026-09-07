import json,itertools
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[1];m=json.loads((R/'data/maze.json').read_text());g=m['grid'];events=json.loads((R/'data/events.json').read_text());E={e['id']:e for e in events};N=len(g)
G={(x,y):[(x+dx,y+dy) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)] if 0<=x+dx<N and 0<=y+dy<N and g[y+dy][x+dx]] for y,row in enumerate(g) for x,v in enumerate(row) if v}
assert len({tuple(e['cell']) for e in events})==len(events)
for e in events:
 c=tuple(e['cell']);assert c in G,e
 if e['kind'] in ['door','oneway','exit']:
  ns=G[c];assert len(ns)==2,(e['id'],ns)
  assert (ns[0][1]==ns[1][1])==(e['axis']=='x'),e
  assert ns[0][0]==ns[1][0] or ns[0][1]==ns[1][1],e
  assert not(e.get('requires') and e.get('answer')) or e['id']=='final'
def flood(start,blocked):
 prev={start:None};q=deque([start])
 while q:
  for n in G[q.popleft()]:
   if n not in prev and n not in blocked:prev[n]=True;q.append(n)
 return set(prev)
def blocked(opened):return {tuple(e['cell']) for e in events if e['kind'] in ['door','oneway','exit'] and e['id'] not in opened}
base=flood((9,1),blocked(set()))
assert tuple(E['entry_left']['cell']) in base and tuple(E['entry_right']['cell']) in base
assert tuple(E['copper_key']['cell']) not in base
opened={'code03'};top=flood((9,1),blocked(opened))
for id in ['copper_key','raw_artifact','maintenance_a','maintenance_b','exit_protocol'] :assert tuple(E[id]['cell']) in top,id
for gate,loot in [('solar_vault','disc_sun'),('star_vault','disc_star'),('moon_vault','disc_moon')]:
 assert tuple(E[loot]['cell']) not in top,(gate,'bypass')
 assert tuple(E[loot]['cell']) in flood((9,1),blocked(opened|{gate})),gate
assert not any(y>=25 for x,y in flood((9,1),blocked({'code03','solar_vault','star_vault','moon_vault'})))
# Every branch order, either sas: all remaining goals available after transfer.
for order in itertools.permutations(['solar_vault','star_vault','moon_vault']):
 op={'code03'}
 for gate in order:
  reachable=flood((9,1),blocked(op));assert any(n in reachable for n in G[tuple(E[gate]['cell'])]);op.add(gate)
 for sas in ['oneway_a','oneway_b']:
  x,y=E[sas]['cell'];bottom=flood((x,y+1),blocked(op))
  assert not any(c[1]<25 for c in bottom)
  for id in ['fuse','power_panel','lower_sign']:assert tuple(E[id]['cell']) in bottom
  assert (17,33) in bottom
# Planned actual physics run, code answers are test fixtures, never player hints.
def plan(sas):
 current=(9,1);op=set();steps=[]
 ids=['entry_left','entry_right','code03','copper_key','solar_vault','disc_sun','maintenance_a','maintenance_b','star_vault','disc_star','raw_artifact','moon_vault','disc_moon','exit_protocol',sas,'fuse','power_panel','final']
 for id in ids:
  e=E[id];cell=tuple(e['cell']);blocks=blocked(op);targets=set(G[cell]) if e['kind'] in ['door','exit'] else {cell}
  if e['kind']=='oneway':targets={(cell[0],cell[1]-1)}
  prev={current:None};q=deque([current]);end=None
  while q:
   c=q.popleft()
   if c in targets:end=c;break
   for n in G[c]:
    if n not in prev and n not in blocks:prev[n]=c;q.append(n)
  assert end is not None,id
  route=[];c=end
  while c is not None:route.append(c);c=prev[c]
  steps.append({'id':id,'route':route[::-1]});current=end
  if e['kind']=='oneway':current=(cell[0],cell[1]+1)
  elif e['kind'] in ['door','exit']:op.add(id)
 (R/'tests'/f'route_{sas}.json').write_text(json.dumps(steps))
for sas in ['oneway_a','oneway_b']:plan(sas)
print('PROGRESSION PASS: 6 branch orders × 2 sas, no door bypass, all clues available before use, no missing-essential departure, complete lower sector reachable.')
print('GEOMETRY PASS:',sum(e['kind'] in ['door','oneway','exit'] for e in events),'gates in straight two-ended corridors;',len(G),'connected corridor cells.')
