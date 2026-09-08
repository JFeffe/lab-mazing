"""Five source-exact maps and French solution guides for chapter five."""
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
font=str(R/'game/assets/Interface.ttf');pdfmetrics.registerFont(TTFont('Interface',font));design=json.loads((R/'scripts/chapter5_design.json').read_text());guidance=json.loads((D/'guidance.json').read_text())
cs={'pickup':'#e9be72','clue':'#8eddd5','mechanism':'#93aff0','door':'#ee9478','exit':'#ffffff'}
styles={k:ParagraphStyle(k,fontName='Interface',fontSize=fs,leading=lead,spaceAfter=gap,textColor=colors.HexColor('#203b43'),keepWithNext=k in ['title','head']) for k,fs,lead,gap in [('title',24,29,15),('head',14,19,8),('body',10,15,9),('cell',8.7,12,0)]}
def zone(n,x,y):
 if n==21:return 0 if x<22 else 1 if y<17 else 2
 if n==22:return 2 if 13<=x<=21 and 13<=y<=21 else 1 if 7<=x<=27 and 7<=y<=27 else 0
 if n==23:return 0 if y<21 else 1 if x<17 else 2
 if n==24:return 2 if y>19 else 0 if x<15 else 1
 return 0 if y<11 else 1 if y<23 else 2
palettes=[['#ab8e68','#809a96','#8797b2'],['#a2a084','#8e9cae','#8cab98'],['#6c97a2','#8f85a4','#88a798'],['#849fa2','#b49a6d','#8e8eae'],['#9582a8','#8c9c98','#ae986f']]
for n in range(21,26):
 num=n-20;entry=design[str(n)];folder=out/f'Niveau-{num}';folder.mkdir(exist_ok=True);prefix=f'Chapitre-5-Niveau-{num}-v0.19'
 m,E,S=[json.loads((D/f'{k}{n}.json').read_text()) for k in ['maze','events','shortcuts']];by={e['id']:e for e in E};route=json.loads((R/f'game/tests/route_level{n}.json').read_text())
 im=Image.new('RGB',(2020,1870),'#101f2b');dr=ImageDraw.Draw(im)
 def txt(x,y,t,size=24,color='#e7edf0',width=None):
  while width and ImageFont.truetype(font,size).getlength(t)>width:size-=1
  dr.text((x,y),t,font=ImageFont.truetype(font,size),fill=color)
 txt(65,30,f'FOLAMOUR / V0.19 / CHAPITRE 5 / NIVEAU {num} / SPOILERS',27,'#e9be72');txt(65,85,entry['title'].upper(),44,width=1890)
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
 txt(65,1820,f'3 SECRETS / {len(S)} RACCOURCIS / 3 ÉNIGMES / ESSAIS RÉVERSIBLES / TEMPS RÉEL ILLIMITÉ',24,'#e9be72')
 png=folder/f'{prefix}-Map-vue-de-haut.png';im.save(png)
 cv=canvas.Canvas(str(folder/f'{prefix}-Map-vue-de-haut.pdf'),pagesize=landscape(A3));w,h=landscape(A3);scale=min(w/im.width,h/im.height);cv.drawImage(str(png),(w-im.width*scale)/2,(h-im.height*scale)/2,im.width*scale,im.height*scale);cv.showPage();cv.save()
 story=[];md=[f'# {entry["title"]}\n\nChapitre 5 / Niveau {num} / Version 0.19 / SPOILERS\n']
 def p(t,style='body'):
  story.append(Paragraph(escape(str(t)).replace('\n','<br/>'),styles[style]));md.append(('## ' if style=='title' else '### ' if style=='head' else '')+str(t)+'\n')
 def page(title):
  if story:story.append(PageBreak())
  p(title,'title')
 def table(rows,widths):
  t=Table([[Paragraph(escape(str(v)),styles['cell']) for v in row] for row in rows],colWidths=widths,repeatRows=1)
  t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8dfce')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#c9d7cf'))]));story.extend([t,Spacer(1,10)])
  md.append('\n'.join(['| '+' | '.join(map(str,rows[0]))+' |','| '+' | '.join(['---']*len(rows[0]))+' |']+['| '+' | '.join(map(str,r))+' |' for r in rows[1:]])+'\n')
 page(entry['title']+f'\nChapitre 5 / Niveau {num}')
 p('SPOILERS / VERSION 0.19','head');p(entry['intro']);p(entry['layout'])
 p('Parcours conseillé','head')
 p('Menu > Choisir un chapitre > Chapitre 5. Le démarrage direct remplace la sauvegarde après confirmation. Enchaîner les missions conserve les bilans ; le sac et le journal se renouvellent à chaque niveau.')
 for i,sec in enumerate(entry['sections'],1):
  e=by[sec['id']];p(f'{i}. '+('Ramasser la mallette 101 et l’installer au poste 203. ' if i==1 else '')+f'Lire les consignes {(i+1)*100+1} et {(i+1)*100+2}, puis résoudre {e["ref"]} : {e["title"]}. '+('Le sas '+str(110+i)+' s’ouvre.' if i<3 else 'Rejoindre ensuite le passage 900.'))
 p('Les trois secrets 501/502/503 sont facultatifs. Le parcours principal fonctionne sans ouvrir de raccourci. Chaque essai est réversible et propose trois niveaux d’indice.')
 p('Rythme et sauvegarde','head');p('Aucune échéance réelle. Au niveau 4, HORIZON descend de l’étape 3 à l’étape 0 uniquement après les validations. Lecture, réflexion et pause ne font pas avancer la procédure. Les réglages, observations, programmes et réponses sont sauvegardés. La réinitialisation ne rend pas la mallette installée et ne supprime pas les constats lus.')
 page('Plan du labyrinthe')
 story.append(PDFImage(str(png),width=507,height=507*im.height/im.width));p('La carte A3 et le PNG séparés permettent de lire les coordonnées à pleine résolution. Nord en haut ; origine (0,0). Les couleurs indiquent les secteurs. Les numéros correspondent exactement aux objets du jeu.')
 for i,sec in enumerate(entry['sections'],1):
  e=by[sec['id']];page(f'{i:02d} / {e["title"]}')
  p(f'Poste {e["ref"]} : {tuple(e["cell"])}. '+('Mallette 101 requise.' if i==1 else f'Validation du poste {i*100+3} requise.'))
  p(e['text'])
  for k in [2*i-1,2*i]:
   note=by[f'c{n}_n{k}'];p(f'{note["ref"]} / {tuple(note["cell"])}','head');p(note['text'])
  if e.get('world_gates'):
   table([['Accès','Porte','Inspection']]+[[b['label'],str(tuple(b['cell'])),by[e['observations'][j]]['ref']+' / '+str(tuple(by[e['observations'][j]]['cell']))] for j,b in enumerate(e['world_gates'])],[70,130,307])
   p('Les commandes de pont sont utilisables uniquement près du poste 203. Une fois le poste validé, les trois accès restent ouverts. Les relevés restent acquis après réinitialisation.')
  if e.get('boards'):
   p('Plans des capsules : nord en haut. D = départ ; * = tampon ; R = retour ; X = conduit interdit. Un carré plein est un mur.','head')
   tile=28;mini=Image.new('RGB',(len(e['boards'])*174,180),'white');pen=ImageDraw.Draw(mini)
   for bi,board in enumerate(e['boards']):
    pen.text((bi*174+14,0),'Capsule '+('A' if bi==0 else 'B'),font=ImageFont.truetype(font,14),fill='#203b43')
    for y,row in enumerate(board):
     for x,v in enumerate(row):
      xx=bi*174+14+x*tile;yy=27+y*tile;pen.rectangle((xx,yy,xx+tile-2,yy+tile-2),fill='#314957' if v=='#' else '#d6e4dc')
      if v not in '.#':pen.text((xx+tile/2,yy+tile/2),v,font=ImageFont.truetype(font,17),anchor='mm',fill='#203b43')
    md.append('Plan '+('A' if bi==0 else 'B')+' :\n\n| Ligne | Cases |\n| --- | --- |\n'+'\n'.join(f'| {j+1} | {" · ".join(row)} |' for j,row in enumerate(board))+'\n')
   import io
   buf=io.BytesIO();mini.save(buf,format='PNG');buf.seek(0);story.append(PDFImage(buf,width=mini.width,height=mini.height));story.append(Spacer(1,8))
  if e['mode']=='feedback':table([['Lien','Nature']]+[[e['names'][a]+' > '+e['names'][b],'Apport original à conserver' if j in e['protected'] else 'Copie circulaire'] for j,(a,b) in enumerate(e['edges'])],[210,297])
  p('Solution depuis la réinitialisation','head');p(sec['solution']);p(sec['explanation'])
  if e['mode'] in ['courier','chronology','redaction','protocol','feedback','policy','damping']:p('Attention : modifier le réglage ou le programme invalide son dernier test. Relancer « Tester la procédure » avant de valider.')
  if e['mode']=='dialogue':
   for j in range(3):p(e['questions'][j]);p('Réponse : '+e['answers'][j][e['correct'][j]]);p(e['responses'][j])
 page('Repères et raccourcis')
 table([['Repère','Objet / poste','Coordonnées']]+[[e['ref'],e['title'],str(tuple(e['cell']))] for e in sorted(E,key=lambda e:int(e['ref']))],[55,340,112])
 p('Raccourcis facultatifs','head')
 if S:table([['ID','Mur','Côtés à parcourir','Gain minimal']]+[[s['id'],str(tuple(s['cell'])),' / '.join(str(tuple(c)) for c in s['sides']),str(s['minimum_saved_steps'])+' pas'] for s in S],[45,85,277,100])
 else:p('Aucun raccourci caché : les anneaux offrent déjà des boucles de circulation.')
 p('Le gain est mesuré entre les côtés du mur même lorsque les autres raccourcis sont ouverts. Aucun passage ne contourne un sas d’énigme.')
 page('Archives et conclusion')
 for e in E:
  if e.get('secret') or '_obs' in e['id']:p(f'{e["ref"]} / {tuple(e["cell"])}','head');p(e['text'])
 p('Révélation de fin de mission','head');p(entry['outro'])
 p('La suite','head');p('Le bouton « Continuer la mission suivante » conserve le bilan et démarre le prochain niveau.' if n<25 else 'Le dialogue autorise la sortie 900. Le bilan termine l’aventure et propose « Regarder la surface ». La dernière annonce : « Vous quittez une zone entièrement sécurisée. Bonne chance avec le reste. » Le bouton « Revoir la conclusion » permet de retrouver le bilan.')
 p('Vérification','head');p(f'Le parcours de référence effectue {sum(len(s["route"])-1 for s in route)} pas et visite tous les objets interactifs, y compris les trois secrets. Les solutions sont exercées par les boutons réels du jeu, avec sauvegarde partielle, reprise et indices en français et en anglais.')
 def footer(c,d):
  c.setFont('Interface',8);c.setFillColor(colors.HexColor('#647e70'));c.drawString(44,25,f'FOLAMOUR / V0.19 / CHAPITRE 5 - NIVEAU {num} / SPOILERS');c.drawRightString(A4[0]-44,25,str(d.page))
 SimpleDocTemplate(str(folder/f'{prefix}-Cheatsheet.pdf'),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=42,bottomMargin=43).build(story,onFirstPage=footer,onLaterPages=footer)
 (folder/f'{prefix}-Cheatsheet.md').write_text('\n'.join(md))
 print(prefix,'map + guide generated')
summary=['# Lab-Mazing v0.19 - Pour votre tranquillité définitive\n','Le chapitre final ajoute cinq niveaux, quinze énigmes, quinze secrets et seize raccourcis. La campagne comprend désormais cinq chapitres et vingt-cinq niveaux.\n','[Jouer](https://jfeffe.github.io/lab-mazing/)\n','## Les cinq missions\n']
for n,d in design.items():summary.append(f'### {int(n)-20}. {d["title"]}\n\n{d["layout"]}\n\n'+ '\n'.join('- '+s['solution'] for s in d['sections'])+'\n')
summary+=['## Histoire et mise en scène\n','HORIZON prolonge directement la fin du chapitre 4. La cité devait conserver les habitants conformes, tandis que les fusées traitaient les « variables extérieures ». Le joueur découvre que MIROIR se cite lui-même et provoque ses propres preuves. Les copies ont retiré les réserves du mandat original. Folamour, obsédé par la protection, doit accepter l’incertitude et le droit de changer d’avis.\n','Les trois interventions du niveau 4 réduisent les étapes restantes de 3 à 0. L’ambiance mécanique change avec la progression, les installations bougent puis s’immobilisent. Les annonces absurdes restent dans le journal. Au niveau 5, le bruit et la musique s’effacent. Le dialogue se termine dans un petit bureau avec une tasse froide ; la scène extérieure conclut l’aventure.\n','## Validation\n','Topologie et parcours physiques complets ; quinze solutions via les boutons ; sauvegardes partielles et finales ; reprise du chapitre 4 ; indices français/anglais ; oracle indépendant pour les contraintes et les trajets de capsules. Vérification des interfaces étroites et régressions des anciens chapitres avant publication. Un essai sur un téléphone physique reste à faire.\n','## Documents\n','Chaque dossier contient une carte exacte en PNG et PDF A3, ainsi que la cheatsheet détaillée en PDF A4 et Markdown. Le ZIP rassemble les cinq dossiers et ce résumé. Les versions précédentes restent archivées. Les plans, textes, scènes et sons du chapitre sont créés pour le projet.\n']
(out/'Resume-v0.19.md').write_text('\n'.join(summary))
with zipfile.ZipFile(out/'Lab-Mazing-v0.19-Chapitre-5-Cheatsheets.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(out.rglob('*')):
  if f.is_file() and f.suffix!='.zip':z.write(f,f.relative_to(out))
