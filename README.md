# Lab-mazing — Le Labyrinthe de Folamour

Version 0.9 : jeu solo 3D isométrique, chapitre 1 complet (cinq niveaux), français/anglais, déplacement au clic et au toucher.

Jouer dans le navigateur : https://jfeffe.github.io/lab-mazing/

## Publication
Dans Settings → Pages → Build and deployment, sélectionner **GitHub Actions**. Ensuite lancer le workflow **Build and publish game** depuis Actions. Les prochains changements sur main reconstruisent et publient le jeu.

Le workflow télécharge Godot 4.5.1 et ses modèles officiels, importe le projet et exporte le jeu web sans threads. Aucun export manuel ni exécutable Windows à déposer dans ce dépôt.

## Développement
Ouvrir game/project.godot avec Godot 4.5.1. Pour exporter localement, installer ses modèles d’export puis exécuter `python scripts/export_web.py /chemin/vers/godot`.

## Nouveautés v0.9
Le niveau 5 conclut le chapitre 1 : hall central, ailes ouest et est explorables dans les deux ordres, puis aile nord verrouillée. Trois nouvelles manipulations : dosage 5/3 litres, transfert de trois disques et rotors couplés. 18 repères, trois secrets, six raccourcis.

Folamour apparaît en 3D et en portrait au début, lance son défi impossible, puis revient féliciter le joueur et lui proposer un stage non rémunéré. Le menu « Choisir un chapitre » propose le chapitre 1 (niveaux 1 à 5) ; le chapitre 2 reste indisponible. « Sélection de niveau / test » permet les essais isolés après confirmation du remplacement de la sauvegarde.

Les sauvegardes v0.8 restent compatibles : reprendre un niveau 4 terminé permet de continuer au niveau 5. Les volumes, disques, orientations et objets installés sont sauvegardés. Toutes les configurations atteignables des trois nouvelles énigmes permettent encore de réussir.

Génération reproductible : `python scripts/build_level5.py`. Validation : `python game/tests/validate_level5.py`, puis Godot avec `--headless --path game --fixed-fps 60 --script res://tests/verify_level5.gd`.

## Nouveautés v0.8
Niveau 4 : département des essais, 23 repères, trois secrets, six raccourcis et un labyrinthe avec des boucles.

- Balance interactive à quatre masses et deux plateaux.
- Séquence de cinq symboles à déduire de trois rapports.
- Aimant et corde pour récupérer une pièce hors de portée.
- Quatre inverseurs commandant cinq voyants à allumer ensemble.

Les manipulations sont réversibles et sauvegardées, y compris en cours d’énigme. Les objets restent installés après une réinitialisation. Les sauvegardes v0.7 sont compatibles : reprendre un niveau 3 terminé permet de continuer au niveau 4. L’accès direct au niveau 4 est également disponible au menu.

## Commandes
Cliquer ou toucher une case explorée pour se déplacer ; toucher un objet pour l’examiner. Sac, journal, carte et pause sont accessibles par les boutons. La langue se choisit au menu. La sauvegarde reste dans le navigateur utilisé.

## Documents
Cartes, solutions et résumé v0.8 : https://drive.google.com/drive/folders/1ZHkHMa2LCTvpp0QWtD-yezvawd5hWacm

Les anciens documents restent dans docs/ et le dossiers Drive des versions précédentes. Pour régénérer les documents du niveau 4 : `python scripts/document_level4.py /chemin/de/sortie` (Pillow, ReportLab).

Le guide historique v0.6 décrit le ZIP avec export précompilé. Ce dépôt utilise désormais la compilation automatique décrite ci-dessus.

## Validation
Progression, navigation, interfaces et traductions vérifiées dans Godot. La v0.6 a été testée sur cellulaire par le joueur. La v0.8 vérifie également les trois nouvelles énigmes en français/anglais, les panneaux en portrait/paysage, l’unicité des solutions et la reprise de chaque mécanisme partiellement résolu.

Licences des composants tiers fournies à la racine.
