"""Shared geometry and route authoring for chapter four."""
from pathlib import Path
from collections import deque
import json, random
R=Path(__file__).resolve().parents[1];D=R/'game/data';T=R/'game/tests'
en=json.loads((D/'en.json').read_text());aid=json.loads((D/'guidance.json').read_text());design={}
def tr(fr,eng):en[fr]=eng;return fr
def pair(fr,eng):return [fr,eng]
def save(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def neighbours(c):return [(c[0]+dx,c[1]+dy) for dx,dy in [(0,-1),(1,0),(0,1),(-1,0)]]
def path(a,targets,F):
 q=deque([a]);prev={a:None}
 while q:
  c=q.popleft()
  if c in targets:
   route=[]
   while c is not None:route.append(c);c=prev[c]
   return route[::-1]
  for n in neighbours(c):
   if n in F and n not in prev:prev[n]=c;q.append(n)
 return []
class Level:
 def __init__(self,n,title,layout,intro,outro):
  self.n=n;self.g=[[0]*35 for _ in range(35)];self.E=[];self.rng=random.Random(18000+n);self.title=tr(*title);self.layout=layout;self.intro=tr(*intro);self.outro=tr(*outro);self.sections=[];self.order=[];self.ranges=[]
 def rect(self,x0,x1,y0,y1,v=1):
  for y in range(y0,y1+1):
   for x in range(x0,x1+1):self.g[y][x]=v
 def maze(self,x0,x1,y0,y1):
  self.ranges.append((x0,x1,y0,y1));stack=[(x0,y0)];self.g[y0][x0]=1
  while stack:
   x,y=stack[-1];ns=[(x+dx,y+dy) for dx,dy in [(2,0),(-2,0),(0,2),(0,-2)] if x0<=x+dx<=x1 and y0<=y+dy<=y1 and not self.g[y+dy][x+dx]]
   if not ns:stack.pop();continue
   a,b=self.rng.choice(ns);self.g[(y+b)//2][(x+a)//2]=self.g[b][a]=1;stack.append((a,b))
 def event(self,id,kind,cell,ref,title,text,**kw):
  id=f'c{self.n}_{id}';e=dict(id=id,kind=kind,cell=list(cell),ref=str(ref),title=tr(*title),text=tr(*text),**kw);self.E.append(e)
  if kind!='door':self.order.append(id)
  return e
 def clue(self,id,cell,ref,title,text,secret=False):return self.event(id,'clue',cell,ref,title,text,**({'secret':True} if secret else {}))
 def puzzle(self,num,cell,title,text,mode,notes,solution,actions,**kw):
  id=f'c{self.n}_p{num}';e=self.event('p'+str(num),'mechanism',cell,(num+1)*100+3,title,text,puzzle_type='certainty',model='certainty',mode=mode,**kw)
  if num==1:e['requires']=[f'c{self.n}_kit']
  if num>1:e['prerequisites']=[f'c{self.n}_p{num-1}']
  if num<3:e['opens']=[f'c{self.n}_gate{num}']
  e['success']=tr('Validation enregistrée. '+['Le deuxième secteur est ouvert.','Le troisième secteur est ouvert.','Le passage de fin de niveau est autorisé.'][num-1], 'Approval recorded. '+['The second sector is open.','The third sector is open.','The final passage is authorised.'][num-1])
  aid['hints'][id]=[notes[0],notes[1],solution]
  aid['objectives'][id]=pair('Résoudre '+str((num+1)*100+3)+' : '+title[0]+'.','Solve '+str((num+1)*100+3)+': '+title[1]+'.')
  self.sections.append(dict(id=id,solution=solution[0],actions=actions,explanation=notes[1][0]));return e
 def finish(self,start,kit,welcome,secrets,gates,exitcell):
  self.start=start
  if self.n!=18:self.rect(max(1,exitcell[0]-2),min(33,exitcell[0]+2),max(1,exitcell[1]-2),min(33,exitcell[1]+2))
  self.event('welcome','clue',welcome,100,pair('Ordre de mission','Assignment order'),pair(self.layout,self.layout_en))
  self.event('kit','pickup',kit,101,pair('Mallette de service','Service kit'),pair('À installer au premier poste 203. Le matériel reste en place après les essais.','Install at the first station, 203. Equipment stays installed after trials.'),resource=f'c{self.n}_kit',amount=1,appearance='key')
  for i,(cell,axis) in enumerate(gates,1):self.event('gate'+str(i),'door',cell,110+i,pair('Sas de secteur '+str(i),'Sector gate '+str(i)),pair('Commande depuis le poste '+str((i+1)*100+3)+'.','Controlled from station '+str((i+1)*100+3)+'.'),axis=axis,controlled_by=f'c{self.n}_p{i}')
  for i,(cell,texts) in enumerate(secrets,1):self.clue('secret'+str(i),cell,500+i,pair('Note confidentielle '+str(i),'Confidential note '+str(i)),texts,True)
  self.event('exit','exit',exitcell,900,pair('Passage de service','Service passage'),pair('Les trois validations sont nécessaires. Votre bilan sera conservé.','All three approvals are required. Your results will be retained.'),prerequisites=[f'c{self.n}_p{i}' for i in [1,2,3]],action=tr('Terminer la mission','Complete the assignment'))
  F={(x,y) for y,row in enumerate(self.g) for x,v in enumerate(row) if v};blocked={tuple(e['cell']) for e in self.E if e['kind'] in ['door','exit']}
  assert all(tuple(e['cell']) in F for e in self.E),(self.n,'event in wall')
  assert len({tuple(e['cell']) for e in self.E})==len(self.E),(self.n,'overlap')
  # Shortcuts stay inside the same initially unlocked component; each has useful marginal savings.
  safe=F-blocked-{tuple(b['cell']) for e in self.E for b in e.get('world_gates',[])};components={};ci=0
  for c in sorted(safe):
   if c in components:continue
   q=[c];components[c]=ci
   for a in q:
    for b in neighbours(a):
     if b in safe and b not in components:components[b]=ci;q.append(b)
   ci+=1
  S=[];candidates=[]
  for y in range(1,34):
   for x in range(1,34):
    c=(x,y)
    if c in F:continue
    ns=[p for p in neighbours(c) if p in safe]
    if len(ns)!=2 or not (ns[0][0]==ns[1][0] or ns[0][1]==ns[1][1]) or components[ns[0]]!=components[ns[1]]:continue
    dist=len(path(ns[0],{ns[1]},safe))-1
    if dist>=14:candidates.append((dist,c,ns))
  for dist,c,ns in sorted(candidates,reverse=True):
   network=safe|{tuple(s['cell']) for s in S}|{c}
   if len(path(ns[0],{ns[1]},network-{c}))-3<12:continue
   if any(len(path(tuple(s['sides'][0]),{tuple(s['sides'][1])},network-{tuple(s['cell'])}))-3<12 for s in S):continue
   S.append(dict(id=f'C{self.n-15}{len(S)+1}',cell=list(c),axis='x' if ns[0][1]==ns[1][1] else 'y',sides=[list(v) for v in ns]))
   if len(S)==4:break
  for s in S:s['minimum_saved_steps']=len(path(tuple(s['sides'][0]),{tuple(s['sides'][1])},safe|{tuple(t['cell']) for t in S if t!=s}))-3
  # Select a complete walk in stages, including all clues and secrets as soon as reachable.
  done=set();current=tuple(start);route=[];remaining=[e for e in self.E if e['kind']!='door'];owned=set()
  while remaining:
   legal=[]
   locked={tuple(e['cell']) for e in self.E if e['kind'] in ['door','exit'] and e['id'] not in done}
   for e in remaining:
    if not set(e.get('prerequisites',[]))<=done or not set(e.get('requires',[]))<=owned:continue
    # Finish reading all reachable notes before completing the sector puzzle.
    targets={tuple(e['cell'])} if e['kind']!='exit' else set(neighbours(tuple(e['cell'])))
    p=path(current,targets,F-locked)
    if p:legal.append((0 if e['kind'] in ['clue','pickup'] else 1,len(p),e,p))
   assert legal,(self.n,'no reachable next event',[e['id'] for e in remaining])
   _,_,e,p=min(legal,key=lambda a:(a[0],a[1]));remaining.remove(e);current=p[-1];route.append(dict(id=e['id'],route=p));done.add(e['id']);done.update(e.get('opens',[]))
   if e['kind']=='pickup':owned.add(e['resource'])
  aid['objectives'][f'c{self.n}_kit']=pair('Récupérer la mallette 101 pour le poste 203.','Collect kit 101 for station 203.')
  aid['objectives'][f'c{self.n}_exit']=pair('Rejoindre le passage 900 et terminer la mission.','Reach passage 900 and complete the assignment.')
  aid['stages'][str(self.n)]=[[[f'c{self.n}_{k}'],f'c{self.n}_{k}'] for k in ['kit','p1','p2','p3','exit']]
  meta=dict(title=self.title,intro=self.intro,outro=self.outro,layout=tr(self.layout,self.layout_en),start=start,sections=self.sections)
  design[str(self.n)]=meta
  for name,data in [('maze',dict(grid=self.g,start=start)),('events',self.E),('shortcuts',S),('items',{e['resource']:dict(title=e['title'],text=e['text']) for e in self.E if e['kind']=='pickup'})]:save(D/f'{name}{self.n}.json',data)
  save(T/f'route_level{self.n}.json',route)
  print(self.n,self.title,len(self.E),'events',len(S),'shortcuts',sum(len(s['route'])-1 for s in route),'steps')
