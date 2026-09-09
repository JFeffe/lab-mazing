"""Verify useful marginal savings, gate safety and reproducible itinerary gains."""
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'))
from optimize_shortcuts import load,distance,simulate
report=json.loads((R/'game/tests/shortcut_audit.json').read_text())
for row in report:
 data=load(row['level']);links=row['after']
 # Historical v0.10 itinerary remains reproducible. Current additive links
 # are independently checked for every level by validate_return_links.py.
 current={s['id']:s for s in data['old']}
 for s in links:
  assert all(current[s['id']][k]==s[k] for k in ['cell','sides','axis'])
 assert len(links)==(8 if row['level']==1 else 6)
 assert len({s['id'] for s in links})==len(links)
 network=data['safe']|{tuple(s['cell']) for s in links}
 for s in links:
  a,b=map(tuple,s['sides']);c=tuple(s['cell'])
  assert c not in data['floors'] and data['components'][a]==data['components'][b]
  assert distance(data['safe'],a,b)==s['original_detour_steps']
  assert distance(network-{c},a,b)-2==s['minimum_saved_steps']>=12
  unlocked=(data['floors']|{tuple(v['cell']) for v in links})-{tuple(e['cell']) for e in data['events'] if e['kind']=='oneway'}
  assert distance(unlocked-{c},a,b)-2>=12
 for i,order in enumerate(data['orders']):
  for label,ss in [('none',[]),('before',row['before']),('after',links)]:
   assert simulate(data,ss,order)==row['benchmarks'][label][i]['steps']
  assert row['benchmarks']['after'][i]['steps']<row['benchmarks']['before'][i]['steps']
 print('LEVEL',row['level'],'SHORTCUT GRAPH + GATE SAFETY + BENCHMARK PASS')
