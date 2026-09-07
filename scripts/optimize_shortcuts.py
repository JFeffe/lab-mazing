"""Select useful return links, without crossing any puzzle barrier.

The benchmark follows existing test itineraries with complete map knowledge;
only shortcuts whose two sides have actually been walked may open. It is a
comparison of prescribed itineraries, not a prediction of a blind playthrough.
"""
from pathlib import Path
from collections import deque
import json,sys
R=Path(__file__).resolve().parents[1];D=R/'game/data'
DIRS=[(0,-1),(1,0),(0,1),(-1,0)]
def adjacent(c):return [(c[0]+dx,c[1]+dy) for dx,dy in DIRS]
def path(floor,start,targets,blocked=frozenset()):
 q=deque([start]);prev={start:None}
 while q:
  c=q.popleft()
  if c in targets:
   result=[]
   while c is not None:result.append(c);c=prev[c]
   return result[::-1]
  for v in adjacent(c):
   if v in floor and v not in blocked and v not in prev:prev[v]=c;q.append(v)
 return []
def distance(floor,a,b):
 p=path(floor,a,{b});return len(p)-1 if p else None

def load(n):
 suffix='' if n==1 else str(n)
 m=json.loads((D/f'maze{suffix}.json').read_text());ev=json.loads((D/f'events{suffix}.json').read_text());old=json.loads((D/f'shortcuts{suffix}.json').read_text())
 floors={(x,y) for y,row in enumerate(m['grid']) for x,v in enumerate(row) if v}
 barriers={tuple(e['cell']) for e in ev if e['kind'] in ['door','oneway','exit','creature']}
 safe=floors-barriers;components={};regions=[]
 for cell in sorted(safe):
  if cell in components:continue
  group={cell};q=deque([cell])
  while q:
   for v in adjacent(q.popleft()):
    if v in safe and v not in group:group.add(v);q.append(v)
  index=len(regions);regions.append(group);components.update({c:index for c in group})
 candidates=[]
 for y in range(1,len(m['grid'])-1):
  for x in range(1,len(m['grid'][y])-1):
   if (x,y) in floors:continue
   ns=[v for v in adjacent((x,y)) if v in floors]
   if len(ns)!=2 or ns[0][0]+ns[1][0]!=2*x or ns[0][1]+ns[1][1]!=2*y:continue
   a,b=ns
   if a not in components or b not in components or components[a]!=components[b]:continue
   detour=distance(safe,a,b)
   if detour<14:continue
   candidates.append(dict(cell=[x,y],sides=[list(a),list(b)],axis='x' if a[1]==b[1] else 'y',original_detour_steps=detour,component=components[a]))
 files=['route_oneway_a.json','route_oneway_b.json'] if n==1 else [f'route_level{n}.json']
 orders=[[s['id'] for s in json.loads((R/'game/tests'/f).read_text())] for f in files]
 if n==5:
  order=orders[0];west=[id for id in order if id in ['f_water_note','f_water_tip','f_secret1','f_dosing']];east=[id for id in order if id in ['f_tower_note','f_tower_tip','f_secret2','f_tower']]
  orders.append(order[:3]+east+west+order[11:])
 return dict(n=n,suffix=suffix,maze=m,events=ev,old=old,floors=floors,safe=safe,candidates=candidates,orders=orders,components=components)
def simulate(data,links,order,details=False):
 floor=set(data['floors']);by={e['id']:e for e in data['events']};done=set();walked={tuple(data['maze']['start'])};opened=set();pos=tuple(data['maze']['start']);steps=0;crossings={};legs=[]
 for id in order:
  e=by[id];c=tuple(e['cell']);blocked={tuple(t['cell']) for t in data['events'] if (t['kind'] in ['door','exit','creature'] and t['id'] not in done) or t['kind']=='oneway'}
  targets={v for v in adjacent(c) if v in floor} if c in blocked else {c}
  if e['kind']=='oneway':targets={tuple([c[0]-int(e['direction'][0]),c[1]-int(e['direction'][1])])}
  before=steps
  while pos not in targets:
   route=path(floor,pos,targets,blocked)
   assert route,(data['n'],id,pos)
   for pos in route[1:]:
    steps+=1;walked.add(pos)
    for i in opened:
     if pos==tuple(links[i]['cell']):crossings[i]=crossings.get(i,0)+1
    new=[i for i,s in enumerate(links) if i not in opened and all(tuple(v) in walked for v in s['sides'])]
    if new:
     for i in new:opened.add(i);floor.add(tuple(links[i]['cell']))
     break
  legs.append({'id':id,'steps':steps-before})
  done.add(id);done.update(e.get('opens',[]))
  if e['kind']=='oneway':pos=(c[0]+int(e['direction'][0]),c[1]+int(e['direction'][1]));walked.add(pos)
 return {'steps':steps,'opened':len(opened),'crossings':crossings,'legs':legs} if details else steps

def optimize(data):
 cs=data['candidates'];orders=data['orders'];safe=data['safe'];baseline=sum(simulate(data,[],o) for o in orders);selected=[]
 # Keep the existing number of shortcuts, but reject redundant parallel links.
 for _ in range(len(data['old'])):
  floor=safe|{tuple(s['cell']) for s in selected}
  choices=[]
  for c in cs:
   if c in selected or any(abs(c['cell'][0]-s['cell'][0])+abs(c['cell'][1]-s['cell'][1])<3 for s in selected):continue
   marginal=distance(floor,*map(tuple,c['sides']))-2
   if marginal<12:continue
   trial=selected+[c];network=safe|{tuple(s['cell']) for s in trial}
   if any(distance(network-{tuple(s['cell'])},*map(tuple,s['sides']))<14 for s in trial):continue
   cost=sum(simulate(data,trial,o) for o in orders)
   # Return itinerary savings first, then useful independent detour reduction.
   choices.append(((baseline-cost,marginal,c['original_detour_steps']),c,cost))
  assert choices,(data['n'],len(selected))
  _,best,cost=max(choices,key=lambda v:v[0]);selected.append(best)
 # Improve every slot while preserving a meaningful marginal benefit for all.
 for _ in range(2):
  changed=False
  for slot in range(len(selected)):
   current=sum(simulate(data,selected,o) for o in orders);best=current;replacement=None
   for c in cs:
    if c in selected:continue
    trial=selected.copy();trial[slot]=c
    if any(abs(c['cell'][0]-s['cell'][0])+abs(c['cell'][1]-s['cell'][1])<3 for i,s in enumerate(trial) if i!=slot):continue
    network=safe|{tuple(s['cell']) for s in trial}
    if any(distance(network-{tuple(s['cell'])},*map(tuple,s['sides']))<14 for s in trial):continue
    cost=sum(simulate(data,trial,o) for o in orders)
    if cost<best:best=cost;replacement=c
   if replacement:selected[slot]=replacement;changed=True
  if not changed:break
 selected.sort(key=lambda s:(s['cell'][1],s['cell'][0]))
 result=[];network=safe|{tuple(s['cell']) for s in selected}
 for old,s in zip(data['old'],selected):
  c={k:v for k,v in s.items() if k!='component'};c['id']=old['id'];c['minimum_saved_steps']=distance(network-{tuple(s['cell'])},*map(tuple,s['sides']))-2;result.append(c)
 return result
if __name__=='__main__':
 audit_path=R/'game/tests/shortcut_audit.json'
 previous=json.loads(audit_path.read_text()) if audit_path.exists() else []
 report=[]
 for n in range(1,6):
  data=load(n);new=optimize(data)
  original=next((row['before'] for row in previous if row['level']==n and row['after']==data['old']),data['old'])
  scores={label:[simulate(data,links,o,True) for o in data['orders']] for label,links in [('none',[]),('before',original),('after',new)]}
  print('LEVEL',n,'steps', {k:[x['steps'] for x in v] for k,v in scores.items()},'minimum savings',[s['minimum_saved_steps'] for s in new],flush=True)
  report.append(dict(level=n,before=original,after=new,benchmarks=scores))
  if '--write' in sys.argv:(D/f"shortcuts{data['suffix']}.json").write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n')
 if '--write' in sys.argv:audit_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
