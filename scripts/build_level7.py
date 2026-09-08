"""Office assignment: three reversible puzzles in wings around a central reception."""
from pathlib import Path
from itertools import product
import json, random
D=Path(__file__).resolve().parents[1]/'game/data'
g=[[0]*35 for _ in range(35)];rng=random.Random(130702)
for x0,x1,y0,y1 in [(1,15,1,13),(19,33,1,13),(1,33,21,33)]:
 stack=[(x0,y0)];g[y0][x0]=1
 while stack:
  x,y=stack[-1];ns=[(x+dx,y+dy) for dx,dy in [(2,0),(-2,0),(0,2),(0,-2)] if x0<=x+dx<=x1 and y0<=y+dy<=y1 and not g[y+dy][x+dx]]
  if not ns:stack.pop();continue
  a,b=rng.choice(ns);g[(b+y)//2][(a+x)//2]=g[b][a]=1;stack.append((a,b))
for y in range(15,20):
 for x in range(13,22):g[y][x]=1
for x in range(5,26):g[17][x]=1
for y in range(13,18):g[y][5]=g[y][25]=1
for y in range(19,22):g[y][17]=1
E=[];en=json.loads((D/'en.json').read_text())
def tr(fr,eng):en[fr]=eng;return fr
def ev(id,kind,cell,ref,title,text,**kw):
 e=dict(id=id,kind=kind,cell=cell,ref=str(ref),title=tr(*title),text=tr(*text),**kw);E.append(e);return e
def result(e,fr,eng):e['success']=tr(fr,eng)
def rotate(a):return [a[(2-x)*3+y] for y in range(3) for x in range(3)]
def overlay(masks,s):
 out=[0]*9
 for a,n in zip(masks,s):
  for _ in range(n):a=rotate(a)
  out=[int(x or y) for x,y in zip(out,a)]
 return out
# Choose sparse asymmetric layers whose composite has exactly one orientation tuple.
masks=[[1,0,0,0,0,0,1,0,0],[0,0,0,0,1,0,1,1,0],[0,0,0,0,1,0,0,1,0]]
solution=[1,3,2];target=overlay(masks,solution)
assert sum(overlay(masks,s)==target for s in product(range(4),repeat=3))==1
ev('p_welcome','clue',[17,17],100,('Service des photocopies','Photocopy service'),('Accueil central. Préparation à l’ouest, archives au nord-est, salle des copies au sud. Le badge des archives est délivré par la table lumineuse 203. Le classement 303 ouvre la salle des copies.','Central reception. Preparation to the west, archives to the northeast, copy room to the south. Light table 203 issues the archive badge. Filing station 303 opens the copy room.'))
ev('p_delivery','exit',[21,19],101,('Bac de livraison','Delivery tray'),('Déposez la copie approuvée par la machine 403. Folamour attend UNE copie conforme au modèle.','Deliver the copy approved by machine 403. Folamour expects ONE copy matching the reference.'),requires=['approved_copy'],prerequisites=['p_overlay','p_filing','p_copier'],action=tr('Livrer la copie','Deliver the copy'))
ev('p_archive_door','door',[25,15],102,('Porte des archives','Archive door'),('La table lumineuse 203 autorise l’accès aux archives.','Light table 203 authorises archive access.'),axis='y',controlled_by='p_overlay')
ev('p_copy_door','door',[17,20],103,('Porte de la salle des copies','Copy room door'),('Le classement validé en 303 déverrouille cette porte.','Approved filing at 303 unlocks this door.'),axis='y',controlled_by='p_filing')
ev('p_layers','pickup',[1,1],201,('Pochette de transparents','Transparency sleeve'),('Trois calques A, B et C pour la table 203. Les marques noires se superposent : elles ne s’effacent jamais.','Three layers A, B and C for table 203. Black marks overlap; they never cancel each other.'),resource='layers',amount=1,appearance='card')
ev('p_overlay_note','clue',[15,1],202,('Notice de la table','Light table instructions'),('Tournez séparément les calques A, B et C par quarts de tour. Une case est noire si AU MOINS UN calque la marque. Reproduisez exactement le modèle, sans case noire supplémentaire. Les trois petits tableaux montrent chaque calque orienté.','Rotate layers A, B and C independently in quarter turns. A cell is black if AT LEAST ONE layer marks it. Match the reference exactly, with no extra black cells. The three small boards show each rotated layer.'))
e=ev('p_overlay','mechanism',[9,9],203,('Table lumineuse','Light table'),('Installez la pochette 201. Superposez les trois calques pour reproduire le modèle. Le résultat change à chaque rotation.','Install sleeve 201. Superimpose all three layers to match the reference. The result changes with each rotation.'),requires=['layers'],puzzle_type='overlay',model='overlay',masks=masks,target=target,opens=['p_archive_door'])
result(e,'Les marques concordent. Les archives sont accessibles. « Bravo. Vous venez de rendre trois feuilles aussi utiles qu’une seule. » — Folamour','The marks match. The archives are accessible. “Well done. You have made three sheets as useful as one.” — Folamour')
ev('p_overlay_tip','clue',[1,13],204,('Note du technicien','Technician’s note'),('Commencez par éviter les cases que le modèle laisse blanches. Ensuite, cherchez les marques manquantes. Chaque calque peut couvrir une marque déjà présente.','First avoid cells that are white in the reference. Then look for missing marks. A layer may cover a mark already present.'))
ev('p_files','pickup',[33,1],301,('Dossiers à classer','Files to sort'),('Quatre dossiers : Lune, Miroir, Serre et Zéro. À installer dans le classeur 303.','Four files: Moon, Mirror, Greenhouse and Zero. Install them in cabinet 303.'),resource='files',amount=1,appearance='card')
ev('p_valid_note','clue',[19,1],302,('Directive VALIDÉE — version B','APPROVED directive — version B'),('Seule la version B fait foi. Quatre casiers numérotés de gauche à droite, un dossier par casier. MIROIR est immédiatement à droite de SERRE. LUNE est à droite de MIROIR. ZÉRO occupe une extrémité, mais pas le casier 4.','Only version B is valid. Four slots numbered from left to right, one file per slot. MIRROR is immediately to the right of GREENHOUSE. MOON is to the right of MIRROR. ZERO is at an end, but not in slot 4.'))
e=ev('p_filing','mechanism',[29,11],303,('Classeur de validation','Approval cabinet'),('Installez les dossiers 301. Touchez chaque dossier pour choisir son casier de 1 à 4. Les doublons sont permis pendant les essais, mais la validation exige un dossier par casier et le respect de la directive VALIDÉE 302.','Install files 301. Tap each file to choose a slot from 1 to 4. Duplicates are allowed during trials, but approval requires one file per slot and compliance with APPROVED directive 302.'),requires=['files'],puzzle_type='filing',model='filing',opens=['p_copy_door'],grants={'master':1})
result(e,'Classement approuvé. La salle des copies est ouverte et l’original est récupéré. « Les dossiers étaient déjà classés. Mais maintenant, ils le sont correctement. » — Folamour','Filing approved. The copy room is open and the original is retrieved. “The files were already sorted. But now they are sorted correctly.” — Folamour')
ev('p_old_note','clue',[33,13],304,('Directive ANNULÉE — version A','CANCELLED directive — version A'),('ANNULÉE : « Lune dans le casier 1 ; Zéro dans le casier 4. » Tampon : remplacée par la version B, référence 302. Ce document explique l’ancien classement ; ne pas l’appliquer.','CANCELLED: “Moon in slot 1; Zero in slot 4.” Stamp: replaced by version B, reference 302. This document explains the old arrangement; do not apply it.'))
ev('p_paper','pickup',[1,21],401,('Papier homologué','Approved paper'),('Une rame entière pour une copie. La machine 403 conserve le papier pendant les essais.','A whole ream for one copy. Machine 403 keeps the paper during trials.'),resource='paper',amount=1,appearance='card')
ev('p_toner','pickup',[33,33],402,('Cartouche de toner','Toner cartridge'),('Du toner noir pour la machine 403. Aucun essai ne gaspille la cartouche.','Black toner for machine 403. Trials do not waste the cartridge.'),resource='toner',amount=1,appearance='key')
initial=[1,1,0,0,1,0,0,0,1];copy_target=rotate(initial);copy_target=[copy_target[y*3+2-x] for y in range(3) for x in range(3)]
e=ev('p_copier','mechanism',[17,29],403,('Photocopieur expérimental','Experimental photocopier'),('Installez l’original, le papier et le toner. Reproduisez le modèle en tournant l’image et en utilisant le miroir gauche-droite. Les transformations agissent sur l’image actuelle : leur ordre compte.','Install the original, paper and toner. Match the reference by rotating the image and using the left-right mirror. Transformations act on the current image: their order matters.'),requires=['master','paper','toner'],puzzle_type='copier',model='copier',initial=initial,target=copy_target,grants={'approved_copy':1})
result(e,'Copie conforme. Rapportez-la au bac 101 dans l’accueil central. « Incroyable. Du papier qui ressemble à du papier. » — Folamour','Copy approved. Return it to tray 101 at central reception. “Incredible. Paper that looks like paper.” — Folamour')
ev('p_copy_note','clue',[33,21],404,('Notice des transformations','Transformation instructions'),('Rotation : un quart de tour dans le sens horaire. Miroir : échange la gauche et la droite, sans échanger le haut et le bas. On peut toujours annuler : quatre rotations ou deux miroirs retrouvent l’image de départ.','Rotation: a clockwise quarter turn. Mirror: swaps left and right, without swapping top and bottom. You can always undo: four rotations or two mirrors restore the starting image.'))
for id,cell,ref,fr,eng in [
 ('p_secret1',[15,13],205,'Formulaire 8 : demande d’autorisation de demander une autorisation. À fournir en trois exemplaires identiques.','Form 8: request for permission to request permission. Submit three identical copies.'),
 ('p_secret2',[19,13],305,'Rapport RH : « Le stage est enrichissant. » La comptabilité confirme que cela ne concerne pas le stagiaire.','HR report: “The internship is enriching.” Accounting confirms this does not apply to the intern.'),
 ('p_secret3',[1,33],405,'La touche « économie » réduit la consommation de toner et augmente le temps de travail. Gain net pour le laboratoire.','The “economy” button reduces toner use and increases working time. A net gain for the laboratory.')]:ev(id,'clue',cell,ref,('Archive administrative '+str(ref),'Administrative archive '+str(ref)),(fr,eng),secret=True)
items={e['resource']:{'title':e['title'],'text':e['text']} for e in E if e['kind']=='pickup'}
for id,fr,eng,desc,edesc in [('master','Original validé','Approved original','À installer au photocopieur 403.','Install in photocopier 403.'),('approved_copy','Copie conforme','Approved copy','À livrer au bac 101.','Deliver to tray 101.')]:items[id]={'title':tr(fr,eng),'text':tr(desc,edesc)}
translations={
'VERSION 0.13 · LE SERVICE DES PHOTOCOPIES':'VERSION 0.13 · THE PHOTOCOPY SERVICE',
'Le chapitre 2 propose deux missions : les serres expérimentales et le service des photocopies.':'Chapter 2 offers two assignments: the experimental greenhouses and the photocopy service.',
'Deux missions disponibles : les serres, puis le service des photocopies.':'Two assignments available: the greenhouses, then the photocopy service.',
'C2 / MISSION 2 / PHOTOCOPIES':'C2 / ASSIGNMENT 2 / PHOTOCOPIES',
'Mission 2 — Le service des photocopies':'Assignment 2 — The photocopy service',
'« Votre café était presque tiède. Passons à une tâche à votre portée : une photocopie. Les archives sont verrouillées et le photocopieur inverse les images. Des détails, pour quelqu’un d’aussi peu rémunéré. » — Folamour':'“Your coffee was almost warm. Let us try something within your abilities: a photocopy. The archives are locked and the copier reverses images. Minor details, for someone so poorly paid.” — Folamour',
'Alignez les calques à l’ouest, classez les dossiers au nord-est, puis préparez la copie au sud. Rapportez-la à l’accueil. Les essais sont réversibles et sauvegardés.':'Align the western layers, sort the northeastern files, then prepare the copy in the south. Return it to reception. Trials are reversible and saved.',
'Accepter la mission':'Accept the assignment',
'STAGE / DEUXIÈME MISSION\nPréparer une photocopie : calques, classement, papier, toner et transformations. Livraison à l’accueil 101.':'INTERNSHIP / SECOND ASSIGNMENT\nMake a photocopy: layers, filing, paper, toner and transformations. Deliver to reception 101.',
'Passer aux photocopies':'Continue to photocopying',
'Votre bilan est sauvegardé. La deuxième mission du stage est disponible.':'Your results are saved. The second internship assignment is available.',
'CHAPITRE 2 / MISSION 2 TERMINÉE':'CHAPTER 2 / ASSIGNMENT 2 COMPLETE',
'Une copie presque parfaite.':'An almost perfect copy.',
'Folamour examine la feuille, la retourne et vous adresse un sourire satisfait.':'Folamour examines the sheet, turns it over and gives you a satisfied smile.',
'« Félicitations. Une copie parfaitement conforme ! J’avais oublié de préciser : je la voulais recto verso. Mais gardez votre enthousiasme, c’est la seule chose que nous ne fournissons pas. » — Folamour':'“Congratulations. A perfect copy! I forgot to mention: I wanted it double-sided. But keep your enthusiasm; it is the only thing we do not supply.” — Folamour',
'Mission réussie. Votre copie est acceptée et votre bilan est sauvegardé. La suite du stage arrivera plus tard.':'Assignment complete. Your copy is accepted and your results are saved. More internship assignments will arrive later.',
'Modèle à reproduire':'Reference to match','Résultat actuel':'Current result',
'Calque %s : %d°':'Layer %s: %d°','Casier de %s : %d':'Slot for %s: %d',
'Lune':'Moon','Miroir':'Mirror','Serre':'Greenhouse','Zéro':'Zero',
'Tourner de 90° ↻':'Rotate 90° ↻','Miroir gauche-droite ↔':'Left-right mirror ↔',
'Chaque case noire est marquée. Les cases claires sont vides.':'Each black cell is marked. Light cells are empty.',
'Les calques ne correspondent pas encore au modèle. Vérifiez les cases manquantes et les marques en trop.':'The layers do not match the reference yet. Check missing cells and extra marks.',
'Classement refusé. Un dossier par casier ; seule la directive validée fait foi.':'Filing rejected. One file per slot; only the approved directive is valid.',
'Image différente du modèle. La rotation et le miroir agissent sur le résultat actuel.':'Image differs from the reference. Rotation and mirror act on the current result.'}
en.update(translations)
aid=json.loads((D/'guidance.json').read_text())
aid['hints'].update({
'p_overlay':[['Comparez d’abord les cases blanches du modèle.','First compare the white cells in the reference.'],['Chaque calque se tourne séparément ; les marques superposées restent noires.','Each layer turns independently; overlapping marks stay black.'],['Après réinitialisation : A une fois (90°), B trois fois (270°), C deux fois (180°). Validez.','After reset: A once (90°), B three times (270°), C twice (180°). Validate.']],
'p_filing':[['Écartez la directive annulée. Cherchez une extrémité imposée.','Ignore the cancelled directive. Look for a forced end slot.'],['Zéro est en 1. Le bloc Serre–Miroir doit laisser une place à Lune sur sa droite.','Zero is in 1. The Greenhouse–Mirror block must leave a slot for Moon to its right.'],['De gauche à droite : Zéro, Serre, Miroir, Lune. Réglages Lune 4, Miroir 3, Serre 2, Zéro 1. Validez.','Left to right: Zero, Greenhouse, Mirror, Moon. Settings: Moon 4, Mirror 3, Greenhouse 2, Zero 1. Validate.']],
'p_copier':[['Repérez le groupe de trois marques et la marque isolée.','Locate the group of three marks and the isolated mark.'],['Une rotation seule ne suffit pas : le modèle est aussi réfléchi.','A rotation alone is not enough: the reference is reflected too.'],['Après réinitialisation : une rotation de 90° dans le sens horaire, puis un miroir gauche-droite. Validez et livrez la copie en 101.','After reset: one clockwise 90° rotation, then a left-right mirror. Validate and deliver the copy at 101.']]})
aid['objectives'].update({
'p_overlay':['Trouver les calques à l’ouest et reproduire le modèle à la table 203.','Find the western layers and match the reference at table 203.'],
'p_filing':['Récupérer les dossiers aux archives et les classer en 303 selon la directive validée 302.','Collect the archive files and sort them at 303 using approved directive 302.'],
'p_supplies':['Récupérer le papier 401 et le toner 402 dans l’aile sud.','Collect paper 401 and toner 402 in the southern wing.'],
'p_copier':['Installer le matériel en 403 et transformer l’image pour reproduire le modèle.','Install the supplies at 403 and transform the image to match the reference.'],
'p_delivery':['Rapporter la copie approuvée au bac 101, à l’accueil central.','Return the approved copy to tray 101 at central reception.']})
aid['stages']['7']=[[[k],k] for k in ['p_overlay','p_filing']]+[[['p_paper','p_toner'],'p_supplies']]+[[[k],k] for k in ['p_copier','p_delivery']]
for name,data in [('maze7',{'grid':g,'start':[17,19]}),('events7',E),('items7',items),('en',en),('guidance',aid)]: (D/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
if not (D/'shortcuts7.json').exists():(D/'shortcuts7.json').write_text(json.dumps([{'id':'p_shortcut'+str(i)} for i in range(1,7)])+'\n')
print('Level 7:',len(E),'events; masks',masks,'target',target)
