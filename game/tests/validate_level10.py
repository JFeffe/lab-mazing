"""Reachability across moving stacks, prerequisite gates and useful return links."""
from pathlib import Path
from collections import deque
from itertools import product
import json
D=Path(__file__).resolve().parents[1]/'data';T=D.parent/'tests'
m=json.loads((D/'maze10.json').read_text());E=json.loads((D/'events10.json').read_text());S=json.loads((D/'shortcuts10.json').read_text());by={e['id']:e for e in E}
F={(x,y) for y,row in enumerate(m['grid']) for x,v in enumerate(row) if v}
def adjacent(c):return [(c[0]+dx,c[1]+dy) for dx,dy in [(0,-1),(1,0),(0,1),(-1,0)]]
def blocks(v):return {(x,y) for y,gap in zip([4,7,10],[14+3*a for a in v]) for x in range(13,22) if x!=gap}
def path(start,targets,walk):
 q=deque([start]);prev={start:None}
 while q:
  c=q.popleft()
  if c in targets:
   out=[]
   while c is not None:out.append(c);c=prev[c]
   return out[::-1]
  for n in adjacent(c):
   if n in walk and n not in prev:prev[n]=c;q.append(n)
 return []
assert len(by)==len(E)==len({tuple(e['cell']) for e in E})
assert all(tuple(e['cell']) in F for e in E)
# Every shelf configuration permits leaving the shelving area, preventing softlocks.
for v in product(range(3),repeat=3):
 walk=F-blocks(v)-{(29,20),(21,19)}
 for c in walk:
  if 13<=c[0]<=21 and c[1]<12:assert path(c,{(17,14)},walk),(v,c)
assert not path((17,23),{(29,25)},F-blocks([0,0,0])-{(29,20),(21,19)})
assert path((17,23),{(29,7)},F-blocks([0,0,0])-{(29,20),(21,19)})
order=['a_welcome','a_manual','a_secret2','a_rails','a_stacks','a_seal','a_access','a_clock','a_object','a_secret1','a_reports','a_twin_note','a_original','a_secret3','a_twin','a_final']
def route(order):
 current=tuple(m['start']);done=set();owned=set();steps=[]
 for id in order:
  e=by[id];c=tuple(e['cell'])
  locked={tuple(t['cell']) for t in E if t['kind'] in ['door','exit'] and t['id'] not in done}
  walk=F-blocks([2,0,1] if 'a_stacks' in done else [0,0,0])-locked
  cells=path(current,set(adjacent(c)) if e['kind']=='exit' else {c},walk)
  assert cells,id
  assert set(e.get('requires',[]))<=owned,id
  assert set(e.get('prerequisites',[]))<=done,id
  current=cells[-1];steps.append({'id':id,'route':cells});done.add(id);done.update(e.get('opens',[]))
  if e['kind']=='pickup':owned.add(e['resource'])
 assert len(done)==len(E)
 return steps
steps=route(order)
# Player may complete evidence and visit the original room before working the stacks.
route(['a_welcome','a_access','a_clock','a_object','a_secret1','a_reports','a_twin_note','a_original','a_secret3','a_twin','a_manual','a_secret2','a_rails','a_stacks','a_seal','a_final'])
(T/'route_level10.json').write_text(json.dumps(steps)+'\n')
# Every control count modulo 3 has one solution. I twice + II once.
assert [v for v in product(range(3),repeat=3) if [(v[0]+v[2])%3,(v[0]+v[1])%3,(v[1]+v[2])%3]==[2,0,1]]==[(2,1,0)]
for s in S:
 a,b=map(tuple,s['sides']);c=tuple(s['cell']);walk=F|{tuple(t['cell']) for t in S if t!=s}
 assert c not in F and set(adjacent(c))&F=={a,b}
 assert len(path(a,{b},walk))-3==s['minimum_saved_steps']>=12
walk=(F|{tuple(s['cell']) for s in S})-{(29,20),(21,19)}
assert not path((17,23),{(29,25)},walk),'Shortcut bypasses room lock'
print('LEVEL10 GRAPH PASS: 27 escapable shelf states, 2 objective orders, 4 safe return links;',sum(len(s['route'])-1 for s in steps),'route steps')
