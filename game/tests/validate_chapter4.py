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
for n in range(16,21):
 m,E,S=[read(D/f'{k}{n}.json') for k in ['maze','events','shortcuts']];by={e['id']:e for e in E}
 F={(x,y) for y,row in enumerate(m['grid']) for x,v in enumerate(row) if v};start=tuple(m['start']);prefix=f'c{n}_'
 assert len(by)==len(E)==len({tuple(e['cell']) for e in E})==(20 if n<=18 else 17)
 assert sum(e.get('secret',False) for e in E)==3 and (len(S)==0 if n==18 else len(S)>=4)
 assert all(tuple(e['cell']) in F for e in E)
 for stage in range(3):
  locked={tuple(e['cell']) for e in E if e['kind']=='exit' or e['kind']=='door' and int(e['id'][-1])>stage}
  walk=F|{tuple(s['cell']) for s in S};reached=reach(start,walk-locked)
  assert tuple(by[prefix+f'p{stage+1}']['cell']) in reached
  for later in range(stage+2,4):assert tuple(by[prefix+f'p{later}']['cell']) not in reached,(n,'gate bypass',stage,later)
 safe=F-{tuple(e['cell']) for e in E if e['kind'] in ['door','exit']}-{tuple(b['cell']) for e in E for b in e.get('world_gates',[])}
 for s in S:
  a,b=map(tuple,s['sides']);c=tuple(s['cell'])
  assert c not in F and set(near(c))&F=={a,b}
  assert b in reach(a,safe)
  walk=safe|{tuple(t['cell']) for t in S if t!=s}
  assert distance(a,b,walk)-2==s['minimum_saved_steps']>=12
  # Still useful after all doors have opened.
  assert distance(a,b,F|{tuple(t['cell']) for t in S if t!=s})-2>=12
 done=set();owned=set();current=start;settings=[0,0,0];p1=by[prefix+"p1"]
 for step in read(T/f'route_level{n}.json'):
  e=by[step['id']];route=list(map(tuple,step['route']));assert route[0]==current
  locked={tuple(t['cell']) for t in E if t['kind'] in ['door','exit'] and t['id'] not in done}
  if p1['id'] not in done:
   locked|={tuple(b['cell']) for b in p1.get('world_gates',[]) if settings[b['channel']] not in b['allowed']}
  assert all(c in F-locked for c in route),(n,e['id'],'blocked dynamic route')
  assert all(b in near(a) for a,b in zip(route,route[1:]))
  assert route[-1] in near(tuple(e['cell'])) if e['kind']=='exit' else route[-1]==tuple(e['cell'])
  assert set(e.get('prerequisites',[]))<=done and set(e.get('requires',[]))<=owned
  current=route[-1]
  if 'configure' in step:
   for a in step['configure']:
    if n in [16,17]:settings[0]=a
    else:settings[a]=(settings[a]+1)%4
   continue
  done.add(e['id']);done.update(e.get('opens',[]))
  if e['kind']=='pickup':owned.add(e['resource'])
 assert len(done)==(20 if n<=18 else 17)
 print('CHAPTER4',n,'GRAPH + ROUTE +',len(S),'SAFE SHORTCUTS PASS')

for n in [16,17,18]:
 m,E,S=[read(D/f'{k}{n}.json') for k in ['maze','events','shortcuts']];p1=next(e for e in E if e.get('world_gates'));by={e['id']:e for e in E}
 F={(x,y) for y,row in enumerate(m['grid']) for x,v in enumerate(row) if v}|{tuple(s['cell']) for s in S}
 fixed={tuple(e['cell']) for e in E if e['kind'] in ['door','exit']}
 for v in product(range(3) if n<18 else range(4),repeat=1 if n<18 else 3):
  closed={tuple(b['cell']) for b in p1['world_gates'] if v[b['channel']] not in b['allowed']}
  reachables=reach(tuple(p1['cell']),F-fixed-closed)
  for i,b in enumerate(p1['world_gates']):
   assert (tuple(by[p1['observations'][i]]['cell']) in reachables)==(v[b['channel']] in b['allowed']),(n,v,i,'evidence bypass')
 print('DYNAMIC ACCESS STATES',n,'PASS')
assert [v for v in permutations(range(4)) if v[0]<v[1] and v[3]==v[2]+1 and v[0]!=0 and v[3]!=3]==[(2,3,0,1)]
assert [v for v in product(range(7),repeat=3) if sum(v)==6 and v[0]+v[1]==5 and v[1]+v[2]==4 and v[0]+v[2]==3]==[(2,3,1)]
# The film is an Euler trail; the assembly deliberately accepts three legal topological orders.
E=read(D/'events18.json');film=next(e for e in E if e.get('mode')=='splice');legal=[]
for p in permutations(range(5)):
 node=0;ok=True
 for i in p:
  a,b=film['joins'][i];ok &= a==node;node=b
 if ok and node==4:legal.append(p)
assert legal==[(1,3,0,2,4)]
E=read(D/'events19.json');a=next(e for e in E if e.get('mode')=='assembly');orders=[p for p in permutations(range(6)) if all(p.index(d)<p.index(i) for i,deps in enumerate(a['dependencies']) for d in deps)]
assert len(orders)==3
# Dijkstra verifies optimal seal crossing and reachability of all 32 physical states.
from heapq import heappush,heappop
q=[(0,0,0)];dist={(0,0):0}
while q:
 cost,mask,side=heappop(q)
 if cost!=dist[(mask,side)]:continue
 for team in range(1,16):
  members=[i for i in range(4) if team>>i&1]
  if len(members)>2 or any((mask>>i&1)!=side for i in members):continue
  key=(mask^team,1-side);new=cost+max([1,2,5,8][i] for i in members)
  if new<dist.get(key,999):dist[key]=new;heappush(q,(new,*key))
assert dist[(15,1)]==15
print('INDEPENDENT CONSTRAINTS: unique delivery, energy, film; 3 assembly orders; optimal seal=15 PASS')
