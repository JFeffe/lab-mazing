"""Five source-exact maps and French solution guides for chapter four."""
from pathlib import Path
from xml.sax.saxutils import escape
import json,sys,zipfile,textwrap
from PIL import Image,ImageDraw,ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,A3,landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer,PageBreak,Image as PDFImage
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[1];D=R/'game/data';out=Path(sys.argv[1]).resolve();out.mkdir(parents=True,exist_ok=True)
font=str(R/'game/assets/Interface.ttf');pdfmetrics.registerFont(TTFont('Interface',font));design=json.loads((R/'scripts/chapter4_design.json').read_text());guidance=json.loads((D/'guidance.json').read_text())
cs={'pickup':'#e9be72','clue':'#8eddd5','mechanism':'#93aff0','door':'#ee9478','exit':'#ffffff'}
styles={k:ParagraphStyle(k,fontName='Interface',fontSize=fs,leading=lead,spaceAfter=gap,textColor=colors.HexColor('#203b43'),keepWithNext=k in ['title','head']) for k,fs,lead,gap in [('title',24,29,15),('head',14,19,8),('body',10,15,9),('cell',8.7,12,0)]}
def zone(n,x,y):
 if n==16:return 0 if y<16 else 1 if x<17 else 2
 if n==17:return 0 if x<17 else 1 if y<17 else 2
 if n==18:return 2 if 15<=x<=19 and 15<=y<=19 else 1 if 9<=x<=25 and 9<=y<=25 else 0
 if n==19:return 0 if x<13 else 1 if x<25 else 2
 return 1 if x<12 else 2 if x>22 else 0
palettes=[['#ab8e68','#809a96','#8797b2'],['#a2a084','#8e9cae','#8cab98'],['#6c97a2','#8f85a4','#88a798'],['#849fa2','#b49a6d','#8e8eae'],['#9582a8','#8c9c98','#ae986f']]
for n in range(16,21):
 num=n-15;entry=design[str(n)];folder=out/f'Niveau-{num}';folder.mkdir(exist_ok=True);prefix=f'Chapitre-4-Niveau-{num}-v0.18'
 m,E,S=[json.loads((D/f'{k}{n}.json').read_text()) for k in ['maze','events','shortcuts']];by={e['id']:e for e in E};route=json.loads((R/f'game/tests/route_level{n}.json').read_text())
 im=Image.new('RGB',(2020,1870),'#101f2b');dr=ImageDraw.Draw(im)
 def txt(x,y,t,size=24,color='#e7edf0',width=None):
  while width and ImageFont.truetype(font,size).getlength(t)>width:size-=1
  dr.text((x,y),t,font=ImageFont.truetype(font,size),fill=color)
 txt(65,30,f'FOLAMOUR / V0.18 / CHAPITRE 4 / NIVEAU {num} / SPOILERS',27,'#e9be72');txt(65,85,entry['title'].upper(),44,width=1890)
 txt(65,150,'Carte exacte du niveau - nord en haut - coordonnées (x, y) depuis zéro.',25)
 ox,oy,c=95,240,38
 for y,row in enumerate(m['grid']):
  for x,v in enumerate(row):dr.rectangle((ox+x*c,oy+y*c,ox+(x+1)*c-1,oy+(y+1)*c-1),fill=palettes[num-1][zone(n,x,y)] if v else '#20313e')
 for k in range(35):txt(ox+k*c+7,oy-28,str(k),16,'#b7c7cf');txt(ox-35,oy+k*c+8,str(k),16,'#b7c7cf')
 for e in E:
  x,y=e['cell'];x=ox+x*c;y=oy+y*c;dr.rounded_rectangle((x+1,y+3,x+c-2,y+c-3),radius=5,fill=cs[e['kind']]);dr.text((x+c/2,y+c/2),e['ref'],anchor='mm',font=ImageFont.truetype(font,16),fill='#101f2b')
  if e.get('secret'):dr.rectangle((x+3,y+1,x+c-4,y+4),fill='white')
 for e in E:
  for gate in e.get('world_gates',[]):
   x,y=gate['cell'];x=ox+x*c;y=oy+y*c;dr.rectangle((x+2,y+2,x+c-3,y+c-3),fill='#c888aa');dr.text((x+c/2,y+c/2),gate['label'],anchor='mm',font=ImageFont.truetype(font,19),fill='#101f2b')
 for s in S:
  x,y=s['cell'];x=ox+x*c;y=oy+y*c;dr.rectangle((x+3,y+3,x+c-4,y+c-4),fill='#54cda4');dr.text((x+c/2,y+c/2),s['id'],anchor='mm',font=ImageFont.truetype(font,16),fill='#102b25')
 x,y=m['start'];dr.ellipse((ox+x*c+6,oy+y*c+6,ox+x*c+32,oy+y*c+32),fill='white');dr.text((ox+x*c+19,oy+y*c+19),'D',anchor='mm',font=ImageFont.truetype(font,17),fill='#101f2b')
 sx=1480;txt(sx,225,'REPÈRES DU JEU',24,'#e9be72')
 for i,e in enumerate(sorted(E,key=lambda e:int(e['ref']))):txt(sx,270+i*34,e['ref']+'  '+e['title'],20,cs[e['kind']],width=490)
 txt(sx,1005,'PROGRESSION',23,'#e9be72')
 for i,t in enumerate(['101 : récupérer la mallette','203 : valider, ouvre le sas 111','303 : valider, ouvre le sas 112','403 : valider le dernier essai','900 : terminer la mission']):txt(sx,1050+i*36,t,21,width=490)
 txt(sx,1285,'LÉGENDE',23,'#e9be72')
 for i,(t,col) in enumerate([('Or : objet à ramasser',cs['pickup']),('Turquoise : note / preuve',cs['clue']),('Bleu : mécanisme',cs['mechanism']),('Corail : sas verrouillé',cs['door']),('Blanc : sortie ; D : départ','#ffffff'),('Vert : raccourci à révéler','#54cda4'),('Rose A/B/C : accès variable','#c888aa'),('501, 502, 503 : notes secrètes','#ffffff')]):txt(sx,1330+i*32,t,21,col,width=490)
 txt(65,1630,f'Départ : {tuple(m["start"])}. Les trois secteurs se débloquent dans l’ordre 203 → 303 → 403.',24)
 for i,t in enumerate(textwrap.wrap(entry['layout'],width=130)):txt(65,1680+i*36,t,23)
 txt(65,1770,'Raccourcis verts : murs au départ. Visitez physiquement leurs deux côtés pour les ouvrir.',23)
 txt(65,1820,f'3 SECRETS / {len(S)} RACCOURCIS / 3 ÉNIGMES / ESSAIS RÉVERSIBLES / AUCUN COMPTE À REBOURS',24,'#e9be72')
 png=folder/f'{prefix}-Map-vue-de-haut.png';im.save(png)
 cv=canvas.Canvas(str(folder/f'{prefix}-Map-vue-de-haut.pdf'),pagesize=landscape(A3));w,h=landscape(A3);scale=min(w/im.width,h/im.height);cv.drawImage(str(png),(w-im.width*scale)/2,(h-im.height*scale)/2,im.width*scale,im.height*scale);cv.showPage();cv.save()
 story=[];md=[f'# {entry["title"]}\n\nChapitre 4 / Niveau {num} / Version 0.18 / SPOILERS\n']
 def p(t,style='body'):
  story.append(Paragraph(escape(str(t)).replace('\n','<br/>'),styles[style]));md.append(('## ' if style=='title' else '### ' if style=='head' else '')+str(t)+'\n')
 def page(title):
  if story:story.append(PageBreak())
  p(title,'title')
 def table(rows,widths):
  t=Table([[Paragraph(escape(str(v)),styles['cell']) for v in row] for row in rows],colWidths=widths,repeatRows=1);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8dfce')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#c9d7cf'))]));story.extend([t,Spacer(1,10)]);md.append('\n'.join([' | '.join(map(str,rows[0])),' | '.join(['---']*len(rows[0]))]+[' | '.join(map(str,r)) for r in rows[1:]])+'\n')
 page(entry['title']+f'\nChapitre 4 / Niveau {num}')
 p('SPOILERS / VERSION 0.18','head');p(entry['intro']);p(entry['layout'])
 p('Parcours conseillé','head')
 p('Menu → Choisir un chapitre → Chapitre 4, puis choisir ce niveau. La transition depuis la mission précédente conserve les bilans. Le sac et le journal repartent à zéro à chaque nouveau niveau.')
 for i,sec in enumerate(entry['sections'],1):
  e=by[sec['id']];notes=[by[f'c{n}_n{2*i-1}'],by[f'c{n}_n{2*i}']]
  p(f'{i}. '+('Ramasser la mallette 101 et l’installer au poste 203. ' if i==1 else '')+f'Lire {notes[0]["ref"]} et {notes[1]["ref"]}, puis résoudre {e["ref"]} : {e["title"]}. '+('Le sas '+str(110+i)+' s’ouvre.' if i<3 else 'Rejoindre ensuite le passage 900.'))
 p('Les notes secrètes 501, 502 et 503 sont facultatives. Leur lecture compte au bilan. '+(f'Les {len(S)} raccourcis demandent de marcher des deux côtés du mur ; la simple visibilité ne suffit pas.' if S else 'Les anneaux offrent déjà des boucles de circulation : aucun raccourci caché dans ce niveau.'))
 p('Commandes et sauvegarde','head');p('Clic ou toucher : marcher et examiner. WASD / ZQSD / flèches : marcher ; E : interagir ; I : sac ; J : journal ; M : carte. Aucune limite de temps. Les manipulations, mesures et programmes sont sauvegardés. Réinitialiser un essai restaure ses réglages sans rendre la mallette déjà installée. Après une simulation, modifier une commande exige un nouveau test.')
 p('Indices graduels','head');p('Chaque poste propose une piste, une méthode, puis la solution complète. Ouvrir le panneau ne révèle rien automatiquement. Les indices consultés et les essais incorrects sont comptés au bilan.')
 for i,sec in enumerate(entry['sections'],1):
  e=by[sec['id']];page(f'{i:02d} / {e["title"]}')
  p(f'Poste {e["ref"]} : {tuple(e["cell"])}. '+('Mallette 101 requise.' if i==1 else f'Validation {str((i)*100+3)} requise.'))
  p(e['text'])
  for k in [2*i-1,2*i]:
   note=by[f'c{n}_n{k}'];p(f'{note["ref"]} / {note["title"]} / {tuple(note["cell"])}','head');p(note['text'])
  if 'board' in e:
   boards=[e['board']]+([e['board_b']] if 'board_b' in e else []);tile=37;mini=Image.new('RGB',(len(boards)*240,230),'white');pen=ImageDraw.Draw(mini)
   for bidx,board in enumerate(boards):
    for y,row in enumerate(board):
     for x,v in enumerate(row):
      a=bidx*240+x*tile+22;b=25+y*tile;pen.rectangle((a,b,a+tile-2,b+tile-2),fill='#273d4a' if v=='#' else '#e1ebe6');pen.text((a+tile/2,b+tile/2),v if v not in '.#' else '',font=ImageFont.truetype(font,20),anchor='mm',fill='#203b43')
    pen.text((22+bidx*240,1),'B' if bidx else 'A',font=ImageFont.truetype(font,17),fill='#203b43')
   # This exact board is embedded in the PDF; text version uses a coordinate table.
   import io
   buf=io.BytesIO();mini.save(buf,format='PNG');buf.seek(0);story.append(PDFImage(buf,width=mini.width*.65,height=mini.height*.65));story.append(Spacer(1,8))
   p('Nord en haut. D = départ ; S = sortie ; * = station à visiter. Sur la surveillance, A/B/C = caméras et * = cibles.' if e['mode']=='cameras' else 'Nord en haut. D = départ ; S = sortie ; * = station à visiter. Un mur bloque le déplacement sans arrêter le programme.')
   for bidx,board in enumerate(boards):md.append('Plan '+('B' if bidx else 'A')+' (nord en haut) :\n\n| Ligne | Cases de gauche à droite |\n| --- | --- |\n'+'\n'.join(f'| {i+1} | {" · ".join(row)} |' for i,row in enumerate(board))+'\n')
  if e.get('world_gates'):
   p('Visites physiques requises','head')
   p('Les registres restent acquis après réinitialisation du pupitre. Les changements d’accès se font uniquement près du pupitre ; revenez-y après chaque visite. Après validation du poste, les trois accès restent ouverts.')
   table([['Accès','Position de la porte','Registre à visiter']]+[[b['label'],str(tuple(b['cell'])),by[e['observations'][i]]['ref']+' / '+str(tuple(by[e['observations'][i]]['cell']))] for i,b in enumerate(e['world_gates'])],[70,150,287])
  if e.get('edges'):
   p('Sorties du réseau','head')
   table([['Nœud','Sortie 0','Sortie 1']]+[[e['names'][i],e['names'][a],e['names'][b]] for i,(a,b) in enumerate(e['edges'])],[95,206,206])
   if e['mode']=='conveyor':p('Liaisons fixes : D → 1 ; M → 2 ; R → 3 ; C → S. Stations dans l’ordre : M (moulage), R (refroidissement), C (contrôle).')
  if e['mode']=='seal':
   table([['Traversée','Coût','Total'],['A + B vers le conseil','2','2'],['A revient aux bureaux','1','3'],['C + D vers le conseil','8','11'],['B revient aux bureaux','2','13'],['A + B vers le conseil','2','15']],[307,100,100])
  p('Solution exacte depuis la réinitialisation','head');p(sec['solution']);p(sec['explanation'])
  if e['mode']=='tanks':table([['Transfert','A / B / C'],['Départ','8 / 0 / 0'],['A → B','3 / 5 / 0'],['B → C','3 / 2 / 3'],['C → A','6 / 2 / 0'],['B → C','6 / 0 / 2'],['A → B','1 / 5 / 2'],['B → C','1 / 4 / 3'],['C → A','4 / 4 / 0']],[200,307])
  if e['mode']=='echoes':table([['Tour','Commande','Voyants allumés après le tour'],['1','I','1, 2'],['2','II','1, 2, 3, 4'],['3','III','1, 2, 5'],['4','ATTENDRE','1, 2, 4'],['5','ATTENDRE','1, 2, 3, 4, 5, 6 ; aucun écho']],[50,115,342])
  p(e['success'])
 page('Repères, secrets et raccourcis')
 table([['Repère','Objet / poste','Coordonnées']]+[[e['ref'],e['title'],str(tuple(e['cell']))] for e in sorted(E,key=lambda e:int(e['ref']))],[55,340,112])
 p('Raccourcis facultatifs','head')
 if S:
  table([['ID','Mur','Deux côtés à visiter','Gain minimal*']]+[[s['id'],str(tuple(s['cell'])),' ↔ '.join(str(tuple(c)) for c in s['sides']),str(s['minimum_saved_steps'])+' pas'] for s in S],[45,85,277,100]);p('* Gain sur le trajet entre les deux côtés, même avec les autres raccourcis ouverts. Le parcours principal fonctionne sans ouvrir aucun raccourci.')
 else:p('Aucun raccourci caché : les deux anneaux constituent déjà les boucles de circulation. Les accès A/B/C sont des portes à caméra, pas des raccourcis.')
 page('Archives confidentielles\net fin de mission')
 for e in E:
  if e.get('secret'):p(f'{e["ref"]} / {tuple(e["cell"])}','head');p(e['text'])
 p('Révélation de fin de niveau','head');p(entry['outro'])
 for e in E:
  if '_obs' in e['id']:p(e['ref']+' / '+e['title'],'head');p(e['text'])
 p('La suite','head');p('Le bouton « Continuer la mission suivante » enchaîne le niveau suivant et conserve le bilan.' if n<20 else 'Fin du chapitre 4. Le chapitre 5 et le programme HORIZON sont annoncés, mais ne sont pas encore jouables dans la version 0.18.')
 p('Vérification du parcours','head');p(f'Le trajet de référence parcourt {sum(len(s["route"])-1 for s in route)} cases de déplacement et visite les {len(E)-2} points interactifs, dont les trois secrets. Les deux sas portent le total à {len(E)} repères. Les solutions du guide sont utilisées par les tests des commandes réelles du jeu.')
 def footer(c,d):
  c.setFont('Interface',8);c.setFillColor(colors.HexColor('#647e70'));c.drawString(44,25,f'FOLAMOUR / V0.18 / CHAPITRE 4 - NIVEAU {num} / SPOILERS');c.drawRightString(A4[0]-44,25,str(d.page))
 SimpleDocTemplate(str(folder/f'{prefix}-Cheatsheet.pdf'),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=42,bottomMargin=43).build(story,onFirstPage=footer,onLaterPages=footer)
 (folder/f'{prefix}-Cheatsheet.md').write_text('\n'.join(md))
 print(prefix,'map + guide generated')
summary=['# Lab-Mazing v0.18 — Le complexe de la certitude\n','Cinq niveaux jouables, quinze nouveaux essais, quinze notes secrètes et seize raccourcis. Français / anglais.\n','[Jouer](https://jfeffe.github.io/lab-mazing/)\n','## Les cinq missions\n']
for n,d in design.items():summary.append(f'### {int(n)-15}. {d["title"]}\n\n{d["layout"]}\n\n'+ '\n'.join('- '+s['solution'] for s in d['sections'])+'\n')
summary+=['## Validation et recherches\n','Les parcours physiques, les quinze solutions via les commandes, les sauvegardes partielles, les indices et les transitions sont vérifiés dans Godot 4.5.1. Les panneaux sont contrôlés en 390×844 et 844×390, en français et en anglais. Les contraintes combinatoires sont également vérifiées indépendamment. Test sur appareil réel à effectuer.\n','Inspirations méthodologiques : [Matthew VanDevander, concepteur de Taiji](https://taiji-game.com/2022/02/23/84-how-i-design-puzzles/) — construire autour d’une déduction, accepter les solutions alternatives qui préservent l’idée ; [Clara Fernandez-Vara, GDC](https://gdcvault.com/play/1013851/Puzzle-Writing-Best) — fournir les indices nécessaires et relier les énigmes au récit. Les données, textes et plans de ce chapitre sont originaux ; le passage du sceau adapte le classique problème du pont et de la lampe.\n','## Progression narrative\n','La cité souterraine confond les prévisions de MIROIR et le réel. Les badges, les routines, les caméras et les usines forment une administration toujours plus démesurée. Le joueur remplace les copies par des observations. La perte de certitude déclenche le protocole de sérénité maximale et révèle les silhouettes du programme HORIZON, futur chapitre 5.\n','## Contenu\n','Chaque dossier de niveau contient la carte exacte en PNG et PDF A3, ainsi que le guide détaillé en PDF A4 et Markdown. Les documents contiennent les solutions. Les versions précédentes restent archivées.\n']
(out/'Resume-v0.18.md').write_text('\n'.join(summary))
with zipfile.ZipFile(out/'Lab-Mazing-v0.18-Chapitre-4-Cheatsheets.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(out.rglob('*')):
  if f.is_file() and f.suffix!='.zip':z.write(f,f.relative_to(out))
