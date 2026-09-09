"""Independent checks of authored rewards against the unmodified walkable map."""
from pathlib import Path
from collections import deque
import json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'data'
read=lambda p:json.loads(p.read_text())
placements=read(D/'collectibles.json');audit=read(R/'tests/collectible_placement_audit.json');endings=read(D/'endings.json')
def bfs(start,cells):
 q=deque([start]);dist={start:0}
 while q:
  x,y=q.popleft()
  for c in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if c in cells and c not in dist:dist[c]=dist[x,y]+1;q.append(c)
 return dist
ids=set();total_dead=0
for n in range(1,26):
 suffix='' if n==1 else str(n);m=read(D/f'maze{suffix}.json');events=read(D/f'events{suffix}.json');shortcuts=read(D/f'shortcuts{suffix}.json');items=placements[str(n)]
 assert len(items)==10
 assert hashlib.sha256(json.dumps(m,sort_keys=True).encode()).hexdigest()==audit[str(n)]['maze_sha256'],'Maze changed; placements require review'
 for e in events:
  if e['id']==endings[str(n)]['id']:e['cell']=endings[str(n)]['cell']
 cells={(x,y) for y,row in enumerate(m['grid']) for x,v in enumerate(row) if v};occupied={tuple(e['cell']) for e in events}|{tuple(m['start'])}|{tuple(g['cell']) for e in events for g in e.get('world_gates',[])}
 # No secret passage is required. Physical doors can open after their normal puzzles.
 reach=bfs(tuple(m['start']),cells);maps={tuple(e['cell']):bfs(tuple(e['cell']),cells) for e in items}
 for i,e in enumerate(items):
  c=tuple(e['cell']);assert c in reach and c not in occupied and e['id'] not in ids;ids.add(e['id'])
  assert min(abs(c[0]-p[0])+abs(c[1]-p[1]) for p in occupied)>=3
  assert min(maps[c].get(p,10000) for p in occupied)>=5
  assert c not in {tuple(side) for s in shortcuts for side in s['sides']}
  for other in items[i+1:]:
   p=tuple(other['cell']);assert maps[c][p]>=8 and abs(c[0]-p[0])+abs(c[1]-p[1])>=4
  if e['type']=='impasse':
   neighbors=lambda p:[v for v in [(p[0]-1,p[1]),(p[0]+1,p[1]),(p[0],p[1]-1),(p[0],p[1]+1)] if v in cells]
   assert len(neighbors(c))==1
   branch=list(map(tuple,e['branch']));assert branch[0]==c and len(branch)-1==e['depth']
   assert not set(branch[:-1])&occupied
   assert all(b in neighbors(a) for a,b in zip(branch,branch[1:]));assert all(len(neighbors(a))<=2 for a in branch[:-1])
   total_dead+=1
 print(f'COLLECTIBLES {n:02d}: ten reachable, spaced, no content overlap, original maze hash')
assert len(ids)==250
print(f'PASS: {total_dead} empty dead ends, {250-total_dead} quiet corners; 25 original maze hashes')
