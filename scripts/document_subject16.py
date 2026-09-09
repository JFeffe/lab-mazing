"""Rebuild all 25 v0.21 spoiler guides from canonical game data and authored solutions."""
from pathlib import Path
from xml.sax.saxutils import escape
import json,sys,zipfile,csv
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
 def table(self,rows,widths):
  table=Table([[Paragraph(escape(str(v)),ST['cell']) for v in row] for row in rows],colWidths=widths,repeatRows=1)
  table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dbe8e7')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#c6d3d5'))]));self.story.extend([table,Spacer(1,10)])
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
 t(65,32,f'FOLAMOUR / V0.21 / CHAPITRE {c} / NIVEAU {(n-1)%5+1} / SPOILERS',29,'#'+theme['color'].lstrip('#'))
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
 im.save(path)
 cv=canvas.Canvas(str(path.with_suffix('.pdf')),pagesize=landscape(A3));w,h=landscape(A3);scale=min(w/im.width,h/im.height);cv.drawImage(str(path),(w-im.width*scale)/2,(h-im.height*scale)/2,im.width*scale,im.height*scale);cv.showPage();cv.save()
 return im.size

for n in range(1,26):
 c=(n-1)//5+1;k=(n-1)%5+1;theme=SUB['chapters'][str(c)];m,E,S=level_data(n);by={e['id']:e for e in E};entry=DESIGN.get(str(n),{});title=TITLES[n-1] if n<=10 else entry['title'];folder=OUT/f'Chapitre-{c}'/f'Niveau-{k}';folder.mkdir(parents=True,exist_ok=True);prefix=f'Chapitre-{c}-Niveau-{k}-v0.21'
 png=folder/f'{prefix}-Carte.png';size=draw_map(n,m,E,S,png,title)
 g=Guide(folder/f'{prefix}-Cheatsheet',f'FOLAMOUR / V0.21 / C{c} N{k} / SPOILERS')
 g.page(title);g.p(f'Chapitre {c} / Niveau {k} • Version 0.21 • Solutions complètes','head')
 g.p(entry.get('intro','Explorez les départements, recoupez les indices et terminez les expériences de Folamour.'))
 if entry.get('layout'):g.p(entry['layout'])
 g.p('Cette édition remplace les anciennes cartes de ce niveau. Elle ajoute les dix souvenirs K01–K10 et utilise la position actuelle de la fin de mission. Les énigmes et les labyrinthes sont conservés.')
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
 if S:g.table([['ID','Mur','Deux cases à visiter','Gain minimal']]+[[s['id'],str(tuple(s['cell'])),str(tuple(s['sides'][0]))+' / '+str(tuple(s['sides'][1])),str(s['minimum_saved_steps'])+' pas'] for s in S],[43,83,286,95])
 else:g.p('Ce niveau utilise des boucles naturelles et ne contient pas de raccourci caché.')
 g.p('Marcher sur les deux côtés du mur ouvre le raccourci. Voir les cases sur la carte ne suffit pas. Le gain minimal mesure les pas encore économisés lorsque les autres raccourcis sont ouverts.')
 g.p('Carte : clic droit sur un passage découvert et accessible pour fermer la carte et marcher vers ce point. Zoom : molette ou boutons de zoom ; recul maximal augmenté. Dossier : bouton près de l’objectif, menu Pause ou bilan de fin.')
 g.p('Folamour réagit aux rencontres, découvertes, essais et réussites. Les options « Animations décoratives » et « Répliques de Folamour » sont séparées dans la pause. Désactiver les répliques n’efface pas les observations archivées.')
 g.p('Sauvegarde locale au navigateur et à l’appareil. Les anciennes sauvegardes v4 sont compatibles ; la collection commence vide. Les totaux des anciennes parties couvrent uniquement les informations qui ont été enregistrées. Aucun ancien souvenir n’est attribué automatiquement.')
 g.save();print('Documents',n,flush=True)

# One machine-readable placement index and chapter archives for convenient sharing.
with (OUT/'Index-250-souvenirs-v0.21.csv').open('w',newline='') as f:
 writer=csv.writer(f,lineterminator="\n");writer.writerow(['chapitre','niveau','niveau_global','repere','x','y','situation','profondeur_impasse','distance_repere'])
 for n,items in COL.items():
  for e in items:writer.writerow([e['chapter'],(int(n)-1)%5+1,n,e['ref'],*e['cell'],e['type'],e['depth'],e['event_distance']])
for c in range(1,6):
 with zipfile.ZipFile(OUT/f'Chapitre-{c}-v0.21.zip','w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted((OUT/f'Chapitre-{c}').rglob('*')):
   if p.is_file():z.write(p,p.relative_to(OUT))

report=Guide(OUT/'Recherche-et-audit-v0.21','FOLAMOUR / V0.21 / RECHERCHE ET AUDIT')
report.page('Le dossier du sujet 16');report.p('Conception, recherche et audit des 25 niveaux • 9 septembre 2026','head')
report.p('Objectif : récompenser la curiosité, donner une présence plus sensible au docteur et différencier les cinq chapitres, en conservant toutes les grilles et toutes les énigmes. Cette édition ajoute 250 souvenirs fixes, quinze archives et un dossier de progression. Les changements restent compatibles avec les sauvegardes existantes.')
report.p('La demande de dix récompenses dans de longues impasses rencontre une contrainte réelle : plusieurs niveaux contiennent peu de branches terminales et les niveaux globaux 18 et 22 n’en possèdent aucune. Le choix retenu consiste à préserver le tracé et le nombre de récompenses, puis à compléter les meilleurs fonds d’impasse par des recoins calmes. Cette concession est explicite et mesurée, plutôt que de présenter tous les emplacements comme de longues impasses.')
report.table([['Résultat','Quantité'],['Niveaux / chapitres','25 / 5'],['Souvenirs fixes','250 ; exactement 10 par niveau'],['Fonds d’impasse','196, dont 129 branches de 4 à 24 pas et 67 branches de 2 pas'],['Recoins de couloir','54'],['Archives narratives','15 ; seuils de 10, 25 et 50 par chapitre'],['Silhouettes de collection','5, avec 1 à 5 marques selon la mission'],['Grilles, énigmes et raccourcis modifiés','0']],[225,282])
report.p('Le dossier est une trace de l’aventure en cours. Il réunit la collection, les étapes terminées, les énigmes et raccourcis comptabilisés, les indices consultés et les observations originales de Folamour. La collection ne donne aucun pouvoir, ne remplace aucun indice et ne devient jamais une condition de fin.')
report.page('Recherche et décisions de conception')
report.p('Récompenser une exploration volontaire','head')
report.p('La présentation de Leah Miller à la GDC 2019 distingue les objets finis, placés à des endroits précis, des ressources répétitives. Elle relie leur réussite à la cohérence entre art, récit et jeu, et recommande de récompenser l’exploration et l’observation sans interrompre le rythme. Elle signale notamment la répétition fastidieuse et les objets incongrus parmi les écueils. [1]')
report.p('Application à Folamour — décision de conception : chaque détour rapporte une petite pièce d’archive liée à son chapitre. Le ramassage confirme immédiatement la trouvaille, sans ouvrir une fenêtre. Les récompenses sont uniques, ne réapparaissent pas après sauvegarde et ne nécessitent aucun retour obligatoire. Les nouvelles archives donnent une raison narrative à la collection ; elles n’accordent pas de monnaie artificielle ou de puissance sans rapport avec le jeu.')
report.p('Le nombre dix est une contrainte demandée pour chaque niveau, pas une conclusion de la recherche. Son intérêt pratique est une progression compréhensible. Son coût est de devoir utiliser des branches courtes ou des recoins dans les cartes en anneaux. Le dossier de reprise permet de revenir compléter une mission terminée sans perdre les trouvailles antérieures. Le joueur voit explicitement que ses énigmes recommenceront.')
report.p('Lisibilité et mouvement discret','head')
report.p('Les Game Accessibility Guidelines recommandent d’éviter les scintillements et les motifs visuels répétitifs qui provoquent une gêne, et de proposer la désactivation des effets concernés. [2] Application choisie : les nouveaux gestes du docteur sont lents, sans flash ; une option indépendante coupe ces animations. Les silhouettes et les marques de mission complètent les couleurs. La collection ne dépend donc pas uniquement de la distinction turquoise, ocre, violet, bleu ou cuivre.')
report.p('Budget graphique','head')
report.p('La documentation Godot 4.5 décrit les gains du masquage des objets lointains et le coût des surfaces transparentes. [3] Application choisie : petites formes opaques, maillages et matériaux partagés, aucun nouvel éclairage dynamique et intégration des décors au masquage existant. Les accessoires n’ajoutent pas de collisions et ne peuvent pas modifier les itinéraires physiques. Cette architecture vise la sobriété ; elle ne constitue pas une mesure de fréquence d’image sur téléphone.')
report.page('Identités des chapitres et Folamour')
report.table([['Chapitre','Collection','Langage visuel'],['1 — Laboratoire','Ampoule témoin','Turquoise ; flacons, laboratoire artisanal'],['2 — Stage','Tampon de service','Ocre ; dossiers, rangement administratif'],['3 — Prévoyance','Rouage de prévoyance','Violet ; cadrans et mécanismes prédictifs'],['4 — Certitude','Prisme MIROIR','Bleu ; surfaces jumelles et symétrie'],['5 — HORIZON','Capsule de retour','Cuivre ; conduites, protection et retour']],[115,150,242])
report.p('Les palettes s’intègrent aux couleurs déjà présentes par secteur, afin de conserver les repères spatiaux de chaque mission. L’ambiance lumineuse et le fond suivent le chapitre. Les accessoires sont placés au-dessus des murs et les incrustations de sol restent minces. Le grand décor narratif du dernier chapitre est conservé. Les silhouettes de collection sont distinctes ; le nombre de petites marques varie de un à cinq au sein du chapitre.')
report.p('Une présence liée à la situation','head')
report.p('Le docteur tourne doucement la tête et le corps vers le sujet lorsqu’il approche. Une respiration légère et des gestes de bras rendent sa posture moins figée ; les gestes deviennent un peu plus amples pendant ses remarques. Les copies décoratives utilisent aussi ces mouvements. Les discussions de fin conservent leurs conditions et leurs textes propres à chaque mission.')
report.p('Quatre familles de réactions sont écrites dans les deux langues : rencontre, réussite, erreur et découverte. Leur ton évolue du laboratoire ironique vers la conclusion plus humaine. Chaque déclenchement est mémorisé pour éviter une relance continue en restant près du docteur. Les observations identiques sont regroupées dans le dossier. Le premier, cinquième et dixième souvenir d’un niveau peuvent déclencher une remarque ; seules les remarques courtes s’affichent dans le HUD.')
report.p('Les commentaires et les animations disposent de deux réglages séparés dans la pause. Couper les commentaires masque leur affichage temporaire, tout en laissant leurs observations consultables. Les menus interrompent le temps de jeu et les nouveaux mouvements. Les sous-titres du dossier et des nouvelles répliques suivent la langue sélectionnée sans réécrire les données sauvegardées.')
report.page('Placement : méthode et niveaux 1 à 15')
report.p('Le placement utilise les cases de sol et leurs quatre voisines. Les positions actuelles des fins de niveau sont appliquées avant l’analyse. Sont exclus : événements, départ, accès variables, décors narratifs réservés et côtés des raccourcis. Chaque candidat reste à trois cases Manhattan et à cinq pas de chemin au minimum des éléments réservés.')
report.p('Une branche terminale est suivie jusqu’à sa première jonction ; elle doit être vide d’interaction. Les vrais fonds sont prioritaires, puis leur profondeur, leur éloignement du contenu et leur dispersion. Deux souvenirs restent à huit pas de chemin et quatre cases Manhattan au minimum. L’ordre des égalités est stable : relancer le générateur produit les mêmes coordonnées et identifiants.')
report.table([['Niveau global','Chapitre / niveau','Impasses','Recoins','Écart min. (pas)']]+[[n,f'{(n-1)//5+1} / {(n-1)%5+1}',AUDIT[str(n)]['dead_ends'],10-AUDIT[str(n)]['dead_ends'],AUDIT[str(n)]['min_event_distance']] for n in range(1,16)],[82,105,80,80,160])
report.p('Les valeurs mesurent la grille normale, sans raccourcis. Une impasse de deux pas est signalée comme telle dans le guide. L’algorithme donne priorité aux branches longues disponibles, sous les contraintes de dégagement et de séparation. Les coordonnées complètes, profondeur et distances sont aussi fournies dans un CSV de 250 lignes.','small')
report.page('Placement : niveaux 16 à 25 et cas particuliers')
report.table([['Niveau global','Chapitre / niveau','Impasses','Recoins','Écart min. (pas)']]+[[n,f'{(n-1)//5+1} / {(n-1)%5+1}',AUDIT[str(n)]['dead_ends'],10-AUDIT[str(n)]['dead_ends'],AUDIT[str(n)]['min_event_distance']] for n in range(16,26)],[82,105,80,80,160])
report.p('Niveaux 18 et 22 : les anneaux offrent déjà des retours directs et ne présentent aucun fond d’impasse. Les dix récompenses de chacun sont réparties dans des sections retirées, contre les limites des couloirs, à distance des postes. Le guide les nomme « recoins », sans inventer une branche terminale.')
report.p('Niveau 1 : les sas à sens unique restent irréversibles. Les guides demandent de visiter les souvenirs du secteur nord avant de les franchir. Le dossier donne ensuite la possibilité de rejouer le niveau terminé ; aucun souvenir manqué n’empêche de continuer la campagne.')
report.p('Niveaux à accès variables : les collectibles ne commandent aucune porte. Ils restent des cases traversables après ouverture normale du secteur. Les validators de progression continuent de vérifier les accès pilotés par les postes et les tests physiques des 25 niveaux restent inchangés. Les 250 ramassages ont en plus été testés avec le routage réel depuis une case adjacente praticable.')
report.p('Les dix récompenses sont ajoutées séparément aux données d’événements. Les grilles, coordonnées des énigmes, raccourcis et objets requis de la version 0.20 sont inchangés octet pour octet dans le dépôt. Un manifeste conserve une empreinte de chaque carte : une modification ultérieure oblige à revalider le placement.')
report.page('Vérifications et portée des résultats')
report.table([['Contrôle','Résultat'],['Placement indépendant','250 identifiants uniques ; sol accessible ; distances et branches vérifiées'],['Ramassage physique','250 / 250 via demande de déplacement, marche et interaction'],['État des énigmes','Ramasser ne modifie ni le sac ni les validations'],['Sauvegarde','Collection complète, reprise, ancienne sauvegarde et nouvelle aventure testées'],['Rejouer','Collection conservée ; objets déjà trouvés masqués ; énigmes réinitialisées'],['Interface','Dossier FR/EN ; 390×844, 844×390 et 1280×800 ; débordements contrôlés'],['Folamour','Rotation, respiration, désactivation et archive des remarques testées'],['Régressions','23 tests Godot existants réussis ; nouveau test ajouté au workflow'],['Publication','Compilation, export web et suite GitHub Actions réussis']],[147,360])
report.p('Limite visuelle : le navigateur de contrôle disponible n’expose pas WebGL 2. Le rendu 3D en navigateur et la fluidité sur un téléphone physique ne sont donc pas validés par cette session. Les vérifications d’interface portent sur les dimensions calculées par Godot ; les cartes et les PDF ont été rendus et relus visuellement. Ces contrôles ne remplacent pas une appréciation humaine du rythme ou du plaisir de collection.')
report.p('Les tests physiques des souvenirs démarrent depuis des cases adjacentes accessibles ; ils vérifient les collisions locales et le ramassage. La possibilité de rejoindre leurs secteurs est contrôlée séparément sur le graphe, avec les régressions de progression et d’accès variables. Cette distinction évite de présenter les 250 ramassages comme un parcours intégral unique de collection.')
report.p('Références primaires consultées','head')
report.p('[1] Leah Miller, GDC 2019, Rewarding Exploration with Collectables and Gatherables. Diapositives : objets finis (4), cohérence (11), écueils (18), exploration (20–23), lisibilité (34). https://media.gdcvault.com/gdc2019/presentations/Miller_Leah_Rewarding_Exploration_With.pdf','small')
report.p('[2] Game Accessibility Guidelines, Avoid flickering images and repetitive patterns. https://gameaccessibilityguidelines.com/avoid-flickering-images-and-repetitive-patterns/','small')
report.p('[3] Godot 4.5 Documentation, Optimizing 3D performance. https://docs.godotengine.org/en/4.5/tutorials/performance/optimizing_3d_performance.html','small')
report.save()
with zipfile.ZipFile(OUT/'Lab-Mazing-v0.21-Guides-complets.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(OUT.rglob('*')):
  if p.is_file() and p.suffix!='.zip':z.write(p,p.relative_to(OUT))
print('All guides and research report complete',flush=True)
