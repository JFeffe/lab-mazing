"""Real maze reachability, both errand orders, puzzle uniqueness and return links."""
from pathlib import Path
from collections import deque
from itertools import product
import json
R=Path(__file__).resolve().parents[1];D=R/'data'
m=json.loads((D/'maze9.json').read_text());E=json.loads((D/'events9.json').read_text());by={e['id']:e for e in E};g=m['grid']
F={(x,y) for y,row in enumerate(g) for x,v in enumerate(row) if v}
def ns(c):return [p for p in [(c[0]-1,c[1]),(c[0]+1,c[1]),(c[0],c[1]-1),(c[0],c[1]+1)] if p in F]
def path(start,targets,blocks):
 q=deque([start]);prev={start:None}
 while q:
  c=q.popleft()
  if c in targets:
   out=[]
   while c is not None:out.append(c);c=prev[c]
   return out[::-1]
  for n in ns(c):
   if n not in prev and n not in blocks:prev[n]=c;q.append(n)
 return []
assert len(by)==len(E)==len({tuple(e['cell']) for e in E})
assert all(tuple(e['cell']) in F for e in E)
blocks={tuple(by[k]['cell']) for k in ['r_east','r_westdoor','r_northdoor','r_southdoor']}
for id in ['r_badges','r_seating','r_cables','r_wiring_note']:
 assert path(tuple(m['start']),{tuple(by[id]['cell'])},blocks),id
for id in ['r_agenda','r_schedule','r_conference']:
 assert not path(tuple(m['start']),{tuple(by[id]['cell'])},blocks),id
prefix=['r_welcome','r_badges','r_seat_note','r_president','r_secret1','r_seating']
suffix=['r_agenda','r_schedule_note','r_schedule_tip','r_secret2','r_schedule','r_cables','r_wiring_note','r_secret3','r_conference','r_final']
def route(order):
 current=tuple(m['start']);done=set();owned=set();steps=[]
 for id in order:
  e=by[id];c=tuple(e['cell']);blocked={tuple(t['cell']) for t in E if t['kind'] in ['door','exit'] and t['id'] not in done}
  cells=path(current,set(ns(c)) if e['kind']=='exit' else {c},blocked)
  assert cells,id
  assert set(e.get('requires',[]))<=owned,(id,'missing objects')
  assert set(e.get('prerequisites',[]))<=done,(id,'missing steps')
  current=cells[-1];steps.append({'id':id,'route':cells})
  done.add(id);done.update(e.get('opens',[]));owned-=set(e.get('requires',[]));owned.update(e.get('grants',{}))
  if e['kind']=='pickup':owned.add(e['resource'])
 assert len(done)==len(E)
 return steps
steps=route(prefix+suffix)
route(['r_cables','r_wiring_note','r_secret3']+prefix+suffix[:5]+suffix[-2:])
(R/'tests/route_level9.json').write_text(json.dumps(steps)+'\n')
def neighbour(a,b):return (a-b)%6 in (1,5)
def seated(v):return len(set(v))==6 and v[0]==0 and v[1]==3 and v[3]==(v[0]+1)%6 and v[4]==(v[3]+3)%6 and neighbour(v[5],v[1]) and not neighbour(v[5],v[4]) and not neighbour(v[2],v[3])
assert [v for v in product(range(6),repeat=6) if seated(v)]==[(0,3,5,1,4,2)]
def scheduled(v):
 slots=[s for i in range(4) for s in range(v[i],v[i]+[1,2,2,1][i])]
 return sorted(slots)==list(range(6)) and v[0]==0 and v[3]==5 and v[2]+2<=v[1]
assert [v for v in product(range(6),repeat=4) if scheduled(v)]==[(0,3,1,5)]
def trace(v,start):
 result=[start]
 while result[-1]<4:
  nxt=[3,2,4,5][v[result[-1]]]
  if nxt in result:return result+[nxt,-1]
  result.append(nxt)
 return result
assert [v for v in product(range(4),repeat=4) if len(set(v))==4 and trace(v,0)==[0,2,3,4] and trace(v,1)==[1,5]]==[(1,3,0,2)]
print('LEVEL9 GRAPH PASS: 20 events, four locks, both supply orders, all three puzzles unique;',sum(len(s['route'])-1 for s in steps),'base route steps')
S=json.loads((D/'shortcuts9.json').read_text())
if S and 'cell' in S[0]:
 safe=F-{tuple(e['cell']) for e in E if e['kind'] in ['door','exit']}
 for sc in S:
  a,b=map(tuple,sc['sides']);c=tuple(sc['cell']);assert c not in F
  assert set(ns(c))=={a,b}
  # Even all return links combined must stay on the same side of the growth barrier.
  original=F.copy();F.clear();F.update(safe|{tuple(t['cell']) for t in S if t!=sc})
  detour=path(a,{b},set());assert detour and len(detour)-3>=12
  F.clear();F.update(original)
  assert path(a,{b},set(original-safe)), 'Shortcut bypasses a lock'
 print('LEVEL9 SHORTCUTS PASS:',len(S),'links, each saves at least 12 steps')
