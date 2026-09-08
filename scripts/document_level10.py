"""Versioned French map, exact solutions and release summary for the archives."""
from pathlib import Path
import json, sys, zipfile
from xml.sax.saxutils import escape
from PIL import Image,ImageDraw,ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,A3,landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[1];D=R/'game/data';out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
prefix='Chapitre-2-Niveau-5-v0.16';font=str(R/'game/assets/Interface.ttf');pdfmetrics.registerFont(TTFont('Interface',font))
m,E,S=[json.loads((D/(k+'10.json')).read_text()) for k in ['maze','events','shortcuts']]
by={e['id']:e for e in E}
im=Image.new('RGB',(2020,1940),'#101f2b');dr=ImageDraw.Draw(im)
def txt(x,y,t,size=24,color='#e7edf0',width=None):
 while width and ImageFont.truetype(font,size).getlength(t)>width:size-=1
 dr.text((x,y),t,font=ImageFont.truetype(font,size),fill=color)
txt(65,30,'FOLAMOUR / V0.16 / CHAPITRE 2 / NIVEAU 5 / SPOILERS',27,'#e9be72')
txt(65,85,'LE SERVICE DES ARCHIVES',44)
txt(65,145,'Carte exacte - rayonnages en position validée ; état initial dans l’encadré.',25)
ox,oy,c=95,235,38
for y,row in enumerate(m['grid']):
 for x,v in enumerate(row):
  col='#638ba5' if x>=25 and y>=20 else '#a48a64' if y<13 else '#819990'
  dr.rectangle((ox+x*c,oy+y*c,ox+(x+1)*c-1,oy+(y+1)*c-1),fill=col if v else '#20313e')
for y,gap in zip([4,7,10],[20,14,17]):
 for x in range(13,22):
  if x!=gap:dr.rectangle((ox+x*c+1,oy+y*c+1,ox+(x+1)*c-2,oy+(y+1)*c-2),fill='#554436',outline='#d3b276',width=2)
for k in range(35):txt(ox+k*c+7,oy-28,str(k),16,'#b7c7cf');txt(ox-35,oy+k*c+8,str(k),16,'#b7c7cf')
cs={'pickup':'#e9be72','clue':'#8eddd5','mechanism':'#93aff0','door':'#ee9478','exit':'#ffffff'}
for e in E:
 x,y=e['cell'];x=ox+x*c;y=oy+y*c
 dr.rounded_rectangle((x+1,y+3,x+c-2,y+c-3),radius=5,fill=cs[e['kind']])
 dr.text((x+c/2,y+c/2),e['ref'],anchor='mm',font=ImageFont.truetype(font,16),fill='#101f2b')
 if e.get('secret'):dr.rectangle((x+3,y+1,x+c-4,y+4),fill='white')
for s in S:
 x,y=s['cell'];x=ox+x*c;y=oy+y*c
 dr.rectangle((x+3,y+3,x+c-4,y+c-4),fill='#54cda4')
 dr.text((x+c/2,y+c/2),s['id'],anchor='mm',font=ImageFont.truetype(font,16),fill='#102b25')
x,y=m['start'];dr.ellipse((ox+x*c+6,oy+y*c+6,ox+x*c+32,oy+y*c+32),fill='white');dr.text((ox+x*c+19,oy+y*c+19),'D',anchor='mm',font=ImageFont.truetype(font,17),fill='#101f2b')
sx=1480;txt(sx,225,'REPÈRES DU JEU',24,'#e9be72')
for i,e in enumerate(E):txt(sx,270+i*40,e['ref']+'  '+e['title'],20,cs[e['kind']],width=490)
txt(sx,990,'RAYONNAGES / ÉTAT INITIAL',22,'#e9be72')
txt(sx,1028,'Nord en haut - ouvertures à l’ouest',19)
for row,y in enumerate([4,7,10]):
 txt(sx,1088+row*55,['A / y=4','B / y=7','C / y=10'][row],18)
 for x in range(9):dr.rectangle((sx+115+x*34,1085+row*55,sx+146+x*34,1117+row*55),fill='#819990' if x==1 else '#554436',outline='#d3b276')
txt(sx,1275,'Position validée : A EST, B OUEST, C CENTRE',19,width=490)
txt(sx,1330,'LÉGENDE',23,'#e9be72')
for i,(t,col) in enumerate([('Or : objet à ramasser','#e9be72'),('Turquoise : preuve / note','#8eddd5'),('Bleu : mécanisme','#93aff0'),('Corail : porte verrouillée','#ee9478'),('Blanc : dossier final ; D : départ','#ffffff'),('Vert : raccourci à révéler','#54cda4'),('Brun bordé d’or : rayonnage mobile','#d3b276')]):txt(sx,1372+i*32,t,19,col,width=490)
txt(65,1650,'Coordonnées (x, y) depuis zéro. Nord en haut. Départ : (17, 23).',24)
txt(65,1705,'Porte 402 : fermée jusqu’à la validation du rapport 303. Dossier 105 : trois validations et sceau 204.',22)
txt(65,1760,'Salles jumelles : original au nord-est (401), copie au sud-est (403). Aucune inversion gauche-droite.',22)
txt(65,1815,'Les raccourcis verts sont des murs au départ : visiter physiquement leurs deux côtés pour les ouvrir.',22)
txt(65,1870,'3 SECRETS : 205, 305, 405     /     4 RACCOURCIS     /     3 ÉNIGMES     /     AUCUN COMPTE À REBOURS',23,'#e9be72')
png=out/f'{prefix}-Map-vue-de-haut.png';im.save(png)
cv=canvas.Canvas(str(out/f'{prefix}-Map-vue-de-haut.pdf'),pagesize=landscape(A3));w,h=landscape(A3);scale=min(w/im.width,h/im.height);cv.drawImage(str(png),(w-im.width*scale)/2,(h-im.height*scale)/2,im.width*scale,im.height*scale);cv.showPage();cv.save()
styles={k:ParagraphStyle(k,fontName='Interface',fontSize=fs,leading=lead,spaceAfter=gap,textColor=colors.HexColor('#204137'),keepWithNext=k in ['title','head']) for k,fs,lead,gap in [('title',25,31,20),('head',15,20,10),('body',10.5,16,10),('cell',9,13,0)]}
story=[];md=['# Chapitre 2 - Niveau 5 : Le service des archives\n\nVersion 0.16 - SPOILERS\n']
def p(t,style='body'):
 story.append(Paragraph(escape(str(t)).replace('\n','<br/>'),styles[style]));md.append(('## ' if style=='title' else '### ' if style=='head' else '')+str(t)+'\n')
def page(title):
 if story:story.append(PageBreak())
 p(title,'title')
def table(rows,widths):
 t=Table([[Paragraph(escape(str(v)),styles['cell']) for v in row] for row in rows],colWidths=widths,repeatRows=1)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8dfce')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#c9d7cf'))]));story.extend([t,Spacer(1,12)])
 md.append('\n'.join([' | '.join(map(str,rows[0])),' | '.join(['---']*len(rows[0]))]+[' | '.join(map(str,row)) for row in rows[1:]])+'\n')
page('Le service des archives\nChapitre 2 / Niveau 5')
p('SPOILERS - Version 0.16. Après le comité artificiel, Folamour réclame le dossier MIROIR original. Le laboratoire conserve plusieurs versions des mêmes événements. À vous de distinguer les faits des copies.')
p('Accès','head');p('Menu → Choisir un chapitre → Chapitre 2 · Niveau 5 - Le service des archives. Après la réunion, « Passer au service des archives » conserve les bilans précédents. Numéro interne du niveau : 10.')
p('Parcours conseillé','head')
for t in ['1. Au hall, lire 100. Au sud, lire la notice 202 et l’archive facultative 205.','2. Au nord, lire le plan 201. À la console 203, régler les rayonnages puis valider. Traverser les rangées pour ramasser le sceau 204.','3. À l’ouest, lire les preuves 301, 302 et 304 ; l’archive 305 est facultative. Authentifier le rapport au lecteur 303. La porte 402 s’ouvre.','4. À l’est, lire la note 404, observer la salle originale 401 au nord et lire l’archive facultative 405.','5. Entrer dans la salle copiée au sud. Régler les quatre états en 403, tester puis valider.','6. Au hall, ouvrir le dossier 105 avec le sceau. Découvrir le véritable rôle de MIROIR et votre fiche d’évaluation.']:p(t)
p('Les secteurs peuvent être explorés dans un autre ordre. Les rapports et la salle jumelle peuvent être terminés avant les rayonnages. Le sceau, les trois validations et la lecture de l’original restent nécessaires. Les preuves sont conservées dans le journal.')
p('Commandes','head');p('Clic ou toucher sur le sol pour marcher ; sur un objet pour l’examiner. Clavier : WASD / ZQSD / flèches, E pour interagir. Aucun compte à rebours. Les essais, le journal et les indices restent sauvegardés. La remise à zéro d’une énigme ne recommence pas le niveau.')
page('01 / Les rayonnages\nOuvrir le chemin balisé')
p('Plan 201 : (13, 11). Notice 202 : (21, 25). Console 203 : (17, 14). Sceau 204 : (17, 1). Les rangées A, B et C occupent respectivement y=4, 7 et 10, du nord au sud.')
p('Chaque commande avance deux ouvertures d’une position : OUEST → CENTRE → EST → OUEST. Les positions correspondent à x=14, 17 et 20. Les passages entre les rangées permettent de changer de côté.')
table([['Commande','Rangées déplacées','Pressions depuis zéro'],['I','A + B','2'],['II','B + C','1'],['III','A + C','0']],[110,185,212])
p('Séquence : Réinitialiser cet essai → I → I → II → Valider l’essai. Les états passent de O/O/O à C/C/O, puis E/E/O, puis E/O/C.')
table([['Rangée','Ouverture finale','Case libre'],['A (nord)','EST','(20, 4)'],['B (milieu)','OUEST','(14, 7)'],['C (sud)','CENTRE','(17, 10)']],[150,130,227])
p('Raisonnement','head');p('La cible est donnée par le plan 201. Deux pressions sur I placent A et B à l’est. Une pression sur II fait revenir B à l’ouest et avance C au centre. A reste à l’est : le chemin balisé est dégagé.')
p('Après validation, les commandes sont immobilisées. Depuis la console, monter par l’ouverture C, rejoindre l’ouest entre les rangées pour franchir B, puis l’est pour franchir A. Ramasser le sceau au fond et revenir au hall.')
p('Sécurité','head');p('Avant validation, toutes les configurations permettent de sortir de la salle. Les rayonnages ne peuvent pas être déplacés si le personnage se trouve parmi eux. Les collisions et les trajets au clic/toucher suivent leurs positions ; la carte reflète les ouvertures actuelles.')
page('02 / Les rapports\nTrois preuves indépendantes')
p('Registre 301 : (1, 1). Horloge 302 : (9, 1). Lecteur 303 : (5, 17). Objet 304 : (1, 33). Les preuves n’exigent aucun souvenir des niveaux précédents.')
table([['Rapport','Occupant','Heure','Objet'],['A','Boréal','14:27','Bobine de cuivre'],['B','Boréal','14:17','Bobine de cuivre'],['C','Cobalt','14:17','Prisme de verre']],[70,110,80,247])
p('Le registre mécanique identifie le badge B-6, celui de Boréal : entré à 14:12, sorti à 14:24. L’horloge scellée donne 14:17. La photo argentique confirme la bobine de cuivre. Le rapport A se trompe sur l’heure, le rapport C sur la personne et l’objet.')
table([['Bouton','Réglage correct','Pressions depuis zéro'],['Rapport sélectionné','B','1'],['Registre','Boréal','1'],['Horloge','14:17','1'],['Objet','Bobine de cuivre','2']],[170,170,167])
p('Valider l’essai authentifie le rapport B et ouvre la porte 402 en (29, 20), dans les deux sens. Un mauvais essai ne consomme aucune preuve. Le journal conserve les textes lus.')
p('Archive facultative 305 : (9, 33). Une version falsifiée du passage dans les serres prétend que le stagiaire a demandé à être payé en café.')
page('03 / La salle jumelle\nReproduire quatre états')
p('Relevé original 401 : (29, 7), pièce au nord-est. Note 404 : (27, 17). Console de la copie 403 : (29, 25), pièce au sud-est. Il faut authentifier le rapport et lire le relevé original avant de corriger la copie.')
p('Observer les accessoires dans les deux pièces : lampe, socles, bobine, projecteur et interrupteur. Le relevé 401 donne aussi tous les états par écrit. Les couleurs d’ambiance ambrée et bleue ne sont pas des indices ; les points cardinaux sont identiques dans les deux salles.')
table([['Élément','État correct','Pressions depuis zéro'],['Lampe','ALLUMÉ','1'],['Bobine','Socle GAUCHE','1 (droite → gauche)'],['Projecteur','EST','2 (ouest → nord → est)'],['Ventilation','ABAISSÉ','1']],[130,170,207])
p('Choisir « Tester la copie » : 4 / 4 correspondances. Puis « Valider l’essai ». Les changements se voient également sur les objets de la salle copiée.')
p('Le test ne corrige pas les réglages. Modifier un élément annule le résultat précédent : relancer le test avant de valider. Un test incomplet affiche le nombre de correspondances et permet de continuer sans pénalité matérielle.')
p('Retour au dossier','head');p('Rejoindre 105 en (21, 19), dans le hall. Le bouton « Ouvrir le dossier MIROIR » utilise le sceau et termine la mission. Les trois énigmes doivent déjà être validées.')
p('Révélation finale','head');p('MIROIR cherche à reproduire le laboratoire et les comportements de ses occupants. Le comité artificiel était un premier essai ; l’UNIFICATION doit réunir ses observations dans une copie cohérente. Votre fiche juge votre curiosité « préoccupante ». Folamour vous reproche d’avoir ouvert le dossier au lieu de simplement le rapporter.')
p('Un voyant annonce le secteur des prototypes et une porte s’entrouvre. Il s’agit d’une annonce narrative : cette suite n’est pas encore jouable. La conclusion et le bilan restent accessibles en reprenant la sauvegarde.')
page('Carte et références\nTous les points d’intérêt')
table([['Repère','Objet ou installation','(x, y)']]+[[e['ref'],e['title'],str(tuple(e['cell']))] for e in E],[60,347,100])
p('Trois secrets facultatifs : 205 (13, 33), 305 (9, 33), 405 (33, 3). Les numéros correspondent aux étiquettes dans le jeu. La carte PNG/PDF montre la grille exacte et les rayonnages validés ; l’encadré rappelle leur état de départ.')
page('Raccourcis et sauvegardes\nRevenir sans se perdre')
p('Chaque raccourci est un mur au départ. Il apparaît après une visite physique de ses deux cases adjacentes, dans n’importe quel ordre. Révéler ces cases sur la carte ne suffit pas. Une fois ouvert, il fonctionne dans les deux sens et reste sauvegardé.')
table([['ID','Mur','Cases à visiter','Gain minimal']]+[[s['id'],str(tuple(s['cell'])),str(tuple(s['sides'][0]))+' / '+str(tuple(s['sides'][1])),str(s['minimum_saved_steps'])+' pas'] for s in S],[40,85,282,100])
p('Le gain minimal mesure le détour évité pour traverser ce mur, même si les trois autres raccourcis sont ouverts. Ce n’est pas une estimation de la durée d’une première partie. Aucun raccourci ne contourne la porte 402.')
p('Sauvegardes','head');p('Le niveau, les rayonnages, les réponses du rapport, les réglages et le dernier test de la copie, le sceau, les notes, les indices et les raccourcis sont sauvegardés. La transition depuis la réunion conserve les bilans des missions précédentes. Vitesse +30 %, netteté mobile et réglages audio conservés.')
page('Indices progressifs\nPiste, méthode, solution')
aid=json.loads((D/'guidance.json').read_text())
for id in ['a_stacks','a_reports','a_twin']:
 p(by[id]['ref']+' / '+by[id]['title'],'head')
 for i,pair in enumerate(aid['hints'][id]):p(['Piste : ','Méthode : ','Solution : '][i]+pair[0])
def footer(c,d):
 c.setFont('Interface',8);c.setFillColor(colors.HexColor('#647e70'));c.drawString(44,25,'FOLAMOUR / V0.16 / CHAPITRE 2 - NIVEAU 5 / SPOILERS');c.drawRightString(A4[0]-44,25,str(d.page))
SimpleDocTemplate(str(out/f'{prefix}-Cheatsheet-solutions.pdf'),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=42,bottomMargin=45).build(story,onFirstPage=footer,onLaterPages=footer)
(out/f'{prefix}-Cheatsheet-solutions.md').write_text('\n'.join(md))
(out/'Resume-v0.16.md').write_text('''# Lab-Mazing v0.16 - Le service des archives

Chapitre 2, niveau 5 (numéro interne 10).

- Hall central, rayonnages au nord, preuves à l’ouest et salles jumelles à l’est.
- Trois énigmes : commandes couplées des rayonnages, rapports contradictoires, copie physique à corriger.
- 17 repères, trois secrets et quatre raccourcis à révéler par exploration.
- 27 configurations de rayonnages avec issue ; sécurité contre le déplacement lorsque le personnage est dans la salle.
- Projet MIROIR : reproduction des lieux et des comportements, prolongement du comité artificiel et de l’UNIFICATION.
- Introduction et conclusion de Folamour, fiche du sujet et annonce du secteur des prototypes (non jouable à ce stade).
- Menu : Chapitre 2 · Niveau 5 - Le service des archives ; transition depuis la réunion avec bilans conservés.
- Français/anglais, indices progressifs, journal, sauvegardes des essais, clavier/clic/toucher.
- Vitesse +30 %, netteté mobile et audio conservés.

Vérification : parcours physique, verrou de la salle copiée, sécurité des rayonnages, deux ordres d’exploration, sauvegardes partielles et finales, panneaux FR/EN portrait/paysage. Pas de validation sur téléphone physique.

Ce dossier contient les cartes PNG/PDF, les solutions PDF/Markdown, ce résumé et un ZIP des cinq documents. Aucun exécutable.

Jeu : https://jfeffe.github.io/lab-mazing/
''')
with zipfile.ZipFile(out/'Lab-Mazing-v0.16-Chapitre-2-Niveau-5-Cheatsheets.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(out.iterdir()):
  if f.suffix!='.zip':z.write(f,f.name)
print('Generated six files in',out)
