# L’unanimité absolue

Chapitre 4 / Niveau 5 / Version 0.18 / SPOILERS

## L’unanimité absolue
Chapitre 4 / Niveau 5

### SPOILERS / VERSION 0.18

« Nous sommes tous d’accord. Nous attendons simplement de savoir avec qui. » Cinq Folamour occupent cinq bureaux. Chaque signature attend les quatre autres.

Une salle de décision centrale dessert cinq bureaux : un au nord, deux à l’ouest et deux à l’est. Les couloirs latéraux contournent les bureaux, tandis que les deux sas gardent les réseaux du conseil.

### Parcours conseillé

Menu → Choisir un chapitre → Chapitre 4, puis choisir ce niveau. La transition depuis la mission précédente conserve les bilans. Le sac et le journal repartent à zéro à chaque nouveau niveau.

1. Ramasser la mallette 101 et l’installer au poste 203. Lire 201 et 202, puis résoudre 203 : Cinq faits contre cinq certitudes. Le sas 111 s’ouvre.

2. Lire 301 et 302, puis résoudre 303 : Le réseau de confiance. Le sas 112 s’ouvre.

3. Lire 401 et 402, puis résoudre 403 : Le sceau à usage collectif. Rejoindre ensuite le passage 900.

Les notes secrètes 501, 502 et 503 sont facultatives. Leur lecture compte au bilan. Les 4 raccourcis demandent de marcher des deux côtés du mur ; la simple visibilité ne suffit pas.

### Commandes et sauvegarde

Clic ou toucher : marcher et examiner. WASD / ZQSD / flèches : marcher ; E : interagir ; I : sac ; J : journal ; M : carte. Aucune limite de temps. Les manipulations, mesures et programmes sont sauvegardés. Réinitialiser un essai restaure ses réglages sans rendre la mallette déjà installée. Après une simulation, modifier une commande exige un nouveau test.

### Indices graduels

Chaque poste propose une piste, une méthode, puis la solution complète. Ouvrir le panneau ne révèle rien automatiquement. Les indices consultés et les essais incorrects sont comptés au bilan.

## 01 / Cinq faits contre cinq certitudes

Poste 203 : (17, 17). Mallette 101 requise.

Affecter une preuve à chaque bureau, sans doublon. Les copies ont été retirées ; les cinq originaux sont disponibles, même lors d’un accès direct à ce niveau.

### 201 / Consigne 201 / (13, 1)

Cinq bureaux : habitat, météo, sécurité, industrie, transport. Affecter à chacun une preuve originale. Le dossier d’arrivée ne va ni à la météo ni à l’industrie. Le pluviomètre va au service qui annonce le temps.

### 202 / Consigne 202 / (21, 9)

Le film du chariot va à la sécurité. Le bon des coques va à l’industrie. Le test de l’ascenseur va au transport. Chaque preuve et chaque bureau sont utilisés une fois.

### Solution exacte depuis la réinitialisation

Habitat : dossier ; météo : pluviomètre ; sécurité : film ; industrie : commande ; transport : ascenseur. Valider.

Sécurité reçoit film, industrie reçoit commande, transport reçoit ascenseur, météo reçoit pluviomètre. Le dossier d’arrivée reste pour habitat.

Validation enregistrée. Le deuxième secteur est ouvert.

## 02 / Le réseau de confiance

Poste 303 : (5, 17). Validation 203 requise.

Choisir une source pour chaque bureau. A et B doivent remonter à X ; C, D et E à Y. Tester trace toutes les chaînes et signale les boucles.

### 301 / Consigne 301 / (1, 1)

A peut croire B ou le capteur X. B peut croire C ou A. C peut croire A ou le capteur Y. D peut croire E ou B. E peut croire D ou C. X et Y sont les seuls constats physiques.

### 302 / Consigne 302 / (9, 33)

A et B doivent finir sur X ; C, D et E doivent finir sur Y. Aucune boucle n’est recevable. Une chaîne de copies aboutissant au bon capteur est recevable, mais ne multiplie pas les preuves.

### Sorties du réseau

Nœud | Sortie 0 | Sortie 1
--- | --- | ---
A | B | X
B | C | A
C | A | Y
D | E | B
E | D | C

### Solution exacte depuis la réinitialisation

A → X ; B → A ; C → Y ; D → E ; E → C. Tester puis valider.

A doit joindre X, B doit joindre A, C doit joindre Y. D ne peut passer par B (origine X) : il rejoint E, qui rejoint C.

Validation enregistrée. Le troisième secteur est ouvert.

## 03 / Le sceau à usage collectif

Poste 403 : (29, 17). Validation 303 requise.

Sélectionner une ou deux copies du côté du sceau, puis Traverser. Coût = durée du plus lent : A1, B2, C5, D8. Tous au conseil en 15 unités maximum. Aucune limite en temps réel. Annulation et remise à zéro disponibles.

### 401 / Consigne 401 / (25, 1)

Quatre copies portent leurs dossiers au cinquième Folamour par une passerelle. Durées : A=1, B=2, C=5, D=8 unités. Au plus deux copies traversent ensemble. Le sceau unique doit accompagner chaque traversée et chaque retour.

### 402 / Consigne 402 / (33, 33)

Une traversée coûte la durée du plus lent. Tout le monde part côté bureaux. Amener les quatre copies et le sceau au conseil en 15 unités maximum. Le temps avance uniquement quand vous appuyez sur Traverser. Annuler restitue le temps.

Traversée | Coût | Total
--- | --- | ---
A + B vers le conseil | 2 | 2
A revient aux bureaux | 1 | 3
C + D vers le conseil | 8 | 11
B revient aux bureaux | 2 | 13
A + B vers le conseil | 2 | 15

### Solution exacte depuis la réinitialisation

A+B aller (2), A retour (1), C+D aller (8), B retour (2), A+B aller (2). Total 15. Valider.

Faire voyager C et D ensemble économise leurs longs trajets. A et B servent de passeurs du sceau. Le plus rapide ne doit pas faire tous les retours.

Validation enregistrée. Le passage de fin de niveau est autorisé.

## Repères, secrets et raccourcis

Repère | Objet / poste | Coordonnées
--- | --- | ---
100 | Ordre de mission | (19, 21)
101 | Mallette de service | (15, 21)
111 | Sas de secteur 1 | (11, 17)
112 | Sas de secteur 2 | (23, 17)
201 | Consigne 201 | (13, 1)
202 | Consigne 202 | (21, 9)
203 | Cinq faits contre cinq certitudes | (17, 17)
301 | Consigne 301 | (1, 1)
302 | Consigne 302 | (9, 33)
303 | Le réseau de confiance | (5, 17)
401 | Consigne 401 | (25, 1)
402 | Consigne 402 | (33, 33)
403 | Le sceau à usage collectif | (29, 17)
501 | Note confidentielle 1 | (21, 1)
502 | Note confidentielle 2 | (1, 33)
503 | Note confidentielle 3 | (33, 1)
900 | Passage de service | (17, 3)

### Raccourcis facultatifs

ID | Mur | Deux côtés à visiter | Gain minimal*
--- | --- | --- | ---
C51 | (25, 24) | (25, 23) ↔ (25, 25) | 12 pas
C52 | (26, 29) | (27, 29) ↔ (25, 29) | 12 pas
C53 | (25, 4) | (25, 3) ↔ (25, 5) | 40 pas
C54 | (7, 2) | (7, 1) ↔ (7, 3) | 40 pas

* Gain sur le trajet entre les deux côtés, même avec les autres raccourcis ouverts. Le parcours principal fonctionne sans ouvrir aucun raccourci.

## Archives confidentielles
et fin de mission

### 501 / (21, 1)

Folamour original : « Les quatre autres sont des copies. » Exemplaire 5 sur 5.

### 502 / (1, 33)

Le conseil a voté l’interdiction des votes divisés. Résultat : cinq versions différentes du procès-verbal.

### 503 / (33, 1)

Programme HORIZON. Destination : suffisamment loin. Retour : non prévu au formulaire.

### Révélation de fin de niveau

Vous avez remplacé les copies par des constats et réuni les signatures. MIROIR annonce : « CERTITUDE INSUFFISANTE. » Folamour ouvre un tiroir : « Toute incertitude déclenche le protocole de sérénité maximale. C’est écrit très petit, mais très officiellement. » L’ascenseur monte vers un hangar vertical. Des silhouettes de fusées disparaissent dans l’obscurité. PROGRAMME HORIZON — POUR QUE PLUS JAMAIS RIEN NE PUISSE ARRIVER. « Ah, vous voilà. Nous cherchions quelqu’un pour la vérification finale. » CHAPITRE 5 À VENIR.

### La suite

Fin du chapitre 4. Le chapitre 5 et le programme HORIZON sont annoncés, mais ne sont pas encore jouables dans la version 0.18.

### Vérification du parcours

Le trajet de référence parcourt 409 cases de déplacement et visite les 15 points interactifs, dont les trois secrets. Les deux sas portent le total à 17 repères. Les solutions du guide sont utilisées par les tests des commandes réelles du jeu.
