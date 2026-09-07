# Lab-mazing — Le Labyrinthe de Folamour

Version 0.7 : jeu solo 3D isométrique, trois niveaux, français/anglais, déplacement au clic et au toucher.

Jouer dans le navigateur : https://jfeffe.github.io/lab-mazing/

## Publication
Dans Settings → Pages → Build and deployment, sélectionner **GitHub Actions**. Ensuite lancer le workflow **Build and publish game** depuis Actions. Les prochains changements sur main reconstruisent et publient le jeu.

Le workflow télécharge Godot 4.5.1 et ses modèles officiels, importe le projet et exporte le jeu web sans threads. Aucun export manuel ni exécutable Windows à déposer dans ce dépôt.

## Développement
Ouvrir game/project.godot avec Godot 4.5.1. Pour exporter localement, installer ses modèles d’export puis exécuter `python scripts/export_web.py /chemin/vers/godot`.

## Nouveautés v0.7
Niveau 3 : département d’optique, 23 repères, trois secrets, six raccourcis, assemblage et deux énigmes à indices croisés. Accessible après le niveau 2 ou depuis le menu.

Sauvegarde toutes les quatre secondes et après les actions, copie de secours, résumé de la partie au menu, statut en pause, destination nommée et itinéraire sur la carte. Les sauvegardes v0.6 restent compatibles ; elles restent propres au navigateur et à l’appareil.

## Commandes
Cliquer ou toucher une case explorée pour se déplacer ; toucher un objet pour l’examiner. Sac, journal, carte et pause sont accessibles par les boutons. La langue se choisit au menu. La sauvegarde reste dans le navigateur utilisé.

## Documents
Cartes, solutions et résumé v0.7 : https://drive.google.com/drive/folders/13YL7ySZVE24gNmXFySOb0l8iHPqOXP-8

Les anciens documents restent dans docs/ et le dossier Drive v0.6. Pour régénérer les documents du niveau 3 : `python scripts/document_level3.py /chemin/de/sortie` (Pillow, ReportLab).

Le guide historique v0.6 décrit le ZIP avec export précompilé. Ce dépôt utilise désormais la compilation automatique décrite ci-dessus.

## Validation
Progression, navigation, interfaces et traductions vérifiées dans Godot. La v0.6 a été testée sur cellulaire par le joueur. La v0.7 ajoute des tests de disposition portrait/paysage, de destination et de reprise.

Licences des composants tiers fournies à la racine.
