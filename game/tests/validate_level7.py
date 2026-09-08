"""Real maze reachability, both errand orders, puzzle uniqueness and return links."""
from pathlib import Path
from collections import deque
from itertools import product
import json
R=Path(__file__).resolve().parents[1];D=R/'data'
m=json.loads((D/'maze7.json').read_text());E=json.loads((D/'events7.json').read_text());by={e['id']:e for e in E};g=m['grid']
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
blocks={tuple(by[k]['cell']) for k in ['p_archive_door','p_copy_door','p_delivery']}
for id in ['p_layers','p_overlay','p_overlay_note']:
 assert path(tuple(m['start']),{tuple(by[id]['cell'])},blocks),id
for id in ['p_files','p_filing','p_paper','p_copier']:
 assert not path(tuple(m['start']),{tuple(by[id]['cell'])},blocks),id
prefix=['p_welcome','p_layers','p_overlay_note','p_overlay_tip','p_secret1','p_overlay']
suffix=['p_valid_note','p_files','p_old_note','p_secret2','p_filing','p_paper','p_secret3','p_copy_note','p_toner','p_copier','p_delivery']
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
route(prefix+suffix[:5]+['p_toner','p_copy_note','p_secret3','p_paper']+suffix[-2:])
(R/'tests/route_level7.json').write_text(json.dumps(steps)+'\n')
def rotate(a):return [a[(2-x)*3+y] for y in range(3) for x in range(3)]
def mirror(a):return [a[y*3+2-x] for y in range(3) for x in range(3)]
def overlay(s):
 out=[0]*9
 for a,n in zip(by['p_overlay']['masks'],s):
  for _ in range(n):a=rotate(a)
  out=[int(x or y) for x,y in zip(out,a)]
 return out
assert [s for s in product(range(4),repeat=3) if overlay(s)==by['p_overlay']['target']]==[(1,3,2)]
assert [s for s in product(range(4),repeat=4) if len(set(s))==4 and s[1]==s[2]+1 and s[0]>s[1] and s[3]==0]==[(3,2,1,0)]
initial=by['p_copier']['initial'];target=by['p_copier']['target']
assert mirror(rotate(initial))==target and initial!=target and rotate(initial)!=target and mirror(initial)!=target
states={tuple(initial):[]};q=deque([initial])
while q:
 a=q.popleft()
 for name,op in [('rotation',rotate),('miroir',mirror)]:
  v=op(a)
  if tuple(v) not in states:states[tuple(v)]=states[tuple(a)]+[name];q.append(v)
assert len(states)==8 and len(states[tuple(target)])==2
for a in states:
 assert rotate(rotate(rotate(rotate(a))))==list(a) and mirror(mirror(a))==list(a)
print('LEVEL7 GRAPH PASS: 19 events, two gated wings, both supply orders, unique overlay/filing solutions, 8 reversible copier images;',sum(len(s['route'])-1 for s in steps),'base route steps')
S=json.loads((D/'shortcuts7.json').read_text())
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
 print('LEVEL7 SHORTCUTS PASS:',len(S),'links, each saves at least 12 steps')
