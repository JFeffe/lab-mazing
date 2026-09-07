"""Create versioned, source-grounded level-four maps and solutions."""
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
D=r/'game/data';m=json.loads((D/'maze4.json').read_text());E=json.loads((D/'events4.json').read_text());S=json.loads((D/'shortcuts4.json').read_text());by={e['id']:e for e in E}
font=str(r/'game/assets/Interface.ttf');pdfmetrics.registerFont(TTFont('Interface',font))
# High-resolution map: cells and numbers come directly from the shipped JSON.
im=Image.new('RGB',(2020,1740),'#101f2b');dr=ImageDraw.Draw(im)
def txt(x,y,t,size=24,color='#e7edf0'):dr.text((x,y),t,font=ImageFont.truetype(font,size),fill=color)
txt(65,35,'FOLAMOUR  /  V0.8  /  NIVEAU 4  /  SPOILERS',27,'#e9be72')
txt(65,88,'LE DÉPARTEMENT DES ESSAIS',46)
txt(65,153,'Carte complète - coordonnées (x, y) à partir de 0 - nord en haut',23)
ox,oy,cell=95,232,38
pal=['#a18d72','#788ba2','#6b968d']
for y,row in enumerate(m['grid']):
 for x,v in enumerate(row):
  dr.rectangle((ox+x*cell,oy+y*cell,ox+(x+1)*cell-1,oy+(y+1)*cell-1),fill=pal[0 if y<12 else 1 if y<24 else 2] if v else '#20313e')
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
sx=1480
txt(sx,232,'REPÈRES',26,'#e9be72')
for i,e in enumerate(E):
 txt(sx,280+i*42,e['ref']+'  '+e['title'],18,cs[e['kind']])
txt(sx,1290,'LÉGENDE',24,'#e9be72')
for i,(t,col) in enumerate([('Or : objet à ramasser','#e9be72'),('Turquoise : note / indice','#8eddd5'),('Bleu : assemblage / mécanisme','#93aff0'),('Corail : porte verrouillée','#ee9478'),('Blanc : sortie','#ffffff'),('Vert T1-T6 : raccourci à révéler','#54cda4')]):txt(sx,1332+i*34,t,19,col)
txt(65,1610,'DÉPART : 100 (1, 1)     |     SORTIE : 305 (17, 33)     |     SECRETS : 108, 208, 306',24,'#e9be72')
txt(65,1660,'Les raccourcis apparaissent après avoir marché de leurs deux côtés. Les cases vertes sont des murs au départ.',22)
map_png=out/'Niveau-4-v0.8-Map-vue-de-haut.png';im.save(map_png)
c=canvas.Canvas(str(out/'Niveau-4-v0.8-Map-vue-de-haut.pdf'),pagesize=landscape(A3));w,h=landscape(A3);scale=min(w/im.width,h/im.height);c.drawImage(str(map_png),(w-im.width*scale)/2,(h-im.height*scale)/2,im.width*scale,im.height*scale);c.showPage();c.save()
styles=getSampleStyleSheet()
for name in styles.byName:styles[name].fontName='Interface'
styles.add(ParagraphStyle(name='Main',fontName='Interface',fontSize=25,leading=31,textColor=colors.HexColor('#173743'),spaceAfter=20))
styles.add(ParagraphStyle(name='Body',fontName='Interface',fontSize=10.5,leading=16,spaceAfter=12))
styles.add(ParagraphStyle(name='Section',fontName='Interface',fontSize=17,leading=22,textColor=colors.HexColor('#236878'),spaceBefore=10,spaceAfter=13))
styles.add(ParagraphStyle(name='SmallCell',fontName='Interface',fontSize=8.5,leading=12))
story=[];md=['# Lab-Mazing v0.8 - Niveau 4 : Département des essais\n\n**SPOILERS : solutions complètes.**\n']
def p(t,style='Body'):story.append(Paragraph(escape(t).replace('\n','<br/>'),styles[style]));md.append(t+'\n')
def page(title):
 if story:story.append(PageBreak())
 p(title,'Main')
def table(rows,widths):
 cells=[[Paragraph(escape(str(t)),styles['SmallCell']) for t in row] for row in rows]
 t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#deecec')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#c6d4d8'))]));story.append(t);story.append(Spacer(1,10))
 md.extend([' | '.join(map(str,row))+'\n' for row in rows])
page('Niveau 4\nLe département des essais')
p('FOLAMOUR / VERSION 0.8 / SOLUTIONS COMPLÈTES','Section')
p('Trois nouvelles manipulations remplacent les codes : répartir des masses, composer une séquence et inverser des voyants. Une récupération à l’aimant relie les objets des deux derniers secteurs.')
p('Accès : reprendre un niveau 3 terminé et choisir « Continuer vers le niveau 4 ». Pour un test indépendant, « Tester directement le niveau 4 » remplace la partie actuelle après confirmation.')
table([['Secteur','Épreuve','Solution rapide'],['Masses (haut)','Balance 106','Gauche : 1 + 5 kg ; droite : 2 + 3 kg'],['Séquences (centre)','Console 204','Lune / Étoile / Soleil / Planète / Comète'],['Circuits (bas)','Tableau 304','Depuis Réinitialiser : leviers I, III, IV']],[100,130,275])
p('Parcours conseillé','Section')
p('100 → 101, 102, 103, 104, 105 → 106 → porte 107.\n201, 202, 203 → 204 → ramasser 205 et 206 → porte 207.\n301 → 302, 303 → 304 → sas 305.\nLes détours vers les secrets 108, 208 et 306 sont facultatifs.')
p('Carte exacte','Section')
p('La carte est générée à partir du labyrinthe livré. Coordonnées (x, y), origine (0, 0) en haut à gauche : x augmente vers la droite et y vers le bas. Les nombres à trois chiffres sont les repères du jeu. Les six raccourcis T1 à T6 se révèlent après un passage physique de leurs deux côtés.')
p('Les portes ouvertes restent ouvertes : un objet oublié peut toujours être récupéré. Les labyrinthes des niveaux précédents et leurs solutions restent inchangés.')
page('01 / La balance\nRépartir, pas équilibrer')
p('Ramasser les quatre masses','Section')
table([['Repère','Coordonnées','Objet'],['101','(31, 1)','1 kg'],['102','(3, 9)','2 kg'],['103','(21, 5)','3 kg'],['104','(33, 9)','5 kg']],[75,130,300])
p('Lire 105 (1, 7), puis installer les quatre masses dans la balance 106 (17, 7). Chaque bouton déplace une masse selon le cycle réserve → gauche → droite → réserve.')
p('Le raisonnement','Section')
p('La consigne impose toutes les masses, exactement deux par plateau, et 1 kg de plus à gauche. Le total est 11 kg : gauche = 6 kg et droite = 5 kg. Avec deux masses par plateau, la seule répartition est 1 + 5 à gauche et 2 + 3 à droite.')
table([['Masse','Emplacement','Pressions depuis Réinitialiser'],['1 kg','GAUCHE','1'],['2 kg','DROITE','2'],['3 kg','DROITE','2'],['5 kg','GAUCHE','1']],[95,160,250])
p('Choisir « Valider l’essai ». La porte 107 (9, 11) s’ouvre. Le déséquilibre visible est volontaire : une balance parfaitement horizontale ne respecte pas la consigne.')
p('Une erreur laisse les masses installées. « Réinitialiser cet essai » remet leurs emplacements à la réserve de la balance ; les objets ne retournent pas au sac et ne sont pas perdus.')
page('02 / L’ordre de lancement\nEt les objets à emporter')
p('Recouper trois rapports','Section')
table([['Repère','Règle','Conséquence'],['201 (1, 13)','Soleil en troisième position','Case 3 = Soleil'],['202 (33, 15)','Lune immédiatement avant Étoile','Le duo doit rester adjacent'],['203 (7, 21)','Comète dernière ; Planète après Soleil','Case 5 = Comète ; case 4 = Planète']],[100,230,175])
p('Il reste les deux premières cases pour le duo Lune / Étoile. L’unique ordre est donc : LUNE → ÉTOILE → SOLEIL → PLANÈTE → COMÈTE.')
p('À la console 204 (19, 17), toucher les cinq symboles dans cet ordre, puis « Valider l’essai ». Un symbole déjà choisi devient indisponible. « Retirer le dernier symbole » annule la dernière entrée ; « Réinitialiser cet essai » vide la suite.')
p('La validation ouvre 207 (27, 23) et délivre un fusible de sécurité. Il est ajouté automatiquement au sac, une seule fois.')
p('Préparer la récupération','Section')
p('Ramasser l’aimant 205 (31, 21) et la corde 206 (3, 17). Après la porte 207, rejoindre le conduit 301 (1, 25). Choisir « Nouer l’aimant et récupérer le contact ».')
p('Le contact métallique est ajouté au sac. L’aimant et la corde restent attachés au conduit. Il n’est pas nécessaire de chercher un établi : les deux objets sont employés ensemble sur place.')
p('Pièces requises au prochain tableau : le fusible reçu en 204 et le contact récupéré en 301. Les secteurs précédents restent accessibles si l’aimant ou la corde ont été oubliés.')
page('03 / Les inverseurs\nPenser aux effets croisés')
p('Installer avant de régler','Section')
p('Lire 302 (33, 25) et 303 (9, 29), puis installer le fusible et le contact dans le tableau 304 (29, 29). Les voyants A et D sont allumés au départ. Chaque levier inverse ses voyants : allumé devient éteint et inversement.')
table([['Levier','Voyants inversés'],['I','A + B'],['II','B + C'],['III','C + D'],['IV','A + D + E']],[100,405])
p('Pour retrouver un état connu, choisir « Réinitialiser cet essai ». Les pièces restent installées. Actionner ensuite I, III et IV, une fois chacun ; laisser II intact.')
table([['Étape','Voyants allumés'],['Départ / Réinitialiser','A, D'],['Après I','B, D'],['Après III','B, C'],['Après IV','A, B, C, D, E']],[190,315])
p('Pourquoi cela marche : E ne dépend que de IV, donc IV est nécessaire. Son effet sur D doit être compensé par III. III allume C ; II doit rester inchangé. Enfin I corrige A et allume B. L’ordre des trois leviers est libre ; deux pressions sur le même levier s’annulent.')
p('Choisir « Valider l’essai », puis rejoindre le sas 305 (17, 33) et « Terminer les essais ». Balance, séquence et circuit doivent tous être validés. Aucun autre code n’est nécessaire.')
page('Tous les repères')
table([['Repère','Nom','(x, y)']]+[[e['ref'],e['title'],str(tuple(e['cell']))] for e in E],[55,365,85])
page('Secrets et reprise\nTester sans se bloquer')
p('Les trois secrets','Section')
p('108 (33, 3) : Régime expérimental.\n208 (33, 13) : Compte rendu du lancement.\n306 (1, 33) : Certificat provisoire.\nLire les trois avant de terminer pour obtenir 3 / 3 au bilan.')
p('Ce qui reste sauvegardé','Section')
p('La position de chaque masse, les symboles déjà saisis et l’état des cinq voyants sont enregistrés après chaque manipulation. Les objets installés, portes ouvertes, notes lues, découvertes et bilans précédents sont également conservés. La sauvegarde automatique reste propre au navigateur et à l’appareil.')
p('Les boutons de réinitialisation ne concernent que l’essai affiché. Ils ne ferment pas les portes, ne recommencent pas le niveau et ne consomment pas de nouvelles pièces. Une mauvaise réponse augmente seulement le compteur d’erreurs.')
p('Contrôles conseillés','Section')
p('1. Placer une masse, fermer le menu et reprendre : l’emplacement doit rester identique.\n2. Entrer deux symboles, puis reprendre : ils doivent être conservés ; retirer le dernier doit fonctionner.\n3. Actionner un levier deux fois : les voyants doivent revenir à leur état précédent.\n4. Réinitialiser le tableau après installation : fusible et contact doivent rester installés.\n5. Revenir dans le secteur précédent : les portes validées doivent rester ouvertes.')
p('Retour de test','Section')
p('Indiquer v0.8, niveau 4, repère ou coordonnées, action effectuée et résultat attendu. Exemple : « 304, après deux pressions sur III, le voyant D ne revient pas à son état précédent. »')
def footer(c,doc):
 c.setFont('Interface',8);c.setFillColor(colors.HexColor('#57727c'));c.drawString(44,28,'FOLAMOUR / V0.8 / NIVEAU 4 / SPOILERS');c.drawRightString(A4[0]-44,28,str(doc.page))
SimpleDocTemplate(str(out/'Niveau-4-v0.8-Cheatsheet-solutions.pdf'),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=44,bottomMargin=46).build(story,onFirstPage=footer,onLaterPages=footer)
(out/'Niveau-4-v0.8-Cheatsheet-solutions.md').write_text('\n'.join(md))
(out/'Resume-v0.8.md').write_text('''# Lab-Mazing - Version 0.8

## Niveau 4 : département des essais
- Nouveau labyrinthe à trois secteurs, avec boucles, six raccourcis, 23 repères et trois secrets.
- Balance interactive : placer quatre masses sur deux plateaux selon des contraintes.
- Console de séquence : déduire un ordre de cinq symboles à partir de trois rapports.
- Récupération d’un contact avec un aimant et une corde, puis installation avec un fusible.
- Circuit à inverseurs : quatre leviers modifient plusieurs voyants à la fois.
- Réinitialisation réversible et sauvegarde des manipulations partielles.
- Tout le nouveau contenu est disponible en français et en anglais.

## Accès
Continuer après un niveau 3 terminé ou choisir « Tester directement le niveau 4 » au menu. L’accès direct remplace la partie après confirmation. Les sauvegardes v0.7 restent compatibles.

## Documents
Carte exacte en PNG et PDF A3 ; solutions détaillées en PDF (6 pages) et Markdown ; présent résumé. Les anciens documents restent dans leurs dossiers de version.

## Validation
Solutions uniques vérifiées exhaustivement, progression complète avec collisions et boutons, reprise des trois énigmes partielles, objets conservés après réinitialisation.
La sauvegarde reste propre au navigateur et à l’appareil.

Jeu : https://jfeffe.github.io/lab-mazing/
Sources : https://github.com/JFeffe/lab-mazing
''')
print('Documents written to',out)
