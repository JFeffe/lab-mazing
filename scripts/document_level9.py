"""Chapter 2, assignment 4: exact current map and a complete French solution guide."""
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
prefix='Chapitre-2-Mission-4-v0.15';font=str(R/'game/assets/Interface.ttf');pdfmetrics.registerFont(TTFont('Interface',font))
# Reuse the established map renderer, without executing the campaign exporter.
source=ast.parse((R/'scripts/document_campaign.py').read_text());nodes=[]
for node in source.body:
 if isinstance(node,ast.FunctionDef) and node.name=='make_guide':break
 nodes.append(node)
namespace={'__file__':str(R/'scripts/document_campaign.py')};exec(compile(ast.Module(body=nodes,type_ignores=[]),'campaign-map','exec'),namespace)
namespace['VERSION']='0.15'
m,E,S=[json.loads((D/(name+'9.json')).read_text()) for name in ['maze','events','shortcuts']];by={e['id']:e for e in E}
namespace['make_map'](9,m,E,S)
for ext in ['png','pdf']:(out/f'Niveau-9-v0.15-Map-vue-de-haut.{ext}').rename(out/f'{prefix}-Map-vue-de-haut.{ext}')
styles={k:ParagraphStyle(k,fontName='Interface',fontSize=size,leading=lead,spaceAfter=gap,textColor=colors.HexColor('#204137'),keepWithNext=k in ['title','head']) for k,size,lead,gap in [('title',25,31,20),('head',15,20,10),('body',10.5,16,10),('cell',9,13,0)]}
story=[];md=['# Chapitre 2 - Mission 4 : La salle de réunion\n\nVersion 0.15 - SPOILERS\n']
def p(text,style='body'):
 story.append(Paragraph(escape(str(text)).replace('\n','<br/>'),styles[style]));md.append(('## ' if style=='title' else '### ' if style=='head' else '')+str(text)+'\n')
def page(title):
 if story:story.append(PageBreak())
 p(title,'title')
def table(rows,widths):
 t=Table([[Paragraph(escape(str(v)).replace('\n','<br/>'),styles['cell']) for v in row] for row in rows],colWidths=widths,repeatRows=1)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#d9e9dc')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#cad7cf'))]));story.extend([t,Spacer(1,12)])
 md.append('\n'.join([' | '.join(map(str,rows[0])),' | '.join(['---']*len(rows[0]))]+[' | '.join(map(str,row)) for row in rows[1:]])+'\n')
page('La salle de réunion\nChapitre 2 / Niveau 4')
p('SPOILERS — Version 0.15. Folamour vous charge de préparer son comité scientifique. Attribuez les places, organisez la séance, puis remettez la conférence en service. Les essais sont réversibles et il n’y a aucun compte à rebours.')
p('Accès','head');p('Menu → Choisir un chapitre → Chapitre 2 · Niveau 4 — La salle de réunion. Après le courrier : « Passer à la salle de réunion » conserve les bilans précédents. Numéro interne du niveau : 9.')
p('Une nouvelle disposition','head');p('Départ (17, 23), au sud de la grande salle centrale fermée. Un couloir périphérique relie les bureaux ouest, nord et sud. Les bureaux est sont verrouillés par 101. La salle centrale possède trois accès : 102 à l’ouest, 103 au nord, 104 au sud.')
p('Parcours conseillé','head')
for text in ['1. Lire 100. À l’ouest, prendre les invitations 201 et croiser les demandes 202 avec la décision officielle 204.','2. Réussir le plan de table 203 : la porte 101 ouvre les bureaux est.','3. À l’est, récupérer le dossier 301, lire 302 et 304, puis valider le planning 303. Les trois accès de la salle s’ouvrent.','4. Prendre les câbles 401 au sud et lire le schéma 402 au nord. Ces deux détours peuvent aussi être faits dès le début.','5. Dans la salle, brancher le système 403, tester les deux trajets et valider.','6. Rejoindre le pupitre 105 et choisir « Ouvrir la réunion ».']:p(text)
p('Trois archives facultatives : 205 à l’ouest, 305 à l’est, 404 au nord. Six raccourcis réduisent les retours. Déplacement +30 % et absence de bruit de pas conservés.')
page('01 / Le plan de table\nSix invités, six places')
p('Invitations 201 : (1, 1). Demandes 202 : (9, 1). Plan de table 203 : (5, 17). Décision officielle 204 : (1, 33). Installer les invitations au pupitre avant les essais.')
p('La porte est en bas. Les places tournent dans le sens horaire : 1 en haut, 2 et 3 à droite, 4 en bas, 5 et 6 à gauche. Chaque bouton avance l’invité d’une place ; après 6, il revient à 1. Le schéma affiche les occupations.')
table([['Invité','Place','Pressions après réinitialisation'],['Aster','1','0'],['Boréal','4','3'],['Cobalt','6','5'],['Delta','2','1'],['Écho','5','4'],['Fermi','3','2']],[130,70,300])
p('Raisonnement','head');p('Aster fait face à la porte : 1. La décision officielle nomme Boréal président : 4, malgré la revendication de Cobalt. Delta suit Aster dans le sens horaire : 2. Écho lui fait face : 5. Fermi doit être voisin de Boréal sans être voisin d’Écho : 3. Il reste 6 pour Cobalt, qui n’est pas voisin de Delta.')
p('Choisir « Valider l’essai ». Le jeu vérifie toutes les contraintes et l’unicité des places ; la porte 101 en (24, 17) s’ouvre. Un placement incorrect laisse les invitations installées. Réinitialiser remet tous les invités en place 1.')
page('02 / Le planning\nUne heure sans pause')
p('Dossier 301 : (25, 1). Contraintes 302 : (33, 1). Planning 303 : (29, 17). Note 304 : (33, 33). Installer le dossier au planning.')
p('Quatre interventions occupent six créneaux de dix minutes, de 09:00 à 10:00. Les boutons changent les heures de début ; les durées restent fixes. Le tableau indique les chevauchements et un message signale une intervention qui dépasse la fin de séance.')
table([['Intervention','Début → fin','Durée','Pressions depuis 09:00'],['Ouverture','09:00 → 09:10','10 min','0'],['Rapport','09:10 → 09:30','20 min','1'],['Démonstration','09:30 → 09:50','20 min','3'],['Vote','09:50 → 10:00','10 min','5']],[110,140,70,180])
p('Attention à l’ordre des boutons : Ouverture, Démonstration, Rapport, Vote. Les réglages sont donc 09:00, 09:30, 09:10, 09:50, de haut en bas.')
p('Raisonnement','head');p('L’ouverture est imposée au début, le vote à la fin. Il reste quarante minutes, exactement les deux interventions de vingt minutes. Le rapport doit se terminer avant la démonstration. Cela impose leur ordre et leurs heures.')
p('Valider ouvre simultanément 102 (12, 17), 103 (17, 12) et 104 (17, 22). Les trois portes restent ouvertes dans les deux sens pour éviter un long détour autour de la salle.')
page('03 / La conférence\nImage et son séparés')
p('Valise 401 : (13, 33), bureaux sud. Schéma 402 : (13, 1), bureaux nord. Système 403 : (17, 17), au centre. Installer les câbles ; le placement et le planning doivent être validés.')
p('Le schéma impose une copie de l’image avant sa diffusion : Caméra → Archives vidéo → Projecteur → Écrans. Le micro rejoint directement l’amplificateur. Une seule liaison par entrée ; aucune boucle.')
table([['Entrée','Destination'],['A','Projecteur'],['B','Archives vidéo'],['C','Écrans'],['D','Amplificateur']],[100,400])
table([['Sortie / bouton','Entrée correcte','Pressions depuis A'],['Caméra','B','1'],['Micro','D','3'],['Archives vidéo','A','0'],['Projecteur','C','2']],[200,130,170])
p('Choisir « Tester la conférence » : les deux trajets complets apparaissent. Choisir ensuite « Valider l’essai ». Changer un branchement annule le résultat du test ; il faut tester à nouveau avant de valider.')
p('Les mauvais branchements peuvent produire une boucle ou envoyer l’image vers une mauvaise sortie. Le test décrit le trajet obtenu sans perdre les câbles. Après validation, rejoindre 105 en (21, 21), puis « Ouvrir la réunion ».')
page('Tous les repères\nCarte exacte')
table([['Référence','Objet ou installation','(x, y)']]+[[e['ref'],e['title'],str(tuple(e['cell']))] for e in E],[65,330,105])
p('Coordonnées depuis zéro, nord en haut. Départ (17, 23). Les cartes PNG et PDF représentent la grille exacte du jeu, portes et raccourcis compris. Les archives 205, 305 et 404 sont facultatives.')
page('Les six raccourcis\nÉcourter les retours')
p('Un passage apparaît après une visite physique des deux cases indiquées de part et d’autre du mur, dans n’importe quel ordre. Une case seulement révélée sur la carte ne compte pas. Le passage reste ouvert dans les deux sens et son état est sauvegardé.')
table([['ID','Mur','Deux cases à visiter','Gain minimal']]+[[s['id'],str(tuple(s['cell'])),str(tuple(s['sides'][0]))+' / '+str(tuple(s['sides'][1])),str(s['minimum_saved_steps'])+' pas'] for s in S],[40,85,275,100])
audit=json.loads((R/'game/tests/audit_level9.json').read_text());base=audit['without_shortcuts']['steps'];short=audit['with_shortcuts']['steps']
p(f'Parcours de référence : {base} pas sans raccourcis ; {short} avec leur ouverture progressive. Gain : {base-short} pas, soit {(base-short)/base*100:.1f} %.')
p('Ce parcours visite les trois archives et suit le même ordre d’objectifs, avec la carte connue. Il sert à comparer les retours, pas à prédire la durée d’une première partie. Les six passages sont empruntés sur ce parcours.')
p('Chaque passage évite encore au moins 12 pas lorsque les cinq autres sont ouverts. Aucun ne contourne les quatre portes verrouillées. Les trois accès permanents de la salle, ouverts par le planning, facilitent également les déplacements entre les ailes.')
page('Indices progressifs\nLes trois paliers')
aid=json.loads((D/'guidance.json').read_text())
for id in ['r_seating','r_schedule','r_conference']:
 p(by[id]['ref']+' — '+by[id]['title'],'head')
 for i,pair in enumerate(aid['hints'][id]):p(['Piste : ','Méthode : ','Solution : '][i]+pair[0])
p('Les indices sont facultatifs et sans pénalité. Ils ne modifient pas les places, le planning ou les branchements. Les commandes, objectifs, notes et indices sont disponibles en français et en anglais.')
page('Fin de mission\nUn comité très indépendant')
p('Les six écrans montrent six versions artificielles de Folamour. Aster réclame une pause, Boréal ouvre la séance, Cobalt conteste sa présidence. Les collègues se disputent sur tout, sauf sur le maintien de votre stage non rémunéré : décision unanime.')
p('« Une réunion productive : nous avons confirmé une décision prise avant votre arrivée. Vous commencez à comprendre le fonctionnement du laboratoire. » — Folamour')
p('Un dossier apparaît sur les écrans : PROJET MIROIR — UNIFICATION. Folamour coupe la transmission. Cette révélation prépare le dernier niveau du chapitre 2, qui n’est pas encore disponible.')
p('Sauvegardes et menu','head');p('Le chapitre 2 contient quatre missions : serres, photocopies, courrier et réunion. La sélection distingue les chapitres et leurs numéros locaux. Le passage direct depuis le courrier conserve les bilans précédents ; les accès de nouvelle partie affichent la confirmation habituelle.')
p('Places, horaires, branchements et résultat du dernier test sont sauvegardés, ainsi que le matériel installé, les indices, archives et raccourcis. Une réinitialisation conserve les objets installés. Reprendre une mission terminée réaffiche la conclusion et son bilan.')
p('Confort et vérification','head');p('Vitesse +30 %, netteté mobile et corrections audio conservées. Aucun bruit de pas. Le décor utilise six petits portraits sans rendu vidéo supplémentaire. Les tests couvrent parcours physique, barrières, solutions uniques, sauvegardes partielles et panneaux FR/EN en portrait/paysage. Ils ne remplacent pas un essai sur chaque modèle de téléphone.')
def footer(c,d):
 c.setFont('Interface',8);c.setFillColor(colors.HexColor('#647e70'));c.drawString(44,25,'FOLAMOUR / V0.15 / CHAPITRE 2 - NIVEAU 4 / SPOILERS');c.drawRightString(A4[0]-44,25,str(d.page))
SimpleDocTemplate(str(out/f'{prefix}-Cheatsheet-solutions.pdf'),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=42,bottomMargin=45).build(story,onFirstPage=footer,onLaterPages=footer)
(out/f'{prefix}-Cheatsheet-solutions.md').write_text('\n'.join(md))
(out/'Resume-v0.15.md').write_text(f'''# Lab-Mazing v0.15 — La salle de réunion

Chapitre 2, niveau 4 (numéro interne 9).

- Grande salle centrale et quatre ailes de bureaux ; 20 repères, quatre portes et trois archives secrètes.
- Trois énigmes : plan de table à six invités, planning de six créneaux, branchements image/son.
- Six raccourcis : {base} → {short} pas sur le parcours de référence, après visite physique des deux côtés.
- Introduction de Folamour, révélation du comité artificiel et annonce du projet MIROIR.
- Accès direct au menu ou transition depuis le courrier, bilans précédents conservés.
- Objectifs et indices FR/EN, contrôles réversibles, reprise des essais partiels.
- Vitesse +30 %, netteté mobile, musique et corrections audio conservées. Aucun bruit de pas.

Accès : Choisir un chapitre → Chapitre 2 · Niveau 4 — La salle de réunion.

Ce dossier contient la carte PNG/PDF, le cheatsheet PDF/Markdown, ce résumé et une archive ZIP des cinq documents. Les cartes et solutions des énigmes précédentes restent valides ; la fin du courrier permet désormais d’enchaîner sur la réunion.

Jeu : https://jfeffe.github.io/lab-mazing/
''')
with zipfile.ZipFile(out/'Lab-Mazing-v0.15-Chapitre-2-Mission-4.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(out.iterdir()):
  if f.suffix!='.zip':z.write(f,f.name)
print('Six documents generated:',out)
