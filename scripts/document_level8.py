"""Chapter 2, assignment 3: exact current map and a complete French solution guide."""
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
prefix='Chapitre-2-Mission-3-v0.14';font=str(R/'game/assets/Interface.ttf');pdfmetrics.registerFont(TTFont('Interface',font))
# Reuse the established map renderer, without executing the campaign exporter.
source=ast.parse((R/'scripts/document_campaign.py').read_text());nodes=[]
for node in source.body:
 if isinstance(node,ast.FunctionDef) and node.name=='make_guide':break
 nodes.append(node)
namespace={'__file__':str(R/'scripts/document_campaign.py')};exec(compile(ast.Module(body=nodes,type_ignores=[]),'campaign-map','exec'),namespace)
namespace['VERSION']='0.14'
m,E,S=[json.loads((D/(name+'8.json')).read_text()) for name in ['maze','events','shortcuts']];by={e['id']:e for e in E}
namespace['make_map'](8,m,E,S)
for ext in ['png','pdf']:(out/f'Niveau-8-v0.14-Map-vue-de-haut.{ext}').rename(out/f'{prefix}-Map-vue-de-haut.{ext}')
styles={k:ParagraphStyle(k,fontName='Interface',fontSize=size,leading=lead,spaceAfter=gap,textColor=colors.HexColor('#204137'),keepWithNext=k in ['title','head']) for k,size,lead,gap in [('title',25,31,20),('head',15,20,10),('body',10.5,16,10),('cell',9,13,0)]}
story=[];md=['# Chapitre 2 - Mission 3 : Le courrier interne\n\nVersion 0.14 - SPOILERS\n']
def p(text,style='body'):
 story.append(Paragraph(escape(str(text)).replace('\n','<br/>'),styles[style]));md.append(('## ' if style=='title' else '### ' if style=='head' else '')+str(text)+'\n')
def page(title):
 if story:story.append(PageBreak())
 p(title,'title')
def table(rows,widths):
 t=Table([[Paragraph(escape(str(v)).replace('\n','<br/>'),styles['cell']) for v in row] for row in rows],colWidths=widths,repeatRows=1)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#d9e9dc')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#cad7cf'))]));story.extend([t,Spacer(1,12)])
 md.append('\n'.join([' | '.join(map(str,rows[0])),' | '.join(['---']*len(rows[0]))]+[' | '.join(map(str,row)) for row in rows[1:]])+'\n')
page('Le courrier interne\nChapitre 2 / Niveau 3')
p('SPOILERS - Version 0.14. Folamour demande une livraison. Retrouvez le colis plus lourd, remettez le tri pneumatique en service et reconstituez l’adresse du destinataire. Aucun compte à rebours ; les essais restent réversibles.')
p('Accès','head');p('Menu → Choisir un chapitre → Chapitre 2 · Niveau 3 - Le courrier interne. La sélection de niveau est également regroupée par chapitre. Après les photocopies : « Passer au courrier interne » conserve les bilans précédents. Numéro interne du niveau : 8.')
p('Le circuit de livraison','head');p('Départ à la réception est, en (31, 19). Le grand couloir fait le tour de deux entrepôts : la balance à l’ouest, le réseau au centre. L’expédition occupe une aile horizontale au sud. Les portes 102 et 103 s’ouvrent successivement et restent ouvertes pour le retour.')
p('Parcours conseillé','head')
for text in ['1. Lire 100. Suivre le circuit vers l’ouest et récupérer les six colis en 201.','2. Lire 202 et 204, comparer les colis puis sélectionner E à la balance 203.','3. Entrer au centre par 102. Récupérer la capsule 301 ; consulter 302 et 304.','4. Régler le réseau 303, lancer la capsule et valider son arrivée à l’expédition.','5. Au sud, récupérer 401 et croiser l’annuaire 402 avec l’avis 404. Adresser le colis en 403.','6. Revenir à la réception est et remettre le colis au guichet 101.']:p(text)
p('Trois secrets facultatifs : 205 à l’ouest, 305 au centre et 405 au sud. La vitesse de déplacement reste augmentée de 30 %, comme en v0.13. Aucun bruit de pas.')
page('01 / La balance\nDeux comparaisons suffisent')
p('Lot 201 : (3, 3). Notice 202 : (11, 3). Balance 203 : (7, 15). Méthode 204 : (3, 25). Installer le lot avant les essais.')
p('Cinq colis ont exactement le même poids ; un seul est plus lourd. Chaque commande passe de RÉSERVE à GAUCHE, puis DROITE, puis RÉSERVE. La balance calcule réellement le poids de chaque plateau. Les pesées sont illimitées.')
table([['Pesée','Plateau gauche','Plateau droit','Résultat'],['1','A + B + C','D + E + F','Droite plus lourde'],['2','D','E','Droite plus lourde']],[60,140,140,160])
p('Conclusion : E est plus lourd. Choisir E avec le bouton « Colis choisi », puis « Valider l’essai ». Le colis E entre dans le sac ; la porte 102 en (25, 13) s’ouvre.')
p('Manipulations exactes','head');p('Après réinitialisation, tous les colis sont en réserve. Pour la première pesée : A, B et C une pression chacun ; D, E et F deux pressions chacun ; « Peser les colis ». Remettre ensuite les six colis en réserve, placer D à gauche et E à droite, puis peser. Choisir E : quatre pressions sur « Colis choisi » depuis A.')
p('Pourquoi la méthode fonctionne','head');p('La première pesée réduit la recherche à trois colis. La deuxième compare deux de ces trois : le plus lourd est la réponse ; s’ils s’équilibrent, le troisième est la réponse. La méthode a été vérifiée pour chacun des six colis possibles. Dans ce niveau, E est toujours le bon.')
p('Modifier le placement efface le résultat affiché jusqu’à la prochaine pesée. Réinitialiser ne retire pas le lot installé et ne fait perdre aucun colis.')
page('02 / Le réseau\nSuivre la capsule')
p('Capsule 301 : (15, 3). Plan 302 : (23, 3). Réseau 303 : (19, 17). Consigne 304 : (15, 25).')
p('Le schéma relie le départ aux aiguillages A, B et C. Chaque aiguillage sélectionne une branche numérotée. Le lancement dessine progressivement le trajet de la capsule. Les sorties RETOUR ramènent automatiquement la capsule au départ.')
table([['Aiguillage','Branche 1','Branche 2','Choix correct'],['A','Retour','Vers B','2'],['B','Vers C','Retour','1'],['C','Retour','Expédition','2']],[80,140,140,140])
p('Depuis une réinitialisation','head');p('A une pression ; B aucune ; C une pression. Choisir « Lancer la capsule ». Le trajet est DÉPART → A → B → C → EXPÉDITION. Choisir ensuite « Valider l’essai ». Le bordereau rejoint le sac et la porte 103 en (17, 28) ouvre l’aile sud.')
p('Changer un aiguillage annule le résultat du dernier essai. Il faut relancer avant de valider. Les mauvaises destinations ne consomment pas la capsule. Les huit configurations ont été vérifiées : une seule atteint l’expédition.')
p('L’animation est un petit dessin 2D dont le rafraîchissement s’arrête à la fin du trajet. Aucun effet lourd n’est ajouté au décor du labyrinthe.')
page('03 / L’adresse\nRecouper trois documents')
p('Fragment 401 : (3, 29). Annuaire 402 : (31, 29). Terminal 403 : (17, 33). Avis 404 : (31, 33). Installer le colis E, le bordereau et le fragment au terminal.')
table([['Source','Information utile'],['401 - Étiquette','F. ; direction scientifique'],['402 - Annuaire','Folamour dirige la science. Faraday travaille à la maintenance ; Foucault à la comptabilité.'],['404 - Avis en vigueur','La direction scientifique a quitté le Nord pour l’Ouest. Bureau immédiatement après le numéro 3.']],[145,355])
p('Solution','head');p('Dr Folamour - aile OUEST - bureau 4. L’annuaire donne son ancienne adresse, Nord / 2 ; l’avis de déménagement la remplace. L’initiale F seule ne suffit pas, puisque les trois noms commencent par F.')
table([['Commande','Valeur finale','Pressions après réinitialisation'],['Destinataire','Dr Folamour','1'],['Aile','OUEST','2'],['Bureau','4','3']],[110,150,240])
p('Valider pour obtenir le colis adressé. Revenir au guichet 101 en (27, 21), à la réception est. Installer le colis et choisir « Remettre le colis ». Aucune autre énigme ne suit la livraison.')
page('Tous les repères\nCarte exacte')
table([['Référence','Objet ou installation','(x, y)']]+[[e['ref'],e['title'],str(tuple(e['cell']))] for e in E],[70,325,105])
p('Coordonnées à partir de zéro, nord en haut. Départ (31, 19). La carte PNG/PDF représente la grille exacte. Les trois archives secrètes restent facultatives.')
page('Les six raccourcis\nÉcourter les retours')
p('Chaque passage est un mur au départ. Il apparaît après une visite physique des deux cases adjacentes indiquées, dans n’importe quel ordre. Une case seulement dévoilée sur la carte ne compte pas. Le passage reste ouvert dans les deux sens.')
table([['ID','Mur','Deux cases à visiter','Gain minimal']]+[[s['id'],str(tuple(s['cell'])),str(tuple(s['sides'][0]))+' / '+str(tuple(s['sides'][1])),str(s['minimum_saved_steps'])+' pas'] for s in S],[40,85,275,100])
audit=json.loads((R/'game/tests/audit_level8.json').read_text());base=audit['without_shortcuts']['steps'];short=audit['with_shortcuts']['steps']
p(f'Parcours de référence : {base} pas sans raccourcis ; {short} avec ouvertures progressives. Gain : {base-short} pas.')
p('Même ordre d’objectifs et carte connue : cette mesure ne prédit pas la longueur d’une première partie. Chaque raccourci évite encore au moins 12 pas lorsque les cinq autres sont ouverts. Aucun ne contourne les accès verrouillés 102 ou 103. Aucun raccourci n’est obligatoire.')
page('Indices progressifs\nLes trois paliers')
aid=json.loads((D/'guidance.json').read_text())
for id in ['m_balance','m_network','m_address']:
 p(by[id]['ref']+' - '+by[id]['title'],'head')
 for i,pair in enumerate(aid['hints'][id]):p(['Piste : ','Méthode : ','Solution : '][i]+pair[0])
p('Les indices sont facultatifs et sans pénalité. Ils ne déplacent pas les colis, ne changent pas les aiguillages et ne remplissent pas l’adresse. Les textes, objectifs et commandes existent en français et en anglais.')
page('Fin de mission\nLa sonnette de Folamour')
p('Folamour ouvre le colis : une sonnette de bureau. Il la fait tinter, puis vous regarde.')
p('« Excellent ! Maintenant, vous pourrez annoncer votre arrivée avant de me déranger. » - Folamour')
p('Sauvegarde et suite','head');p('La mission est terminée et le bilan est enregistré. Le chapitre 2 contient maintenant trois missions : serres, photocopies et courrier. La suite du stage arrivera plus tard. Le passage direct depuis les photocopies conserve les bilans précédents.')
p('Les placements et choix de colis, le dernier résultat de pesée, les aiguillages et leur essai, l’adresse partielle, les objets installés, les raccourcis, indices et découvertes sont sauvegardés. Une réinitialisation conserve le matériel installé.')
p('Menu clarifié','head');p('La sélection sépare les chapitres et numérote leurs niveaux localement : chapitre 1, niveaux 1 à 5 ; chapitre 2, niveaux 1 à 3. Les sauvegardes et confirmations utilisent les mêmes noms. Les anciens numéros internes 6, 7 et 8 désignent respectivement les trois missions du chapitre 2.')
p('Confort et vérification','head');p('Déplacement +30 % conservé, réglages audio et netteté mobile conservés. Parcours physique, barrières, solutions et reprises partielles vérifiés dans Godot. Panneaux français/anglais vérifiés en portrait et paysage. Ces contrôles automatisés ne constituent pas un essai sur chaque modèle de téléphone.')
def footer(c,d):
 c.setFont('Interface',8);c.setFillColor(colors.HexColor('#647e70'));c.drawString(44,25,'FOLAMOUR / V0.14 / CHAPITRE 2 - NIVEAU 3 / SPOILERS');c.drawRightString(A4[0]-44,25,str(d.page))
SimpleDocTemplate(str(out/f'{prefix}-Cheatsheet-solutions.pdf'),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=42,bottomMargin=45).build(story,onFirstPage=footer,onLaterPages=footer)
(out/f'{prefix}-Cheatsheet-solutions.md').write_text('\n'.join(md))
summary=f"""# Lab-Mazing - v0.14 : Le courrier interne

- Chapitre 2, niveau 3 (numéro interne 8) : circuit autour des entrepôts, 19 repères, trois secrets.
- Trois énigmes : balance à six colis, aiguillages pneumatiques avec trajet animé, adresse à reconstituer.
- Six raccourcis utiles : parcours de référence {base} → {short} pas. Déclenchement après visite physique des deux côtés.
- Folamour confie une livraison puis découvre sa sonnette de bureau.
- Menu regroupé par chapitre, accès direct aux trois missions du chapitre 2, sauvegardes et confirmations clairement nommées.
- Objectifs et indices français/anglais, essais sauvegardés, objets installés conservés.
- Déplacement +30 %, réglages de netteté et corrections audio conservés. Aucun bruit de pas.

Accès : Choisir un chapitre → Chapitre 2 · Niveau 3 - Le courrier interne, ou « Passer au courrier interne » après les photocopies.

Les cartes et solutions précédentes restent valides. Les anciens numéros globaux 6 et 7 correspondent maintenant aux niveaux 1 et 2 du chapitre 2 dans les menus.

Ce dossier contient la carte PNG/PDF, le cheatsheet PDF/Markdown, ce résumé et une archive ZIP des cinq documents.

Jeu : https://jfeffe.github.io/lab-mazing/
"""
(out/'Resume-v0.14.md').write_text(summary)
with zipfile.ZipFile(out/'Lab-Mazing-v0.14-Chapitre-2-Mission-3.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(out.iterdir()):
  if f.suffix!='.zip':z.write(f,f.name)
print('Six documents generated:',out)
