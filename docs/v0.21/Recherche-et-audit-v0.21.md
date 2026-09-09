## Le dossier du sujet 16

### Conception, recherche et audit des 25 niveaux • 9 septembre 2026

Objectif : récompenser la curiosité, donner une présence plus sensible au docteur et différencier les cinq chapitres, en conservant toutes les grilles et toutes les énigmes. Cette édition ajoute 250 souvenirs fixes, quinze archives et un dossier de progression. Les changements restent compatibles avec les sauvegardes existantes.

La demande de dix récompenses dans de longues impasses rencontre une contrainte réelle : plusieurs niveaux contiennent peu de branches terminales et les niveaux globaux 18 et 22 n’en possèdent aucune. Le choix retenu consiste à préserver le tracé et le nombre de récompenses, puis à compléter les meilleurs fonds d’impasse par des recoins calmes. Cette concession est explicite et mesurée, plutôt que de présenter tous les emplacements comme de longues impasses.

| Résultat | Quantité |
| --- | --- |
| Niveaux / chapitres | 25 / 5 |
| Souvenirs fixes | 250 ; exactement 10 par niveau |
| Fonds d’impasse | 196, dont 129 branches de 4 à 24 pas et 67 branches de 2 pas |
| Recoins de couloir | 54 |
| Archives narratives | 15 ; seuils de 10, 25 et 50 par chapitre |
| Silhouettes de collection | 5, avec 1 à 5 marques selon la mission |
| Grilles, énigmes et raccourcis modifiés | 0 |

Le dossier est une trace de l’aventure en cours. Il réunit la collection, les étapes terminées, les énigmes et raccourcis comptabilisés, les indices consultés et les observations originales de Folamour. La collection ne donne aucun pouvoir, ne remplace aucun indice et ne devient jamais une condition de fin.

## Recherche et décisions de conception

### Récompenser une exploration volontaire

La présentation de Leah Miller à la GDC 2019 distingue les objets finis, placés à des endroits précis, des ressources répétitives. Elle relie leur réussite à la cohérence entre art, récit et jeu, et recommande de récompenser l’exploration et l’observation sans interrompre le rythme. Elle signale notamment la répétition fastidieuse et les objets incongrus parmi les écueils. [1]

Application à Folamour — décision de conception : chaque détour rapporte une petite pièce d’archive liée à son chapitre. Le ramassage confirme immédiatement la trouvaille, sans ouvrir une fenêtre. Les récompenses sont uniques, ne réapparaissent pas après sauvegarde et ne nécessitent aucun retour obligatoire. Les nouvelles archives donnent une raison narrative à la collection ; elles n’accordent pas de monnaie artificielle ou de puissance sans rapport avec le jeu.

Le nombre dix est une contrainte demandée pour chaque niveau, pas une conclusion de la recherche. Son intérêt pratique est une progression compréhensible. Son coût est de devoir utiliser des branches courtes ou des recoins dans les cartes en anneaux. Le dossier de reprise permet de revenir compléter une mission terminée sans perdre les trouvailles antérieures. Le joueur voit explicitement que ses énigmes recommenceront.

### Lisibilité et mouvement discret

Les Game Accessibility Guidelines recommandent d’éviter les scintillements et les motifs visuels répétitifs qui provoquent une gêne, et de proposer la désactivation des effets concernés. [2] Application choisie : les nouveaux gestes du docteur sont lents, sans flash ; une option indépendante coupe ces animations. Les silhouettes et les marques de mission complètent les couleurs. La collection ne dépend donc pas uniquement de la distinction turquoise, ocre, violet, bleu ou cuivre.

### Budget graphique

La documentation Godot 4.5 décrit les gains du masquage des objets lointains et le coût des surfaces transparentes. [3] Application choisie : petites formes opaques, maillages et matériaux partagés, aucun nouvel éclairage dynamique et intégration des décors au masquage existant. Les accessoires n’ajoutent pas de collisions et ne peuvent pas modifier les itinéraires physiques. Cette architecture vise la sobriété ; elle ne constitue pas une mesure de fréquence d’image sur téléphone.

## Identités des chapitres et Folamour

| Chapitre | Collection | Langage visuel |
| --- | --- | --- |
| 1 — Laboratoire | Ampoule témoin | Turquoise ; flacons, laboratoire artisanal |
| 2 — Stage | Tampon de service | Ocre ; dossiers, rangement administratif |
| 3 — Prévoyance | Rouage de prévoyance | Violet ; cadrans et mécanismes prédictifs |
| 4 — Certitude | Prisme MIROIR | Bleu ; surfaces jumelles et symétrie |
| 5 — HORIZON | Capsule de retour | Cuivre ; conduites, protection et retour |

Les palettes s’intègrent aux couleurs déjà présentes par secteur, afin de conserver les repères spatiaux de chaque mission. L’ambiance lumineuse et le fond suivent le chapitre. Les accessoires sont placés au-dessus des murs et les incrustations de sol restent minces. Le grand décor narratif du dernier chapitre est conservé. Les silhouettes de collection sont distinctes ; le nombre de petites marques varie de un à cinq au sein du chapitre.

### Une présence liée à la situation

Le docteur tourne doucement la tête et le corps vers le sujet lorsqu’il approche. Une respiration légère et des gestes de bras rendent sa posture moins figée ; les gestes deviennent un peu plus amples pendant ses remarques. Les copies décoratives utilisent aussi ces mouvements. Les discussions de fin conservent leurs conditions et leurs textes propres à chaque mission.

Quatre familles de réactions sont écrites dans les deux langues : rencontre, réussite, erreur et découverte. Leur ton évolue du laboratoire ironique vers la conclusion plus humaine. Chaque déclenchement est mémorisé pour éviter une relance continue en restant près du docteur. Les observations identiques sont regroupées dans le dossier. Le premier, cinquième et dixième souvenir d’un niveau peuvent déclencher une remarque ; seules les remarques courtes s’affichent dans le HUD.

Les commentaires et les animations disposent de deux réglages séparés dans la pause. Couper les commentaires masque leur affichage temporaire, tout en laissant leurs observations consultables. Les menus interrompent le temps de jeu et les nouveaux mouvements. Les sous-titres du dossier et des nouvelles répliques suivent la langue sélectionnée sans réécrire les données sauvegardées.

## Placement : méthode et niveaux 1 à 15

Le placement utilise les cases de sol et leurs quatre voisines. Les positions actuelles des fins de niveau sont appliquées avant l’analyse. Sont exclus : événements, départ, accès variables, décors narratifs réservés et côtés des raccourcis. Chaque candidat reste à trois cases Manhattan et à cinq pas de chemin au minimum des éléments réservés.

Une branche terminale est suivie jusqu’à sa première jonction ; elle doit être vide d’interaction. Les vrais fonds sont prioritaires, puis leur profondeur, leur éloignement du contenu et leur dispersion. Deux souvenirs restent à huit pas de chemin et quatre cases Manhattan au minimum. L’ordre des égalités est stable : relancer le générateur produit les mêmes coordonnées et identifiants.

| Niveau global | Chapitre / niveau | Impasses | Recoins | Écart min. (pas) |
| --- | --- | --- | --- | --- |
| 1 | 1 / 1 | 10 | 0 | 6 |
| 2 | 1 / 2 | 10 | 0 | 6 |
| 3 | 1 / 3 | 10 | 0 | 10 |
| 4 | 1 / 4 | 10 | 0 | 6 |
| 5 | 1 / 5 | 10 | 0 | 8 |
| 6 | 2 / 1 | 10 | 0 | 12 |
| 7 | 2 / 2 | 10 | 0 | 8 |
| 8 | 2 / 3 | 9 | 1 | 5 |
| 9 | 2 / 4 | 10 | 0 | 8 |
| 10 | 2 / 5 | 5 | 5 | 6 |
| 11 | 3 / 1 | 10 | 0 | 6 |
| 12 | 3 / 2 | 10 | 0 | 8 |
| 13 | 3 / 3 | 10 | 0 | 8 |
| 14 | 3 / 4 | 2 | 8 | 8 |
| 15 | 3 / 5 | 10 | 0 | 5 |

Les valeurs mesurent la grille normale, sans raccourcis. Une impasse de deux pas est signalée comme telle dans le guide. L’algorithme donne priorité aux branches longues disponibles, sous les contraintes de dégagement et de séparation. Les coordonnées complètes, profondeur et distances sont aussi fournies dans un CSV de 250 lignes.

## Placement : niveaux 16 à 25 et cas particuliers

| Niveau global | Chapitre / niveau | Impasses | Recoins | Écart min. (pas) |
| --- | --- | --- | --- | --- |
| 16 | 4 / 1 | 6 | 4 | 8 |
| 17 | 4 / 2 | 9 | 1 | 8 |
| 18 | 4 / 3 | 0 | 10 | 8 |
| 19 | 4 / 4 | 10 | 0 | 10 |
| 20 | 4 / 5 | 6 | 4 | 6 |
| 21 | 5 / 1 | 7 | 3 | 8 |
| 22 | 5 / 2 | 0 | 10 | 5 |
| 23 | 5 / 3 | 4 | 6 | 6 |
| 24 | 5 / 4 | 10 | 0 | 6 |
| 25 | 5 / 5 | 8 | 2 | 8 |

Niveaux 18 et 22 : les anneaux offrent déjà des retours directs et ne présentent aucun fond d’impasse. Les dix récompenses de chacun sont réparties dans des sections retirées, contre les limites des couloirs, à distance des postes. Le guide les nomme « recoins », sans inventer une branche terminale.

Niveau 1 : les sas à sens unique restent irréversibles. Les guides demandent de visiter les souvenirs du secteur nord avant de les franchir. Le dossier donne ensuite la possibilité de rejouer le niveau terminé ; aucun souvenir manqué n’empêche de continuer la campagne.

Niveaux à accès variables : les collectibles ne commandent aucune porte. Ils restent des cases traversables après ouverture normale du secteur. Les validators de progression continuent de vérifier les accès pilotés par les postes et les tests physiques des 25 niveaux restent inchangés. Les 250 ramassages ont en plus été testés avec le routage réel depuis une case adjacente praticable.

Les dix récompenses sont ajoutées séparément aux données d’événements. Les grilles, coordonnées des énigmes, raccourcis et objets requis de la version 0.20 sont inchangés octet pour octet dans le dépôt. Un manifeste conserve une empreinte de chaque carte : une modification ultérieure oblige à revalider le placement.

## Vérifications et portée des résultats

| Contrôle | Résultat |
| --- | --- |
| Placement indépendant | 250 identifiants uniques ; sol accessible ; distances et branches vérifiées |
| Ramassage physique | 250 / 250 via demande de déplacement, marche et interaction |
| État des énigmes | Ramasser ne modifie ni le sac ni les validations |
| Sauvegarde | Collection complète, reprise, ancienne sauvegarde et nouvelle aventure testées |
| Rejouer | Collection conservée ; objets déjà trouvés masqués ; énigmes réinitialisées |
| Interface | Dossier FR/EN ; 390×844, 844×390 et 1280×800 ; débordements contrôlés |
| Folamour | Rotation, respiration, désactivation et archive des remarques testées |
| Régressions | 23 tests Godot existants réussis ; nouveau test ajouté au workflow |
| Publication | Compilation, export web et suite GitHub Actions réussis |

Limite visuelle : le navigateur de contrôle disponible n’expose pas WebGL 2. Le rendu 3D en navigateur et la fluidité sur un téléphone physique ne sont donc pas validés par cette session. Les vérifications d’interface portent sur les dimensions calculées par Godot ; les cartes et les PDF ont été rendus et relus visuellement. Ces contrôles ne remplacent pas une appréciation humaine du rythme ou du plaisir de collection.

Les tests physiques des souvenirs démarrent depuis des cases adjacentes accessibles ; ils vérifient les collisions locales et le ramassage. La possibilité de rejoindre leurs secteurs est contrôlée séparément sur le graphe, avec les régressions de progression et d’accès variables. Cette distinction évite de présenter les 250 ramassages comme un parcours intégral unique de collection.

### Références primaires consultées

[1] Leah Miller, GDC 2019, Rewarding Exploration with Collectables and Gatherables. Diapositives : objets finis (4), cohérence (11), écueils (18), exploration (20–23), lisibilité (34). https://media.gdcvault.com/gdc2019/presentations/Miller_Leah_Rewarding_Exploration_With.pdf

[2] Game Accessibility Guidelines, Avoid flickering images and repetitive patterns. https://gameaccessibilityguidelines.com/avoid-flickering-images-and-repetitive-patterns/

[3] Godot 4.5 Documentation, Optimizing 3D performance. https://docs.godotengine.org/en/4.5/tutorials/performance/optimizing_3d_performance.html
