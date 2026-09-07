"""Check both wing orders, gate isolation and every puzzle state's recoverability."""
from pathlib import Path
from collections import deque
from itertools import product
import json
r=Path(__file__).resolve().parents[1];D=r/'data'
m=json.loads((D/'maze5.json').read_text());g=m['grid'];E=json.loads((D/'events5.json').read_text());by={e['id']:e for e in E}
G={(x,y):[(x+dx,y+dy) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)] if 0<=x+dx<35 and 0<=y+dy<35 and g[y+dy][x+dx]] for y,row in enumerate(g) for x,v in enumerate(row) if v}
assert len({tuple(e['cell']) for e in E})==len(E) and all(tuple(e['cell']) in G for e in E)
def reach(blocks):
 seen={tuple(m['start'])};q=deque(seen)
 while q:
  for v in G[q.popleft()]:
   if v not in blocks and v not in seen:seen.add(v);q.append(v)
 return seen
closed=reach({tuple(by['f_gate']['cell']),tuple(by['f_exit']['cell'])})
assert tuple(by['f_dosing']['cell']) in closed and tuple(by['f_tower']['cell']) in closed
assert not any(y<12 for x,y in closed)
assert len(reach(set()))==len(G)
for sc in json.loads((D/'shortcuts5.json').read_text()):
 x,y=sc['cell'];a,b=map(tuple,sc['sides']);assert not g[y][x] and a in G and b in G
 assert all(v in closed for v in [a,b]) or all(v[1]<10 for v in [a,b])
 assert abs(a[0]-b[0])+abs(a[1]-b[1])==2
west=['f_water_note','f_water_tip','f_secret1','f_dosing'];east=['f_tower_note','f_tower_tip','f_secret2','f_tower']
def route(order):
 current=tuple(m['start']);done=set();owned=set();steps=[]
 for id in order:
  e=by[id];c=tuple(e['cell']);targets=set(G[c]) if e['kind']=='exit' else {c};blocks={tuple(t['cell']) for t in E if t['kind'] in ['door','exit'] and t['id'] not in done};prev={current:None};q=deque([current]);end=None
  while q:
   t=q.popleft()
   if t in targets:end=t;break
   for v in G[t]:
    if v not in prev and v not in blocks:prev[v]=t;q.append(v)
  assert end is not None,id
  assert set(e.get('requires',[]))<=owned and set(e.get('prerequisites',[]))<=done,id
  cells=[];v=end
  while v is not None:cells.append(v);v=prev[v]
  steps.append({'id':id,'route':cells[::-1]});current=end
  done.add(id);done.update(e.get('opens',[]));owned-=set(e.get('requires',[]));owned.update(e.get('grants',{}))
  if e['kind']=='pickup':owned.add(e['resource'])
 assert len(done)==len(E)
 return steps
prefix=['f_welcome','f_seal','f_hall_note'];suffix=['f_assembly','f_rotor_note','f_rotor_wiring','f_secret3','f_rotors','f_exit']
steps=route(prefix+west+east+suffix);route(prefix+east+west+suffix)
(r/'tests/route_level5.json').write_text(json.dumps(steps)+'\n')
def jug_moves(s):
 a,b=s;t=min(a,3-b);u=min(b,5-a)
 return [(5,b),(a,3),(0,b),(a,0),(a-t,b+t),(a+u,b-u)]
def hanoi_moves(s):
 out=[]
 for a,b in [(0,1),(0,2),(1,0),(1,2),(2,0),(2,1)]:
  n=list(s)
  if a in s:
   i=s.index(a)
   if b not in s or i<s.index(b):n[i]=b
  out.append(tuple(n))
 return out
def rotor_moves(s):return [tuple((a+b)%4 for a,b in zip(s,v)) for v in by['f_rotors']['masks']]
def bfs(start,moves,goal):
 q=deque([start]);prev={start:None};paths={start:[]}
 while q:
  s=q.popleft()
  for i,n in enumerate(moves(s)):
   if n not in prev:prev[n]=s;paths[n]=paths[s]+[i];q.append(n)
 goals=[s for s in prev if goal(s)];assert goals
 # Every reachable state can reach a goal without reset (no dead-end configurations).
 good=set(goals)
 while True:
  before=len(good);good.update(s for s in prev if any(n in good for n in moves(s)))
  if len(good)==before:break
 assert good==set(prev)
 solution=min((paths[s] for s in goals),key=len)
 return solution,len(prev)
solutions={}
for name,start,moves,goal in [('jugs',(0,0),jug_moves,lambda s:s[0]==4),('hanoi',(0,0,0),hanoi_moves,lambda s:s==(2,2,2)),('rotors',(0,0,0),rotor_moves,lambda s:s==(1,2,3))]:
 sol,n=bfs(start,moves,goal);solutions[name]=sol;print(name,'solution',sol,'reachable states',n)
assert [len(solutions[k]) for k in ['jugs','hanoi','rotors']]==[6,7,3]
(r/'tests/solutions_level5.json').write_text(json.dumps(solutions)+'\n')
print('LEVEL5 GRAPH PASS:',len(E),'events, both wing orders, isolated north gate,',sum(len(s['route']) for s in steps),'physical route cells; all puzzle states recoverable.')
