"""Publish a complete v0.10 map/solution set using current game coordinates.

Retains the detailed guides for levels 2-5 and adds a verified shortcut table
for every level. Existing version folders are never edited.
"""
from pathlib import Path
import json,sys,ast,re
from xml.sax.saxutils import escape
from PIL import Image,ImageDraw,ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,A3,landscape
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer,PageBreak,KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[1];D=R/'game/data';out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
VERSION='0.10';font=str(R/'game/assets/Interface.ttf');pdfmetrics.registerFont(TTFont('Interface',font))
audit=json.loads((R/'game/tests/shortcut_audit.json').read_text())
titles={1:'Le laboratoire',2:'Le département des machines',3:'Le département d’optique',4:'Le département des essais',5:'Le défi de Folamour'}
styles={name:ParagraphStyle(name,fontName='Interface',fontSize=size,leading=leading,textColor=colors.HexColor(color),spaceAfter=after,keepWithNext=name in ['Main','Section','ReferenceHeading','Coordinate']) for name,size,leading,color,after in [('Main',25,31,'#173743',18),('Section',16,21,'#236878',12),('Body',10.5,16,'#162f38',11),('SmallCell',8.5,12,'#162f38',0),('Reference',10,13.2,'#162f38',6),('ReferenceHeading',13,17,'#236878',8),('Coordinate',10,13.2,'#162f38',6)]}
cs={'pickup':'#e9be72','clue':'#8eddd5','craft':'#93aff0','mechanism':'#93aff0','door':'#ee9478','oneway':'#ee9478','exit':'#ffffff'}
def data(n):
 suffix='' if n==1 else str(n)
 return [json.loads((D/f'{kind}{suffix}.json').read_text()) for kind in ['maze','events','shortcuts']]
def make_map(n,m,E,S):
 im=Image.new('RGB',(2020,1940),'#101f2b');dr=ImageDraw.Draw(im)
 def txt(x,y,t,size=24,color='#e7edf0',width=None):
  while width and ImageFont.truetype(font,size).getlength(t)>width:size-=1
  dr.text((x,y),t,font=ImageFont.truetype(font,size),fill=color)
 txt(65,30,f'FOLAMOUR / V{VERSION} / NIVEAU {n} / SPOILERS',27,'#e9be72')
 txt(65,80,titles[n].upper(),44)
 txt(65,143,'Raccourcis révisés : revenir plus vite dans les couloirs déjà parcourus',24)
 ox,oy,c=95,220,38
 palettes={1:['#648a83','#7b83a4','#9e8174'],2:['#9e8460','#527f8e','#858371'],3:['#7789a5','#638f94','#93839e'],4:['#a18d72','#788ba2','#6b968d'],5:['#659b9d','#ac9070','#8982a9']}
 for y,row in enumerate(m['grid']):
  for x,v in enumerate(row):
   zone=(2 if y<12 else 0 if x<15 else 1 if x>19 else 2) if n==5 else (0 if y<(11 if n==1 else 12) else 1 if y<24 else 2)
   dr.rectangle((ox+x*c,oy+y*c,ox+(x+1)*c-1,oy+(y+1)*c-1),fill=palettes[n][zone] if v else '#20313e')
 for k in range(len(m['grid'])):
  txt(ox+k*c+7,oy-28,str(k),16,'#b7c7cf');txt(ox-35,oy+k*c+8,str(k),16,'#b7c7cf')
 for e in E:
  x,y=e['cell'];x=ox+x*c;y=oy+y*c
  dr.rounded_rectangle((x+1,y+3,x+c-2,y+c-3),radius=5,fill=cs[e['kind']])
  dr.text((x+c/2,y+c/2),str(e['ref']),anchor='mm',font=ImageFont.truetype(font,16),fill='#101f2b')
  if e.get('secret'):dr.rectangle((x+3,y+1,x+c-4,y+4),fill='#ffffff')
 for s in S:
  x,y=s['cell'];x=ox+x*c;y=oy+y*c
  dr.rectangle((x+3,y+3,x+c-4,y+c-4),fill='#54cda4')
  dr.text((x+c/2,y+c/2),s['id'],anchor='mm',font=ImageFont.truetype(font,16),fill='#102b25')
 x,y=m['start']
 if any(e['cell']==m['start'] for e in E):
  dr.ellipse((ox+x*c+1,oy+y*c+1,ox+x*c+36,oy+y*c+36),outline='white',width=2)
  dr.text((ox+x*c-9,oy+y*c+19),'D',anchor='mm',font=ImageFont.truetype(font,17),fill='white')
 else:
  dr.ellipse((ox+x*c+6,oy+y*c+6,ox+x*c+32,oy+y*c+32),fill='white')
  dr.text((ox+x*c+19,oy+y*c+19),'D',anchor='mm',font=ImageFont.truetype(font,17),fill='#101f2b')
 sx=1540;txt(sx,220,'REPÈRES DU JEU',24,'#e9be72')
 for i,e in enumerate(E):txt(sx,264+i*42,str(e['ref'])+'  '+e['title'],18,cs[e['kind']],width=425)
 txt(sx,1415,'LÉGENDE',23,'#e9be72')
 for i,(text,col) in enumerate([('Or : objet à ramasser','#e9be72'),('Turquoise : note / indice','#8eddd5'),('Bleu : assemblage / mécanisme','#93aff0'),('Corail : porte / sas','#ee9478'),('Blanc : sortie ; D : départ','#ffffff'),('Vert : raccourci à révéler','#54cda4')]):txt(sx,1460+i*34,text,19,col,width=425)
 txt(65,1710,'Coordonnées (x, y) depuis 0. Nord en haut. Chaque case traversée représente un pas.',23)
 txt(65,1760,'Un raccourci apparaît après un passage physique sur ses deux cases adjacentes, de part et d’autre du mur.',22)
 txt(65,1810,'Les ouvertures vertes sont des murs au départ. Voir le cheatsheet pour les deux cases et le gain de chaque passage.',21)
 secrets=', '.join(str(e['ref']) for e in E if e.get('secret'))
 txt(65,1860,f'DÉPART : {tuple(m["start"])}     |     SECRETS : {secrets}     |     {len(S)} RACCOURCIS V{VERSION}',23,'#e9be72')
 png=out/f'Niveau-{n}-v{VERSION}-Map-vue-de-haut.png';im.save(png)
 pdf=canvas.Canvas(str(out/f'Niveau-{n}-v{VERSION}-Map-vue-de-haut.pdf'),pagesize=landscape(A3));w,h=landscape(A3);scale=min(w/im.width,h/im.height);pdf.drawImage(str(png),(w-im.width*scale)/2,(h-im.height*scale)/2,im.width*scale,im.height*scale);pdf.showPage();pdf.save()

def make_guide(n,m,E,S):
 story=[];md=[f'# Niveau {n} - {titles[n]} - v{VERSION}\n\n**SPOILERS : solutions complètes et nouveaux raccourcis.**\n']
 def updated(t):
  t=str(t)
  if not t.startswith('Les sauvegardes'):
   t=re.sub(r'(?i)(version |v)0\.[789]\b',lambda match:match[1]+VERSION,t)
  t=t.replace('« Tester directement le niveau 3 »','« Sélection de niveau / test », puis « Niveau 3 »').replace('« Tester directement le niveau 4 »','« Sélection de niveau / test », puis « Niveau 4 »')
  t=t.replace('Ils restent dans leurs ailes et ne contournent pas le sas principal.','Ils peuvent aussi relier une aile au hall après exploration des deux côtés, sans contourner le sas principal.')
  return t
 def p(t,style='Body'):
  if style=='Reference' and ' | X=' in str(t):style='Coordinate'
  t=updated(t);story.append(Paragraph(escape(t).replace('\n','<br/>'),styles[style]));md.append(('## ' if style=='Main' else '### ' if style in ['Section','ReferenceHeading'] else '')+t+'\n')
 def page(title):
  if story:story.append(PageBreak())
  p(title,'Main')
 def table(rows,widths):
  rows=[[updated(t) for t in row] for row in rows]
  t=Table([[Paragraph(escape(str(v)).replace('\n','<br/>'),styles['SmallCell']) for v in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
  t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#deecec')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#c6d4d8'))]))
  story.extend([t,Spacer(1,10)]);md.append('\n'.join([' | '.join(rows[0]),' | '.join(['---']*len(rows[0]))]+[' | '.join(row) for row in rows[1:]])+'\n')
 if n==1:
  page('Niveau 1\nLe laboratoire')
  p('SPOILERS / VERSION 0.10','Section')
  p('Les solutions des énigmes sont conservées. Cette édition déplace les raccourcis et recalcule leurs avantages sur les retours. Les numéros ci-dessous sont les références affichées dans le jeu, et non les numéros du vieux plan de correction.')
  steps=[('1 / Entrer','Lire les fragments 38 (3, 3) et 02 (11, 1). Ils donnent 47 puis 26. Saisir 4726 à l’accès 03 (16, 3).'),('2 / Soleil','Prendre la clé de cuivre 33 (13, 3) et l’utiliser à la réserve 29 (25, 3). Ramasser le disque S (25, 5) : Soleil = 6.'),('3 / Étoile','Lire les fiches 53 (11, 7) et 54 (31, 7). Suivre CUVE, BOBINE, FILTRE, LENTILLE : 8512. Ouvrir le verrou 87 (17, 12) et prendre E (19, 13) : Étoile = 9.'),('4 / Lune','Prendre l’artéfact 93 (27, 13) et l’installer en 19 (3, 18). Prendre L (3, 15) : Lune = 4.'),('5 / Calibration','Lire la fiche 20 (33, 1) : LUNE, SOLEIL, ÉTOILE. Conserver les trois disques. Le registre 21 aide à s’orienter.'),('6 / Sas à sens unique','Approcher un sas 50 depuis le nord : (13, 24) ou (27, 24). Les trois disques et la lecture de la fiche 20 sont obligatoires. Le départ est irréversible ; lire les secrets 61 et 84 avant de partir.'),('7 / Courant et sortie','Prendre le fusible F (1, 27), l’installer dans le tableau 65 (3, 30). Au pupitre 00 (17, 34), installer les trois disques et entrer 469. Continuer ensuite vers le niveau 2.')]
  for i,(title,text) in enumerate(steps):
   if i==4:page('Le départ\nPuis le confinement')
   p(title,'Section');p(text)
  p('Secrets facultatifs','Section');p('61 (5, 1), 84 (25, 23), 41 (33, 27). Les deux premiers doivent être lus avant le sas. Aucun raccourci ne permet de revenir à travers le sas à sens unique.')
  page('Textes et conditions\nRéférences du jeu')
  names={e.get('resource'):e['title'] for e in E if e['kind']=='pickup'}
  for e in E:
   p(str(e['ref'])+' / '+e['title'],'ReferenceHeading');p('Coordonnées : '+str(tuple(e['cell']))+'\n'+e['text'],'Reference')
   if e.get('requires'):p('Objets à installer : '+', '.join(names.get(k,k) for k in e['requires'])+'.','Reference')
   if e.get('answer'):p('Solution : '+e['answer']+'.','Reference')
   if e.get('success'):p('Résultat : '+e['success'],'Reference')
 elif n==2:
  # Preserve the earlier full text and conditions, replacing only the old
  # shortcut section and edition number. Positions of events are unchanged.
  source=(R/'docs/Niveau-2-v0.6-Cheatsheet-solutions.md').read_text()
  source=re.sub(r'## Raccourcis\n.*?(?=## Textes complets)', '',source,flags=re.S).replace('0.6',VERSION)
  reference=False
  for block in re.split(r'\n\s*\n',source):
   block=block.strip()
   if not block:continue
   if block.startswith('# '):page('Niveau 2\nLe département des machines')
   elif block.startswith('## Textes complets'):page('Textes complets\nEt conditions');reference=True
   elif block.startswith('### '):
    if block.startswith('### 5.'):page('Le relais et l’ascenseur')
    p(block[4:],'ReferenceHeading' if reference else 'Section')
   elif block.startswith('## '):p(block[3:],'Section')
   else:p(block.replace('**',''),'Reference' if reference else 'Body')
 else:
  # Reuse the authored explanatory sections (no export or file I/O nodes).
  source=ast.parse((R/f'scripts/document_level{n}.py').read_text())
  first=next(i for i,v in enumerate(source.body) if isinstance(v,ast.Expr) and isinstance(v.value,ast.Call) and isinstance(v.value.func,ast.Name) and v.value.func.id=='page')
  last=next(i for i,v in enumerate(source.body) if isinstance(v,ast.FunctionDef) and v.name=='footer')
  exec(compile(ast.Module(body=source.body[first:last],type_ignores=[]),f'level{n}_guide','exec'),dict(p=p,page=page,table=table,E=E,S=S,by={e['id']:e for e in E}))
 page('Raccourcis v0.10\nLes nouveaux retours')
 p('Déclenchement conservé','Section')
 p('Marcher sur chacune des deux cases indiquées suffit, dans n’importe quel ordre. Voir la case sur la carte ne suffit pas. Le mur devient ensuite un passage permanent de deux pas entre ses deux côtés, utilisable à pied, au clic et au toucher.')
 rows=[['ID','Mur (x, y)','Deux cases à parcourir','Détour seul','Gain minimal']]
 for s in S:rows.append([s['id'],str(tuple(s['cell'])),str(tuple(s['sides'][0]))+' / '+str(tuple(s['sides'][1])),str(s['original_detour_steps'])+' pas',str(s['minimum_saved_steps'])+' pas'])
 table(rows,[36,78,195,92,104])
 p('Comment lire les gains','Section')
 p('« Détour seul » : distance entre les deux cases sans aucun raccourci, dans la zone située du même côté des verrous. « Gain minimal » : pas encore économisés par ce passage lorsque tous les autres raccourcis sont ouverts. Aucun passage ne traverse une porte d’énigme ni une limite de sas.')
 row=audit[n-1];before=row['benchmarks']['before'];after=row['benchmarks']['after']
 details=' ; '.join(f'{a["steps"]} → {b["steps"]} pas (gain : {a["steps"]-b["steps"]})' for a,b in zip(before,after))
 p('Comparaison de parcours : '+details+'.')
 p('Mesure sur les mêmes itinéraires de référence, carte connue, avec ouverture seulement après visite des deux côtés. Ce ne sont ni une durée ni un nombre de pas garantis pour une première exploration. Deux variantes sont vérifiées au niveau 1 (choix du sas) et au niveau 5 (ordre des ailes).')
 page('Sauvegarde et accès\nÉdition 0.10')
 p('Reprendre une ancienne partie','Section')
 p('Le niveau, le sac, les énigmes résolues et les manipulations partielles sont conservés. Les anciens identifiants de raccourcis ne déverrouillent pas leurs nouveaux emplacements : le jeu vérifie les deux cases réellement parcourues pour chaque passage actuel. Si elles l’ont déjà été, le passage s’ouvre à la reprise.')
 p('Si la sauvegarde se trouve dans un ancien passage redevenu mur, le personnage est replacé sur le sol déjà parcouru le plus proche. Les anciennes notes de raccourcis sont actualisées ; les notes d’énigmes sont conservées.')
 p('Choix de chapitre','Section')
 p('Le menu « Choisir un chapitre » propose le chapitre 1, composé des niveaux 1 à 5 dans l’ordre. « Continuer la partie » reprend le niveau courant. Le chapitre 2 reste indisponible. Pour un essai isolé : « Sélection de niveau / test », puis « Niveau '+str(n)+' » ; une confirmation précède le remplacement de la partie.')
 p('Les sauvegardes restent propres au navigateur et à l’appareil. Aucun raccourci n’est nécessaire pour terminer : tous les objectifs restent accessibles par les chemins ordinaires.')
 p('Documents de cette édition','Section')
 p(f'Carte complète : Niveau-{n}-v{VERSION}-Map-vue-de-haut.png et .pdf.\nSolutions : Niveau-{n}-v{VERSION}-Cheatsheet-solutions.pdf et .md.\nLe dossier v{VERSION} regroupe les cinq niveaux et le résumé des modifications.')
 def footer(c,d):
  c.setFont('Interface',8);c.setFillColor(colors.HexColor('#57727c'));c.drawString(44,25,f'FOLAMOUR / V{VERSION} / NIVEAU {n} / SPOILERS');c.drawRightString(A4[0]-44,25,str(d.page))
 SimpleDocTemplate(str(out/f'Niveau-{n}-v{VERSION}-Cheatsheet-solutions.pdf'),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=42,bottomMargin=45).build(story,onFirstPage=footer,onLaterPages=footer)
 (out/f'Niveau-{n}-v{VERSION}-Cheatsheet-solutions.md').write_text('\n'.join(md))

for n in range(1,6):
 m,E,S=data(n);make_map(n,m,E,S);make_guide(n,m,E,S);print('Level',n,'documents generated',flush=True)
summary=['# Lab-Mazing - Version 0.10\n','## Des raccourcis utiles pour les cinq niveaux\n','Les 32 raccourcis ont été réévalués et leurs emplacements révisés. Chaque passage évite au moins 12 pas entre ses deux côtés, même avec tous les autres raccourcis de sa zone ouverts. Leur apparition reste liée à une visite physique des deux cases adjacentes ; voir les cases dans le brouillard dissipé ne suffit pas. Aucun raccourci ne contourne les portes d’énigmes ou les sas à sens unique.\n','## Comparaison de trajets\n','Niveau | Avant | Après | Pas évités','--- | --- | --- | ---']
for row in audit:
 for i,(a,b) in enumerate(zip(row['benchmarks']['before'],row['benchmarks']['after'])):summary.append(f'{row["level"]}'+(f' / variante {i+1}' if len(row['benchmarks']['after'])>1 else '')+f' | {a["steps"]} | {b["steps"]} | {a["steps"]-b["steps"]}')
summary+=['\nMême ordre d’objectifs avant/après, carte connue, ouverture dynamique après exploration physique des deux côtés. Cette simulation ne prédit pas le nombre de pas d’un joueur découvrant le labyrinthe. Les variantes correspondent aux deux sas du niveau 1 et aux deux ordres de visite des ailes du niveau 5.\n','## Sauvegardes\n','Progression et inventaire conservés. Les ouvertures sont recalculées selon les cases déjà parcourues aux nouveaux emplacements. Une position dans un ancien raccourci redevenu mur est replacée sur le sol connu le plus proche.\n','## Documents\n','Ce dossier contient les cartes exactes PNG/PDF et les cheatsheets PDF/Markdown des cinq niveaux. Chaque guide comprend les solutions, les nouvelles coordonnées des raccourcis et leurs gains mesurés. Les anciens dossiers de version restent archivés.\n','## Vérification\n','Comparaison des trajets des cinq niveaux, gain minimal de chaque raccourci, absence de contournement des verrous, collisions dans les deux sens, navigation au clic/toucher, apparition après deux visites et migration des anciennes sauvegardes.\n','Jeu : https://jfeffe.github.io/lab-mazing/\n']
(out/f'Resume-v{VERSION}.md').write_text('\n'.join(summary))
