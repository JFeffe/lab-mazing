"""Independent checks of all current doors, additive compatibility and real gains."""
from pathlib import Path
from collections import deque
import json

R=Path(__file__).resolve().parents[2];D=R/'game/data'
read=lambda p:json.loads(p.read_text())
audit=read(R/'game/tests/return_links_audit.json')
endings=read(D/'endings.json');collectibles=read(D/'collectibles.json')

def adjacent(c):
 return [(c[0]+dx,c[1]+dy) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]]

def flood(floor,start):
 q=deque([start]);dist={start:0}
 while q:
  c=q.popleft()
  for p in adjacent(c):
   if p in floor and p not in dist:dist[p]=dist[c]+1;q.append(p)
 return dist

total=added=0
assert [r['level'] for r in audit['levels']]==list(range(1,26))
for row in audit['levels']:
 n=row['level'];suffix='' if n==1 else str(n)
 m,E,S=[read(D/f'{k}{suffix}.json') for k in ['maze','events','shortcuts']]
 assert S==row['after']
 by={s['id']:s for s in S};assert len(by)==len(S)==len({tuple(s['cell']) for s in S})
 old_ids={s['id'] for s in row['before']}
 assert set(row['added_ids'])==set(by)-old_ids
 for old in row['before']:
  assert all(by[old['id']][k]==old[k] for k in ['cell','sides','axis']),('relocated save ID',n,old)
 for e in E:
  if e['id']==endings[str(n)]['id']:e['cell']=endings[str(n)]['cell']
 events={e['id']:e for e in E}
 F={(x,y) for y,line in enumerate(m['grid']) for x,v in enumerate(line) if v}
 locks={tuple(e['cell']) for e in E if e['kind'] in ['door','exit','oneway','creature']}
 locks|={tuple(g['cell']) for e in E for g in e.get('world_gates',[])}
 if n==10:locks|={(x,y) for y in [4,7,10] for x in range(13,22)}
 safe=F-locks
 full=(F|{tuple(s['cell']) for s in S})-{tuple(e['cell']) for e in E if e['kind']=='oneway'}
 for s in S:
  c=tuple(s['cell']);a,b=map(tuple,s['sides'])
  assert c not in F and set(adjacent(c))&F=={a,b}
  assert a[0]+b[0]==2*c[0] and a[1]+b[1]==2*c[1]
  assert s['axis']==('x' if a[1]==b[1] else 'y')
  assert a in safe and b in flood(safe,a),(n,s['id'],'bypasses fixed/variable barrier')
  assert not {a,b}&{tuple(e['cell']) for e in collectibles[str(n)]}
  saved=flood(full-{c},a)[b]-2
  assert saved==s['fully_open_saved_steps']>=(12 if s['id'] in old_ids else 20)
  if s['id'] not in old_ids:
   example=s['return_example'];assert example
   start=tuple(events[example['origin']]['cell']);target=tuple(events[example['target']]['cell'])
   target_event=events[example['target']]
   assert target_event['kind'] in ['mechanism','craft','exit','creature'] or (target_event['kind']=='door' and ('answer' in target_event or 'requires' in target_event))
   assert flood(full-{c},start)[target]==example['before']
   assert flood(full,start)[target]==example['after']
   assert example['before']-example['after']==example['saved']>=20
 total+=len(S);added+=len(row['added_ids'])
 print(f'RETURNS {n:02}: {len(S)} safe doors / {len(row["added_ids"])} added / save IDs preserved')
assert added>0
print(f'RETURN AUDIT PASS: {total} doors, {added} added, minimum new saving 20 steps')
