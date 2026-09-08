# L’observatoire des intentions hostiles

Chapitre 5 / Niveau 2 / Version 0.19 / SPOILERS

## L’observatoire des intentions hostiles
Chapitre 5 / Niveau 2

### SPOILERS / VERSION 0.19

La carte du monde clignote de certitudes. Une fenêtre s’allume : hostilité. Une fenêtre s’éteint : dissimulation. « Absence de comportement suspect : préparation particulièrement réussie. » Les opérateurs ont quitté leurs fauteuils. Leurs rapports continuent d’arriver.

Trois enceintes imbriquées : relevés sur le grand circuit extérieur, chronologie sur l’anneau médian, boucle des sources au centre. Le passage ouest 111 puis le passage nord 112 donnent accès aux enceintes suivantes.

### Parcours conseillé

Menu > Choisir un chapitre > Chapitre 5. Le démarrage direct remplace la sauvegarde après confirmation. Enchaîner les missions conserve les bilans ; le sac et le journal se renouvellent à chaque niveau.

1. Ramasser la mallette 101 et l’installer au poste 203. Lire les consignes 201 et 202, puis résoudre 203 : Trois horloges, une panique. Le sas 111 s’ouvre.

2. Lire les consignes 301 et 302, puis résoudre 303 : Le montage de la menace. Le sas 112 s’ouvre.

3. Lire les consignes 401 et 402, puis résoudre 403 : Deux sources, six certitudes. Rejoindre ensuite le passage 900.

Les trois secrets 501/502/503 sont facultatifs. Le parcours principal fonctionne sans ouvrir de raccourci. Chaque essai est réversible et propose trois niveaux d’indice.

### Rythme et sauvegarde

Aucune échéance réelle. Au niveau 4, HORIZON descend de l’étape 3 à l’étape 0 uniquement après les validations. Lecture, réflexion et pause ne font pas avancer la procédure. Les réglages, observations, programmes et réponses sont sauvegardés. La réinitialisation ne rend pas la mallette installée et ne supprime pas les constats lus.

## Plan du labyrinthe

La carte A3 et le PNG séparés permettent de lire les coordonnées à pleine résolution. Nord en haut ; origine (0,0). Les couleurs indiquent les secteurs. Les numéros correspondent exactement aux objets du jeu.

## 01 / Trois horloges, une panique

Poste 203 : (17, 33). Mallette 101 requise.

Choisir les décalages (affiché − réel). B affiche 11:59 à 12:00 réelles. A est trois minutes devant B ; C une minute derrière A. Chaque décalage est entre −2 et +2.

### 201 / (1, 7)

Les horloges A/B/C ont un décalage constant entre −2 et +2 minutes. Heure réelle = heure affichée moins décalage. À 12:00 réelles, B indiquait 11:59.

### 202 / (33, 27)

Au même instant A affiche trois minutes de plus que B. C affiche une minute de moins que A. Les écarts portent sur les horloges, pas sur les événements.

### Solution depuis la réinitialisation

A : +2 ; B : −1 ; C : +1. Valider.

B vaut −1. Donc A vaut +2 et C vaut +1. Soustraire ces valeurs remet les rapports à la même heure.

## 02 / Le montage de la menace

Poste 303 : (17, 7). Validation du poste 203 requise.

Reconstituer les cinq événements à leur heure réelle. A avance de 2 minutes, B retarde de 1, C avance de 1. Un exemplaire de chaque image ; tester puis valider.

### 301 / (7, 7)

Images originales : cuisine allumée A 12:02 ; prévision MIROIR B 12:00 ; sirène C 12:03 ; volets fermés A 12:05 ; hostilité « confirmée » B 12:03.

### 302 / (27, 27)

Retirer les décalages A=+2, B=−1, C=+1. Classer les cinq images de la première à la dernière. Une confirmation postérieure ne peut pas être la cause de l’alerte initiale.

### Solution depuis la réinitialisation

Cuisine → prévision → sirène → volets → confirmation. Tester puis valider.

Les heures corrigées sont 12:00 cuisine, 12:01 prévision, 12:02 sirène, 12:03 volets, 12:04 confirmation.

Attention : modifier le réglage ou le programme invalide son dernier test. Relancer « Tester la procédure » avant de valider.

## 03 / Deux sources, six certitudes

Poste 403 : (17, 17). Validation du poste 303 requise.

Chaque flèche fournit une preuve au nœud suivant. Suspendre exactement deux copies pour rendre le graphe sans boucle. Conserver Capteur→A, Fenêtre→C, A→B, C→D. Tester le graphe avant validation.

### 401 / (13, 13)

Les flèches signifient « sert de preuve à ». Capteur → A et Fenêtre → C sont les deux apports physiques à conserver. A → B et C → D sont les registres horodatés à conserver.

### 402 / (21, 21)

B → A et D → C sont des copies ajoutées après les rapports. Suspendre exactement deux liens, éliminer tout raisonnement circulaire, garder les quatre apports originaux.

| Lien | Nature |
| --- | --- |
| Capteur > A | Apport original à conserver |
| A > B | Apport original à conserver |
| B > A | Copie circulaire |
| Fenêtre > C | Apport original à conserver |
| C > D | Apport original à conserver |
| D > C | Copie circulaire |

### Solution depuis la réinitialisation

Suspendre B → A et D → C uniquement. Tester puis valider.

Chaque copie revient vers son propre ancêtre. Retirer B→A et D→C laisse les deux chaînes d’observation ouvertes.

Attention : modifier le réglage ou le programme invalide son dernier test. Relancer « Tester la procédure » avant de valider.

## Repères et raccourcis

| Repère | Objet / poste | Coordonnées |
| --- | --- | --- |
| 100 | Ordre de mission | (1, 31) |
| 101 | Mallette de service | (3, 33) |
| 111 | Sas de secteur 1 | (4, 17) |
| 112 | Sas de secteur 2 | (17, 10) |
| 201 | Consigne 201 | (1, 7) |
| 202 | Consigne 202 | (33, 27) |
| 203 | Trois horloges, une panique | (17, 33) |
| 301 | Consigne 301 | (7, 7) |
| 302 | Consigne 302 | (27, 27) |
| 303 | Le montage de la menace | (17, 7) |
| 401 | Consigne 401 | (13, 13) |
| 402 | Consigne 402 | (21, 21) |
| 403 | Deux sources, six certitudes | (17, 17) |
| 501 | Note confidentielle 1 | (33, 1) |
| 502 | Note confidentielle 2 | (7, 23) |
| 503 | Note confidentielle 3 | (13, 21) |
| 900 | Passage de service | (21, 15) |

### Raccourcis facultatifs

Aucun raccourci caché : les anneaux offrent déjà des boucles de circulation.

Le gain est mesuré entre les côtés du mur même lorsque les autres raccourcis sont ouverts. Aucun passage ne contourne un sas d’énigme.

## Archives et conclusion

### 501 / (33, 1)

Le dernier opérateur a noté : « Je n’ai rien vu. » Sa précision lui a valu une formation corrective.

### 502 / (7, 23)

La radio cite le rapport qui cite la radio. Deux sources indépendantes, selon la radio.

### 503 / (13, 21)

Le dîner a été reclassé en offensive alimentaire. Le dessert fait encore débat.

### Révélation de fin de mission

La lumière précédait l’alerte. Les volets ont fermé après la sirène. MIROIR a provoqué les réactions qu’il présentait comme preuves. En retirant les deux copies circulaires, vous laissez subsister un fait minuscule : quelqu’un a allumé sa cuisine. HORIZON avait classé le dîner comme une manœuvre.

### La suite

Le bouton « Continuer la mission suivante » conserve le bilan et démarre le prochain niveau.

### Vérification

Le parcours de référence effectue 289 pas et visite tous les objets interactifs, y compris les trois secrets. Les solutions sont exercées par les boutons réels du jeu, avec sauvegarde partielle, reprise et indices en français et en anglais.
