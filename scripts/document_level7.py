"""Chapter 2, assignment 2: exact current map and a complete French solution guide."""
from pathlib import Path
import ast,json,sys,zipfile
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Table,TableStyle,Spacer,PageBreak,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[1];D=R/'game/data';out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
prefix='Chapitre-2-Mission-2-v0.13';font=str(R/'game/assets/Interface.ttf');pdfmetrics.registerFont(TTFont('Interface',font))
# Reuse the established map renderer, without executing the campaign exporter.
source=ast.parse((R/'scripts/document_campaign.py').read_text());nodes=[]
for node in source.body:
 if isinstance(node,ast.FunctionDef) and node.name=='make_guide':break
 nodes.append(node)
namespace={'__file__':str(R/'scripts/document_campaign.py')};exec(compile(ast.Module(body=nodes,type_ignores=[]),'campaign-map','exec'),namespace)
namespace['VERSION']='0.13'
m,E,S=[json.loads((D/(name+'7.json')).read_text()) for name in ['maze','events','shortcuts']];by={e['id']:e for e in E}
namespace['make_map'](7,m,E,S)
for ext in ['png','pdf']:(out/f'Niveau-7-v0.13-Map-vue-de-haut.{ext}').rename(out/f'{prefix}-Map-vue-de-haut.{ext}')
styles={k:ParagraphStyle(k,fontName='Interface',fontSize=size,leading=lead,spaceAfter=gap,textColor=colors.HexColor('#204137'),keepWithNext=k in ['title','head']) for k,size,lead,gap in [('title',25,31,20),('head',15,20,10),('body',10.5,16,10),('cell',9,13,0)]}
story=[];md=['# Chapitre 2 - Mission 2 : Le service des photocopies\n\nVersion 0.13 - SPOILERS\n']
def p(text,style='body'):
 story.append(Paragraph(escape(str(text)).replace('\n','<br/>'),styles[style]));md.append(('## ' if style=='title' else '### ' if style=='head' else '')+str(text)+'\n')
def page(title):
 if story:story.append(PageBreak())
 p(title,'title')
def table(rows,widths):
 t=Table([[Paragraph(escape(str(v)).replace('\n','<br/>'),styles['cell']) for v in row] for row in rows],colWidths=widths,repeatRows=1)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#d9e9dc')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#cad7cf'))]));story.extend([t,Spacer(1,12)])
 md.append('\n'.join([' | '.join(map(str,rows[0])),' | '.join(['---']*len(rows[0]))]+[' | '.join(map(str,row)) for row in rows[1:]])+'\n')
page('Le service des photocopies\nChapitre 2 / Mission 2')
p('SPOILERS — Version 0.13. Mission : livrer une copie conforme à Folamour. Trois énigmes réversibles : superposer des calques, classer des dossiers et transformer une image. Aucun compte à rebours.')
p('Accès','head');p('Après le café du niveau 6 : « Passer aux photocopies ». Les bilans précédents sont conservés. Pour un accès direct : menu → Sélection de niveau / test → Niveau 7. Une nouvelle partie remplace la sauvegarde courante après confirmation.')
p('Disposition','head');p('Accueil central, préparation au nord-ouest, archives au nord-est et grande aile des copies au sud. Départ (17, 19). La table 203 ouvre la porte 102 ; le classement 303 ouvre la porte 103. Les couloirs restent praticables dans les deux sens.')
p('Parcours conseillé','head')
for text in ['1. Lire 100 à l’accueil. À l’ouest, récupérer 201 ; lire 202 et 204.','2. Résoudre les calques en 203 : les archives du nord-est s’ouvrent.','3. Aux archives, récupérer 301. Lire la directive VALIDÉE 302 et identifier la note ANNULÉE 304. Classer les dossiers en 303.','4. Dans l’aile sud, récupérer papier 401 et toner 402 ; lire 404.','5. Installer le matériel en 403, transformer l’image et valider.','6. Revenir à l’accueil et livrer la copie au bac 101.']:p(text)
p('Déplacement accéléré de 30 % dans tous les niveaux : 7 → 9,1 unités/s, au clavier et lors des trajets au clic ou au toucher. Cette augmentation concerne la vitesse ; elle ne change pas les distances ni le nombre de cases.')
page('01 / Les transparents\nComposer une seule image')
p('Pochette 201 : (1, 1). Notice 202 : (15, 1). Table 203 : (9, 9). Conseil 204 : (1, 13). Installer la pochette avant de manipuler.')
p('Les trois calques sont indépendants. Une case est noire dès qu’au moins un calque la marque. Deux marques superposées restent noires. Le modèle et le résultat sont affichés au-dessus des commandes ; les trois petits tableaux montrent les calques orientés.')
table([['Calque','Orientation finale','Pressions après réinitialisation'],['A','90°','1'],['B','270°','3'],['C','180°','2']],[100,140,260])
p('Choisir « Valider l’essai ». La porte des archives 102, en (25, 15), s’ouvre définitivement. Les calques restent installés.')
p('Modèle noir / vide','head')
def pattern(values):
 rows=[]
 for y in range(3):rows.append(['NOIR' if values[y*3+x] else 'vide' for x in range(3)])
 table(rows,[85,85,85])
pattern(by['p_overlay']['target'])
p('Méthode : éliminer les orientations qui noircissent une case blanche du modèle, puis couvrir les marques restantes. Les 64 combinaisons d’orientations ont été vérifiées : une seule correspond exactement au modèle.')
page('02 / Les dossiers\nDistinguer les deux directives')
p('Dossiers 301 : (33, 1). Directive validée 302 : (19, 1). Classeur 303 : (29, 11). Directive annulée 304 : (33, 13).')
p('La version A est explicitement ANNULÉE. Seule la version B doit être appliquée. Les casiers sont numérotés de gauche à droite. Il faut exactement un dossier dans chacun.')
p('Déduction','head');p('Zéro est à une extrémité, mais pas en 4 : il est donc en 1. Miroir est immédiatement à droite de Serre. Puisque Lune doit être encore plus à droite, Serre et Miroir occupent 2 et 3 ; Lune prend 4.')
table([['Casier 1','Casier 2','Casier 3','Casier 4'],['Zéro','Serre','Miroir','Lune']],[125,125,125,125])
table([['Commande affichée','Valeur finale','Pressions après réinitialisation'],['Lune','4','3'],['Miroir','3','2'],['Serre','2','1'],['Zéro','1','0']],[120,110,270])
p('Chaque dossier commence dans le casier 1 ; les doublons sont permis pendant la recherche, jamais à la validation. Après « Valider l’essai », la porte 103 en (17, 20) s’ouvre et l’original validé est ajouté au sac.')
page('03 / Le photocopieur\nRotation et réflexion')
p('Papier 401 : (1, 21). Toner 402 : (33, 33). Machine 403 : (17, 29). Notice 404 : (33, 21). Installer papier, toner et original obtenu en 303.')
p('Depuis une réinitialisation','head');p('1. Appuyer une fois sur « Tourner de 90° ».\n2. Appuyer une fois sur « Miroir gauche-droite ».\n3. Choisir « Valider l’essai ».')
p('Original','head');pattern(by['p_copier']['initial'])
p('Modèle attendu','head');pattern(by['p_copier']['target'])
p('Le miroir échange la gauche et la droite de l’image actuelle. Il ne retourne pas le haut et le bas. L’ordre des transformations compte. Les deux actions sont réversibles : quatre rotations ou deux miroirs annulent leur effet. Toute suite produisant le bon résultat est acceptée.')
p('Le motif possède huit orientations ou réflexions distinctes. Le chemin le plus court jusqu’au modèle utilise deux actions. Aucun essai ne gaspille le matériel installé.')
p('Livraison','head');p('La machine donne la copie conforme. Revenir au bac 101 en (21, 19), installer la copie puis choisir « Livrer la copie ». Les deux portes restent ouvertes pour le retour.')
page('Tous les repères\nCarte exacte')
table([['Référence','Objet ou installation','(x, y)']]+[[e['ref'],e['title'],str(tuple(e['cell']))] for e in E],[70,325,105])
p('Coordonnées à partir de zéro, nord en haut. Départ : (17, 19). Trois secrets facultatifs : 205, 305 et 405. Tous peuvent être lus avant la livraison finale.')
page('Les six raccourcis\nDes retours plus courts')
p('Un raccourci apparaît après un passage physique sur les deux cases indiquées, de part et d’autre du mur. L’ordre des visites est libre. La carte dévoilée ne suffit pas. Le passage reste ensuite ouvert dans les deux sens.')
table([['ID','Mur','Deux cases à visiter','Gain minimal']]+[[s['id'],str(tuple(s['cell'])),str(tuple(s['sides'][0]))+' / '+str(tuple(s['sides'][1])),str(s['minimum_saved_steps'])+' pas'] for s in S],[40,85,275,100])
audit=json.loads((R/'game/tests/audit_level7.json').read_text())
p(f"Parcours de référence : {audit['without_shortcuts']['steps']} pas sans raccourcis, {audit['with_shortcuts']['steps']} avec ouvertures progressives, soit 88 pas évités.")
p('Comparaison du même itinéraire sur une carte connue, et non prédiction d’une première partie. Chaque raccourci évite encore au moins 12 pas entre ses côtés lorsque les cinq autres sont ouverts. Aucun ne contourne une porte verrouillée. Ils ne sont jamais obligatoires.')
page('Indices progressifs\nAider sans bloquer')
aid=json.loads((D/'guidance.json').read_text())
for id in ['p_overlay','p_filing','p_copier']:
 p(by[id]['ref']+' — '+by[id]['title'],'head')
 for i,pair in enumerate(aid['hints'][id]):p(['Piste : ','Méthode : ','Solution : '][i]+pair[0])
p('Les indices sont facultatifs et sans pénalité. Leur ouverture ne modifie ni les objets, ni les essais, ni le nombre d’erreurs. Les objectifs, commandes, indices et dialogues existent en français et en anglais.')
page('La livraison\nEt la suite du stage')
p('Folamour examine la copie','head');p('« Félicitations. Une copie parfaitement conforme ! J’avais oublié de préciser : je la voulais recto verso. Mais gardez votre enthousiasme, c’est la seule chose que nous ne fournissons pas. » — Folamour')
p('La mission est bien réussie : la remarque sur le recto verso est une plaisanterie de fin, pas une quatrième énigme. La suite du chapitre 2 reste à venir.')
p('Sauvegarde','head');p('Les calques orientés, les casiers choisis, l’image transformée, les objets installés, les indices, le journal, les raccourcis et le résultat sont conservés. Réinitialiser un essai ne retire pas les objets installés. Le passage direct depuis les serres conserve les bilans précédents.')
p('Confort et vérification','head');p('Les réglages graphiques mobiles et les corrections audio de la version stable sont conservés. Aucun bruit de pas. La musique douce reste réglable. Le parcours physique et les collisions sont vérifiés dans Godot, ainsi que les solutions, les reprises partielles et la livraison. Les panneaux sont vérifiés en français et en anglais, en portrait et paysage. Ces tests automatisés ne remplacent pas une partie sur chaque modèle de téléphone.')
def footer(c,d):
 c.setFont('Interface',8);c.setFillColor(colors.HexColor('#647e70'));c.drawString(44,25,'FOLAMOUR / V0.13 / CHAPITRE 2 - MISSION 2 / SPOILERS');c.drawRightString(A4[0]-44,25,str(d.page))
SimpleDocTemplate(str(out/f'{prefix}-Cheatsheet-solutions.pdf'),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=42,bottomMargin=45).build(story,onFirstPage=footer,onLaterPages=footer)
(out/f'{prefix}-Cheatsheet-solutions.md').write_text('\n'.join(md))
summary="""# Lab-Mazing — v0.13 : Le service des photocopies

- Chapitre 2, mission 2 (niveau 7) : accueil central et trois ailes, 19 repères, trois secrets.
- Trois manipulations : calques superposés, classement logique avec directive annulée, rotation et miroir au photocopieur.
- Six raccourcis utiles : parcours de référence 747 → 659 pas. Déclenchement après visite physique des deux côtés.
- Déplacement +30 % dans tous les niveaux : 7 → 9,1 unités/s.
- Folamour confie la mission puis réclame plaisamment une copie recto verso à la fin.
- Objectifs, indices et textes en français et anglais. Sauvegardes partielles et bilans conservés.
- Réglages de stabilité et netteté mobiles conservés ; aucun bruit de pas.

Accès : terminer le café puis « Passer aux photocopies », ou sélection de test → Niveau 7.
Le chapitre 2 contient maintenant deux missions. Les anciennes cartes et solutions demeurent valides ; leurs dossiers ne sont pas modifiés.

Ce dossier contient le cheatsheet PDF et Markdown, la carte PDF et PNG, ce résumé et une archive ZIP de ces cinq documents.

Jeu : https://jfeffe.github.io/lab-mazing/
"""
(out/'Resume-v0.13.md').write_text(summary)
with zipfile.ZipFile(out/'Lab-Mazing-v0.13-Chapitre-2-Mission-2.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(out.iterdir()):
  if f.suffix!='.zip':z.write(f,f.name)
print('Six documents generated:',out)
