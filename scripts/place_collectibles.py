"""Deterministic, audited optional rewards. Never changes maze or puzzle data."""
from pathlib import Path
from collections import deque
import json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'game/data'
DIRS=[(0,-1),(1,0),(0,1),(-1,0)]
def distances(adj,starts):
 d={c:0 for c in starts if c in adj};q=deque(d)
 while q:
  c=q.popleft()
  for nxt in adj[c]:
   if nxt not in d:d[nxt]=d[c]+1;q.append(nxt)
 return d
def layout(n):
 suffix='' if n==1 else str(n)
 m=json.loads((D/f'maze{suffix}.json').read_text());E=json.loads((D/f'events{suffix}.json').read_text());S=json.loads((D/f'shortcuts{suffix}.json').read_text())
 ending=json.loads((D/'endings.json').read_text())[str(n)]
 for e in E:
  if e['id']==ending['id']:e['cell']=ending['cell']
 cells={(x,y) for y,row in enumerate(m['grid']) for x,v in enumerate(row) if v}
 adj={c:[(c[0]+dx,c[1]+dy) for dx,dy in DIRS if (c[0]+dx,c[1]+dy) in cells] for c in cells}
 occupied={tuple(e['cell']) for e in E}|{tuple(m['start'])}
 for e in E:
  for gate in e.get('world_gates',[]):occupied.add(tuple(gate['cell']))
 # Movable archive crossing and narrative props that occupy floor cells.
 if n==10:occupied|={(17,17),(17,18),(17,19),(17,20),(17,21)}
 if n==20:occupied|={(5,5),(29,5),(5,29),(29,29)}
 if n==23:occupied|={(5,5),(17,5),(29,5),(15,15),(19,15)}
 if n==25:occupied|={(20,30),(11,26),(23,26),(11,32),(23,32)}
 return m,E,S,adj,occupied

def choose(n):
 m,E,S,adj,occupied=layout(n);dist=distances(adj,occupied)
 shortcut_sides={tuple(c) for s in S for c in s['sides']}
 candidates=[]
 for c in sorted(adj,key=lambda c:(c[1],c[0])):
  if c in occupied or c in shortcut_sides:continue
  euclid=min(abs(c[0]-x)+abs(c[1]-y) for x,y in occupied)
  if euclid<3 or dist[c]<5:continue
  trail=[c];cur=c;prev=None
  if len(adj[c])==1:
   while len(adj[cur])<3:
    nxt=[v for v in adj[cur] if v!=prev]
    if not nxt:break
    prev,cur=cur,nxt[0];trail.append(cur)
  clear=len(trail)>1 and not any(v in occupied for v in trail[:-1])
  depth=len(trail)-1 if clear else 0
  kind='impasse' if clear else 'recoin'
  # Alternate rewards only in quiet, low-degree side corridors/corners.
  if not clear and len(adj[c])>3:continue
  candidates.append(dict(cell=list(c),depth=depth,event_distance=dist[c],clearance=euclid,type=kind,branch=[list(v) for v in trail]))
 chosen=[];remaining=candidates[:];spreads=[]
 while len(chosen)<10:
  def score(e):
   c=tuple(e['cell']);spread=min((d.get(c,1000) for d in spreads),default=35)
   return (int(e['type']=='impasse'), e['depth']*6+min(e['event_distance'],30)*2+min(spread,35),e['event_distance'],-c[1],-c[0])
  eligible=[e for e in remaining if all(abs(e['cell'][0]-v['cell'][0])+abs(e['cell'][1]-v['cell'][1])>=4 and spreads[i][tuple(e['cell'])]>=8 for i,v in enumerate(chosen))]
  if not eligible:raise RuntimeError(f'Cannot place ten spaced rewards in level {n}')
  pick=max(eligible,key=score);chosen.append(pick);spreads.append(distances(adj,[tuple(pick["cell"])]));remaining.remove(pick)
 chosen.sort(key=lambda e:(e['cell'][1],e['cell'][0]))
 for i,e in enumerate(chosen,1):e.update(id=f'collection_{n:02d}_{i:02d}',ref=f'K{i:02d}',chapter=(n-1)//5+1,level=n)
 return chosen,hashlib.sha256(json.dumps(m,sort_keys=True).encode()).hexdigest()

def main():
 all_data={};audit={}
 for n in range(1,26):
  selected,sha=choose(n);all_data[str(n)]=selected;audit[str(n)]={'maze_sha256':sha,'count':len(selected),'dead_ends':sum(e['type']=='impasse' for e in selected),'min_event_distance':min(e['event_distance'] for e in selected),'min_clearance':min(e['clearance'] for e in selected)}
  print(n,audit[str(n)])
 (D/'collectibles.json').write_text(json.dumps(all_data,ensure_ascii=False,indent=2)+'\n')
 (R/'game/tests/collectible_placement_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
if __name__=='__main__':main()
