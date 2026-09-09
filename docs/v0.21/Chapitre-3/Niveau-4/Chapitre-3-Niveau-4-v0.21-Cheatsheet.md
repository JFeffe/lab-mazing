## Le simulateur de crise

### Chapitre 3 / Niveau 4 • Version 0.21 • Solutions complètes

« Nous allons simuler une petite panne. Si vous réussissez, nous en ajouterons une deuxième. Nous finirons bien par obtenir un résultat représentatif. » — Folamour

Trois plateformes autour de bassins techniques : distribution au nord-ouest, hydraulique au nord-est et évacuation au sud. Des passerelles étroites relient les plateformes.

Cette édition remplace les anciennes cartes de ce niveau. Elle ajoute les dix souvenirs K01–K10 et utilise la position actuelle de la fin de mission. Les énigmes et les labyrinthes sont conservés.

### Collection et dossier

Collection : Rouage de prévoyance. Ramasser les dix souvenirs est facultatif. Le dossier compte les trouvailles par niveau et par chapitre ; une archive se révèle à 10, 25 et 50 trouvailles dans ce chapitre. Rien ne doit être dépensé ou remis à Folamour.

Une collection n’apparaît sur la carte du jeu qu’après découverte de sa case. Son cercle disparaît après ramassage. Le présent guide dévoile tous les emplacements. Le clic ou toucher permet de s’y rendre et de ramasser ; le bouton Ramasser et la touche E fonctionnent aussi.

La collection suit la sauvegarde de cette aventure. Dans le dossier, rejouer un niveau terminé conserve la collection et les bilans, mais recommence ses énigmes et remplace le niveau en cours après confirmation. Une nouvelle aventure remet le dossier à zéro.

## Plan exact du labyrinthe

[Cartes PNG/PDF et guides du chapitre dans Drive](https://drive.google.com/drive/folders/1F0mZ6lVM_MrYT-yZxJ4aE68lWWD1HXjO)

Pour lire les petits repères, utiliser le PNG en pleine résolution ou le PDF A3 séparé. Les coordonnées désignent les cases du labyrinthe ; le nord est en haut.

## Les dix souvenirs

Les fonds de branches vides sont privilégiés, en donnant priorité aux branches longues. Lorsqu’il manque d’impasses adaptées, les autres objets sont dans des recoins éloignés des interactions. Aucun mur n’a été déplacé.

| Repère | Case (x, y) | Situation | Distance minimale aux repères |
| --- | --- | --- | --- |
| K01 | (8, 10) | Recoin dans un couloir calme | 8 pas |
| K02 | (27, 10) | Recoin dans un couloir calme | 9 pas |
| K03 | (1, 17) | Fond d’impasse ; branche de 8 pas | 20 pas |
| K04 | (1, 21) | Recoin dans un couloir calme | 12 pas |
| K05 | (29, 22) | Recoin dans un couloir calme | 11 pas |
| K06 | (32, 23) | Recoin dans un couloir calme | 15 pas |
| K07 | (1, 27) | Fond d’impasse ; branche de 2 pas | 10 pas |
| K08 | (24, 27) | Recoin dans un couloir calme | 11 pas |
| K09 | (14, 30) | Recoin dans un couloir calme | 18 pas |
| K10 | (9, 33) | Recoin dans un couloir calme | 16 pas |

Longueur de branche : du fond à la première jonction. Distance aux repères : chemin le plus court jusqu’à un objet, une interaction, un départ ou un élément de décor réservé, sur la grille et sans raccourci. Deux souvenirs sont séparés d’au moins huit pas et de quatre cases en distance Manhattan.

## Parcours et fin de mission

### Ordre de visite de référence :

100 → 101 → 202 → 501 → 201 → 203 → 302 → 502 → 301 → 303 → 402 → 401 → 503 → 403 → 900

Cet ordre comprend les indices et secrets. Les manipulations des postes figurent ci-dessous. Les souvenirs peuvent être ramassés lors des détours, dès que leur secteur est accessible. Aucun raccourci ni souvenir n’est requis pour terminer.

### Fin : 900 — Folamour — Une crise simulée suffit — (33, 33)

Parler au docteur et choisir « Faire le bilan avec Folamour ». Il remplace la dernière porte.

Validations requises : 203 — Répartition d’urgence, 303 — Équilibrage des cuves, 403 — Évacuation à deux équipes

Les dix souvenirs n’entrent jamais dans ces conditions.

## Énigmes et manipulations

### 203 — Répartition d’urgence

Distribuer les douze unités entre ventilation, archives, pompe et éclairage. Les barres affichent les quantités et la réserve.

Piste : Exprimez chaque besoin à partir de celui de la ventilation.

Méthode : Si ventilation = x, les besoins sont x, x−1, x+1, x. Leur somme vaut 4x = 12.

Solution : Ventilation 3 ; archives 2 ; pompe 4 ; éclairage 3. Valider.

Depuis la réinitialisation : Ventilation 3 ; archives 2 ; pompe 4 ; éclairage 3. Valider.

Si ventilation = x, les besoins sont x, x−1, x+1, x. Leur somme vaut 4x = 12.

### 303 — Équilibrage des cuves

Transvaser dans le circuit fermé. Les jauges changent après chaque action. Les essais et l’historique des transvasements sont sauvegardés.

Piste : La petite cuve mesure trois unités ; la moyenne en contient cinq.

Méthode : Commencez par remplir B puis C depuis B. Récupérez les petits restes pour former quatre unités.

Solution : A vers B → B vers C → C vers A → B vers C → A vers B → B vers C → C vers A. Valider.

Depuis la réinitialisation : A vers B → B vers C → C vers A → B vers C → A vers B → B vers C → C vers A. Valider.

Commencez par remplir B puis C depuis B. Récupérez les petits restes pour former quatre unités.

### 403 — Évacuation à deux équipes

Programmer les deux équipes ensemble. Tester affiche leurs traces et leurs positions finales. Réinitialiser ou retirer un ordre permet de reprendre sans danger.

Piste : Observez les deux cartes après chaque essai : une équipe peut avancer quand l’autre est bloquée.

Méthode : La station de B est décalée vers le bas. Utilisez les murs pour ajuster la synchronisation ; les ordres s’adressent à A.

Solution : N, N, E, E, O, N, N, E, E, S, E, N, N, E. Tester puis valider.

Depuis la réinitialisation : N, N, E, E, O, N, N, E, E, S, E, N, N, E. Tester puis valider.

La station de B est décalée vers le bas. Utilisez les murs pour ajuster la synchronisation ; les ordres s’adressent à A.

## Tous les repères et leurs conditions

### 201 — Priorités électriques — (1, 1)

Douze unités au total. Ventilation et éclairage consomment la même quantité. La pompe prend une unité de plus que la ventilation. Les archives prennent une unité de moins. Aucune unité ne doit rester en réserve.

### 202 — Simulation de surcharge — (13, 13)

Les unités sont transférées depuis la réserve : + attribue une unité, − la restitue. La somme reste toujours égale à douze. Trouver une distribution qui respecte les quatre besoins simultanément.

### 203 — Répartition d’urgence — (7, 3)

Distribuer les douze unités entre ventilation, archives, pompe et éclairage. Les barres affichent les quantités et la réserve.

À installer / remettre : Mallette de service

Ouvre : 111

### 301 — Circuit fermé — (33, 1)

Trois cuves de capacités 8, 5 et 3 unités. La cuve A contient les huit unités initiales. Transvaser continue jusqu’à vider la source ou remplir la destination. Aucun ajout, aucune perte.

### 302 — Équilibre hydraulique — (21, 13)

Obtenir quatre unités dans A et quatre dans B, sans liquide dans C. C sert de mesure intermédiaire. Le bouton Annuler restitue le transvasement précédent.

### 303 — Équilibrage des cuves — (27, 3)

Transvaser dans le circuit fermé. Les jauges changent après chaque action. Les essais et l’historique des transvasements sont sauvegardés.

À valider d’abord : 203 — Répartition d’urgence

Ouvre : 112

### 401 — Deux équipes, un signal — (5, 21)

L’équipe A suit vos directions. L’équipe B reçoit les directions opposées : N devient S, E devient O. Si une équipe bute contre un mur, elle reste sur place ; l’autre continue.

### 402 — Procédure d’évacuation — (29, 33)

Sur chaque plan, aller de D à S en visitant *. Les positions initiales sont opposées mais les murs sont différents. Un obstacle peut servir à décaler les deux équipes. Vingt-quatre ordres au maximum.

### 403 — Évacuation à deux équipes — (17, 23)

Programmer les deux équipes ensemble. Tester affiche leurs traces et leurs positions finales. Réinitialiser ou retirer un ordre permet de reprendre sans danger.

À valider d’abord : 303 — Équilibrage des cuves

### 100 — Ordre de mission — (1, 11)

Trois plateformes autour de bassins techniques : distribution au nord-ouest, hydraulique au nord-est et évacuation au sud. Des passerelles étroites relient les plateformes.

### 101 — Mallette de service — (3, 13)

À installer au premier poste 203. Le matériel reste en place après les essais.

### 111 — Sas de secteur 1 — (17, 3)

Commande depuis le poste 203.

Commande : 203

### 112 — Sas de secteur 2 — (31, 17)

Commande depuis le poste 303.

Commande : 303

### 501 — Note confidentielle 1 — (13, 1)

Simulation 46 : panne du bouton « panne ». Résultat jugé trop rassurant.

Note secrète facultative. Elle est distincte de la collection K01–K10.

### 502 — Note confidentielle 2 — (33, 13)

Le bassin est vide. Un panneau interdit néanmoins de rassurer les visiteurs.

Note secrète facultative. Elle est distincte de la collection K01–K10.

### 503 — Note confidentielle 3 — (1, 33)

Pour augmenter le réalisme, le simulateur souhaite un simulateur qui simule ses erreurs.

Note secrète facultative. Elle est distincte de la collection K01–K10.

### 900 — Folamour — Une crise simulée suffit — (33, 33)

« Terminez les trois essais, puis venez confirmer que la crise était simulée. Le service technique commence à trouver cette précision assez importante. »

À valider d’abord : 203 — Répartition d’urgence, 303 — Équilibrage des cuves, 403 — Évacuation à deux équipes

## Raccourcis et reprise

| ID | Mur | Deux cases à visiter | Gain minimal |
| --- | --- | --- | --- |
| P41 | (4, 33) | (5, 33) / (3, 33) | 12 pas |
| P42 | (30, 23) | (31, 23) / (29, 23) | 20 pas |
| P43 | (33, 26) | (33, 25) / (33, 27) | 12 pas |
| P44 | (4, 29) | (5, 29) / (3, 29) | 12 pas |

Marcher sur les deux côtés du mur ouvre le raccourci. Voir les cases sur la carte ne suffit pas. Le gain minimal mesure les pas encore économisés lorsque les autres raccourcis sont ouverts.

Carte : clic droit sur un passage découvert et accessible pour fermer la carte et marcher vers ce point. Zoom : molette ou boutons de zoom ; recul maximal augmenté. Dossier : bouton près de l’objectif, menu Pause ou bilan de fin.

Folamour réagit aux rencontres, découvertes, essais et réussites. Les options « Animations décoratives » et « Répliques de Folamour » sont séparées dans la pause. Désactiver les répliques n’efface pas les observations archivées.

Sauvegarde locale au navigateur et à l’appareil. Les anciennes sauvegardes v4 sont compatibles ; la collection commence vide. Les totaux des anciennes parties couvrent uniquement les informations qui ont été enregistrées. Aucun ancien souvenir n’est attribué automatiquement.
