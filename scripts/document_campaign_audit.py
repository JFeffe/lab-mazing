"""Rebuild all 25 v0.22 spoiler guides from canonical game data and authored solutions."""
from pathlib import Path
from xml.sax.saxutils import escape
import json,sys,zipfile,csv,io
from PIL import Image,ImageDraw,ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,A3,landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer,PageBreak,Image as PDFImage
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[1];D=R/'game/data';OUT=Path(sys.argv[1]).resolve();OUT.mkdir(parents=True,exist_ok=True)
read=lambda p:json.loads(p.read_text())
SUB=read(D/'subject16.json');COL=read(D/'collectibles.json');ENDS=read(D/'endings.json');HINTS=read(D/'guidance.json')['hints'];AUDIT=read(R/'game/tests/collectible_placement_audit.json')
DESIGN={}
for c in [3,4,5]:DESIGN.update(read(R/f'scripts/chapter{c}_design.json'))
TITLES=['Le laboratoire','Le département des machines','Le département d’optique','Le département des essais','Le défi de Folamour','Les serres expérimentales','Le service des photocopies','Le courrier interne','La salle de réunion','Le service des archives']
FONT=str(R/'game/assets/Interface.ttf');pdfmetrics.registerFont(TTFont('Interface',FONT))
ST={k:ParagraphStyle(k,fontName='Interface',fontSize=z,leading=l,spaceAfter=a,textColor=colors.HexColor('#243c46'),keepWithNext=k in ['title','head']) for k,z,l,a in [('title',23,29,15),('head',14,19,8),('body',10,15,8),('small',8.5,12,6),('cell',8.5,12,0)]}
CS={'pickup':'#e9be72','clue':'#8eddd5','craft':'#93aff0','mechanism':'#93aff0','door':'#ee9478','exit':'#ffffff','oneway':'#ee9478'}
class Guide:
 def __init__(self,path,label):self.path=path;self.label=label;self.story=[];self.md=[]
 def p(self,t,style='body'):
  self.story.append(Paragraph(escape(str(t)).replace('\n','<br/>'),ST[style]));self.md.append(('## ' if style=='title' else '### ' if style=='head' else '')+str(t)+'\n')
 def page(self,t):
  if self.story:self.story.append(PageBreak())
  self.p(t,'title')
 def table(self,rows,widths,padding=6):
  table=Table([[Paragraph(escape(str(v)),ST['cell']) for v in row] for row in rows],colWidths=widths,repeatRows=1)
  table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dbe8e7')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),padding),('BOTTOMPADDING',(0,0),(-1,-1),padding),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#c6d3d5'))]));self.story.extend([table,Spacer(1,10)])
  self.md.append('\n'.join(['| '+' | '.join(map(str,rows[0]))+' |','| '+' | '.join(['---']*len(rows[0]))+' |']+['| '+' | '.join(map(str,row))+' |' for row in rows[1:]])+'\n')
 def save(self):
  def foot(c,d):
   c.setFont('Interface',8);c.setFillColor(colors.HexColor('#56717a'));c.drawString(44,25,self.label);c.drawRightString(A4[0]-44,25,str(d.page))
  SimpleDocTemplate(str(self.path.with_name(self.path.name+'.pdf')),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=40,bottomMargin=44).build(self.story,onFirstPage=foot,onLaterPages=foot)
  self.path.with_name(self.path.name+'.md').write_text('\n'.join(self.md))
def level_data(n):
 suffix='' if n==1 else str(n)
 m,E,S=[read(D/f'{k}{suffix}.json') for k in ['maze','events','shortcuts']]
 overlay=ENDS[str(n)]
 for e in E:
  if e['id']==overlay['id']:
   e['cell']=overlay['cell']
   for k in ['title','text','action','objective','success']:
    if k in overlay:e[k]=overlay[k][0]
   if 'wall_face' in overlay:e['wall_face']=overlay['wall_face']
 return m,E,S

def draw_map(n,m,E,S,path,title):
 c=(n-1)//5+1;theme=SUB['chapters'][str(c)];items=COL[str(n)];span=len(m['grid'])*45;im=Image.new('RGB',(max(2320,90+span+650),260+span+205),'#101f2b');dr=ImageDraw.Draw(im)
 def t(x,y,text,size=24,color='#e5edef',width=None):
  while width and ImageFont.truetype(FONT,size).getlength(text)>width:size-=1
  dr.text((x,y),text,font=ImageFont.truetype(FONT,size),fill=color)
 t(65,32,f'FOLAMOUR / V0.22 / CHAPITRE {c} / NIVEAU {(n-1)%5+1} / SPOILERS',29,'#'+theme['color'].lstrip('#'))
 t(65,90,title.upper(),43,width=2180);t(65,156,'10 SOUVENIRS À TROUVER • COORDONNÉES (x, y) DEPUIS ZÉRO • NORD EN HAUT',25)
 ox,oy,tile=90,260,45
 for y,row in enumerate(m['grid']):
  for x,v in enumerate(row):dr.rectangle((ox+x*tile,oy+y*tile,ox+(x+1)*tile-1,oy+(y+1)*tile-1),fill='#'+theme['palettes'][min(2,y//12)].lstrip('#') if v else '#253745')
 for k in range(len(m['grid'])):
  t(ox+k*tile+8,oy-28,str(k),17,'#bed0d9');t(ox-35,oy+k*tile+10,str(k),17,'#bed0d9')
 for e in E:
  x,y=e['cell'];xx,yy=ox+x*tile,oy+y*tile
  dr.rounded_rectangle((xx+3,yy+4,xx+tile-4,yy+tile-4),radius=5,fill=CS[e['kind']]);dr.text((xx+tile/2,yy+tile/2),str(e['ref']),anchor='mm',font=ImageFont.truetype(FONT,17),fill='#102730')
  if e.get('secret'):dr.line((xx+7,yy+2,xx+tile-8,yy+2),fill='white',width=3)
  if e['kind']=='exit' and n>=5:dr.ellipse((xx+30,yy-8,xx+49,yy+11),fill='#101f2b',outline='white',width=2);dr.text((xx+40,yy+1),'F',anchor='mm',font=ImageFont.truetype(FONT,13),fill='white')
  if e.get('wall_face'):dr.line((xx+5,yy+tile-1,xx+tile-5,yy+tile-1),fill='white',width=5)
  for gate in e.get('world_gates',[]):
   a,b=gate['cell'];xx,yy=ox+a*tile,oy+b*tile;dr.rectangle((xx+5,yy+5,xx+tile-5,yy+tile-5),fill='#ce91b3');dr.text((xx+tile/2,yy+tile/2),gate['label'],anchor='mm',font=ImageFont.truetype(FONT,17),fill='#102730')
 for s in S:
  x,y=s['cell'];xx,yy=ox+x*tile,oy+y*tile;dr.rectangle((xx+5,yy+5,xx+tile-5,yy+tile-5),fill='#53cfaf');dr.text((xx+tile/2,yy+tile/2),s['id'],anchor='mm',font=ImageFont.truetype(FONT,15),fill='#102730')
 for e in items:
  x,y=e['cell'];xx,yy=ox+x*tile+tile/2,oy+y*tile+tile/2;dr.ellipse((xx-20,yy-20,xx+20,yy+20),fill='#101f2b',outline='#'+theme['color'].lstrip('#'),width=4);dr.text((xx,yy),e['ref'],anchor='mm',font=ImageFont.truetype(FONT,15),fill='white')
 x,y=m['start'];xx,yy=ox+x*tile+tile/2,oy+y*tile+tile/2;dr.ellipse((xx-21,yy-21,xx+21,yy+21),outline='white',width=3);t(xx-35,yy-13,'D',20)
 sx=90+span+80;t(sx,230,'REPÈRES DU JEU',25,'#e9be72')
 for i,e in enumerate(E):t(sx,276+i*33,str(e['ref'])+'  '+e['title'],20,CS[e['kind']],width=520)
 y=max(1165,285+len(E)*33);t(sx,y,'COLLECTION DU CHAPITRE',23,'#e9be72');t(sx,y+43,theme['collectible'][0],22,width=520)
 for i,e in enumerate(items):t(sx,y+86+i*31,f'{e["ref"]}  ({e["cell"][0]}, {e["cell"][1]})  '+('impasse' if e['type']=='impasse' else 'recoin'),20)
 t(65,260+span+45,'K01–K10 : souvenirs facultatifs • F : Folamour, fin de mission • Blanc : sortie • D : départ',25)
 t(65,260+span+95,'Or : objet • Turquoise : indice • Bleu : mécanisme • Corail : porte • Vert : raccourci • Rose : accès variable',24)
 t(65,260+span+145,'Les raccourcis verts sont des murs au départ. Le tracé du labyrinthe est inchangé.',24,'#e9be72')
 buffer=io.BytesIO();im.save(buffer,format="PNG");path.write_bytes(buffer.getvalue())
 cv=canvas.Canvas(str(path.with_suffix('.pdf')),pagesize=landscape(A3));w,h=landscape(A3);scale=min(w/im.width,h/im.height);cv.drawImage(str(path),(w-im.width*scale)/2,(h-im.height*scale)/2,im.width*scale,im.height*scale);cv.showPage();cv.save()
 return im.size

for n in range(1,26):
 c=(n-1)//5+1;k=(n-1)%5+1;theme=SUB['chapters'][str(c)];m,E,S=level_data(n);by={e['id']:e for e in E};entry=DESIGN.get(str(n),{});title=TITLES[n-1] if n<=10 else entry['title'];folder=OUT/f'Chapitre-{c}'/f'Niveau-{k}';folder.mkdir(parents=True,exist_ok=True);prefix=f'Chapitre-{c}-Niveau-{k}-v0.22'
 png=folder/f'{prefix}-Carte.png';size=draw_map(n,m,E,S,png,title)
 g=Guide(folder/f'{prefix}-Cheatsheet',f'FOLAMOUR / V0.22 / C{c} N{k} / SPOILERS')
 g.page(title);g.p(f'Chapitre {c} / Niveau {k} • Version 0.22 • Solutions complètes','head')
 g.p(entry.get('intro','Explorez les départements, recoupez les indices et terminez les expériences de Folamour.'))
 if entry.get('layout'):g.p(entry['layout'])
 g.p('Cette édition remplace les anciennes cartes de ce niveau. Elle montre les nouveaux passages B1–B4, les portes existantes, les dix souvenirs K01–K10 et la position actuelle de Folamour. Les énigmes et les cases de base sont conservées.')
 g.p('Collection et dossier','head');g.p(f'Collection : {theme["collectible"][0]}. Ramasser les dix souvenirs est facultatif. Le dossier compte les trouvailles par niveau et par chapitre ; une archive se révèle à 10, 25 et 50 trouvailles dans ce chapitre. Rien ne doit être dépensé ou remis à Folamour.')
 g.p('Une collection n’apparaît sur la carte du jeu qu’après découverte de sa case. Son cercle disparaît après ramassage. Le présent guide dévoile tous les emplacements. Le clic ou toucher permet de s’y rendre et de ramasser ; le bouton Ramasser et la touche E fonctionnent aussi.')
 g.p('La collection suit la sauvegarde de cette aventure. Dans le dossier, rejouer un niveau terminé conserve la collection et les bilans, mais recommence ses énigmes et remplace le niveau en cours après confirmation. Une nouvelle aventure remet le dossier à zéro.')
 if n==1:g.p('SAS À SENS UNIQUE : trouvez les souvenirs situés au nord des sas 50 avant de franchir un sas vers le sud. Les souvenirs manqués restent récupérables en rejouant ce niveau depuis le dossier après sa réussite.','head')
 g.page('Plan exact du labyrinthe');g.story.append(PDFImage(str(png),width=507,height=507*size[1]/size[0]));g.md.append(f'![Carte]({png.name})\n');g.p('Pour lire les petits repères, utiliser le PNG en pleine résolution ou le PDF A3 séparé. Les coordonnées désignent les cases du labyrinthe ; le nord est en haut.','small')
 g.page('Les dix souvenirs');g.p('Les fonds de branches vides sont privilégiés, en donnant priorité aux branches longues. Lorsqu’il manque d’impasses adaptées, les autres objets sont dans des recoins éloignés des interactions. Aucun mur n’a été déplacé.')
 rows=[['Repère','Case (x, y)','Situation','Distance minimale aux repères']]
 for e in COL[str(n)]:rows.append([e['ref'],str(tuple(e['cell'])),f'Fond d’impasse ; branche de {e["depth"]} pas' if e['type']=='impasse' else 'Recoin dans un couloir calme',str(e['event_distance'])+' pas'])
 g.table(rows,[48,83,251,125]);g.p('Longueur de branche : du fond à la première jonction. Distance aux repères : chemin le plus court jusqu’à un objet, une interaction, un départ ou un élément de décor réservé, sur la grille et sans raccourci. Deux souvenirs sont séparés d’au moins huit pas et de quatre cases en distance Manhattan.','small')
 g.page('Parcours et fin de mission')
 route=read(R/('game/tests/route_oneway_a.json' if n==1 else f'game/tests/route_level{n}.json'))
 refs=[]
 for step in route:
  if step['id'] in by:
   e=by[step['id']];v=str(e['ref'])
   if not refs or refs[-1]!=v:refs.append(v)
 g.p('Ordre de visite de référence :','head');g.p(' → '.join(refs));g.p('Cet ordre comprend les indices et secrets. Les manipulations des postes figurent ci-dessous. Les souvenirs peuvent être ramassés lors des détours, dès que leur secteur est accessible. Aucun raccourci ni souvenir n’est requis pour terminer.')
 end=by[ENDS[str(n)]['id']];g.p(f'Fin : {end["ref"]} — {end["title"]} — {tuple(end["cell"])}','head')
 g.p('Parler au docteur et choisir « '+end.get('action','Valider')+' ». Il remplace la dernière porte.' if n>=5 else 'Le point de sortie reste une vraie porte.'+(' Le seuil est fixé au mur sud.' if n in [3,4] else ''))
 if end.get('prerequisites'):g.p('Validations requises : '+', '.join(str(by[x]['ref'])+' — '+by[x]['title'] for x in end['prerequisites']))
 g.p('Les dix souvenirs n’entrent jamais dans ces conditions.')
 if n==25:g.p('Folamour se trouve en (17, 28), près du bureau 403 en (17, 29). Terminer les trois expériences, dont le dialogue du bureau, puis lui parler. Le parcours mène ensuite à l’épilogue extérieur.')
 g.page('Énigmes et manipulations')
 sections={s['id']:s for s in entry.get('sections',[])}
 for e in E:
  if 'puzzle_type' not in e and 'answer' not in e:continue
  g.p(str(e['ref'])+' — '+e['title'],'head');g.p(e.get('question',e['text']))
  if e['id'] in HINTS:
   for i,pair in enumerate(HINTS[e['id']]):g.p(['Piste : ','Méthode : ','Solution : '][i]+pair[0])
  if e['id'] in sections:
   g.p('Depuis la réinitialisation : '+sections[e['id']]['solution']);g.p(sections[e['id']]['explanation'])
  if 'answer' in e:g.p('Code / réglage validé : '+str(e['answer']))
  for i,board in enumerate(e.get('boards',[])):
   g.p('Plan de la capsule '+chr(65+i)+' (nord en haut)','head');g.table([['Ligne','Cases']]+[[str(j+1),' · '.join(row)] for j,row in enumerate(board)],[45,462]);g.p('D : départ ; * : tampon ; R : retour ; X : interdit ; # : mur.','small')
 g.page('Tous les repères et leurs conditions')
 suffix='' if n==1 else str(n);catalog=read(D/f'items{suffix}.json') if n>1 else {}
 def item_name(v):
  if v in catalog:return catalog[v].get('name',catalog[v].get('title',v))
  for e in E:
   if e.get('resource')==v:return e['title']
  return v
 for e in E:
  g.p(str(e['ref'])+' — '+e['title']+' — '+str(tuple(e['cell'])),'head');g.p(e['text'])
  if e.get('secret'):g.p('Note secrète facultative. Elle est distincte de la collection K01–K10.','small')
  if e.get('requires'):g.p('À installer / remettre : '+', '.join(item_name(x) for x in e['requires']))
  if e.get('prerequisites'):g.p('À valider d’abord : '+', '.join(str(by[x]['ref'])+' — '+by[x]['title'] for x in e['prerequisites']))
  if e.get('controlled_by'):g.p('Commande : '+by[e['controlled_by']]['ref'])
  if e.get('opens'):g.p('Ouvre : '+', '.join(str(by[x]['ref']) for x in e['opens'] if x in by))
  if e.get('grants'):g.p('Produit : '+', '.join(item_name(x)+' × '+str(q) for x,q in e['grants'].items()))
 g.page('Raccourcis et reprise')
 if S:g.table([['ID','Mur','Deux cases à visiter','Gain minimal']]+[[s['id'],str(tuple(s['cell'])),str(tuple(s['sides'][0]))+' / '+str(tuple(s['sides'][1])),str(s['fully_open_saved_steps'])+' pas'] for s in S],[43,83,286,95],padding=3)
 else:g.p('Ce niveau utilise des boucles naturelles et ne contient pas de raccourci caché.')
 g.p('Marcher sur les deux côtés du mur ouvre le raccourci. Voir les cases sur la carte ne suffit pas. Le gain minimal compare les deux côtés du mur : passage de 2 pas contre le détour restant lorsque les autres raccourcis et les verrous sont ouverts. Les sas à sens unique restent exclus. Chaque nouvelle porte économise au moins 20 pas ; les portes antérieures au moins 12.')
 new_links=[link for link in S if link.get('return_example')]
 if new_links:
  g.p('Nouvelles portes : retours utiles','head')
  for link in new_links:
   ex=link['return_example']
   g.p(link['id']+' : de ['+str(ex['origin_ref'])+'] '+ex['origin_title']+' vers ['+str(ex['target_ref'])+'] '+ex['target_title']+'. '+str(ex['before'])+' pas sans cette porte ; '+str(ex['after'])+' avec : '+str(ex['saved'])+' pas économisés.')
  g.p('Exemples mesurés avec la carte entièrement connue et les autres portes ouvertes. Ce sont des trajets de retour comparables, pas une estimation du temps d’une première partie. Le détour initial reste nécessaire pour visiter les deux côtés du mur.','small')
 g.p('Reprise de v0.21 : les anciennes portes et leur position sont conservées. Une nouvelle porte se révèle immédiatement si ses deux cases avaient déjà été parcourues. Les objets, énigmes et souvenirs restent acquis.')
 g.p('Le clic approche désormais assez près des commandes fixées au mur pour les examiner. Cliquer sur un objet inaccessible annule la destination précédente.')
 g.p('Carte : clic droit sur un passage découvert et accessible pour fermer la carte et marcher vers ce point. Zoom : molette ou boutons de zoom ; recul maximal augmenté. Dossier : bouton près de l’objectif, menu Pause ou bilan de fin.')
 g.p('Folamour réagit aux rencontres, découvertes, essais et réussites. Les options « Animations décoratives » et « Répliques de Folamour » sont séparées dans la pause. Désactiver les répliques n’efface pas les observations archivées.')
 g.p('Sauvegarde locale au navigateur et à l’appareil. Les anciennes sauvegardes v4 sont compatibles ; une collection déjà commencée est conservée. Les totaux des anciennes parties couvrent uniquement les informations qui ont été enregistrées. Aucun ancien souvenir n’est attribué automatiquement.')
 g.save();print('Documents',n,flush=True)

# One machine-readable placement index and chapter archives for convenient sharing.
with (OUT/'Index-250-souvenirs-v0.22.csv').open('w',newline='') as f:
 writer=csv.writer(f,lineterminator="\n");writer.writerow(['chapitre','niveau','niveau_global','repere','x','y','situation','profondeur_impasse','distance_repere'])
 for n,items in COL.items():
  for e in items:writer.writerow([e['chapter'],(int(n)-1)%5+1,n,e['ref'],*e['cell'],e['type'],e['depth'],e['event_distance']])
for c in range(1,6):
 with zipfile.ZipFile(OUT/f'Chapitre-{c}-v0.22.zip','w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted((OUT/f'Chapitre-{c}').rglob('*')):
   if p.is_file():z.write(p,p.relative_to(OUT))


AUDIT_RETURNS=read(R/'game/tests/return_links_audit.json')
ADDED=sum(len(row['added_ids']) for row in AUDIT_RETURNS['levels']);TOTAL=sum(len(row['after']) for row in AUDIT_RETURNS['levels']);CHANGED=sum(bool(row['added_ids']) for row in AUDIT_RETURNS['levels'])
GAINS=[s['fully_open_saved_steps'] for row in AUDIT_RETURNS['levels'] for s in row['after'] if s['id'] in row['added_ids']]
report=Guide(OUT/'Audit-et-raccourcis-v0.22','FOLAMOUR / V0.22 / AUDIT DE LA CAMPAGNE')
report.page('Des retours plus courts')
report.p('Audit des 25 niveaux - 9 septembre 2026','head')
report.p(f'Version 0.22 : {ADDED} portes secrètes ajoutées sur {CHANGED} niveaux. La campagne compte désormais {TOTAL} raccourcis, contre 112. Les 25 labyrinthes, les conditions des énigmes, les notes secrètes et les 250 souvenirs sont conservés.')
report.p(f'Chaque nouvelle porte économise entre {min(GAINS)} et {max(GAINS)} pas entre ses deux côtés, même lorsque les autres passages et les verrous sont ouverts. Les exemples vers les machines, commandes ou Folamour explicitent les retours utiles dans chaque guide. Les anciens passages conservent au moins 12 pas de gain.')
report.p('Règle de découverte','head')
report.p('Un raccourci est un mur au départ. Il se révèle uniquement après avoir marché sur ses deux cases voisines. Voir le mur ou les deux cases dans le brouillard ne suffit pas. Le passage reste ensuite ouvert dans les deux sens et figure sur la carte et dans le journal.')
report.p('Les portes existantes restent exactement à leur place avec les mêmes identifiants. Les nouvelles portes portent les repères B1 à B4. Si leurs deux côtés ont déjà été parcourus dans une sauvegarde v0.21, elles se révèlent à la reprise. Les objets, essais partiels, indices et souvenirs sont conservés.')
report.page('Deux bugs reproduits et corrigés')
report.p('Sortie murale du niveau global 3','head')
report.p('Reproduction : depuis la case (17, 32), cliquer sur la sortie située en (17, 33), dont le modèle est fixé au mur sud. Le personnage choisissait sa case actuelle comme destination, mais la distance réelle jusqu’au modèle dépassait la portée de 3 mètres. Le déplacement se terminait sans ouvrir le panneau. Correction : le calcul du trajet vérifie désormais la distance jusqu’au modèle de l’interaction, y compris son décalage mural. Le personnage avance assez près.')
report.p('Nouvelle destination inaccessible','head')
report.p('Reproduction : demander un déplacement accessible, puis cliquer sur un objet situé derrière un secteur fermé ou inconnu. L’alerte apparaissait, mais l’ancien déplacement continuait. Correction : toute nouvelle demande vers un objet remplace le trajet précédent. Si l’objet est inaccessible, le déplacement et son marqueur sont annulés.')
report.p('Les deux défauts ont été reproduits avant correction. Le test verify_interaction_approaches échouait sur ces cas, puis réussit après correction. Les contrôles muraux des niveaux 3 et 4 et la navigation déjà existante sont également couverts.')
report.page('Répartition par niveau')
report.table([['Chapitre / niveau','Avant','Ajout','Total']]+[[f'{(row["level"]-1)//5+1} / {(row["level"]-1)%5+1}',len(row['before']),len(row['added_ids']),len(row['after'])] for row in AUDIT_RETURNS['levels']],[225,94,94,94],padding=3)
report.p('Niveaux sans ajout','head')
report.p(' ; '.join(f"chapitre {(row['level']-1)//5+1} / niveau {(row['level']-1)%5+1}" for row in AUDIT_RETURNS['levels'] if not row['added_ids'])+'. Les candidats sont trop courts, redondants ou sans gain utile vers un poste permanent. Ces niveaux ont été vérifiés ; leurs passages existants sont conservés.')
report.page('Mesures, tests et limites')
report.p('Placement vérifié indépendamment','head')
report.p('Chaque ouverture remplace une case murale entre exactement deux cases de sol opposées. Ses côtés appartiennent déjà à la même zone lorsque tous les sas, portes et accès variables sont fermés. Aucun lien ne contourne donc une barrière d’énigme. Les rayonnages mobiles des archives sont exclus du placement et aucun nouveau côté de porte ne recouvre un souvenir.')
report.p('Le gain est calculé sur les chemins les plus courts, avec les autres raccourcis et les portes ordinaires ouverts. Les sas à sens unique restent fermés au routage. Pour chaque ajout, un trajet entre deux repères démontre un retour vers un poste permanent, une commande ou une fin de mission ; les chiffres sont recalculés par un validateur indépendant.')
report.p('Vérifications exécutées','head')
report.table([['Couverture','Contrôle'],['25 niveaux','Parcours physiques existants, conditions des énigmes, solutions et transitions'],[str(TOTAL)+' portes','Collision fermée, visite des deux côtés, traversée aller/retour, chemin au clic'],['Sauvegardes','25 reprises avec les nouvelles portes ; indices, objets, essais partiels et collection préservés'],['Accès variables','Rayonnages, badges, phases, caméras et ponts ; états réversibles et absence de contournement'],['Collection','250 ramassages et placements ; les 25 empreintes de grille sont inchangées'],['Interface et audio','Français/anglais, dimensions portrait/paysage, confort mobile et transitions audio'],['Documentation','25 cartes PNG/PDF et 25 guides PDF/Markdown régénérés ; exemples et gains des nouvelles portes']],[132,375])
report.p('Les tests de parcours suivent des itinéraires de référence ; les tests des portes et des souvenirs utilisent des points de départ préparés afin de vérifier chaque cas isolément. Ils ne représentent pas une partie humaine unique à l’aveugle. Les durées des tests ne mesurent pas les performances en jeu.')
report.p('Le contrôle visuel dans Godot a couvert les 25 niveaux et les panneaux en portrait/paysage. Le navigateur de contrôle ne fournit pas WebGL 2. Le rendu Web et la fluidité sur un téléphone physique ne sont donc pas validés dans cette session. Les dimensions des interfaces sont contrôlées dans Godot ; les PDF sont rendus et inspectés avant remise.')
report.save()
index=['# Lab-Mazing v0.22 - Cartes et cheatsheets','', f'{ADDED} nouvelles portes, {TOTAL} passages au total. Les guides comprennent les solutions, les 250 souvenirs et les retours utiles.','', '| Chapitre | Niveau | Guide |','| --- | --- | --- |']
for row in AUDIT_RETURNS['levels']:
 n=row['level'];c=(n-1)//5+1;k=(n-1)%5+1;prefix=f'Chapitre-{c}/Niveau-{k}/Chapitre-{c}-Niveau-{k}-v0.22'
 index.append(f'| {c} | {k} | [Solutions et carte]({prefix}-Cheatsheet.md) |')
index+=['','[Audit et détail des corrections](Audit-et-raccourcis-v0.22.md)']
(OUT/'INDEX.md').write_text('\n'.join(index)+'\n')
with zipfile.ZipFile(OUT/'Lab-Mazing-v0.22-Guides-complets.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(OUT.rglob('*')):
  if p.is_file() and p.suffix!='.zip':z.write(p,p.relative_to(OUT))
print('All 25 guides, maps and audit report complete',flush=True)
