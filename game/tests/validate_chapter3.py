"""Independent graph/constraint checks; runtime tests exercise actual UI and physics."""
from pathlib import Path
from collections import deque
from itertools import product,permutations
import json
D=Path(__file__).resolve().parents[1]/'data';T=D.parent/'tests'
def read(p):return json.loads(p.read_text())
def near(c):return [(c[0]+x,c[1]+y) for x,y in [(0,1),(0,-1),(1,0),(-1,0)]]
def reach(a,walk):
 seen={a};q=deque([a])
 while q:
  for b in near(q.popleft()):
   if b in walk and b not in seen:seen.add(b);q.append(b)
 return seen
def distance(a,b,walk):
 q=deque([(a,0)]);seen={a}
 while q:
  c,d=q.popleft()
  if c==b:return d
  for n in near(c):
   if n in walk and n not in seen:seen.add(n);q.append((n,d+1))
 raise AssertionError('Disconnected path')
for n in range(11,16):
 m,E,S=[read(D/f'{k}{n}.json') for k in ['maze','events','shortcuts']];by={e['id']:e for e in E}
 F={(x,y) for y,row in enumerate(m['grid']) for x,v in enumerate(row) if v};start=tuple(m['start']);prefix=f'c{n}_'
 assert len(by)==len(E)==len({tuple(e['cell']) for e in E})==17
 assert sum(e.get('secret',False) for e in E)==3 and len(S)==4
 assert all(tuple(e['cell']) in F for e in E)
 for stage in range(3):
  locked={tuple(e['cell']) for e in E if e['kind']=='exit' or e['kind']=='door' and int(e['id'][-1])>stage}
  walk=F|{tuple(s['cell']) for s in S};reached=reach(start,walk-locked)
  assert tuple(by[prefix+f'p{stage+1}']['cell']) in reached
  for later in range(stage+2,4):assert tuple(by[prefix+f'p{later}']['cell']) not in reached,(n,'gate bypass',stage,later)
 safe=F-{tuple(e['cell']) for e in E if e['kind'] in ['door','exit']}
 for s in S:
  a,b=map(tuple,s['sides']);c=tuple(s['cell'])
  assert c not in F and set(near(c))&F=={a,b}
  assert b in reach(a,safe)
  walk=safe|{tuple(t['cell']) for t in S if t!=s}
  assert distance(a,b,walk)-2==s['minimum_saved_steps']>=12
  # Still useful after all doors have opened.
  assert distance(a,b,F|{tuple(t['cell']) for t in S if t!=s})-2>=12
 done=set();owned=set();current=start
 for step in read(T/f'route_level{n}.json'):
  e=by[step['id']];route=list(map(tuple,step['route']));assert route[0]==current
  locked={tuple(t['cell']) for t in E if t['kind'] in ['door','exit'] and t['id'] not in done}
  assert all(c in F-locked for c in route)
  assert all(b in near(a) for a,b in zip(route,route[1:]))
  assert route[-1] in near(tuple(e['cell'])) if e['kind']=='exit' else route[-1]==tuple(e['cell'])
  assert set(e.get('prerequisites',[]))<=done and set(e.get('requires',[]))<=owned
  done.add(e['id']);done.update(e.get('opens',[]));current=route[-1]
  if e['kind']=='pickup':owned.add(e['resource'])
 assert len(done)==17
 print('CHAPTER3',n,'GRAPH + ROUTE + 4 SAFE SHORTCUTS PASS')
# Constraints, independently enumerated from the written notes.
assert [v for v in permutations(range(4)) if v[0]==3 and v[3]==0 and abs(v[1]-v[3])!=1]==[(3,2,1,0)]
assert [v for v in product(range(13),repeat=4) if sum(v)==12 and v[1]==v[0]-1 and v[2]==v[0]+1 and v[3]==v[0]]==[(3,2,4,3)]
assert [v for v in product([False,True],repeat=4) if sum(v)==2 and v==(not v[1],v[2] and v[3],v[0],not v[0] and not v[2])]==[(True,False,True,False)]
e=next(e for e in read(D/'events13.json') if e.get('mode')=='cameras');solutions=[]
for angles in product(range(4),repeat=3):
 seen=set()
 for p,a in zip(e['cameras'],angles):
  dx,dy=[(0,-1),(1,0),(0,1),(-1,0)][a];x,y=p
  while True:
   x+=dx;y+=dy
   if not (0<=x<5 and 0<=y<5) or e['board'][y][x]=='#':break
   seen.add((x,y))
 if set(map(tuple,e['targets']))<=seen:solutions.append(angles)
assert solutions==[(1,3,0)]
print('CHAPTER3 UNIQUE CONSTRAINT SOLUTIONS PASS')
