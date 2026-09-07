"""Chapter 2, assignment 1: exact current map and a complete French solution guide."""
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
prefix='Chapitre-2-Mission-1-v0.12';font=str(R/'game/assets/Interface.ttf');pdfmetrics.registerFont(TTFont('Interface',font))
# Reuse the established map renderer, without executing the campaign exporter.
source=ast.parse((R/'scripts/document_campaign.py').read_text());nodes=[]
for node in source.body:
 if isinstance(node,ast.FunctionDef) and node.name=='make_guide':break
 nodes.append(node)
namespace={'__file__':str(R/'scripts/document_campaign.py')};exec(compile(ast.Module(body=nodes,type_ignores=[]),'campaign-map','exec'),namespace)
namespace['VERSION']='0.12'
m,E,S=[json.loads((D/(name+'6.json')).read_text()) for name in ['maze','events','shortcuts']];by={e['id']:e for e in E}
namespace['make_map'](6,m,E,S)
for ext in ['png','pdf']:(out/f'Niveau-6-v0.12-Map-vue-de-haut.{ext}').rename(out/f'{prefix}-Map-vue-de-haut.{ext}')
styles={k:ParagraphStyle(k,fontName='Interface',fontSize=size,leading=lead,spaceAfter=gap,textColor=colors.HexColor('#204137'),keepWithNext=k in ['title','head']) for k,size,lead,gap in [('title',25,31,20),('head',15,20,10),('body',10.5,16,10),('cell',9,13,0)]}
story=[];md=['# Chapitre 2 - Mission 1 : Les serres expérimentales\n\nVersion 0.12 - SPOILERS\n']
def p(text,style='body'):
 story.append(Paragraph(escape(str(text)).replace('\n','<br/>'),styles[style]));md.append(('## ' if style=='title' else '### ' if style=='head' else '')+str(text)+'\n')
def page(title):
 if story:story.append(PageBreak())
 p(title,'title')
def table(rows,widths):
 t=Table([[Paragraph(escape(str(v)).replace('\n','<br/>'),styles['cell']) for v in row] for row in rows],colWidths=widths,repeatRows=1)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#d9e9dc')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#cad7cf'))]));story.extend([t,Spacer(1,12)])
 md.append('\n'.join([' | '.join(map(str,rows[0])),' | '.join(['---']*len(rows[0]))]+[' | '.join(map(str,row)) for row in rows[1:]])+'\n')
page('Le stage commence\nLes serres expérimentales')
p('Mission : préparer le café de Folamour. Une boucle centrale dessert l’irrigation à l’ouest, les cultures à l’est, le mélangeur au nord et le vestiaire au sud. Le chapitre 2 contient actuellement cette première mission ; les suivantes sont encore indisponibles.')
p('Accès','head');p('Depuis le menu : Choisir un chapitre → Commencer le chapitre 2. Depuis la fin du chapitre 1 : Accepter le stage — Chapitre 2 conserve les bilans précédents. La sélection de test l’identifie comme le niveau 6. Une nouvelle partie remplace la sauvegarde courante après confirmation.')
p('Parcours conseillé','head')
for text in ['1. Lire 100 et 102 ; récupérer la graine 101.','2. À l’ouest, lire 201 et 204, récupérer le raccord 202 puis résoudre l’irrigation 203.','3. Revenir au bac 104 et faire pousser la liane : la passerelle 106 s’ouvre vers l’est.','4. Récolter 301, 302, 303 et 304. Revenir par la passerelle.','5. Au nord, lire 206 puis préparer le mélange en 205.','6. Au sud, récupérer la tasse 103. Revenir servir le café en 105.']:p(text)
p('La tasse peut être récupérée plus tôt. Les essais n’ont pas de minuterie. Aucun raccourci n’est obligatoire. Trois secrets : 207 à l’ouest, 305 à l’est et 107 au sud.')
page('01 / Irrigation\nRelier les coudes')
p('Raccord 202 : (11, 31). Panneau 203 : (5, 15). Plan 201 : (1, 1). Annotation 204 : (9, 3).')
p('Les quatre pièces sont des coudes, disposés en carré. L’entrée arrive à l’ouest de A ; la sortie se trouve à l’est de B. Une pression tourne la pièce dans le sens horaire. Les ouvertures affichées doivent correspondre à celles des voisines.')
table([['Haut gauche','Haut droite'],['A : OUEST + SUD','B : SUD + EST'],['Bas gauche','Bas droite'],['C : NORD + EST','D : NORD + OUEST']],[250,250])
p('Chemin de l’eau : entrée → A → C → D → B → sortie. Les quatre pièces sont utilisées. Aucun raccord ne fuit vers l’extérieur.')
p('Depuis une réinitialisation','head');p('A deux pressions ; B une pression ; C aucune ; D trois pressions. Choisir « Valider l’essai ». Une réserve d’eau est ajoutée au sac pour le bac 104. Le raccord reste installé.')
p('Réinitialiser remet seulement les orientations à zéro. On peut tester une disposition incorrecte sans perdre le raccord ni rendre le puzzle insoluble.')
page('02 / La liane-pont\nCréer un passage')
p('Graine 101 : (13, 11). Fiche 102 : (13, 23). Bac 104 : (21, 17). Passerelle 106 : (23, 17).')
p('Installer la graine et la réserve d’eau issue de 203. Les trois réglages sont indépendants ; ils peuvent être modifiés dans n’importe quel ordre.')
table([['Réglage','Choix attendu','Depuis une réinitialisation'],['Lumière','DOUCE','1 pression'],['Arrosage','2 doses','2 pressions'],['Treillis','DÉPLOYÉ','1 pression']],[130,150,220])
p('Valider l’essai. La plante grandit sur son support et ouvre définitivement le passage vers les cultures de l’est. Le pont reste praticable dans les deux sens, à pied, au clic et au toucher.')
p('L’ombre ne permet pas la croissance, et une lumière forte fait se recroqueviller la plante. Aucun essai ne détruit la graine ; l’eau est recyclée. Une fois la croissance validée, le passage ne se referme pas.')
p('Folamour commente','head');p(by['g_growth']['success'])
page('03 / Le mélange\nAdditionner les propriétés')
p('Récolter les quatre ingrédients à l’est, puis les installer dans le mélangeur 205, au nord en (17, 3). La commande 206 est en (23, 7).')
table([['Récolte','Coordonnées','Arôme','Amertume','Stabilité','Mesures'],['301 - Grain','(25, 1)',2,2,0,1],['302 - Pétale','(33, 9)',1,0,1,1],['303 - Mousse','(25, 31)',0,0,1,1],['304 - Sel','(33, 33)',0,1,2,0]],[110,100,65,75,75,75])
p('Solution : Grain 1, Pétale 1, Mousse 1, Sel 0. Total : trois mesures, arôme 3, amertume 2, stabilité 2. Valider l’essai pour obtenir la préparation aromatique.')
p('Pourquoi cela fonctionne','head');p('Le grain apporte déjà toute l’amertume demandée. Un pétale complète l’arôme et ajoute un point de stabilité ; la mousse ajoute le dernier point sans modifier les deux autres propriétés. Le sel doit être récolté et installé, mais aucune mesure n’entre dans la recette.')
p('Chaque quantité passe de 0 à 1 puis 2, puis revient à 0. Les essais et la réinitialisation ne consomment pas les récoltes installées. Les propriétés et le nombre total de mesures sont visibles en permanence.')
p('Servir','head');p('La tasse 103 se trouve dans le vestiaire sud en (13, 33). Avec la tasse et la préparation, rejoindre la cafetière 105 en (17, 13), installer les deux objets et terminer la mission.')
page('Tous les repères\nCarte exacte')
table([['Référence','Objet ou installation','(x, y)']]+[[e['ref'],e['title'],str(tuple(e['cell']))] for e in E],[70,325,105])
p('Coordonnées à partir de zéro, nord en haut. Départ : (17, 23). Le plan fourni montre la grille exacte du jeu. Les trois archives secrètes sont facultatives.')
page('Les six raccourcis\nRevenir plus vite')
p('Un raccourci apparaît uniquement après un passage physique sur les deux cases indiquées, de part et d’autre du mur, dans n’importe quel ordre. Le brouillard dissipé ou la simple consultation de la carte ne suffisent pas. Le passage reste ensuite ouvert dans les deux sens.')
table([['ID','Mur','Deux cases à visiter','Gain minimal']]+[[s['id'],str(tuple(s['cell'])),str(tuple(s['sides'][0]))+' / '+str(tuple(s['sides'][1])),str(s['minimum_saved_steps'])+' pas'] for s in S],[40,85,275,100])
audit=json.loads((R/'game/tests/audit_level6.json').read_text())
p(f"Parcours de référence : {audit['without_shortcuts']['steps']} pas sans raccourcis, {audit['with_shortcuts']['steps']} avec leurs ouvertures progressives, soit {audit['without_shortcuts']['steps']-audit['with_shortcuts']['steps']} pas évités.")
p('Cette comparaison utilise le même ordre d’objectifs et une carte connue ; elle ne prédit pas la durée ou le nombre de pas d’une première partie. Chaque raccourci évite encore au moins 12 pas entre ses deux côtés lorsque les cinq autres sont ouverts. Aucun ne contourne la passerelle végétale fermée.')
page('Indices progressifs\nLes trois paliers')
aid=json.loads((D/'guidance.json').read_text())
for id in ['g_irrigation','g_growth','g_blend']:
 p(by[id]['ref']+' - '+by[id]['title'],'head')
 for i,pair in enumerate(aid['hints'][id]):p(['Piste : ','Méthode : ','Solution : '][i]+pair[0])
page('Fin de mission\nSauvegarde et suite')
p('Folamour et le café','head');p('« Excellent. Vous avez restauré un écosystème pour une tasse de café. Voilà exactement le sens des priorités que nous recherchons. Demain, nous verrons si vous savez faire des photocopies. »')
p('Ce niveau termine la première mission du chapitre 2, pas le chapitre entier. Le menu annonce que la suite du stage arrivera plus tard.')
p('Ce qui est conservé','head');p('Les bilans du chapitre 1 restent conservés lorsqu’on poursuit directement après le niveau 5. Le niveau 6 sauvegarde ses orientations de tuyaux, réglages de croissance, quantités du mélange, pièces installées, récoltes, journal, indices, raccourcis et résultat final. Le chronomètre exclut les menus et la lecture. La reprise d’une mission terminée réaffiche son bilan.')
p('Confort de jeu','head');p('Objectif actuel dans le jeu, le journal et la pause. Trois paliers d’indices facultatifs. Déplacement au clic et au toucher. Les panneaux restent consultables en français et en anglais, en portrait et paysage. La musique feutrée du laboratoire et les volumes séparés sont conservés dans les réglages audio.')
p('Vérifications','head');p('Parcours physique complet dans Godot, passerelle fermée puis franchissable, collecte des quatre ingrédients, trois solutions uniques, reprise de chaque mécanisme en cours, conservation des objets installés après réinitialisation, fin de mission sauvegardée. Deux ordres de visite du vestiaire ont été vérifiés sur le graphe du labyrinthe.')
def footer(c,d):
 c.setFont('Interface',8);c.setFillColor(colors.HexColor('#647e70'));c.drawString(44,25,'FOLAMOUR / V0.12 / CHAPITRE 2 - MISSION 1 / SPOILERS');c.drawRightString(A4[0]-44,25,str(d.page))
SimpleDocTemplate(str(out/f'{prefix}-Cheatsheet-solutions.pdf'),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=42,bottomMargin=45).build(story,onFirstPage=footer,onLaterPages=footer)
(out/f'{prefix}-Cheatsheet-solutions.md').write_text('\n'.join(md))
summary='''# Lab-Mazing - v0.12 : Le stage commence

Le chapitre 2 propose sa première mission complète : les serres expérimentales. Folamour demande un café, dont la préparation nécessite de rétablir l’irrigation, de faire pousser une liane-pont, de récolter quatre ingrédients et de composer un mélange selon leurs propriétés.

- Labyrinthe autour d’une serre centrale, quatre branches, 20 repères et trois secrets.
- Trois nouvelles manipulations réversibles : tuyaux orientables, environnement de croissance et mélange de propriétés.
- Six raccourcis révélés après visite physique des deux côtés. Parcours de référence : 741 → 653 pas (88 évités).
- Objectifs et indices progressifs en français/anglais, compatibles avec les commandes mobiles.
- Accès au chapitre 2 depuis le menu ou directement après le stage proposé à la fin du chapitre 1.
- Sauvegardes et bilans conservés ; la première mission du chapitre 2 est disponible, les suivantes viendront plus tard.

Ce dossier contient la carte PNG/PDF, le cheatsheet PDF/Markdown, ce résumé et une archive complète. Les documents des versions précédentes restent archivés dans leurs dossiers.

Jeu : https://jfeffe.github.io/lab-mazing/
'''
(out/'Resume-v0.12.md').write_text(summary)
with zipfile.ZipFile(out/'Lab-Mazing-v0.12-Chapitre-2-Mission-1.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(out.iterdir()):
  if f.suffix!='.zip':z.write(f,f.name)
print('Six documents generated:',out)
