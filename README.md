# Lab-mazing — Le Labyrinthe de Folamour

Version 0.8 : jeu solo 3D isométrique, quatre niveaux, français/anglais, déplacement au clic et au toucher.

Jouer dans le navigateur : https://jfeffe.github.io/lab-mazing/

## Publication
Dans Settings → Pages → Build and deployment, sélectionner **GitHub Actions**. Ensuite lancer le workflow **Build and publish game** depuis Actions. Les prochains changements sur main reconstruisent et publient le jeu.

Le workflow télécharge Godot 4.5.1 et ses modèles officiels, importe le projet et exporte le jeu web sans threads. Aucun export manuel ni exécutable Windows à déposer dans ce dépôt.

## Développement
Ouvrir game/project.godot avec Godot 4.5.1. Pour exporter localement, installer ses modèles d’export puis exécuter `python scripts/export_web.py /chemin/vers/godot`.

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
