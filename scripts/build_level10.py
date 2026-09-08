"""Archives: movable stacks, evidence comparison and a physical twin room."""
from pathlib import Path
import json, random
D=Path(__file__).resolve().parents[1]/'game/data'
g=[[0]*35 for _ in range(35)]; rng=random.Random(1605)
# West archive maze and southern records: deterministic and fully connected.
for x0,x1,y0,y1 in [(1,9,1,33),(13,21,25,33)]:
 stack=[(x0,y0)];g[y0][x0]=1
 while stack:
  x,y=stack[-1];opts=[(x+dx,y+dy) for dx,dy in [(2,0),(-2,0),(0,2),(0,-2)] if x0<=x+dx<=x1 and y0<=y+dy<=y1 and not g[y+dy][x+dx]]
  if not opts:stack.pop();continue
  a,b=rng.choice(opts);g[(y+b)//2][(x+a)//2]=g[b][a]=1;stack.append((a,b))
def room(x0,x1,y0,y1):
 for y in range(y0,y1+1):
  for x in range(x0,x1+1):g[y][x]=1
room(11,23,15,23);room(13,21,1,12)
room(25,33,3,11);room(25,33,21,29)
room(27,31,13,19)
room(9,11,17,17);room(17,17,12,15);room(17,17,23,25)
room(23,29,17,17);room(29,29,11,13);room(29,29,19,21)
# Restricted original dossier: only one entrance from the shelf room.
room(17,17,0,1) # overwritten border below; pedestal stays in row 1
for x in range(35):g[0][x]=0
E=[];en=json.loads((D/'en.json').read_text())
def tr(fr,eng):en[fr]=eng;return fr
def ev(id,kind,cell,ref,title,text,**kw):
 e=dict(id=id,kind=kind,cell=cell,ref=str(ref),title=tr(*title),text=tr(*text),**kw);E.append(e);return e
def result(e,fr,eng):e['success']=tr(fr,eng)
ev('a_welcome','clue',[15,23],100,('Consignes des archives','Archive instructions'),('Trois validations pour le dossier MIROIR : dégager les rayonnages 203, authentifier un rapport en 303 et corriger la copie en 403. Le hall relie les secteurs. Les commandes sont réversibles et sans limite de temps.','Three approvals for the MIRROR file: clear stacks at 203, authenticate a report at 303, and correct the copy at 403. The hall connects all sectors. Controls are reversible and there is no time limit.'))
ev('a_final','exit',[21,19],105,('Dossier MIROIR - UNIFICATION','MIRROR file - UNIFICATION'),('Le sceau des archives et les trois validations sont nécessaires. Le dossier contient aussi une fiche à votre nom.','The archive seal and all three approvals are required. The file also contains a record in your name.'),requires=['archive_seal'],prerequisites=['a_stacks','a_reports','a_twin'],action=tr('Ouvrir le dossier MIROIR','Open the MIRROR file'))
ev('a_rails','clue',[13,11],201,('Plan des rails','Rail plan'),('Vue du nord vers le sud : rangées A, B, C. Les ouvertures ont trois positions : OUEST, CENTRE, EST. Pour dégager le chemin balisé : A à EST, B à OUEST, C au CENTRE. Les couloirs entre les rangées permettent de changer de côté.','From north to south: rows A, B, C. Openings have three positions: WEST, CENTRE, EAST. Clear the marked route: A EAST, B WEST, C CENTRE. Corridors between rows let you change sides.'))
ev('a_manual','clue',[21,25],202,('Notice des commandes couplées','Coupled control manual'),('Les rails avancent en boucle : OUEST → CENTRE → EST → OUEST. Commande I : A et B. Commande II : B et C. Commande III : A et C. Le bouton de remise à zéro replace toutes les ouvertures à OUEST. Valider immobilise les rayonnages en position sûre.','Rails cycle WEST → CENTRE → EAST → WEST. Control I: A and B. Control II: B and C. Control III: A and C. Reset moves all openings WEST. Validation locks the stacks in their safe positions.'))
e=ev('a_stacks','mechanism',[17,14],203,('Console des rayonnages','Stack console'),('Déplacez les trois rangées selon le plan 201 et la notice 202. Le plan affiche leurs ouvertures actuelles. Les rayonnages bougent réellement dans la salle au nord. Après validation, traversez-les pour récupérer le sceau 204.','Move the three rows using plan 201 and manual 202. The plan shows their current openings. Stacks physically move in the northern room. After validation, cross them to collect seal 204.'),puzzle_type='stacks',model='stacks')
result(e,'Rayonnages immobilisés. Le chemin balisé est libre. Récupérez le sceau 204 au nord. « Ne vous perdez pas. Les disparitions sont classées par ordre alphabétique. » — Folamour','Stacks locked. The marked route is clear. Collect seal 204 in the north. “Do not get lost. Disappearances are filed alphabetically.” — Folamour')
ev('a_seal','pickup',[17,1],204,('Sceau des archives','Archive seal'),('Sceau original requis pour ouvrir le dossier 105. Numéro de série : 0001. Sur son socle, une étiquette indique : « Copie certifiée originale ».','Original seal required to open file 105. Serial number: 0001. Its stand is labelled “Certified original copy”.'),resource='archive_seal',amount=1,appearance='key',prerequisites=['a_stacks'])
ev('a_access','clue',[1,1],301,('Preuve : registre d’accès','Evidence: access log'),('Incident du 12 avril. Seul badge entré entre 14 h 00 et 14 h 30 : B-6. Entrée 14 h 12, sortie 14 h 24. B-6 appartient à Boréal. Le registre mécanique est indépendant de MIROIR.','Incident of 12 April. Only badge entering between 14:00 and 14:30: B-6. Entry 14:12, exit 14:24. B-6 belongs to Boreal. The mechanical log is independent of MIRROR.'))
ev('a_clock','clue',[9,1],302,('Preuve : horloge arrêtée','Evidence: stopped clock'),('L’horloge s’est arrêtée à 14 h 17 lors de la coupure. Son mécanisme a été scellé immédiatement. L’incident précède donc la sortie du porteur du badge B-6.','The clock stopped at 14:17 during the outage. Its mechanism was sealed immediately. The incident therefore occurred before badge B-6 left.'))
e=ev('a_reports','mechanism',[5,17],303,('Lecteur de rapports','Report reader'),('Comparez les trois rapports aux preuves 301, 302 et 304. Sélectionnez le rapport authentique, puis associez à chaque preuve le fait qu’elle établit. Toutes les informations utiles sont dans ce niveau et le journal.','Compare three reports against evidence 301, 302 and 304. Select the authentic report, then match each piece of evidence with the fact it establishes. All required information is in this level and the journal.'),puzzle_type='reports',model='reports',opens=['a_copydoor'])
result(e,'Rapport B authentifié. La salle copiée est ouverte. Les deux autres versions ont été produites par MIROIR. « Une erreur répétée trois fois devient parfois un compte rendu. » — Folamour','Report B authenticated. The copied room is open. The other two versions were generated by MIRROR. “An error repeated three times sometimes becomes a report.” — Folamour')
ev('a_object','clue',[1,33],304,('Preuve : objet retrouvé','Evidence: recovered object'),('Sur le socle : une bobine de cuivre, encore dans son support. Aucun prisme et aucun disque. La photographie argentique du constat confirme cet objet ; elle n’a pas été retouchée par MIROIR.','On the stand: a copper coil, still in its holder. No prism or disc. The film photograph of the scene confirms this object; MIRROR has not altered it.'))
ev('a_original','clue',[29,7],401,('Salle originale : relevé physique','Original room: physical record'),('Relevé depuis l’entrée sud, nord en haut : lampe ALLUMÉE, bobine sur le socle de GAUCHE, projecteur vers l’EST, interrupteur de ventilation ABAISSÉ. Reproduisez ces quatre états dans la salle copiée au sud. La copie conserve les mêmes points cardinaux : ce n’est pas une réflexion gauche-droite.','Recorded from the south entrance, north at the top: lamp ON, coil on the LEFT stand, projector facing EAST, ventilation switch DOWN. Reproduce these four states in the copied room to the south. The copy preserves cardinal directions: it is not a left-right reflection.'))
ev('a_copydoor','door',[29,20],402,('Accès à la salle copiée','Copied room entrance'),('L’authentification du rapport 303 autorise l’entrée.','Authenticating report 303 grants access.'),axis='y',controlled_by='a_reports')
e=ev('a_twin','mechanism',[29,25],403,('Correction de la salle jumelle','Twin room correction'),('Ajustez la lampe, le socle de la bobine, le projecteur et la ventilation d’après la salle originale 401. Les objets changent aussi dans la pièce. Testez la copie, puis validez. Chaque nouvelle modification annule le test.','Set the lamp, coil stand, projector and ventilation using original room 401. Objects also change in the room. Test the copy, then validate. Any new change invalidates the test.'),prerequisites=['a_reports','a_original'],puzzle_type='twin',model='twin')
result(e,'Copie conforme. MIROIR avait inversé l’orientation, déplacé la bobine et modifié les deux états électriques. Rejoignez le dossier 105 avec le sceau.','Copy matches. MIRROR had reversed orientation, moved the coil and changed both electrical states. Bring the seal to file 105.')
ev('a_twin_note','clue',[27,17],404,('Note de maintenance MIROIR','MIRROR maintenance note'),('La salle bleue reproduit la salle ambrée. Les couleurs d’éclairage ne sont pas des indices. Les états des objets, les positions et les points cardinaux font foi. Le test affiche le nombre de correspondances, sans corriger vos réglages.','The blue room reproduces the amber room. Lighting colours are not clues. Object states, positions and cardinal directions are authoritative. The test shows the number of matches without correcting settings.'))
for id,cell,ref,fr,eng in [('a_secret1',[9,33],305,'Version alternative des serres : « Le stagiaire a demandé à être rémunéré en café. » Annotation manuscrite : FAUX.','Alternative greenhouse record: “The intern requested payment in coffee.” Handwritten annotation: FALSE.'),('a_secret2',[13,33],205,'Ancien formulaire : « Si vous rencontrez votre double, vérifiez d’abord lequel a réservé ses vacances. »','Old form: “If you meet your double, first check which one booked leave.”'),('a_secret3',[33,3],405,'Essai MIROIR 07 : six instances de Folamour créées pour simuler un comité. Étape suivante : reproduire les lieux et les habitudes. L’unification attend une copie stable.','MIRROR trial 07: six Folamour instances created to simulate a committee. Next step: replicate places and habits. Unification awaits a stable copy.')]:ev(id,'clue',cell,ref,('Archive confidentielle '+str(ref),'Confidential archive '+str(ref)),(fr,eng),secret=True)
# Visible UI and story text in both supported languages.
pairs=[
('Le service des archives','The archive department'),('VERSION 0.16 · LE SERVICE DES ARCHIVES','VERSION 0.16 · THE ARCHIVE DEPARTMENT'),
('Le chapitre 2 propose cinq missions : les serres, les photocopies, le courrier, la réunion et les archives.','Chapter 2 offers five assignments: greenhouses, photocopies, mail, the meeting and archives.'),('Cinq missions disponibles : les serres, les photocopies, le courrier, la réunion et les archives.','Five assignments available: greenhouses, photocopies, mail, the meeting and archives.'),
('C2 / MISSION 5 / ARCHIVES','C2 / ASSIGNMENT 5 / ARCHIVES'),('Mission 5 — Le service des archives','Assignment 5 — The archive department'),('Passer au service des archives','Continue to the archive department'),('La réunion est terminée. Folamour vous attend aux archives pour votre cinquième mission.','The meeting is over. Folamour awaits you in the archives for your fifth assignment.'),
('« Rapportez-moi le dossier MIROIR. L’original, évidemment. Les copies ont une fâcheuse tendance à se prendre pour l’original. » — Folamour','“Bring me the MIRROR file. The original, obviously. Copies have a nasty habit of thinking they are the original.” — Folamour'),
('Explorez les rayonnages au nord, recoupez les preuves à l’ouest et comparez les salles jumelles à l’est. Trois validations et le sceau donnent accès au dossier central.','Explore stacks to the north, compare evidence to the west and inspect twin rooms to the east. Three approvals and the seal unlock the central file.'),
('STAGE / CINQUIÈME MISSION\nRayonnages 203, sceau 204, rapport 303, salle jumelle 403, puis dossier MIROIR 105.','INTERNSHIP / FIFTH ASSIGNMENT\nStacks 203, seal 204, report 303, twin room 403, then MIRROR file 105.'),
('CHAPITRE 2 / MISSION 5 TERMINÉE','CHAPTER 2 / ASSIGNMENT 5 COMPLETE'),('L’original et ses mauvaises habitudes.','The original and its bad habits.'),
('MIROIR reproduit les lieux et les comportements des occupants du laboratoire. Le comité était un premier essai : six versions artificielles de Folamour. L’UNIFICATION doit réunir leurs observations dans une copie cohérente.','MIRROR replicates the laboratory and its occupants’ behaviour. The committee was an initial trial: six artificial Folamour versions. UNIFICATION will combine their observations into a coherent copy.'),
('Votre fiche : « Sujet : en cours d’évaluation. Capacité à résoudre les problèmes : satisfaisante. Capacité à demander pourquoi : préoccupante. »','Your record: “Subject: under evaluation. Problem-solving ability: satisfactory. Tendency to ask why: concerning.”'),
('« Ah. Vous avez ouvert le dossier. J’avais demandé de le rapporter, pas de développer un esprit critique. » — Folamour','“Ah. You opened the file. I asked you to bring it back, not develop critical thinking.” — Folamour'),
('Au fond du hall, un voyant s’allume : SECTEUR DES PROTOTYPES. La porte s’entrouvre. Cette suite n’est pas encore jouable ; votre bilan et vos découvertes sont sauvegardés.','At the back of the hall, an indicator lights up: PROTOTYPE SECTOR. The door opens slightly. This continuation is not playable yet; your results and discoveries are saved.'),
('Rangée %s : ouverture %s','Row %s: opening %s'),('CENTRE','CENTRE'),('Commande I : A + B','Control I: A + B'),('Commande II : B + C','Control II: B + C'),('Commande III : A + C','Control III: A + C'),
('Rayonnages non conformes : comparez les ouvertures au plan 201.','Stacks do not match: compare openings against plan 201.'),('Rapport ou preuves incohérents : recoupez les trois constats.','Report or evidence inconsistent: compare all three records.'),('Copie non conforme : reproduisez les quatre états et relancez le test.','Copy does not match: reproduce all four states and test again.'),
('Les rayonnages ne bougent pas lorsqu’une personne se trouve entre les rangées. Revenez à la console au sud.','Stacks cannot move while someone is among the rows. Return to the southern console.'),
('Rapport A : Boréal, 14 h 27, bobine de cuivre.','Report A: Boreal, 14:27, copper coil.'),('Rapport B : Boréal, 14 h 17, bobine de cuivre.','Report B: Boreal, 14:17, copper coil.'),('Rapport C : Cobalt, 14 h 17, prisme de verre.','Report C: Cobalt, 14:17, glass prism.'),
('Rapport sélectionné : %s','Selected report: %s'),('Registre : %s','Log: %s'),('Horloge : %s','Clock: %s'),('Objet : %s','Object: %s'),('Bobine de cuivre','Copper coil'),('Prisme de verre','Glass prism'),('Disque','Disc'),
('Lampe : %s','Lamp: %s'),('Bobine : socle %s','Coil: %s stand'),('Projecteur : %s','Projector: %s'),('Ventilation : %s','Ventilation: %s'),('ABAISSÉ','DOWN'),('LEVÉ','UP'),('Tester la copie','Test the copy'),('Correspondances : %d / 4','Matches: %d / 4'),('Réglages modifiés : test requis.','Settings changed: test required.'),('ORIGINAL / NORD ↑','ORIGINAL / NORTH ↑'),('COPIE / NORD ↑','COPY / NORTH ↑')]
for fr,eng in pairs:tr(fr,eng)
aid=json.loads((D/'guidance.json').read_text())
hints={
'a_stacks': [('Les commandes déplacent deux rangées à la fois. Notez la cible et partez de zéro.','Controls move two rows at once. Note the target and start from reset.'),('La cible du nord au sud est EST, OUEST, CENTRE. Une commande peut être utilisée plusieurs fois.','The north-to-south target is EAST, WEST, CENTRE. Controls can be used multiple times.'),('Réinitialisez. Appuyez deux fois sur I et une fois sur II ; ne touchez pas III. Validez : A EST, B OUEST, C CENTRE.','Reset. Press I twice and II once; do not press III. Validate: A EAST, B WEST, C CENTRE.')],
'a_reports':[('Chaque preuve vérifie un champ du rapport, indépendamment de MIROIR.','Each piece of evidence verifies one report field independently of MIRROR.'),('Le registre identifie Boréal. L’heure vient de l’horloge et l’objet de la photo argentique.','The log identifies Boreal. The clock gives the time and the film photo gives the object.'),('Choisissez le rapport B ; registre Boréal ; horloge 14:17 ; objet Bobine de cuivre. Validez.','Select report B; log Boreal; clock 14:17; object Copper coil. Validate.')],
'a_twin':[('Lisez le relevé 401. La copie garde les mêmes points cardinaux que l’original.','Read record 401. The copy keeps the original’s cardinal directions.'),('Comparez quatre détails : lampe, socle, orientation et ventilation. Un essai donne le nombre de correspondances.','Compare four details: lamp, stand, orientation and ventilation. A test gives the number of matches.'),('Lampe ALLUMÉE ; bobine GAUCHE ; projecteur EST ; ventilation ABAISSÉE. Testez puis validez.','Lamp ON; coil LEFT; projector EAST; ventilation DOWN. Test, then validate.')]}
aid['hints'].update(hints)
for id,fr,eng in [('a_stacks','Dégager le chemin aux rayonnages 203 avec les notes 201 et 202.','Clear the route at stacks 203 using notes 201 and 202.'),('a_seal','Traverser les rayonnages et ramasser le sceau 204 au nord.','Cross the stacks and collect seal 204 in the north.'),('a_reports','Authentifier un rapport au lecteur 303 avec les preuves 301, 302 et 304.','Authenticate a report at reader 303 using evidence 301, 302 and 304.'),('a_original','Observer la salle originale et lire son relevé 401.','Observe the original room and read record 401.'),('a_twin','Corriger les quatre états de la salle copiée en 403, tester et valider.','Correct the four copied room states at 403, test and validate.'),('a_final','Apporter le sceau au dossier MIROIR 105 et l’ouvrir.','Bring the seal to MIRROR file 105 and open it.')]:aid['objectives'][id]=[fr,eng]
aid['stages']['10']=[[[k],k] for k in ['a_stacks','a_seal','a_reports','a_original','a_twin','a_final']]
for name,data in [('maze10',{'grid':g,'start':[17,23]}),('events10',E),('items10',{e['resource']:{'title':e['title'],'text':e['text']} for e in E if e['kind']=='pickup'}),('en',en),('guidance',aid)]: (D/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
# Select a few useful return links confined to the west and south mazes.
from collections import deque
F={(x,y) for y,row in enumerate(g) for x,v in enumerate(row) if v};S=[]
def distance(a,b,walk):
 q=deque([(a,0)]);seen={a}
 while q:
  c,d=q.popleft()
  if c==b:return d
  for n in [(c[0]-1,c[1]),(c[0]+1,c[1]),(c[0],c[1]-1),(c[0],c[1]+1)]:
   if n in walk and n not in seen:seen.add(n);q.append((n,d+1))
 return 0
for x0,x1,y0,y1 in [(2,8,2,32),(14,20,26,32)]:
 candidates=[]
 for y in range(y0,y1+1):
  for x in range(x0,x1+1):
   if (x,y) in F:continue
   ns=[p for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] if p in F]
   if len(ns)==2 and (ns[0][0]==ns[1][0] or ns[0][1]==ns[1][1]):candidates.append((distance(*ns,F)-2,(x,y),ns))
 for gain,c,ns in sorted(candidates,reverse=True):
  if gain<12 or len([s for s in S if s['cell'][0]<11])>=3 and x0==2:continue
  walk=F|{tuple(s['cell']) for s in S}|{c}
  if distance(*ns,walk-{c})-2<12:continue
  if any(distance(*map(tuple,s['sides']),walk-{tuple(s['cell'])})-2<12 for s in S):continue
  S.append({'id':'A'+str(len(S)+1),'cell':list(c),'axis':'x' if ns[0][1]==ns[1][1] else 'y','sides':[list(p) for p in ns],'minimum_saved_steps':distance(*ns,walk-{c})-2})
  if x0==14:break
for s in S:s['minimum_saved_steps']=distance(*map(tuple,s['sides']),F|{tuple(t['cell']) for t in S if t!=s})-2
(D/'shortcuts10.json').write_text(json.dumps(S,indent=2)+'\n')
print('Level 10:',len(E),'events;',len(S),'return links')
