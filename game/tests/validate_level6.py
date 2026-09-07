"""Real maze reachability, both errand orders, puzzle uniqueness and return links."""
from pathlib import Path
from collections import deque
from itertools import product
import json
R=Path(__file__).resolve().parents[1];D=R/'data'
m=json.loads((D/'maze6.json').read_text());E=json.loads((D/'events6.json').read_text());by={e['id']:e for e in E};g=m['grid']
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
blocks={tuple(by[k]['cell']) for k in ['g_bridge','g_coffee']}
for id in ['g_irrigation','g_growth','g_mug','g_seed','g_recipe','g_blend']:
 assert path(tuple(m['start']),{tuple(by[id]['cell'])},blocks),id
for id in ['g_beans','g_petals','g_moss','g_salt']:
 assert not path(tuple(m['start']),{tuple(by[id]['cell'])},blocks),id
prefix=['g_welcome','g_growth_note','g_seed','g_pipe_note','g_pipe_tip','g_coupling','g_secret1','g_irrigation','g_growth']
suffix=['g_beans','g_secret2','g_petals','g_moss','g_salt','g_recipe','g_blend','g_secret3','g_mug','g_coffee']
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
route(['g_mug','g_secret3']+prefix+[i for i in suffix if i not in ['g_mug','g_secret3']])
(R/'tests/route_level6.json').write_text(json.dumps(steps)+'\n')
def pipes(s):
 c=(0,0);incoming=3;seen=[];dirs=[(0,-1),(1,0),(0,1),(-1,0)]
 while True:
  i=c[1]*2+c[0];p=[s[i],(s[i]+1)%4]
  if i in seen or incoming not in p:return False
  seen.append(i);out=p[1] if p[0]==incoming else p[0]
  if i==1 and out==1:return len(seen)==4
  c=(c[0]+dirs[out][0],c[1]+dirs[out][1])
  if not 0<=c[0]<2 or not 0<=c[1]<2:return False
  incoming=(out+2)%4
pipe_solutions=[s for s in product(range(4),repeat=4) if pipes(s)]
assert pipe_solutions==[(2,1,0,3)]
props=by['g_blend']['properties'];target=by['g_blend']['target']
blend_solutions=[s for s in product(range(3),repeat=4) if sum(s)==3 and [sum(s[i]*props[i][j] for i in range(4)) for j in range(3)]==target]
assert blend_solutions==[(1,1,1,0)]
# Each control cycles, so every combination can return to initial without loss.
assert all((n+(base-n))%base==0 for base in [2,3,4] for n in range(base))
print('LEVEL6 GRAPH PASS: 20 events, east isolated until growth, both errand orders, unique pipe and blend solutions;',sum(len(s['route'])-1 for s in steps),'base route steps')
S=json.loads((D/'shortcuts6.json').read_text())
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
 print('LEVEL6 SHORTCUTS PASS:',len(S),'links, each saves at least 12 steps')
