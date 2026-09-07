"""Create versioned, source-grounded level-five maps and solutions."""
from pathlib import Path
import json, sys
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A3, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xml.sax.saxutils import escape
r=Path(__file__).resolve().parents[1];out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
D=r/'game/data';m=json.loads((D/'maze5.json').read_text());E=json.loads((D/'events5.json').read_text());S=json.loads((D/'shortcuts5.json').read_text());by={e['id']:e for e in E}
font=str(r/'game/assets/Interface.ttf');pdfmetrics.registerFont(TTFont('Interface',font))
# High-resolution map: cells and numbers come directly from the shipped JSON.
im=Image.new('RGB',(2020,1740),'#101f2b');dr=ImageDraw.Draw(im)
def txt(x,y,t,size=24,color='#e7edf0'):dr.text((x,y),t,font=ImageFont.truetype(font,size),fill=color)
txt(65,35,'FOLAMOUR  /  V0.9  /  NIVEAU 5  /  SPOILERS',27,'#e9be72')
txt(65,88,'LE DÉFI DE FOLAMOUR',46)
txt(65,153,'Carte complète - coordonnées (x, y) à partir de 0 - nord en haut',23)
ox,oy,cell=95,232,38
pal=['#659b9d','#ac9070','#8982a9']
for y,row in enumerate(m['grid']):
 for x,v in enumerate(row):
  dr.rectangle((ox+x*cell,oy+y*cell,ox+(x+1)*cell-1,oy+(y+1)*cell-1),fill=pal[2 if y<12 else 0 if x<15 else 1 if x>19 else 2] if v else '#20313e')
for n in range(35):
 txt(ox+n*cell+7,oy-30,str(n),16,'#b7c7cf');txt(ox-35,oy+n*cell+8,str(n),16,'#b7c7cf')
cs={'pickup':'#e9be72','clue':'#8eddd5','craft':'#93aff0','mechanism':'#93aff0','door':'#ee9478','exit':'#ffffff'}
for e in E:
 x,y=e['cell'];x=ox+x*cell;y=oy+y*cell
 dr.rounded_rectangle((x+1,y+3,x+cell-2,y+cell-3),radius=5,fill=cs[e['kind']],outline='#101f2b',width=1)
 dr.text((x+cell/2,y+cell/2),e['ref'],anchor='mm',font=ImageFont.truetype(font,16),fill='#101f2b')
 if e.get('secret'):dr.rectangle((x+3,y+1,x+cell-4,y+4),fill='#ffffff')
for sc in S:
 x,y=sc['cell'];x=ox+x*cell;y=oy+y*cell
 dr.rectangle((x+3,y+3,x+cell-4,y+cell-4),fill='#54cda4')
 dr.text((x+cell/2,y+cell/2),sc['id'],anchor='mm',font=ImageFont.truetype(font,17),fill='#102b25')
x,y=m['start'];dr.ellipse((ox+x*cell+7,oy+y*cell+7,ox+x*cell+31,oy+y*cell+31),fill='#ffffff');txt(ox+x*cell+12,oy+y*cell+9,'D',16,'#101f2b')
sx=1480
txt(sx,232,'REPÈRES',26,'#e9be72')
for i,e in enumerate(E):
 txt(sx,280+i*42,e['ref']+'  '+e['title'],18,cs[e['kind']])
txt(sx,1290,'LÉGENDE',24,'#e9be72')
for i,(t,col) in enumerate([('Or : objet à ramasser','#e9be72'),('Turquoise : note / indice','#8eddd5'),('Bleu : assemblage / mécanisme','#93aff0'),('Corail : porte verrouillée','#ee9478'),('Blanc : sortie','#ffffff'),('Vert F1-F6 : raccourci à révéler','#54cda4')]):txt(sx,1332+i*34,t,19,col)
txt(65,1610,'DÉPART : (17, 21)     |     FINALE : 405 (17, 1)     |     SECRETS : 204, 304, 404',24,'#e9be72')
txt(65,1660,'Les raccourcis apparaissent après avoir marché de leurs deux côtés. Les cases vertes sont des murs au départ.',22)
map_png=out/'Niveau-5-v0.9-Map-vue-de-haut.png';im.save(map_png)
c=canvas.Canvas(str(out/'Niveau-5-v0.9-Map-vue-de-haut.pdf'),pagesize=landscape(A3));w,h=landscape(A3);scale=min(w/im.width,h/im.height);c.drawImage(str(map_png),(w-im.width*scale)/2,(h-im.height*scale)/2,im.width*scale,im.height*scale);c.showPage();c.save()
styles=getSampleStyleSheet()
for name in styles.byName:styles[name].fontName='Interface'
styles.add(ParagraphStyle(name='Main',fontName='Interface',fontSize=25,leading=31,textColor=colors.HexColor('#173743'),spaceAfter=20))
styles.add(ParagraphStyle(name='Body',fontName='Interface',fontSize=10.5,leading=16,spaceAfter=12))
styles.add(ParagraphStyle(name='Section',fontName='Interface',fontSize=17,leading=22,textColor=colors.HexColor('#236878'),spaceBefore=10,spaceAfter=13))
styles.add(ParagraphStyle(name='SmallCell',fontName='Interface',fontSize=8.5,leading=12))
story=[];md=['# Lab-Mazing v0.9 - Niveau 5 : Le défi de Folamour\n\n**SPOILERS : solutions complètes.**\n']
def p(t,style='Body'):story.append(Paragraph(escape(t).replace('\n','<br/>'),styles[style]));md.append(t+'\n')
def page(title):
 if story:story.append(PageBreak())
 p(title,'Main')
def table(rows,widths):
 cells=[[Paragraph(escape(str(t)),styles['SmallCell']) for t in row] for row in rows]
 t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#deecec')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#c6d4d8'))]));story.append(t);story.append(Spacer(1,10))
 md.append(' | '.join(map(str,rows[0])))
 md.append(' | '.join(['---']*len(rows[0])))
 md.extend(' | '.join(map(str,row)) for row in rows[1:])
 md.append('')
page('Niveau 5\nLe défi de Folamour')
p('FOLAMOUR / VERSION 0.9 / FIN DU CHAPITRE 1','Section')
p('SPOILERS : solutions, carte, secrets et scène finale. Le docteur apparaît pour la première fois en personne et défie le sujet 16 de stabiliser le prototype ZÉRO : personne n’y est encore arrivé.')
p('Un hall central dessert deux ailes accessibles dès le départ : dosage à l’ouest et transfert à l’est. On peut les résoudre dans les deux ordres. Leur assemblage ouvre une troisième aile au nord. La difficulté vient de nouvelles manipulations ; il n’y a pas de compte à rebours.')
table([['Étape','Solution rapide'],['203 / Doseur','Grand 5 L : remplir ; grand vers petit ; vider petit ; grand vers petit ; remplir grand ; grand vers petit. Résultat : 4 L / 3 L.'],['303 / Disques','A vers C, A vers B, C vers B, A vers C, B vers A, B vers C, A vers C.'],['103 / Assemblage','Installer la charge de 4 L et le noyau intact. Le sas 104 s’ouvre.'],['403 / Rotors','Depuis Réinitialiser : commande II deux fois, puis III une fois. A = EST, B = SUD, C = OUEST.'],['405 / Finale','Présenter le résultat à Folamour. Félicitations, stage non rémunéré, fin du chapitre 1.']],[125,380])
p('Accès et sauvegarde','Section')
p('Après le niveau 4, choisir « Continuer vers le niveau 5 ». Depuis le menu, « Choisir un chapitre » propose le chapitre 1 : niveaux 1 à 5 dans l’ordre. Le chapitre 2 est grisé. « Sélection de niveau / test » permet un accès direct au niveau 5 après confirmation du remplacement de la partie actuelle.')
p('Les sauvegardes v0.8 restent compatibles. Les manipulations partielles et les objets installés sont conservés. Réinitialiser une épreuve ne retire pas ses objets et ne ferme pas les accès déjà ouverts.')
page('01 / S’orienter\nUn hall, trois ailes')
table([['Repère','Lieu (x, y)','Rôle'],['Départ','(17, 21)','Première rencontre de Folamour'],['100','(17, 19)','Consigne générale'],['101','(19, 21)','Joint à prendre pour le doseur'],['102','(15, 13)','Plan des étapes'],['103','(17, 15)','Assemblage au retour des deux ailes'],['104','(17, 11)','Sas vers le nord'],['201 / 202 / 203','Ouest','Règle, conseil et doseur'],['301 / 302 / 303','Est','Règle, conseil et transfert'],['401 / 402 / 403','Nord','Orientations, liaisons et stabilisateur'],['405','(17, 1)','Démonstration et fin du chapitre']],[95,120,290])
p('Parcours conseillé','Section')
p('Hall : relever le défi, lire 100 et 102, ramasser le joint 101.\nOuest : lire 201 et 202 ; installer le joint en 203 ; réussir le dosage.\nEst : lire 301 et 302 ; réussir le transfert 303.\nHall : assembler les deux résultats en 103, puis franchir 104.\nNord : lire 401 et 402 ; installer la cartouche en 403 ; stabiliser les rotors ; rejoindre 405.')
p('Repères et raccourcis','Section')
p('Les coordonnées de la carte commencent à (0, 0) en haut à gauche. Le nord est en haut. Les six raccourcis F1 à F6 se révèlent après avoir marché de leurs deux côtés. Ils restent dans leurs ailes et ne contournent pas le sas principal. Aucun raccourci n’est obligatoire.')
p('Les détours vers les secrets 204, 304 et 404 sont facultatifs. Les ailes ouest et est restent accessibles une fois le sas nord ouvert.')
page('02 / Le doseur\nIsoler quatre litres')
p('Préparation','Section')
p('Prendre le joint 101 (19, 21), lire la règle 201 (1, 13) et le conseil 202 (13, 31), puis rejoindre le doseur 203 (3, 27). Installer le joint. Les réservoirs commencent à 0 L / 0 L.')
p('Le grand contient au maximum 5 L et le petit 3 L. Un transvasement continue jusqu’à vider la source ou remplir la destination. La cible porte uniquement sur le grand réservoir : exactement 4 L.')
table([['Étape','Commande','Grand / Petit'],['0','Réinitialiser cet essai','0 L / 0 L'],['1','Remplir le grand','5 L / 0 L'],['2','Transvaser grand vers petit','2 L / 3 L'],['3','Vider le petit','2 L / 0 L'],['4','Transvaser grand vers petit','0 L / 2 L'],['5','Remplir le grand','5 L / 2 L'],['6','Transvaser grand vers petit','4 L / 3 L']],[55,325,125])
p('Pourquoi cela fonctionne','Section')
p('On conserve d’abord 2 L dans le petit réservoir. Quand on remplit ensuite le grand à 5 L, le petit ne peut plus recevoir qu’un litre : il reste donc 4 L dans le grand.')
p('Choisir « Valider l’essai ». La charge de 4 L entre dans le sac ; le joint reste installé. Rapportez la charge à la station 103, avec le noyau de l’aile est. Aucun liquide n’est une ressource limitée.')
page('03 / Le transfert\nTrois disques, sept mouvements')
p('Lire 301 (33, 13) et 302 (21, 33), puis manipuler le transfert 303 (31, 27). Aucun objet préalable n’est nécessaire. A est le départ, B le support auxiliaire et C l’arrivée. Taille 1 = petit, 2 = moyen, 3 = grand.')
p('Seul le disque supérieur peut bouger ; un disque ne peut pas reposer sur un disque plus petit. Les commandes impossibles sont grisées. Les piles sont affichées du bas vers le haut.')
table([['Étape','Déplacement','A (bas-haut)','B (bas-haut)','C (bas-haut)'],['0','Départ','3 / 2 / 1','vide','vide'],['1','A vers C','3 / 2','vide','1'],['2','A vers B','3','2','1'],['3','C vers B','3','2 / 1','vide'],['4','A vers C','vide','2 / 1','3'],['5','B vers A','1','2','3'],['6','B vers C','1','vide','3 / 2'],['7','A vers C','vide','vide','3 / 2 / 1']],[45,105,118,118,119])
p('Le raisonnement','Section')
p('Les trois premiers mouvements déplacent la petite pile sur B. Le quatrième libère le grand disque et le place sur C. Les trois derniers reconstruisent la petite pile au-dessus de lui. Sept mouvements suffisent et constituent le minimum pour trois disques.')
p('Valider pour recevoir le noyau intact. Revenir au hall 103 avec le noyau et la charge de refroidissement. Installer les deux : ils deviennent une cartouche stable et le sas 104 se déverrouille. Aucun des deux objets ne doit être installé dans une autre machine.')
page('04 / Le stabilisateur\nRégler des rotors couplés')
p('Dans l’aile nord, lire 401 (1, 9) et 402 (33, 1). Installer la cartouche stable dans le stabilisateur 403 (25, 5). Chaque impulsion fait avancer deux rotors : NORD, EST, SUD, OUEST, puis NORD.')
table([['Commande','Rotors entraînés','Cible finale'],['I','A + B','A : EST'],['II','B + C','B : SUD'],['III','A + C','C : OUEST']],[100,190,215])
p('Solution depuis Réinitialiser','Section')
table([['Étape','Action','A','B','C'],['0','Réinitialiser','NORD','NORD','NORD'],['1','Commande II','NORD','EST','EST'],['2','Commande II','NORD','SUD','SUD'],['3','Commande III','EST','SUD','OUEST']],[55,150,100,100,100])
p('Le rotor A reçoit une impulsion, B en reçoit deux et C en reçoit trois. Deux impulsions de II préparent B et C ; une impulsion de III termine A et C. Il n’est pas nécessaire d’utiliser toutes les commandes.')
p('Choisir « Valider l’essai ». Rejoindre le pupitre 405 (17, 1) et choisir « Présenter le résultat à Folamour ». La finale reste verrouillée tant que le dosage, le transfert, l’assemblage et la stabilisation ne sont pas terminés.')
p('En cas d’erreur','Section')
p('Un rotor déjà bien orienté peut encore tourner avec son voisin : les liaisons restent actives. Réinitialiser remet les trois directions au nord sans retirer la cartouche. Toutes les configurations atteignables permettent encore de réussir.')
page('05 / Secrets et finale\nLa proposition de Folamour')
table([['Secret','Coordonnées','Contenu'],['204','(1, 33)','Budget des graduations : le stagiaire qui compte'],['304','(33, 33)','Le candidat qui déplaçait le laboratoire'],['404','(3, 1)','Le contrat dont la rémunération a été découpée']],[70,105,330])
p('Début : une rencontre en personne','Section')
p('Folamour apparaît en blouse blanche, lunettes et cheveux ébouriffés. Il taquine le sujet 16, soupçonne ses labyrinthes d’être trop accueillants, puis présente ZÉRO. Le défi : réussir là où tous ses assistants ont échoué. « Relever le défi » lance l’exploration et consigne l’objectif au journal.')
p('Fin : les félicitations et le stage','Section')
p('Après la démonstration 405, Folamour revient constater la stabilité parfaite. Il félicite le joueur : personne n’y était jamais arrivé. Puis son humour reprend le dessus : il propose un stage dans son laboratoire, non rémunéré, pour ne pas « fausser l’expérience avec de l’argent ».')
p('L’écran affiche « FIN DU CHAPITRE 1 », les résultats du niveau et le bilan des niveaux terminés dans cette partie. Le choix du chapitre permet de reprendre ou recommencer le chapitre 1 ; le chapitre 2 reste indisponible. Un test direct ne fabrique pas de bilans pour les niveaux sautés.')
p('Contrôles effectués','Section')
p('Les deux ordres de visite ouest/est sont accessibles. Le sas nord bloque réellement le passage. Le parcours complet est testé avec collisions et boutons, ainsi que la reprise des trois énigmes partielles, le maintien des objets installés et la fin sauvegardée. Les états atteignables des énigmes sont vérifiés : 16 pour le dosage, 27 pour les disques, 32 pour les rotors.')
def footer(c,d):
 c.setFont('Interface',8);c.setFillColor(colors.HexColor('#53717b'));c.drawString(44,24,'FOLAMOUR / V0.9 / NIVEAU 5 / SOLUTIONS');c.drawRightString(A4[0]-44,24,str(d.page))
SimpleDocTemplate(str(out/'Niveau-5-v0.9-Cheatsheet-solutions.pdf'),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=42,bottomMargin=45).build(story,onFirstPage=footer,onLaterPages=footer)
(out/'Niveau-5-v0.9-Cheatsheet-solutions.md').write_text('\n'.join(md))
(out/'Resume-v0.9.md').write_text('''# Lab-Mazing - Version 0.9

Le chapitre 1 est complet : cinq niveaux dans l’ordre, avec un choix de chapitre au menu. Seul le chapitre 1 est disponible.

## Niveau 5 : le défi de Folamour
Hall central, ailes ouest et est explorables librement, puis aile nord verrouillée. 18 repères, trois secrets et six raccourcis. Trois nouvelles manipulations : dosage 5/3 litres, transfert de trois disques, rotors couplés. Les manipulations sont sauvegardées et réinitialisables.

Folamour apparaît pour la première fois en personne. Il taquine le joueur et lui lance un défi que personne n’a réussi. À la fin, il revient le féliciter et lui propose un stage non rémunéré. Fin du chapitre 1.

## Accès
Reprendre un niveau 4 terminé, puis continuer vers le niveau 5. Pour un essai isolé : « Sélection de niveau / test » au menu. Cela remplace la partie après confirmation. Les sauvegardes v0.8 restent compatibles et demeurent propres à l’appareil et au navigateur.

## Documents
Carte exacte en PNG et PDF A3 ; solutions détaillées en PDF (6 pages) et Markdown ; présent résumé. Les fichiers des versions précédentes restent dans leurs dossiers.

## Validation
Parcours complet avec collisions, commandes, transitions et sauvegardes. Les deux ordres de visite des premières ailes sont validés. Tous les états atteignables des énigmes restent résolubles. Interface française et anglaise, géométrie mobile portrait et paysage vérifiées automatiquement.

Jeu : https://jfeffe.github.io/lab-mazing/
Sources : https://github.com/JFeffe/lab-mazing
''')
print('Documents written to',out)
