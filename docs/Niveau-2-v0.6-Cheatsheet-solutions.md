# Niveau 2 - Cheatsheet - Version 0.6


**SPOILERS.** Carte et textes issus des données de la version 0.6.


## Solution


### 1. Fabriquer l’outil

Récupérer le manche à cliquet 101 et la douille carrée 102. À l’établi 103, choisir « Assembler la clé à douille ». La clé assemblée rejoint le sac.


### 2. Ouvrir le département hydraulique

Utiliser la clé assemblée sur le générateur 104. Le générateur démarre et ouvre la porte 105. Traverser cette porte pour atteindre le département hydraulique.


### 3. Réunir les indices hydrauliques

Récupérer le volant 201. Consulter les manomètres 202 (pompe = 3), 203 (filtre = 1), 204 (cuve = 2), puis le repérage des conduites 205.


### 4. Vidanger le bassin

Au collecteur 206, installer le volant, puis régler les molettes de gauche à droite : 2 / 3 / 1. Cliquer sur « Mettre le circuit en service » (Activate the circuit). La passerelle 207 devient accessible.


### 5. Fabriquer le relais

Ramasser la bobine de cuivre 208 et le noyau céramique 209. À l’établi électrique 210, les assembler en relais de puissance. Cette étape peut être faite avant l’étape 4.


### 6. Relever le contrepoids

Au-delà de 207, récupérer le câble 301 et le crochet 302. Les installer ensemble sur le treuil 303. Le contrepoids remonte et libère le frein de l’ascenseur.


### 7. Alimenter l’ascenseur

Installer le relais de puissance dans l’armoire 304. Cette étape peut précéder l’étape 6.


### 8. Terminer le niveau

Lorsque le treuil 303 et l’armoire 304 sont activés, interagir avec les commandes 306 puis choisir « Monter dans l’ascenseur » (Board the elevator). Aucun code final supplémentaire.


## Réglage hydraulique

RETOUR / RETURN = CUVE / TANK = 2 ; DÉPART / SUPPLY = POMPE / PUMP = 3 ; PURGE / DRAIN = FILTRE / FILTER = 1.


## Raccourcis

- M1 : mur (26, 3). Cases à visiter : (27, 3) et (25, 3).

- M2 : mur (10, 2). Cases à visiter : (11, 2) et (9, 2).

- M3 : mur (27, 18). Cases à visiter : (27, 19) et (27, 17).

- M4 : mur (8, 19). Cases à visiter : (9, 19) et (7, 19).

- M5 : mur (3, 30). Cases à visiter : (3, 31) et (3, 29).

- M6 : mur (22, 26). Cases à visiter : (22, 27) et (22, 25).


## Textes complets et conditions


### 100 / Département des machines

Machinery department | X=1, Y=1

L’ascenseur est immobilisé. Le générateur du hall, les circuits hydrauliques et le treuil doivent être remis en service. Les établis permettent d’assembler les pièces récupérées. Les manomètres portent les réglages du circuit.

« Nous avions un technicien. Vous avez deux mains. La différence est administrative. » — Folamour


### 101 / Manche à cliquet

Ratchet handle | X=33, Y=1

Une poignée robuste. Son logement carré est vide ; elle ne peut saisir aucun écrou en l’état.


### 102 / Douille carrée

Square socket | X=1, Y=9

Une douille de grande taille, détachée de sa poignée. Le carré d’entraînement porte la même empreinte que celui d’un manche à cliquet.


### 103 / Établi d’assemblage

Assembly workbench | X=15, Y=5

Un étau, un axe de fixation et le dessin d’une clé à douille en deux parties. Le dessin montre un manche et une douille réunis par l’axe.

Objets à installer : Manche à cliquet, Douille carrée.

Résultat : La douille est fixée au manche. Vous récupérez une clé à douille complète.


### 104 / Générateur du hall

Hall generator | X=29, Y=7

Le volant d’entraînement est grippé. Au centre, un écrou carré permet de le débloquer. Une commande de démarrage est reliée au verrou du département hydraulique.

Objets à installer : Clé à douille assemblée.

Résultat : La clé reste engagée dans le volant. Le générateur démarre ; le verrou hydraulique se relève.


### 105 / Porte du département hydraulique

Hydraulics department door | X=17, Y=11

Une serrure électromagnétique, reliée au générateur du hall. Aucun clavier ni serrure manuelle.

Commande distante : Générateur du hall.


### 106 / Plan de l’accouplement

Coupling diagram | X=3, Y=3

Le croquis du générateur représente un écrou carré et une clé à douille. Une annotation indique : « Assemblage à l’étau avant mise en service. »


### 107 / Feuille d’heures

Timesheet | X=33, Y=9

« Temps passé à réparer le générateur : 4 heures. Temps passé à expliquer pourquoi il ne fallait pas y verser de café : 6 heures. » — Ancien technicien

Secret facultatif.


### 201 / Volant de distribution

Distribution handwheel | X=33, Y=13

Un volant à trois branches. Une plaquette porte l’inscription : « Collecteur central — axe principal ». Il manque sur le collecteur du département hydraulique.


### 202 / Manomètre de la pompe

Pump pressure gauge | X=1, Y=15

POMPE — conduite rouge.
L’aiguille et les trois traits du cadran indiquent 3. Une gravure rappelle que les valeurs des cadrans sont les consignes de mise en service.


### 203 / Manomètre du filtre

Filter pressure gauge | X=31, Y=19

FILTRE — conduite turquoise.
L’aiguille est alignée sur le premier trait : 1.


### 204 / Manomètre de la cuve

Tank pressure gauge | X=9, Y=21

CUVE — conduite jaune.
L’aiguille est alignée sur le deuxième trait : 2.


### 205 / Repérage des conduites

Pipe routing diagram | X=13, Y=13

La gravure suit les trois conduites jusqu’au collecteur :
RETOUR ← CUVE
DÉPART ← POMPE
PURGE ← FILTRE

Les cadrans des machines fournissent les consignes. Les trois molettes du collecteur sont graduées de 0 à 3.


### 206 / Collecteur hydraulique

Hydraulic manifold | X=17, Y=17

Il manque le volant principal. Trois molettes commandent RETOUR, DÉPART et PURGE. Chaque conduite rejoint un manomètre dans le département.

Après installation : Le volant principal est en place. Les trois molettes commandent RETOUR, DÉPART et PURGE. Les conduites permettent de retrouver les manomètres correspondants.

Objets à installer : Volant de distribution.

Consigne : Régler les molettes selon les conduites et leurs manomètres.

Solution : 2 / 3 / 1.

Résultat : La pompe se stabilise. Le bassin se vide et la passerelle vers le treuil devient accessible.


### 207 / Passerelle du bassin

Basin walkway | X=25, Y=23

Une barrière interdit la passerelle tant que le bassin n’est pas vidangé. Sa commande dépend du collecteur hydraulique.

Commande distante : Collecteur hydraulique.


### 208 / Bobine de cuivre

Copper coil | X=1, Y=13

Une bobine intacte pour un relais de puissance. Elle doit être montée autour d’un noyau isolant avant d’être utilisée.


### 209 / Noyau céramique

Ceramic core | X=33, Y=21

Un noyau isolant. Sa forme et ses contacts correspondent au support d’un relais de puissance.


### 210 / Établi électrique

Electrical workbench | X=3, Y=19

Le gabarit de montage présente un noyau céramique entouré d’une bobine. Deux contacts attendent le relais ainsi formé.

Objets à installer : Bobine de cuivre, Noyau céramique.

Résultat : La bobine est fixée autour du noyau. Vous récupérez un relais de puissance.


### 211 / Manuel de maintenance

Maintenance manual | X=1, Y=21

Page 1 : Ne rien forcer.
Page 2, manuscrite : Sauf si le docteur regarde.
Toutes les autres pages servent à caler une table.

Secret facultatif.


### 301 / Câble de levage

Hoist cable | X=1, Y=25

Un câble neuf, dépourvu de crochet. Il est dimensionné pour le treuil du contrepoids.


### 302 / Crochet de sécurité

Safety hook | X=33, Y=33

Un crochet avec une goupille intacte. Il peut être fixé à un câble pour rattacher le contrepoids au treuil.


### 303 / Treuil du contrepoids

Counterweight hoist | X=9, Y=29

Le contrepoids repose au sol. Le câble s’est rompu et son crochet a disparu. Le treuil dispose d’un support où assembler et tendre le remplacement.

Objets à installer : Câble de levage, Crochet de sécurité.

Résultat : Le câble et le crochet sont assemblés sur le treuil. Le contrepoids remonte ; le frein de l’ascenseur est libéré.


### 304 / Armoire de l’ascenseur

Elevator power cabinet | X=29, Y=29

Le logement du relais de puissance est vide. Le schéma représente une bobine entourant un noyau isolant. Les ateliers électriques se trouvent dans le département hydraulique.

Objets à installer : Relais de puissance.

Résultat : Le relais est installé. L’armoire alimente les commandes de l’ascenseur.


### 305 / Schéma de sécurité de l’ascenseur

Elevator safety diagram | X=33, Y=25

Deux témoins sont reliés à la cabine : ALIMENTATION et CONTREPOIDS. Le départ est impossible tant que l’un des deux circuits est ouvert.

La passerelle reste praticable après vidange : les ateliers sont accessibles si une pièce a été oubliée.


### 306 / Commandes de l’ascenseur

Elevator controls | X=17, Y=34

Le bouton de départ est relié à deux témoins de sécurité. L’ascenseur attend son alimentation et son contrepoids.

Prérequis : Armoire de l’ascenseur, Treuil du contrepoids activés.

Résultat : Le moteur entraîne la cabine. Vous quittez le département des machines.


### 307 / Message du technicien

Technician’s message | X=1, Y=33

« Si vous êtes parvenu jusqu’ici, vous savez déjà faire mon travail. Ne le dites surtout pas au docteur. Il vous proposera un stage. »

Secret facultatif.


### Clé à douille assemblée

Assembled socket wrench

Le manche et la douille sont solidaires. La tête carrée permet de débloquer le volant du générateur.


### Relais de puissance

Power relay

La bobine de cuivre est montée sur le noyau céramique. Le relais peut être installé dans l’armoire de l’ascenseur.
