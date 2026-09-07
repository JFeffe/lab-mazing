"""Create versioned, source-grounded level-three maps and solutions."""
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
D=r/'game/data';m=json.loads((D/'maze3.json').read_text());E=json.loads((D/'events3.json').read_text());S=json.loads((D/'shortcuts3.json').read_text());by={e['id']:e for e in E}
font=str(r/'game/assets/Interface.ttf');pdfmetrics.registerFont(TTFont('Interface',font))
# High-resolution map: cells and numbers come directly from the shipped JSON.
im=Image.new('RGB',(2020,1740),'#101f2b');dr=ImageDraw.Draw(im)
def txt(x,y,t,size=24,color='#e7edf0'):dr.text((x,y),t,font=ImageFont.truetype(font,size),fill=color)
txt(65,35,'FOLAMOUR  /  V0.7  /  NIVEAU 3  /  SPOILERS',27,'#e9be72')
txt(65,88,'LE DÉPARTEMENT D’OPTIQUE',46)
txt(65,153,'Carte complète - coordonnées (x, y) à partir de 0 - nord en haut',23)
ox,oy,cell=95,232,38
pal=['#7789a5','#638f94','#93839e']
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
for i,(t,col) in enumerate([('Or : objet à ramasser','#e9be72'),('Turquoise : note / indice','#8eddd5'),('Bleu : assemblage / mécanisme','#93aff0'),('Corail : porte verrouillée','#ee9478'),('Blanc : sortie','#ffffff'),('Vert O1-O6 : raccourci à révéler','#54cda4')]):txt(sx,1332+i*34,t,19,col)
txt(65,1610,'DÉPART : 100 (1, 1)     |     SORTIE : 306 (17, 33)     |     SECRETS : 106, 208, 307',24,'#e9be72')
txt(65,1660,'Les raccourcis apparaissent après avoir marché de leurs deux côtés. Les cases vertes sont des murs au départ.',22)
map_png=out/'Niveau-3-v0.7-Map-vue-de-haut.png';im.save(map_png)
c=canvas.Canvas(str(out/'Niveau-3-v0.7-Map-vue-de-haut.pdf'),pagesize=landscape(A3));w,h=landscape(A3);scale=min(w/im.width,h/im.height);c.drawImage(str(map_png),(w-im.width*scale)/2,(h-im.height*scale)/2,im.width*scale,im.height*scale);c.showPage();c.save()
styles=getSampleStyleSheet()
for name in styles.byName:styles[name].fontName='Interface'
styles.add(ParagraphStyle(name='Main',fontName='Interface',fontSize=25,leading=31,textColor=colors.HexColor('#173743'),spaceAfter=20))
styles.add(ParagraphStyle(name='Body',fontName='Interface',fontSize=10.5,leading=16,spaceAfter=12))
styles.add(ParagraphStyle(name='Section',fontName='Interface',fontSize=17,leading=22,textColor=colors.HexColor('#236878'),spaceBefore=10,spaceAfter=13))
styles.add(ParagraphStyle(name='SmallCell',fontName='Interface',fontSize=8.5,leading=12))
story=[];md=['# Lab-Mazing v0.7 - Niveau 3 : Département d’optique\n\n**SPOILERS : solutions complètes.**\n']
def p(t,style='Body'):story.append(Paragraph(escape(t).replace('\n','<br/>'),styles[style]));md.append(t+'\n')
def page(title):
 if story:story.append(PageBreak())
 p(title,'Main')
def table(rows,widths):
 cells=[[Paragraph(escape(str(t)),styles['SmallCell']) for t in row] for row in rows]
 t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#deecec')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#c6d4d8'))]));story.append(t);story.append(Spacer(1,10))
 md.extend([' | '.join(map(str,row))+'\n' for row in rows])
page('Niveau 3\nLe département d’optique')
p('FOLAMOUR / VERSION 0.7 / SOLUTIONS COMPLÈTES','Section')
p('Objectif : réparer le projecteur, calibrer les faisceaux et déchiffrer les archives pour entrer dans la chambre d’observation. Aucun chronomètre limite la partie.')
p('Accès : terminer le niveau 2 puis choisir « Continuer vers le niveau 3 ». Pour tester uniquement ce niveau, choisir « Tester directement le niveau 3 » au menu. Attention : commencer une nouvelle partie remplace la progression actuelle.')
p('Trois secteurs, trois raisonnements','Section')
table([['Secteur','But','Résultat'],['Optique (haut)','101 + 102 au banc 103, puis 104','Ouverture de 105'],['Faisceaux (centre)','Installer 201 dans 206 ; recouper 202-205','GAUCHE 3 / CENTRE 1 / DROITE 2'],['Archives (bas)','Note 209 + plaques 301-303 + consigne 304','Code 243 au lecteur 305 ; sortie 306']],[110,250,145])
p('La carte fournie est exacte : elle est générée depuis les données du jeu. Les coordonnées sont (x, y), avec x vers la droite et y vers le bas ; la première case est (0, 0). Les repères à trois chiffres correspondent aux numéros visibles dans le jeu.')
p('Les portes ouvertes restent ouvertes et aucun objet requis n’est caché derrière son propre verrou. Les trois secrets sont facultatifs. Les couleurs des faisceaux sont accompagnées de formes et de textes.')
page('01 / Assembler\n02 / Calibrer')
p('Secteur optique','Section')
p('1. Depuis 100 (1, 1), explorer les embranchements pour ramasser la lentille 101 (33, 1) et la bague 102 (1, 9).')
p('2. Au banc optique 103 (15, 5), choisir « Assembler l’objectif ». Les deux pièces sont consommées et l’objectif est ajouté au sac.')
p('3. Installer cet objectif dans le projecteur 104 (29, 7). La porte 105 (17, 11) se déverrouille. Le secteur précédent reste accessible.')
p('Secteur des faisceaux','Section')
p('4. Ramasser le prisme 201 (33, 13). Lire les trois étalons et le plan 205 (13, 13).')
table([['Étalon','Valeur','Destination donnée par 205'],['202 - Triangle (1, 15)','2','DROITE'],['203 - Cercle (31, 19)','3','GAUCHE'],['204 - Carré (9, 21)','1','CENTRE']],[200,55,250])
p('5. Au répartiteur 206 (17, 17), installer le prisme. Régler GAUCHE = 3, CENTRE = 1, DROITE = 2, puis valider. Le code est 312, dans l’ordre des molettes. La porte 207 (25, 23) s’ouvre.')
p('6. Avant de poursuivre, lire la note 209 (3, 19) : AUBE, ZÉNITH, CRÉPUSCULE. Cet ordre servira dans le secteur suivant. Il est possible de revenir la chercher plus tard.')
page('03 / Déchiffrer\nPuis sortir')
p('Archives optiques','Section')
p('7. Lire la consigne 304 (9, 29) : compter uniquement les traits éclairés, au-dessus de la ligne. Les traits du dessous sont des distracteurs.')
table([['Plaque','Éclairés','À ignorer'],['301 - Aube (1, 25)','2','5'],['302 - Zénith (33, 25)','4','1'],['303 - Crépuscule (33, 33)','3','6']],[280,100,125])
p('8. La note 209 donne l’ordre Aube / Zénith / Crépuscule : on obtient 2 / 4 / 3. Saisir 243 au lecteur 305 (29, 29).')
p('9. Rejoindre 306 (17, 33) et choisir « Entrer dans la chambre ». Le lecteur 305 et le répartiteur 206 doivent être validés. Le bilan du niveau apparaît ; les résultats des niveaux précédents sont conservés.')
p('Secrets facultatifs','Section')
p('106 (33, 9) : Note sur les lunettes.\n208 (1, 21) : Budget des couleurs.\n307 (1, 33) : Évaluation du sujet.\nLes lire avant de terminer pour obtenir 3 / 3 au bilan.')
p('Raccourcis et retours','Section')
p('O1 à O6 sont indiqués en vert sur la carte complète. Ils se révèlent uniquement après un passage physique des deux côtés du mur, jamais en consultant simplement la carte. Ils restent dans leur secteur et ne contournent pas les portes principales.')
page('Répertoire des repères')
table([['Repère','Nom','(x, y)']]+[[e['ref'],e['title'],str(tuple(e['cell']))] for e in E],[55,365,85])
page('Reprendre sans perdre\nsa progression')
p('Sauvegarde et navigation - v0.7','Section')
p('La progression est sauvegardée toutes les 4 secondes pendant le jeu, après les actions importantes et lors de la mise en pause ou de la perte de focus. La position, le sac, les portes, les notes, la carte, les secrets et les réglages partiels des molettes sont conservés.')
p('Le menu « Continuer la partie » indique le niveau et le temps enregistrés. Dans Pause, un message confirme la sauvegarde ou signale un problème de stockage. Une copie du dernier enregistrement valide permet une récupération si le fichier principal est illisible.')
p('La sauvegarde appartient au navigateur et à l’appareil utilisés : elle ne se synchronise pas entre un cellulaire et un ordinateur. Effacer les données du site supprime aussi la progression.')
p('Cliquer ou toucher une case découverte affiche la destination. Le repère au sol indique l’arrivée ; sur la carte, le trajet est surligné. Toucher un objet demande au personnage de s’en approcher puis de l’examiner. Ouvrir un menu ou utiliser les flèches annule le déplacement automatique.')
p('Compatibilité','Section')
p('Les sauvegardes v0.6 restent utilisables. Une partie déjà terminée au niveau 2 peut être reprise pour continuer au niveau 3. Le passage au niveau suivant vide le sac et les notes du niveau, mais conserve son bilan.')
p('Pour signaler un problème','Section')
p('Indiquer : v0.7, niveau, repère ou coordonnées, action effectuée, résultat observé et résultat attendu. Exemple : « Niveau 3, 206, après installation du prisme, mes molettes ne sont pas conservées à la reprise. »')
def footer(c,doc):
 c.setFont('Interface',8);c.setFillColor(colors.HexColor('#57727c'));c.drawString(44,28,'FOLAMOUR / V0.7 / NIVEAU 3 / SPOILERS');c.drawRightString(A4[0]-44,28,str(doc.page))
SimpleDocTemplate(str(out/'Niveau-3-v0.7-Cheatsheet-solutions.pdf'),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=44,bottomMargin=46).build(story,onFirstPage=footer,onLaterPages=footer)
(out/'Niveau-3-v0.7-Cheatsheet-solutions.md').write_text('\n'.join(md))
(out/'Resume-v0.7.md').write_text('''# Lab-Mazing - Version 0.7

## Nouveautés
- Niveau 3 : département d’optique, trois secteurs, 23 repères, trois secrets et six raccourcis.
- Assemblage d’un objectif, calibration de faisceaux et déchiffrement d’archives.
- Transition du niveau 2 au niveau 3, ou accès direct depuis le menu.
- Sauvegarde toutes les 4 secondes, statut en pause, copie de secours et résumé au menu.
- Destination nommée et trajet dessiné sur la carte.
- Nouveau contenu en français et en anglais ; sauvegardes v0.6 conservées.

## Documents
- Carte vue de haut : PNG haute résolution et PDF imprimable.
- Cheatsheet : PDF de 5 pages et version texte Markdown.
- Les documents de la v0.6 restent dans leur dossier ; les niveaux 1 et 2 ne changent pas de carte ni de solution.

## Utilisation
Reprendre une partie terminée au niveau 2 puis continuer au niveau 3, ou utiliser « Tester directement le niveau 3 » (remplace la partie après confirmation).
La sauvegarde reste propre au navigateur et à l’appareil ; elle ne se synchronise pas entre appareils.

Jeu : https://jfeffe.github.io/lab-mazing/
Sources : https://github.com/JFeffe/lab-mazing
''')
print('\n'.join(str(p) for p in out.iterdir()))
