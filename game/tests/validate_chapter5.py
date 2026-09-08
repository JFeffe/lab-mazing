"""Independent topology, finite-state and clue-derived checks for the finale."""
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
all_events={}
for n in range(21,26):
 m,E,S=[read(D/f'{k}{n}.json') for k in ['maze','events','shortcuts']];by={e['id']:e for e in E};all_events.update(by)
 F={(x,y) for y,row in enumerate(m['grid']) for x,v in enumerate(row) if v};start=tuple(m['start']);prefix=f'c{n}_'
 assert len(by)==len(E)==len({tuple(e['cell']) for e in E})==(20 if n==21 else 17)
 assert sum(e.get('secret',False) for e in E)==3
 assert all(tuple(e['cell']) in F for e in E)
 for stage in range(3):
  locked={tuple(e['cell']) for e in E if e['kind']=='exit' or e['kind']=='door' and int(e['id'][-1])>stage}
  reached=reach(start,(F|{tuple(s['cell']) for s in S})-locked)
  assert tuple(by[prefix+f'p{stage+1}']['cell']) in reached,(n,stage,'missing access')
  for later in range(stage+2,4):assert tuple(by[prefix+f'p{later}']['cell']) not in reached,(n,'gate bypass',stage,later)
 safe=F-{tuple(e['cell']) for e in E if e['kind'] in ['door','exit']}-{tuple(b['cell']) for e in E for b in e.get('world_gates',[])}
 for s in S:
  a,b=map(tuple,s['sides']);c=tuple(s['cell'])
  assert c not in F and set(near(c))&F=={a,b} and b in reach(a,safe)
  assert distance(a,b,safe|{tuple(t['cell']) for t in S if t!=s})-2==s['minimum_saved_steps']>=12
  assert distance(a,b,F|{tuple(t['cell']) for t in S if t!=s})-2>=12
 done=set();owned=set();current=start;settings=[1,2,0];p1=by[prefix+'p1']
 for step in read(T/f'route_level{n}.json'):
  e=by[step['id']];route=list(map(tuple,step['route']));assert route[0]==current
  locked={tuple(t['cell']) for t in E if t['kind'] in ['door','exit'] and t['id'] not in done}
  if p1['id'] not in done:locked|={tuple(b['cell']) for b in p1.get('world_gates',[]) if settings[b['channel']] not in b['allowed']}
  assert all(c in F-locked for c in route),(n,e['id'],'blocked route')
  assert all(b in near(a) for a,b in zip(route,route[1:]))
  assert route[-1] in near(tuple(e['cell'])) if e['kind']=='exit' else route[-1]==tuple(e['cell'])
  assert set(e.get('prerequisites',[]))<=done and set(e.get('requires',[]))<=owned
  current=route[-1]
  if 'configure' in step:
   for a in step['configure']:settings=[(v+p1['masks'][a][i])%3 for i,v in enumerate(settings)]
   continue
  assert set(e.get('observations',[]))<=done
  done.add(e['id']);done.update(e.get('opens',[]))
  if e['kind']=='pickup':owned.add(e['resource'])
 assert len(done)==len(E)
 print('CHAPTER5',n,'TOPOLOGY + FULL ROUTE +',len(S),'SAFE SHORTCUTS PASS')

# Every gantry state is reachable and reversible, and only its matching physical
# opening reaches each alcove. No remote controls can strand someone (runtime).
m,E,S=[read(D/f'{k}21.json') for k in ['maze','events','shortcuts']];e=all_events['c21_p1'];F={(x,y) for y,row in enumerate(m['grid']) for x,v in enumerate(row) if v}|{tuple(s['cell']) for s in S}
fixed={tuple(t['cell']) for t in E if t['kind'] in ['door','exit']};by={t['id']:t for t in E}
for v in product(range(3),repeat=3):
 closed={tuple(b['cell']) for b in e['world_gates'] if v[b['channel']]!=0}
 seen=reach(tuple(e['cell']),F-fixed-closed)
 for i,id in enumerate(e['observations']):assert (tuple(by[id]['cell']) in seen)==(v[i]==0)
reachable={(0,0,0)};q=deque(reachable)
while q:
 v=q.popleft()
 for mask in e['masks']:
  nxt=tuple((a+b)%3 for a,b in zip(v,mask))
  if nxt not in reachable:reachable.add(nxt);q.append(nxt)
assert len(reachable)==27

# Derive solutions from narrative constraints, independently from targets/actions.
loads=[]
for v in product(range(1,4),repeat=5):
 totals=[sum(w for w,d in zip([1,2,3,4,6],v) if d==s) for s in [1,2,3]]
 if totals==[5,5,6] and v[2]==1 and v[0]==v[3] and v[4]==3:loads.append(v)
assert loads==[(2,1,1,2,3)]
assert [v for v in product(range(-2,3),repeat=3) if v[1]==-1 and v[0]-v[1]==3 and v[0]-v[2]==1]==[(2,-1,1)]
records=[(3,1),(3,-1),(2,2),(5,2),(0,-1)]
assert sorted(range(5),key=lambda i:records[i][0]-records[i][1])==[2,4,0,3,1]
groups=[]
for v in product(range(2),repeat=5):
 A,B,C,Dd,Ee=v
 if sum(v)==3 and Ee and (not A or C) and (not C or A) and (not B or Dd) and not(Dd and Ee):groups.append(v)
assert groups==[(1,0,1,0,1)]
policy=all_events['c23_p3'];valid=[]
for v in product(range(3),repeat=3):
 cases=[all(policy['clause_masks'][i][v[i]]&(1<<case) for i in range(3)) for case in range(5)]
 if cases==[True,False,False,False,False]:valid.append(v)
assert valid==[(1,1,1)]
d=all_events['c24_p2'];valid=[]
for v in product(range(2),repeat=4):
 # Odd incidence on all six channels, from wiring rather than solution data.
 if all(sum(v[i]*bool(d['masks'][i]&(1<<j)) for i in range(4))%2==1 for j in range(6)):valid.append(v)
assert valid==[(0,1,1,1)]
protocol=all_events['c24_p1'];orders=[p for p in permutations(range(5)) if all(p.index(dep)<p.index(i) for i,deps in enumerate(protocol['dependencies']) for dep in deps)]
assert orders==[(2,4,1,0,3)]

# Exhaustive oracle for the directed evidence graph (retain physical sources).
e=all_events['c22_p3'];outcomes={}
for v in product(range(2),repeat=6):
 def cyclic():
  matrix=[[False]*6 for _ in range(6)]
  for i,(a,b) in enumerate(e['edges']):matrix[a][b]=not v[i]
  for k in range(6):
   for a in range(6):
    for b in range(6):matrix[a][b]|=matrix[a][k] and matrix[k][b]
  return any(matrix[i][i] for i in range(6))
 outcomes[''.join(map(str,v))]=sum(v)==2 and not any(v[i] for i in e['protected']) and not cyclic()
assert [k for k,v in outcomes.items() if v]==['001001']

# Shortest-path search for the two capsule programs, with persistent visited and
# forbidden cells, independently of the GDScript path simulator.
solutions=read(T/'chapter5_solutions.json')
for eid in ['c21_p3','c24_p3']:
 e=all_events[eid];boards=e['boards'];start=tuple(tuple(x) for x in e['starts'])+(0,);q=deque([(start,[])]);seen={start};best=None
 while q:
  state,actions=q.popleft();positions=state[:-1];mask=state[-1]
  if all(p==tuple(t) for p,t in zip(positions,e['goals'])) and mask==(1<<len(boards))-1:best=actions;break
  for action,(dx,dy) in enumerate([(0,-1),(1,0),(0,1),(-1,0)]):
   new=[];visited=mask;safe=True
   for i,p in enumerate(positions):
    nxt=(p[0]+dx*(-1 if i==1 else 1),p[1]+dy)
    if not(0<=nxt[0]<5 and 0<=nxt[1]<5) or boards[i][nxt[1]][nxt[0]]=='#':nxt=p
    if boards[i][nxt[1]][nxt[0]]=='X':safe=False
    if nxt==tuple(e['checkpoints'][i]):visited|=1<<i
    new.append(nxt)
   key=tuple(new)+(visited,)
   if safe and key not in seen:seen.add(key);q.append((key,actions+[action]))
 assert best is not None and len(best)<=e['max_commands']
 authored=next(p['actions'] for p in solutions[eid[1:3]] if p['id']==eid)
 assert best==authored[:-1],(eid,best,authored)
 print(eid,'CAPSULE BFS shortest path',len(best),'PASS')
save={'feedback':outcomes,'gantry_states':[list(v) for v in sorted(reachable)],'manifest':loads,'policy':[(1,1,1)]}
(T/'chapter5_oracle.json').write_text(json.dumps(save,indent=2)+'\n')
print('CHAPTER5 INDEPENDENT CONSTRAINTS: 27 gantry states, unique manifest/clocks/chronology/quorum/policy/protocol/relays, 64 feedback graphs PASS')
