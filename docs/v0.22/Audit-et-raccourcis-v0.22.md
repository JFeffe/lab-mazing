## Des retours plus courts

### Audit des 25 niveaux - 9 septembre 2026

Version 0.22 : 43 portes secrètes ajoutées sur 20 niveaux. La campagne compte désormais 155 raccourcis, contre 112. Les 25 labyrinthes, les conditions des énigmes, les notes secrètes et les 250 souvenirs sont conservés.

Chaque nouvelle porte économise entre 20 et 72 pas entre ses deux côtés, même lorsque les autres passages et les verrous sont ouverts. Les exemples vers les machines, commandes ou Folamour explicitent les retours utiles dans chaque guide. Les anciens passages conservent au moins 12 pas de gain.

### Règle de découverte

Un raccourci est un mur au départ. Il se révèle uniquement après avoir marché sur ses deux cases voisines. Voir le mur ou les deux cases dans le brouillard ne suffit pas. Le passage reste ensuite ouvert dans les deux sens et figure sur la carte et dans le journal.

Les portes existantes restent exactement à leur place avec les mêmes identifiants. Les nouvelles portes portent les repères B1 à B4. Si leurs deux côtés ont déjà été parcourus dans une sauvegarde v0.21, elles se révèlent à la reprise. Les objets, essais partiels, indices et souvenirs sont conservés.

## Deux bugs reproduits et corrigés

### Sortie murale du niveau global 3

Reproduction : depuis la case (17, 32), cliquer sur la sortie située en (17, 33), dont le modèle est fixé au mur sud. Le personnage choisissait sa case actuelle comme destination, mais la distance réelle jusqu’au modèle dépassait la portée de 3 mètres. Le déplacement se terminait sans ouvrir le panneau. Correction : le calcul du trajet vérifie désormais la distance jusqu’au modèle de l’interaction, y compris son décalage mural. Le personnage avance assez près.

### Nouvelle destination inaccessible

Reproduction : demander un déplacement accessible, puis cliquer sur un objet situé derrière un secteur fermé ou inconnu. L’alerte apparaissait, mais l’ancien déplacement continuait. Correction : toute nouvelle demande vers un objet remplace le trajet précédent. Si l’objet est inaccessible, le déplacement et son marqueur sont annulés.

Les deux défauts ont été reproduits avant correction. Le test verify_interaction_approaches échouait sur ces cas, puis réussit après correction. Les contrôles muraux des niveaux 3 et 4 et la navigation déjà existante sont également couverts.

## Répartition par niveau

| Chapitre / niveau | Avant | Ajout | Total |
| --- | --- | --- | --- |
| 1 / 1 | 8 | 3 | 11 |
| 1 / 2 | 6 | 1 | 7 |
| 1 / 3 | 6 | 4 | 10 |
| 1 / 4 | 6 | 2 | 8 |
| 1 / 5 | 6 | 3 | 9 |
| 2 / 1 | 6 | 3 | 9 |
| 2 / 2 | 6 | 1 | 7 |
| 2 / 3 | 6 | 1 | 7 |
| 2 / 4 | 6 | 0 | 6 |
| 2 / 5 | 4 | 1 | 5 |
| 3 / 1 | 4 | 1 | 5 |
| 3 / 2 | 4 | 3 | 7 |
| 3 / 3 | 4 | 1 | 5 |
| 3 / 4 | 4 | 0 | 4 |
| 3 / 5 | 4 | 1 | 5 |
| 4 / 1 | 4 | 3 | 7 |
| 4 / 2 | 4 | 3 | 7 |
| 4 / 3 | 0 | 0 | 0 |
| 4 / 4 | 4 | 2 | 6 |
| 4 / 5 | 4 | 0 | 4 |
| 5 / 1 | 4 | 2 | 6 |
| 5 / 2 | 0 | 0 | 0 |
| 5 / 3 | 4 | 2 | 6 |
| 5 / 4 | 4 | 2 | 6 |
| 5 / 5 | 4 | 4 | 8 |

### Niveaux sans ajout

chapitre 2 / niveau 4 ; chapitre 3 / niveau 4 ; chapitre 4 / niveau 3 ; chapitre 4 / niveau 5 ; chapitre 5 / niveau 2. Les candidats sont trop courts, redondants ou sans gain utile vers un poste permanent. Ces niveaux ont été vérifiés ; leurs passages existants sont conservés.

## Mesures, tests et limites

### Placement vérifié indépendamment

Chaque ouverture remplace une case murale entre exactement deux cases de sol opposées. Ses côtés appartiennent déjà à la même zone lorsque tous les sas, portes et accès variables sont fermés. Aucun lien ne contourne donc une barrière d’énigme. Les rayonnages mobiles des archives sont exclus du placement et aucun nouveau côté de porte ne recouvre un souvenir.

Le gain est calculé sur les chemins les plus courts, avec les autres raccourcis et les portes ordinaires ouverts. Les sas à sens unique restent fermés au routage. Pour chaque ajout, un trajet entre deux repères démontre un retour vers un poste permanent, une commande ou une fin de mission ; les chiffres sont recalculés par un validateur indépendant.

### Vérifications exécutées

| Couverture | Contrôle |
| --- | --- |
| 25 niveaux | Parcours physiques existants, conditions des énigmes, solutions et transitions |
| 155 portes | Collision fermée, visite des deux côtés, traversée aller/retour, chemin au clic |
| Sauvegardes | 25 reprises avec les nouvelles portes ; indices, objets, essais partiels et collection préservés |
| Accès variables | Rayonnages, badges, phases, caméras et ponts ; états réversibles et absence de contournement |
| Collection | 250 ramassages et placements ; les 25 empreintes de grille sont inchangées |
| Interface et audio | Français/anglais, dimensions portrait/paysage, confort mobile et transitions audio |
| Documentation | 25 cartes PNG/PDF et 25 guides PDF/Markdown régénérés ; exemples et gains des nouvelles portes |

Les tests de parcours suivent des itinéraires de référence ; les tests des portes et des souvenirs utilisent des points de départ préparés afin de vérifier chaque cas isolément. Ils ne représentent pas une partie humaine unique à l’aveugle. Les durées des tests ne mesurent pas les performances en jeu.

Le contrôle visuel dans Godot a couvert les 25 niveaux et les panneaux en portrait/paysage. Le navigateur de contrôle ne fournit pas WebGL 2. Le rendu Web et la fluidité sur un téléphone physique ne sont donc pas validés dans cette session. Les dimensions des interfaces sont contrôlées dans Godot ; les PDF sont rendus et inspectés avant remise.
