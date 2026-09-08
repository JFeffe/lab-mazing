"""Deterministic three-wing finale. Run to regenerate the authored JSON."""
from pathlib import Path
import json, random
D=Path(__file__).resolve().parents[1]/'game/data'
rng=random.Random(90517); g=[[0]*35 for _ in range(35)]
regions=[(1,13,13,33),(21,33,13,33),(1,33,1,9)]
for x0,x1,y0,y1 in regions:
 stack=[(x0,y0)];g[y0][x0]=1
 while stack:
  x,y=stack[-1];ns=[(x+dx,y+dy) for dx,dy in [(2,0),(-2,0),(0,2),(0,-2)] if x0<=x+dx<=x1 and y0<=y+dy<=y1 and not g[y+dy][x+dx]]
  if not ns:stack.pop();continue
  a,b=rng.choice(ns);g[(b+y)//2][(a+x)//2]=g[b][a]=1;stack.append((a,b))
# Central atrium, west/east links, and a single locked north entrance.
for y in range(13,22):
 for x in range(15,20):g[y][x]=1
for x in range(13,22):g[17][x]=1
for y in range(9,14):g[y][17]=1
for y in range(1,4):
 for x in range(15,20):g[y][x]=1
S=[]
for bounds in regions:
 x0,x1,y0,y1=bounds;candidates=[]
 for y in range(y0+1,y1):
  for x in range(x0+1,x1):
   if g[y][x]:continue
   for dx,dy,axis in [(1,0,'x'),(0,1,'y')]:
    if g[y-dy][x-dx] and g[y+dy][x+dx] and not g[y-dx][x-dy] and not g[y+dx][x+dy]:candidates.append((x,y,dx,dy,axis))
 rng.shuffle(candidates)
 for x,y,dx,dy,axis in candidates[:2]:S.append(dict(id='F'+str(len(S)+1),cell=[x,y],sides=[[x-dx,y-dy],[x+dx,y+dy]],axis=axis))
en=json.loads((D/'en.json').read_text());E=[]
def tr(fr,english):en[fr]=english;return fr
def event(id,kind,cell,ref,title,text,**kw):
 E.append(dict(id=id,kind=kind,cell=cell,ref=str(ref),title=tr(*title),text=tr(*text),**kw));return E[-1]
def prose(e,**fields):
 for k,v in fields.items():e[k]=tr(*v)
event('f_welcome','clue',[17,19],100,('Le défi impossible','The impossible challenge'),('Le prototype ZÉRO attend une charge de refroidissement à l’ouest et un noyau intact à l’est. Rapportez les deux à la station 103 du hall. L’aile nord contient le stabilisateur final. Les deux premières ailes peuvent être explorées dans n’importe quel ordre.','Prototype ZERO needs coolant from the west and an intact core from the east. Bring both to station 103 in the hall. The north wing houses the final stabilizer. Explore the first two wings in either order.'))
event('f_seal','pickup',[19,21],101,('Joint de transfert','Transfer seal'),('Ce joint réutilisable rend la station de dosage 203 étanche. Installez-le une seule fois ; remplir et vider les réservoirs ne consomme aucun objet.','This reusable seal makes dosing station 203 watertight. Install it once; filling and emptying tanks consumes no objects.'),resource='transfer_seal',amount=1,appearance='artifact')
event('f_hall_note','clue',[15,13],102,('Plan du prototype','Prototype plan'),('OUEST : doser le refroidissement. EST : déplacer le noyau sans l’écraser. HALL : assembler la cartouche. NORD : orienter les rotors. Aucune minuterie ; les expériences sont réinitialisables.','WEST: measure the coolant. EAST: move the core without crushing it. HALL: assemble the cartridge. NORTH: align the rotors. No timer; experiments can be reset.'))
e=event('f_assembly','craft',[17,15],103,('Station de couplage','Coupling station'),('Installez la charge de 4 litres et le noyau transféré. L’assemblage produit une cartouche stable et déverrouille l’aile nord.','Install the 4-litre charge and the transferred core. Assembly produces a stable cartridge and unlocks the north wing.'),model='bench',requires=['coolant4','intact_core'],grants={'stable_cartridge':1},opens=['f_gate'])
prose(e,action=('Assembler la cartouche','Assemble the cartridge'),success=('Cartouche stable assemblée. L’aile nord est ouverte.','Stable cartridge assembled. The north wing is open.'))
event('f_gate','door',[17,11],104,('Sas du prototype','Prototype airlock'),('Le sas est commandé par la station 103 du hall. Rapportez-y les résultats des deux ailes.','Station 103 in the hall controls this airlock. Bring it the results from both wings.'),controlled_by='f_assembly')
event('f_water_note','clue',[1,13],201,('Dosage sans graduation','Measuring without markings'),('Le grand réservoir contient 5 L, le petit 3 L. Il faut exactement 4 L dans le grand ; le petit peut contenir n’importe quelle quantité. Remplir va jusqu’au bord, vider enlève tout, transvaser s’arrête quand la source est vide ou la destination pleine.','The large tank holds 5 L, the small one 3 L. Leave exactly 4 L in the large tank; any amount may remain in the small one. Fill to capacity, empty completely, or pour until the source is empty or the destination is full.'))
event('f_water_tip','clue',[13,31],202,('Note du technicien','Technician’s note'),('Pour isoler un litre, commencez par en conserver deux dans le petit réservoir. Les évacuations sont recyclées : vous pouvez vider, recommencer et revenir plus tard.','To isolate one litre, start by keeping two in the small tank. Drained fluid is recycled: empty, reset or return later.'))
e=event('f_dosing','mechanism',[3,27],203,('Doseur à deux réservoirs','Twin-tank dispenser'),('Préparez exactement 4 L dans le réservoir de 5 L. Les volumes restent visibles après chaque manipulation. La validation conditionne la charge dans une cartouche.','Prepare exactly 4 L in the 5 L tank. Volumes remain visible after every move. Validation packages the charge into a cartridge.'),model='dosing',puzzle_type='jugs',requires=['transfer_seal'],grants={'coolant4':1})
prose(e,success=('Charge de refroidissement de 4 L obtenue. Rapportez-la au hall 103.','4 L coolant charge obtained. Bring it to hall station 103.'))
event('f_secret1','clue',[1,33],204,('Budget des graduations','Markings budget'),('SECRET — « Les graduations coûtaient trop cher. Nous avons acheté un stagiaire pour compter. Il compte toujours. » — Folamour','SECRET — “Markings cost too much. We bought an intern to count instead. Still counting.” — Folamour'),secret=True)
event('f_tower_note','clue',[33,13],301,('Protocole des disques','Disc protocol'),('Transférez les trois disques de A vers C, avec B comme support auxiliaire. Seul le disque du dessus peut bouger. Un grand disque ne doit jamais reposer sur un plus petit. Les tailles sont indiquées 1, 2, 3 : 1 est le plus petit.','Transfer all three discs from A to C, using B as an auxiliary peg. Only the top disc may move. Never place a larger disc on a smaller one. Sizes are labelled 1, 2, 3; 1 is smallest.'))
event('f_tower_tip','clue',[21,33],302,('Carnet de transfert','Transfer notebook'),('Pour libérer le grand disque, rangez d’abord les deux petits sur B. Le noyau n’est livré qu’une fois toute la pile reconstruite sur C. Une tentative interdite ne déplace rien.','To free the large disc, first stack the two smaller ones on B. The core is released only when the complete stack is rebuilt on C. An illegal move changes nothing.'))
e=event('f_tower','mechanism',[31,27],303,('Transfert du noyau','Core transfer'),('Déplacez la pile complète de A vers C en respectant les tailles. Les disques sont les supports protecteurs du noyau ; aucun ne peut être omis.','Move the entire stack from A to C, respecting disc sizes. The discs protect the core; none may be omitted.'),model='tower',puzzle_type='hanoi',grants={'intact_core':1})
prose(e,success=('Noyau intact récupéré. Rapportez-le à la station 103 du hall.','Intact core retrieved. Bring it to hall station 103.'))
event('f_secret2','clue',[33,33],304,('Le précédent record','The previous record'),('SECRET — « Le dernier candidat a déplacé le laboratoire autour des disques. Créatif. Très coûteux. Disqualifié. » — Folamour','SECRET — “The last candidate moved the laboratory around the discs. Creative. Very expensive. Disqualified.” — Folamour'),secret=True)
event('f_rotor_note','clue',[1,9],401,('Repères de stabilisation','Stabilization markers'),('Le rotor A doit pointer vers EST. Le rotor B doit pointer vers SUD. Le rotor C doit pointer vers OUEST. Chaque impulsion tourne deux rotors d’un quart de tour : NORD → EST → SUD → OUEST → NORD.','Rotor A must point EAST, rotor B SOUTH and rotor C WEST. Each pulse turns two rotors a quarter turn: NORTH → EAST → SOUTH → WEST → NORTH.'))
event('f_rotor_wiring','clue',[33,1],402,('Liaisons mécaniques','Mechanical couplings'),('Commande I : A et B. Commande II : B et C. Commande III : A et C. Au repos, tous pointent vers NORD. Une impulsion agit toujours sur les deux rotors liés, même si l’un était déjà bien orienté.','Control I: A and B. Control II: B and C. Control III: A and C. At reset, all point NORTH. A pulse always moves both linked rotors, even if one was already correctly aligned.'))
e=event('f_rotors','mechanism',[25,5],403,('Stabilisateur ZÉRO','ZERO stabilizer'),('Insérez la cartouche du hall, puis réglez les trois rotors selon les repères 401 et les liaisons 402. Les commandes sont couplées. Vous pouvez réinitialiser sans retirer la cartouche.','Insert the hall cartridge, then align the three rotors using markers 401 and couplings 402. Controls are linked. Resetting leaves the cartridge installed.'),model='rotors',puzzle_type='rotors',requires=['stable_cartridge'],target=[1,2,3],masks=[[1,1,0],[0,1,1],[1,0,1]])
prose(e,success=('Stabilité parfaite. ZÉRO fonctionne ! Rejoignez le pupitre 405.','Perfect stability. ZERO works! Go to console 405.'))
event('f_secret3','clue',[3,1],404,('Contrat préimprimé','Preprinted contract'),('SECRET — Un formulaire attend depuis des années. La case « rémunération » a été soigneusement découpée. « Une économie de papier ciblée. » — Folamour','SECRET — A form has been waiting for years. The “compensation” box has been carefully cut out. “Targeted paper savings.” — Folamour'),secret=True)
e=event('f_exit','exit',[17,1],405,('Validation du prototype','Prototype certification'),('Le stabilisateur doit être opérationnel avant la démonstration. Folamour vous attend pour constater le résultat.','The stabilizer must be operational before the demonstration. Folamour is waiting to see the result.'),prerequisites=['f_dosing','f_tower','f_assembly','f_rotors'],wall_face=[0,-1])
prose(e,action=('Présenter le résultat à Folamour','Show Folamour the result'),success=('Prototype ZÉRO stabilisé. Défi accompli.','Prototype ZERO stabilized. Challenge complete.'))
items={}
for id,fr,eng,desc,edesc in [('transfer_seal','Joint de transfert','Transfer seal','Joint réutilisable pour le doseur 203.','Reusable seal for dispenser 203.'),('coolant4','Charge de 4 litres','4-litre charge','Refroidissement pour la station 103.','Coolant for station 103.'),('intact_core','Noyau intact','Intact core','Transféré sur C ; à assembler en 103.','Transferred to C; assemble at 103.'),('stable_cartridge','Cartouche stable','Stable cartridge','À installer dans le stabilisateur 403.','Install in stabilizer 403.')]:items[id]={'title':tr(fr,eng),'text':tr(desc,edesc)}
for name,obj in [('maze5',{'grid':g,'start':[17,21]}),('events5',E),('items5',items),('en',en)]: (D/(name+'.json')).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print('Built level 5:',len(E),'events. Shortcut placement is maintained by scripts/optimize_shortcuts.py.')
