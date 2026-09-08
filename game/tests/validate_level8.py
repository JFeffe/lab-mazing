"""Real maze reachability, both errand orders, puzzle uniqueness and return links."""
from pathlib import Path
from collections import deque
from itertools import product
import json
R=Path(__file__).resolve().parents[1];D=R/'data'
m=json.loads((D/'maze8.json').read_text());E=json.loads((D/'events8.json').read_text());by={e['id']:e for e in E};g=m['grid']
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
blocks={tuple(by[k]['cell']) for k in ['m_network_door','m_dispatch_door','m_delivery']}
for id in ['m_parcels','m_balance','m_balance_note']:
 assert path(tuple(m['start']),{tuple(by[id]['cell'])},blocks),id
for id in ['m_capsule','m_network','m_label','m_address']:
 assert not path(tuple(m['start']),{tuple(by[id]['cell'])},blocks),id
prefix=['m_welcome','m_parcels','m_balance_note','m_balance_tip','m_secret1','m_balance']
suffix=['m_capsule','m_network_note','m_network_tip','m_secret2','m_network','m_label','m_secret3','m_directory','m_relocation','m_address','m_delivery']
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
route(prefix+suffix[:5]+['m_relocation','m_directory','m_secret3','m_label']+suffix[-2:])
(R/'tests/route_level8.json').write_text(json.dumps(steps)+'\n')
# Two equal-size comparisons identify any one heavier parcel, not merely the authored E.
for heavy in range(6):
 weights=[11 if i==heavy else 10 for i in range(6)]
 group=[0,1,2] if sum(weights[:3])>sum(weights[3:]) else [3,4,5]
 a,b,c=group
 answer=a if weights[a]>weights[b] else b if weights[b]>weights[a] else c
 assert answer==heavy
assert by['m_balance']['heavy']==4
# Each wrong junction returns the reusable capsule; only one setting reaches dispatch.
def trace(s):
 if s[0]==0:return [0,1,2]
 if s[1]==1:return [0,1,3,4]
 return [0,1,3,5,7 if s[2]==1 else 6]
assert [s for s in product(range(2),repeat=3) if trace(s)[-1]==7]==[(1,0,1)]
assert by['m_address']['target']==[1,2,3]
print('LEVEL8 GRAPH PASS: 19 events, two locks, both dispatch errand orders, all 6 heavier-parcel cases, unique network route;',sum(len(s['route'])-1 for s in steps),'base route steps')
S=json.loads((D/'shortcuts8.json').read_text())
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
 print('LEVEL8 SHORTCUTS PASS:',len(S),'links, each saves at least 12 steps')
