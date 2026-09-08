"""The internal mail: reception loop, two warehouses and gated dispatch wing."""
from pathlib import Path
import json,random
D=Path(__file__).resolve().parents[1]/'game/data';g=[[0]*35 for _ in range(35)];rng=random.Random(140803)
# Three long warehouses, surrounded by a reception delivery circuit.
for x0,x1,y0,y1 in [(3,11,3,25),(15,23,3,25),(3,31,29,33)]:
 stack=[(x0,y0)];g[y0][x0]=1
 while stack:
  x,y=stack[-1];ns=[(x+dx,y+dy) for dx,dy in [(2,0),(-2,0),(0,2),(0,-2)] if x0<=x+dx<=x1 and y0<=y+dy<=y1 and not g[y+dy][x+dx]]
  if not ns:stack.pop();continue
  a,b=rng.choice(ns);g[(b+y)//2][(a+x)//2]=g[b][a]=1;stack.append((a,b))
for y in range(1,28):g[y][1]=g[y][33]=1
for x in range(1,34):g[1][x]=g[27][x]=1
# West warehouse accessible from the circuit; middle warehouse through one lock.
for x in range(1,4):g[13][x]=1
for x in range(23,34):g[13][x]=1
for y in range(27,30):g[y][17]=1
# Reception alcove leaves the outer circuit unobstructed.
for y in range(17,22):
 for x in range(27,34):g[y][x]=1
E=[];en=json.loads((D/'en.json').read_text())
def tr(fr,eng):en[fr]=eng;return fr
def ev(id,kind,cell,ref,title,text,**kw):
 e=dict(id=id,kind=kind,cell=cell,ref=str(ref),title=tr(*title),text=tr(*text),**kw);E.append(e);return e
def result(e,fr,eng):e['success']=tr(fr,eng)
ev('m_welcome','clue',[29,19],100,('Circuit du courrier','Mail circuit'),('Le grand circuit fait le tour des entrepôts. À l’ouest : pesée des colis. Au centre : réseau pneumatique. Au sud : expédition. Livrez le colis au guichet 101, à la réception est.','The main circuit surrounds the warehouses. West: parcel weighing. Centre: pneumatic network. South: dispatch. Deliver the parcel to counter 101 at eastern reception.'))
ev('m_delivery','exit',[27,21],101,('Guichet de livraison','Delivery counter'),('Présentez le colis adressé par le terminal 403. La livraison termine la mission.','Present the parcel addressed by terminal 403. Delivery completes the assignment.'),requires=['addressed_parcel'],prerequisites=['m_balance','m_network','m_address'],action=tr('Remettre le colis','Hand over the parcel'))
ev('m_network_door','door',[25,13],102,('Accès au tri pneumatique','Pneumatic sorting access'),('L’identification du colis à la balance 203 autorise l’entrée.','Identifying the parcel at balance 203 authorises entry.'),axis='x',controlled_by='m_balance')
ev('m_dispatch_door','door',[17,28],103,('Accès à l’expédition','Dispatch access'),('Le réseau 303 doit délivrer son bordereau avant l’ouverture.','Network 303 must issue its dispatch slip before this door opens.'),axis='y',controlled_by='m_network')
ev('m_parcels','pickup',[3,3],201,('Lot de six colis','Batch of six parcels'),('Six colis A à F. Cinq ont exactement le même poids. Le colis à livrer est le seul PLUS LOURD. À installer sur la balance 203.','Six parcels A to F. Five have exactly the same weight. The delivery parcel is the only HEAVIER one. Install them at balance 203.'),resource='parcel_batch',amount=1,appearance='crate')
ev('m_balance_note','clue',[11,3],202,('Notice de pesée','Weighing instructions'),('Touchez chaque colis pour le placer en réserve, à gauche ou à droite. Appuyez sur PESER pour comparer. Comparez autant de colis de chaque côté pour chercher le plus lourd. Choisissez ensuite le colis à livrer et validez. Les pesées sont illimitées.','Tap each parcel to place it in reserve, left or right. Press WEIGH to compare. Compare equal numbers on each side to find the heavier parcel. Then select the delivery parcel and validate. Weighing is unlimited.'))
e=ev('m_balance','mechanism',[7,15],203,('Balance des colis','Parcel balance'),('Installez le lot 201. Retrouvez le seul colis plus lourd grâce aux comparaisons, puis sélectionnez-le. Aucun colis n’est ouvert ni consommé pendant les essais.','Install batch 201. Find the only heavier parcel by comparison, then select it. No parcel is opened or consumed during trials.'),requires=['parcel_batch'],puzzle_type='parcels',model='parcels',heavy=4,opens=['m_network_door'],grants={'chosen_parcel':1})
result(e,'Le colis E est identifié. L’accès au tri central s’ouvre. « Vous avez soupesé la situation. C’est plus que la plupart de mes employés. » — Folamour','Parcel E is identified. Central sorting access opens. “You have weighed up the situation. More than most of my employees do.” — Folamour')
ev('m_balance_tip','clue',[3,25],204,('Méthode du magasinier','Warehouse keeper’s method'),('Deux comparaisons suffisent : trois colis contre trois, puis deux colis du groupe le plus lourd l’un contre l’autre. Si ces deux-là s’équilibrent, le troisième est le bon.','Two comparisons suffice: three parcels against three, then two parcels from the heavier group against each other. If those two balance, the third is the one.'))
ev('m_capsule','pickup',[15,3],301,('Capsule de transport','Transport capsule'),('Une capsule réutilisable pour le réseau 303. En cas de mauvaise destination, elle revient automatiquement au départ.','A reusable capsule for network 303. If it reaches the wrong destination, it automatically returns to the start.'),resource='mail_capsule',amount=1,appearance='key')
ev('m_network_note','clue',[23,3],302,('Plan du tri','Sorting plan'),('Trois aiguillages A, B et C. Suivez les traits du schéma : la capsule doit arriver à EXPÉDITION. Chaque commande choisit la branche 1 ou 2. Lancez un essai pour voir son trajet ; une mauvaise branche renvoie la capsule au départ.','Three junctions A, B and C. Follow the diagram lines: the capsule must reach DISPATCH. Each control selects branch 1 or 2. Launch a trial to see its route; a wrong branch returns the capsule to the start.'))
e=ev('m_network','mechanism',[19,17],303,('Réseau pneumatique','Pneumatic network'),('Installez la capsule. Réglez les aiguillages et lancez un essai. Une fois la capsule arrivée à EXPÉDITION, validez pour obtenir le bordereau et ouvrir l’aile sud.','Install the capsule. Set the junctions and launch a trial. Once the capsule reaches DISPATCH, validate to receive the slip and open the southern wing.'),requires=['mail_capsule'],puzzle_type='mailnet',model='mailnet',opens=['m_dispatch_door'],grants={'dispatch_slip':1})
result(e,'La capsule atteint l’expédition. Le bordereau est prêt et l’aile sud s’ouvre. « Notre courrier circule mieux que nos augmentations. » — Folamour','The capsule reaches dispatch. The slip is ready and the southern wing opens. “Our mail moves faster than our pay rises.” — Folamour')
ev('m_network_tip','clue',[15,25],304,('Consigne de retour','Return procedure'),('Une nouvelle manipulation annule le résultat du dernier essai. Après chaque réglage, relancez la capsule. Elle reste disponible même après un retour.','Changing a junction clears the previous trial result. Launch the capsule again after adjustments. It remains available even after a return.'))
ev('m_label','pickup',[3,29],401,('Fragment d’étiquette','Label fragment'),('Destinataire : « F. — direction scientifique ». Le numéro et l’aile ont été déchirés. Croisez l’annuaire 402 et l’avis de déménagement 404.','Recipient: “F. — scientific management”. The number and wing are torn off. Cross-check directory 402 and relocation notice 404.'),resource='label_fragment',amount=1,appearance='card')
ev('m_directory','clue',[31,29],402,('Annuaire du personnel','Staff directory'),('Dr Folamour : direction scientifique, aile Nord, bureau 2. Mme Faraday : maintenance, aile Est, bureau 1. M. Foucault : comptabilité, aile Ouest, bureau 3. Attention : consulter les changements récents en 404.','Dr Folamour: scientific management, North wing, office 2. Ms Faraday: maintenance, East wing, office 1. Mr Foucault: accounting, West wing, office 3. Check recent changes at 404.'))
e=ev('m_address','mechanism',[17,33],403,('Terminal d’adressage','Addressing terminal'),('Installez le colis, le bordereau et le fragment d’étiquette. Identifiez le destinataire et son adresse ACTUELLE. Le guichet de livraison 101 transmettra le colis au bureau choisi.','Install the parcel, slip and label fragment. Identify the recipient and their CURRENT address. Delivery counter 101 will forward the parcel to the chosen office.'),requires=['chosen_parcel','dispatch_slip','label_fragment'],puzzle_type='address',model='address',target=[1,2,3],grants={'addressed_parcel':1})
result(e,'Adresse validée : Dr Folamour, aile Ouest, bureau 4. Rapportez le colis au guichet 101.','Address approved: Dr Folamour, West wing, office 4. Return the parcel to counter 101.')
ev('m_relocation','clue',[31,33],404,('Avis de déménagement — EN VIGUEUR','Relocation notice — IN FORCE'),('La direction scientifique a quitté l’aile Nord. Elle occupe maintenant l’aile OUEST, dans le bureau immédiatement après le numéro 3. La maintenance et la comptabilité ne déménagent pas.','Scientific management has left the North wing. It now occupies the WEST wing, in the office immediately after number 3. Maintenance and accounting are not moving.'))
for id,cell,ref,fr,eng in [('m_secret1',[11,25],205,'Colis perdu : contient le manuel « Ne plus perdre de colis ». Dernière localisation : inconnue.','Lost parcel: contains the manual “Stop losing parcels”. Last location: unknown.'),('m_secret2',[23,25],305,'Le service courrier refuse de livrer les plaintes : elles dépassent la charge maximale autorisée.','The mail service refuses to deliver complaints: they exceed the maximum permitted load.'),('m_secret3',[3,33],405,'Facture : sonnette de bureau. Option silence : supplément. Option stagiaire : incluse.','Invoice: office bell. Silent option: extra charge. Intern option: included.')]:ev(id,'clue',cell,ref,('Archive du courrier '+str(ref),'Mail archive '+str(ref)),(fr,eng),secret=True)
items={e['resource']:{'title':e['title'],'text':e['text']} for e in E if e['kind']=='pickup'}
for id,fr,eng,desc,edesc in [('chosen_parcel','Colis E','Parcel E','Le colis le plus lourd, pour le terminal 403.','The heavier parcel, for terminal 403.'),('dispatch_slip','Bordereau de tri','Sorting slip','Autorisation obtenue au réseau 303. Pour le terminal 403.','Authorisation from network 303. For terminal 403.'),('addressed_parcel','Colis adressé','Addressed parcel','Pour Folamour, aile Ouest, bureau 4. À remettre au guichet 101.','For Folamour, West wing, office 4. Deliver at counter 101.')]:items[id]={'title':tr(fr,eng),'text':tr(desc,edesc)}
en.update({
'Le courrier interne':'Internal mail','VERSION 0.14 · LE COURRIER INTERNE':'VERSION 0.14 · INTERNAL MAIL',
'Le chapitre 2 propose trois missions : les serres, les photocopies et le courrier interne.':'Chapter 2 offers three assignments: greenhouses, photocopies and internal mail.',
'Trois missions disponibles : les serres, les photocopies, puis le courrier interne.':'Three assignments available: greenhouses, photocopies, then internal mail.',
'C2 / MISSION 3 / COURRIER':'C2 / ASSIGNMENT 3 / MAIL',
'Mission 3 — Le courrier interne':'Assignment 3 — Internal mail',
'« Une simple livraison. Même vous devriez pouvoir y arriver. Évitez seulement d’ouvrir le colis : son contenu n’a pas encore accepté son affectation. » — Folamour':'“A simple delivery. Even you should manage it. Just avoid opening the parcel: its contents have not yet accepted their assignment.” — Folamour',
'Identifiez le colis plus lourd à l’ouest, réglez le réseau au centre et reconstituez l’adresse au sud. Livraison à la réception est. Aucun compte à rebours, aucun essai destructif.':'Identify the heavier parcel in the west, configure the central network and reconstruct the address in the south. Deliver at eastern reception. No countdown, no destructive trials.',
'STAGE / TROISIÈME MISSION\nLivrer un colis : balance à l’ouest, réseau au centre, adresse au sud, livraison en 101.':'INTERNSHIP / THIRD ASSIGNMENT\nDeliver a parcel: western balance, central network, southern address terminal, delivery at 101.',
'Passer au courrier interne':'Continue to internal mail',
'Votre copie est acceptée. La troisième mission du stage est disponible.':'Your copy is accepted. The third internship assignment is available.',
'CHAPITRE 2 / MISSION 3 TERMINÉE':'CHAPTER 2 / ASSIGNMENT 3 COMPLETE',
'Livraison accomplie.':'Delivery complete.',
'Folamour ouvre le colis : une sonnette de bureau. Il la fait tinter, puis vous regarde.':'Folamour opens the parcel: an office bell. He rings it, then looks at you.',
'« Excellent ! Maintenant, vous pourrez annoncer votre arrivée avant de me déranger. » — Folamour':'“Excellent! Now you can announce your arrival before disturbing me.” — Folamour',
'Mission réussie. Le colis est livré et votre bilan est sauvegardé. La suite du stage arrivera plus tard.':'Assignment complete. The parcel is delivered and your results are saved. More internship assignments will arrive later.',
'Colis %s : %s':'Parcel %s: %s','Colis choisi : %s':'Selected parcel: %s','Peser les colis':'Weigh the parcels','Aucune pesée effectuée.':'No weighing performed.',
'Dernière pesée : gauche plus lourd.':'Last weighing: left is heavier.','Dernière pesée : droite plus lourd.':'Last weighing: right is heavier.','Dernière pesée : équilibre.':'Last weighing: balanced.',
'Placement modifié : pesez à nouveau.':'Placement changed: weigh again.',
'Aiguillage %s : branche %d':'Junction %s: branch %d','Lancer la capsule':'Launch the capsule','La capsule est prête au départ.':'The capsule is ready at the start.',
'Essai réussi : la capsule atteint EXPÉDITION. Validez.':'Successful trial: capsule reaches DISPATCH. Validate.',
'Mauvaise destination : la capsule revient au départ.':'Wrong destination: capsule returns to the start.',
'DÉPART':'SUPPLY','DÉPART CAPSULE':'START','RETOUR':'RETURN','EXPÉDITION':'DISPATCH',
'Destinataire : %s':'Recipient: %s','Aile : %s':'Wing: %s','Bureau : %d':'Office: %d',
'Mme Faraday':'Ms Faraday','Dr Folamour':'Dr Folamour','M. Foucault':'Mr Foucault',
'Colis incorrect. Comparez des groupes de même taille et choisissez le plus lourd.':'Incorrect parcel. Compare equal-sized groups and select the heavier parcel.',
'Le dernier essai doit atteindre EXPÉDITION. Réglez puis relancez la capsule.':'The latest trial must reach DISPATCH. Adjust and launch the capsule again.',
'Adresse refusée. Croisez le fragment, la fonction du destinataire et l’avis de déménagement.':'Address rejected. Cross-check the fragment, recipient’s role and relocation notice.'})
aid=json.loads((D/'guidance.json').read_text())
aid['hints'].update({
'm_balance':[['Comparez des groupes contenant le même nombre de colis.','Compare groups containing the same number of parcels.'],['Pesez A+B+C contre D+E+F. Puis comparez deux colis du côté le plus lourd.','Weigh A+B+C against D+E+F. Then compare two parcels from the heavier side.'],['La droite est plus lourde. Remettez tout en réserve ; pesez D à gauche contre E à droite. E est plus lourd. Choisissez E puis validez.','The right is heavier. Return everything to reserve; weigh D on the left against E on the right. E is heavier. Select E and validate.']],
'm_network':[['Suivez les traits qui relient le départ à l’expédition.','Follow the lines connecting the start to dispatch.'],['La bonne branche mène successivement à A, B, puis C. Évitez les sorties RETOUR.','The correct branch leads through A, B, then C. Avoid RETURN exits.'],['Réglez A sur branche 2, B sur branche 1 et C sur branche 2. Lancez la capsule, puis validez.','Set A to branch 2, B to branch 1 and C to branch 2. Launch the capsule, then validate.']],
'm_address':[['Le fragment donne une fonction, pas seulement une initiale.','The fragment gives a role, not just an initial.'],['La direction scientifique désigne Folamour. L’annuaire indique son ancienne adresse ; appliquez le déménagement.','Scientific management identifies Folamour. The directory gives his old address; apply the relocation.'],['Destinataire Dr Folamour ; aile OUEST ; bureau 4. Validez, puis livrez le colis au guichet 101.','Recipient Dr Folamour; WEST wing; office 4. Validate, then deliver the parcel at counter 101.']]})
aid['objectives'].update({
'm_balance':['Récupérer le lot 201 et identifier le colis plus lourd sur la balance 203 à l’ouest.','Collect batch 201 and identify the heavier parcel at western balance 203.'],
'm_network':['Trouver la capsule 301 puis l’acheminer à l’expédition par le réseau 303.','Find capsule 301 and route it to dispatch through network 303.'],
'm_label':['Récupérer le fragment d’étiquette 401 dans l’aile sud.','Collect label fragment 401 in the southern wing.'],
'm_address':['Croiser les références 401, 402 et 404 pour adresser le colis en 403.','Cross-check references 401, 402 and 404 to address the parcel at 403.'],
'm_delivery':['Remettre le colis adressé au guichet 101, à la réception est.','Hand over the addressed parcel at counter 101, at eastern reception.']})
aid['stages']['8']=[[[k],k] for k in ['m_balance','m_network','m_label','m_address','m_delivery']]
for name,data in [('maze8',{'grid':g,'start':[31,19]}),('events8',E),('items8',items),('en',en),('guidance',aid)]: (D/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
if not (D/'shortcuts8.json').exists():(D/'shortcuts8.json').write_text(json.dumps([{'id':'C'+str(i)} for i in range(1,7)])+'\n')
print('Level 8:',len(E),'events')
