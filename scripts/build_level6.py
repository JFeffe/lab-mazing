"""Chapter 2 / first assignment: deterministic greenhouse maze and bilingual story."""
from pathlib import Path
import json,random
D=Path(__file__).resolve().parents[1]/'game/data';g=[[0]*35 for _ in range(35)];rng=random.Random(120617)
for x0,x1,y0,y1 in [(1,11,1,33),(25,33,1,33),(13,23,1,7),(13,23,27,33)]:
 stack=[(x0,y0)];g[y0][x0]=1
 while stack:
  x,y=stack[-1];ns=[(x+dx,y+dy) for dx,dy in [(2,0),(-2,0),(0,2),(0,-2)] if x0<=x+dx<=x1 and y0<=y+dy<=y1 and not g[y+dy][x+dx]]
  if not ns:stack.pop();continue
  a,b=rng.choice(ns);g[(b+y)//2][(a+x)//2]=g[b][a]=1;stack.append((a,b))
# A central ring and cross connect four distinctly shaped wings.
for y in range(11,24):
 for x in range(13,22):
  if x in [13,17,21] or y in [11,17,23]:g[y][x]=1
for x in range(11,26):g[17][x]=1
for y in range(7,28):g[y][17]=1
E=[];en=json.loads((D/'en.json').read_text())
def tr(fr,eng):en[fr]=eng;return fr
def ev(id,kind,cell,ref,title,text,**kw):
 e=dict(id=id,kind=kind,cell=cell,ref=str(ref),title=tr(*title),text=tr(*text),**kw);E.append(e);return e
def result(e,fr,eng):e['success']=tr(fr,eng)
ev('g_welcome','clue',[17,21],100,('Première affectation','First assignment'),('Bienvenue aux serres expérimentales. Mission : préparer le café de Folamour. La cafetière 105 dépend du mélangeur au nord, des cultures à l’est et de l’irrigation à l’ouest. Le vestiaire se trouve au sud.','Welcome to the experimental greenhouses. Assignment: make Folamour’s coffee. Coffee maker 105 depends on the northern mixer, the eastern crops and western irrigation. The cloakroom is to the south.'))
ev('g_seed','pickup',[13,11],101,('Graine de liane-pont','Bridge-vine seed'),('Cette liane devient une passerelle lorsqu’elle reçoit de l’eau, une lumière douce et un support. À installer dans le bac 104.','This vine becomes a walkway when given water, soft light and a support. Install it in bed 104.'),resource='bridge_seed',amount=1,appearance='seed')
ev('g_growth_note','clue',[13,23],102,('Fiche de germination','Germination sheet'),('La liane-pont pousse sous une lumière DOUCE. Elle demande DEUX doses d’eau et un treillis DÉPLOYÉ. L’ombre empêche sa croissance ; le soleil fort la fait se recroqueviller. L’eau du circuit est recyclée.','The bridge vine grows in SOFT light. It needs TWO doses of water and a RAISED trellis. Shade prevents growth; strong sunlight makes it curl up. Circuit water is recycled.'))
ev('g_mug','pickup',[13,33],103,('Tasse du docteur','The doctor’s mug'),('Une tasse gravée « Meilleur superviseur, selon moi ». Rapportez-la à la cafetière 105.','A mug engraved “Best supervisor, according to me”. Bring it to coffee maker 105.'),resource='coffee_mug',amount=1,appearance='cup')
e=ev('g_growth','mechanism',[21,17],104,('Bac de la liane-pont','Bridge-vine bed'),('Installez la graine et la réserve d’eau. Ajustez la lumière, l’arrosage et le treillis selon la fiche 102. La croissance déploiera un passage vers les cultures de l’est.','Install the seed and water reserve. Adjust the light, watering and trellis using sheet 102. Growth will deploy a path to the eastern crops.'),requires=['bridge_seed','water_reserve'],puzzle_type='growth',model='growth',opens=['g_bridge'])
result(e,'La liane s’enroule autour du treillis. La passerelle est praticable dans les deux sens ! « Vous voyez ? Même les plantes acceptent les heures supplémentaires. » — Folamour','The vine wraps around the trellis. The walkway can be crossed both ways! “See? Even the plants accept overtime.” — Folamour')
e=ev('g_coffee','exit',[17,13],105,('Cafetière administrative','Administrative coffee maker'),('Il faut la tasse du docteur et une préparation validée au mélangeur 205. Le café ne lance aucun compte à rebours.','You need the doctor’s mug and a preparation approved at mixer 205. Brewing starts no countdown.'),requires=['coffee_mug','coffee_blend'],prerequisites=['g_irrigation','g_growth','g_blend'])
e['action']=tr('Servir le café','Serve the coffee');result(e,'Le café est servi. Première mission du stage réussie.','Coffee served. First internship assignment complete.')
ev('g_bridge','door',[23,17],106,('Passerelle végétale','Living walkway'),('Le treillis est replié. La liane du bac 104 doit pousser pour rendre ce passage sûr.','The trellis is folded. The vine in bed 104 must grow to make this crossing safe.'),axis='x',controlled_by='g_growth')
ev('g_pipe_note','clue',[1,1],201,('Plan de circulation de l’eau','Water circulation plan'),('Les quatre coudes A, B, C et D forment un carré : A et B en haut, C et D en bas. L’eau arrive par l’OUEST de A et doit sortir par l’EST de B. Tournez chaque coude ; deux ouvertures face à face doivent se rejoindre, sans fuite.','The four elbows A, B, C and D form a square: A and B above, C and D below. Water enters A from the WEST and must leave B to the EAST. Rotate each elbow; facing openings must join without leaks.'))
ev('g_coupling','pickup',[11,31],202,('Raccord étanche','Sealed coupling'),('Le dernier raccord du panneau d’irrigation 203. Son joint empêche l’eau de fuir à l’entrée.','The last coupling for irrigation panel 203. Its seal prevents leakage at the inlet.'),resource='water_coupling',amount=1,appearance='key')
e=ev('g_irrigation','mechanism',[5,15],203,('Circuit d’irrigation','Irrigation circuit'),('Installez le raccord puis tournez les quatre coudes. Les flèches indiquent leurs ouvertures actuelles. Le chemin de l’eau doit relier l’entrée à la sortie.','Install the coupling, then rotate all four elbows. The arrows show their current openings. The water path must connect inlet to outlet.'),requires=['water_coupling'],puzzle_type='pipes',model='pipes',grants={'water_reserve':1})
result(e,'L’eau circule. Une réserve est prête pour le bac 104. « Excellent. Maintenant, arrosez quelque chose qui rapporte. » — Folamour','Water is flowing. A reserve is ready for bed 104. “Excellent. Now water something profitable.” — Folamour')
ev('g_pipe_tip','clue',[9,3],204,('Annotation du plombier','Plumber’s annotation'),('Ce sont uniquement des COUDES, jamais des tuyaux droits. L’eau doit faire un détour par le bas du carré avant de rejoindre la sortie.','These are all ELBOWS, never straight pipes. Water must detour through the bottom of the square before reaching the outlet.'))
e=ev('g_blend','mechanism',[17,3],205,('Mélangeur aromatique','Aromatic mixer'),('Installez les quatre récoltes. Composez TROIS mesures au total avec arôme 3, amertume 2 et stabilité 2. Chaque réserve accepte de 0 à 2 mesures. Les propriétés des ingrédients s’additionnent ; les essais ne consomment pas les réserves installées.','Install all four crops. Combine THREE measures in total with aroma 3, bitterness 2 and stability 2. Each supply accepts 0 to 2 measures. Ingredient properties add up; trials do not consume installed supplies.'),requires=['bean_crop','petal_crop','moss_crop','salt_crop'],puzzle_type='blend',model='blend',ingredients=['Grain','Pétale','Mousse','Sel'],properties=[[2,2,0],[1,0,1],[0,0,1],[0,1,2]],target=[3,2,2],grants={'coffee_blend':1})
result(e,'Préparation validée. Rapportez-la à la cafetière 105 avec la tasse. « Une réussite botanique. Espérons qu’elle soit aussi buvable. » — Folamour','Preparation approved. Bring it to coffee maker 105 with the mug. “A botanical success. Let us hope it is drinkable too.” — Folamour')
ev('g_recipe','clue',[23,7],206,('Commande du superviseur','Supervisor’s order'),('TROIS mesures. ARÔME : 3. AMERTUME : 2. STABILITÉ : 2. Un ingrédient peut être omis. Lire les propriétés des récoltes et additionner chaque colonne. « Pas de sucre. Il crée des attentes. » — Folamour','THREE measures. AROMA: 3. BITTERNESS: 2. STABILITY: 2. An ingredient may be omitted. Read the crop properties and add each column. “No sugar. It creates expectations.” — Folamour'))
for id,cell,ref,title,english,resource,desc,eng in [
 ('g_beans',[25,1],301,'Grains de café-lune','Moon-coffee beans','bean_crop','Une mesure : arôme 2, amertume 2, stabilité 0. Réserve pour le mélangeur 205.','One measure: aroma 2, bitterness 2, stability 0. Supply for mixer 205.'),
 ('g_petals',[33,9],302,'Pétales de vanillombre','Shade-vanilla petals','petal_crop','Une mesure : arôme 1, amertume 0, stabilité 1. Réserve pour le mélangeur 205.','One measure: aroma 1, bitterness 0, stability 1. Supply for mixer 205.'),
 ('g_moss',[25,31],303,'Mousse stabilisante','Stabilising moss','moss_crop','Une mesure : arôme 0, amertume 0, stabilité 1. Réserve pour le mélangeur 205.','One measure: aroma 0, bitterness 0, stability 1. Supply for mixer 205.'),
 ('g_salt',[33,33],304,'Sel de rosée','Dew salt','salt_crop','Une mesure : arôme 0, amertume 1, stabilité 2. Réserve pour le mélangeur 205. Récolter n’oblige pas à utiliser.','One measure: aroma 0, bitterness 1, stability 2. Supply for mixer 205. Harvesting does not require using it.')]:
 ev(id,'pickup',cell,ref,(title,english),(desc,eng),resource=resource,amount=1,appearance='seed')
for id,cell,ref,fr,eng in [
 ('g_secret1',[1,33],207,'« Les plantes carnivores ne mangent que les employés rémunérés. Vous ne risquez rien. » — Folamour','“Carnivorous plants only eat paid employees. You are perfectly safe.” — Folamour'),
 ('g_secret2',[33,1],305,'Le syndicat des fougères réclame une pause de photosynthèse. Demande rejetée : exposition insuffisante.','The fern union demands a photosynthesis break. Request denied: insufficient exposure.'),
 ('g_secret3',[23,33],107,'Contrat de stage, annexe B : les pauses café commencent lorsque le café est terminé. La préparation ne compte pas.','Internship contract, appendix B: coffee breaks begin when the coffee is ready. Preparation does not count.')]:ev(id,'clue',cell,ref,('Archive des serres '+str(ref),'Greenhouse archive '+str(ref)),(fr,eng),secret=True)
items={}
for e in E:
 if e['kind']=='pickup':items[e['resource']]={'title':e['title'],'text':e['text']}
for id,fr,eng,desc,edesc in [('water_reserve','Réserve d’eau','Water reserve','Pour le bac 104.','For bed 104.'),('coffee_blend','Préparation aromatique','Aromatic preparation','À servir avec la tasse en 105.','Serve with the mug at 105.')]:items[id]={'title':tr(fr,eng),'text':tr(desc,edesc)}
for name,data in [('maze6',{'grid':g,'start':[17,23]}),('events6',E),('items6',items),('en',en)]:
 (D/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
if not (D/'shortcuts6.json').exists():(D/'shortcuts6.json').write_text('[]\n')
print('Level 6:',len(E),'events')
# New interface strings are canonical French, like the existing chapter.
translations={
'DOCTEUR FOLAMOUR / EXPÉRIENCES':'DOCTOR FOLAMOUR / EXPERIMENTS',
'VERSION 0.12 · LE STAGE COMMENCE':'VERSION 0.12 · THE INTERNSHIP BEGINS',
'Le chapitre 2 commence dans les serres expérimentales : votre première mission de stagiaire est disponible.':'Chapter 2 begins in the experimental greenhouses: your first internship assignment is available.',
'Chapitre 2 — Le stage non rémunéré':'Chapter 2 — The unpaid internship',
'Première mission disponible : les serres expérimentales. Les missions suivantes arriveront plus tard.':'First assignment available: the experimental greenhouses. Further assignments will arrive later.',
'Reprendre le chapitre 2':'Resume chapter 2','Commencer le chapitre 2':'Start chapter 2',
'Accepter le stage — Chapitre 2':'Accept the internship — Chapter 2',
'C2 / MISSION 1 / LES SERRES':'C2 / ASSIGNMENT 1 / GREENHOUSES',
'CHAPITRE 2 / LE STAGE NON RÉMUNÉRÉ':'CHAPTER 2 / THE UNPAID INTERNSHIP',
'Mission 1 — Les serres expérimentales':'Assignment 1 — The experimental greenhouses',
'« Bienvenue dans l’équipe. Pour votre première mission, un simple café. La cafetière dépend de l’irrigation, de la botanique et d’un mélangeur expérimental. Mais je vous fais confiance : je suis déjà en pause. » — Folamour':'“Welcome to the team. For your first assignment, a simple coffee. The machine depends on irrigation, botany and an experimental mixer. But I trust you: I am already on my break.” — Folamour',
'Rétablissez l’eau à l’ouest, faites pousser la liane au centre, récoltez à l’est puis préparez le mélange au nord. Une tasse vous attend dans le vestiaire au sud. Les essais sont réversibles ; aucun compte à rebours.':'Restore water in the west, grow the vine in the centre, harvest in the east and prepare the blend in the north. A mug awaits in the southern cloakroom. Tests are reversible; there is no countdown.',
'Prendre mon service':'Start my shift',
'STAGE / PREMIÈRE MISSION\nPréparer le café : irrigation, liane-pont, récoltes, mélange et tasse. Le rappel d’objectif suit votre progression.':'INTERNSHIP / FIRST ASSIGNMENT\nMake coffee: irrigation, bridge vine, crops, blend and mug. The objective reminder follows your progress.',
'CHAPITRE 2 / MISSION 1 TERMINÉE':'CHAPTER 2 / ASSIGNMENT 1 COMPLETE',
'Le café est servi.':'Coffee is served.',
'Folamour prend une gorgée, examine la tasse et hoche la tête.':'Folamour takes a sip, examines the mug and nods.',
'« Excellent. Vous avez restauré un écosystème pour une tasse de café. Voilà exactement le sens des priorités que nous recherchons. Demain, nous verrons si vous savez faire des photocopies. » — Folamour':'“Excellent. You restored an ecosystem for a cup of coffee. Exactly the sense of priorities we are looking for. Tomorrow, we shall see whether you can make photocopies.” — Folamour',
'Première mission du chapitre 2 réussie. La suite du stage n’est pas encore disponible. Votre bilan est sauvegardé.':'First assignment of chapter 2 complete. The rest of the internship is not available yet. Your results have been saved.',
'Entrée : ouest de A. Sortie : est de B.\nA et B en haut ; C et D en bas.':'Inlet: west of A. Outlet: east of B.\nA and B above; C and D below.',
'Touchez un coude pour le tourner d’un quart de tour.':'Tap an elbow to rotate it a quarter turn.',
'Lumière : ':'Light: ','Arrosage : %d / 2 doses':'Watering: %d / 2 doses','Treillis : ':'Trellis: ',
'OMBRE':'SHADE','DOUCE':'SOFT','FORTE':'STRONG','DÉPLOYÉ':'RAISED','REPLIÉ':'FOLDED',
'Touchez chaque réglage pour le modifier. La croissance est validée seulement lorsque les trois conditions sont réunies.':'Tap each setting to change it. Growth is validated only when all three conditions are met.',
'Arôme : %d / 3 • Amertume : %d / 2 • Stabilité : %d / 2':'Aroma: %d / 3 • Bitterness: %d / 2 • Stability: %d / 2',
'Mesures utilisées : %d / 3':'Measures used: %d / 3',
'Grain':'Bean','Pétale':'Petal','Mousse':'Moss','Sel':'Salt',
'Chaque pression ajoute une mesure ; après deux, la quantité revient à zéro. Les réserves restent installées.':'Each tap adds a measure; after two, the quantity returns to zero. Supplies remain installed.',
'Circuit interrompu : reliez les ouvertures sans fuite, de l’ouest de A à l’est de B.':'Broken circuit: connect the openings without leaks, from west of A to east of B.',
'La liane ne pousse pas encore. Comparez les trois réglages avec la fiche de germination.':'The vine is not growing yet. Compare the three settings with the germination sheet.',
'Mélange refusé : trois mesures, arôme 3, amertume 2, stabilité 2.':'Blend rejected: three measures, aroma 3, bitterness 2, stability 2.'}
en.update(translations);(D/'en.json').write_text(json.dumps(en,ensure_ascii=False,indent=2)+'\n')
aid=json.loads((D/'guidance.json').read_text())
aid['hints'].update({
'g_irrigation':[
 ['Les ouvertures de deux coudes voisins doivent se faire face.','The openings of neighbouring elbows must face each other.'],
 ['L’eau doit descendre de A vers C, traverser vers D, puis remonter en B.','Water must go down from A to C, across to D, then up to B.'],
 ['Après réinitialisation : A deux fois, B une fois, C aucune fois, D trois fois. Ouvertures A ouest/sud ; B sud/est ; C nord/est ; D nord/ouest. Validez.','After reset: A twice, B once, C zero times, D three times. Openings: A west/south; B south/east; C north/east; D north/west. Validate.']],
'g_growth':[
 ['Cette plante a besoin d’un environnement et d’un support adaptés.','This plant needs a suitable environment and support.'],
 ['La fiche 102 distingue la lumière douce du plein soleil. Le treillis doit être prêt avant la croissance.','Sheet 102 distinguishes soft light from full sun. The trellis must be ready before growth.'],
 ['Installez la graine 101 et l’eau obtenue en 203. Réglez lumière DOUCE, arrosage 2 doses et treillis DÉPLOYÉ, puis validez.','Install seed 101 and the water obtained at 203. Set SOFT light, 2 doses of water and RAISED trellis, then validate.']],
'g_blend':[
 ['Additionnez les propriétés, pas les numéros des récoltes. Un ingrédient peut rester inutilisé.','Add the properties, not the crop reference numbers. An ingredient may remain unused.'],
 ['Une mesure de grain fournit déjà toute l’amertume demandée. Complétez l’arôme et la stabilité sans ajouter d’amertume.','One measure of beans already provides all required bitterness. Add aroma and stability without adding bitterness.'],
 ['Après installation des quatre récoltes : Grain 1, Pétale 1, Mousse 1, Sel 0. Trois mesures donnent arôme 3, amertume 2 et stabilité 2. Validez.','After installing all four crops: Bean 1, Petal 1, Moss 1, Salt 0. Three measures give aroma 3, bitterness 2 and stability 2. Validate.']]})
objectives={
'g_irrigation':['Récupérer le raccord à l’ouest et rétablir la circulation de l’eau au panneau 203.','Find the coupling in the west and restore water flow at panel 203.'],
'g_growth':['Installer la graine et l’eau dans le bac 104, puis créer la passerelle végétale.','Install the seed and water in bed 104, then create the living walkway.'],
'g_harvest':['Explorer les cultures à l’est et récolter les quatre ingrédients du mélangeur.','Explore the eastern crops and harvest all four mixer ingredients.'],
'g_blend':['Apporter les récoltes au mélangeur 205 au nord et préparer le mélange demandé.','Take the crops to northern mixer 205 and prepare the requested blend.'],
'g_mug':['Retrouver la tasse du docteur dans le vestiaire au sud.','Find the doctor’s mug in the southern cloakroom.'],
'g_coffee':['Servir le café à la cafetière 105 avec la tasse et la préparation validée.','Serve coffee at machine 105 with the mug and approved preparation.']}
aid['objectives'].update(objectives)
aid['stages']['6']=[[[k],k] for k in ['g_irrigation','g_growth']]+[[['g_beans','g_petals','g_moss','g_salt'],'g_harvest']]+[[[k],k] for k in ['g_blend','g_mug','g_coffee']]
(D/'guidance.json').write_text(json.dumps(aid,ensure_ascii=False,indent=2)+'\n')
