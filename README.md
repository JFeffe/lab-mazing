# Lab-mazing — Le Labyrinthe de Folamour

Version 0.6 : jeu solo 3D isométrique, deux niveaux, français/anglais, déplacement au clic et au toucher.

Adresse prévue après activation de GitHub Pages : https://jfeffe.github.io/lab-mazing/

## Publication
Dans Settings → Pages → Build and deployment, sélectionner **GitHub Actions**. Ensuite lancer le workflow **Build and publish game** depuis Actions. Les prochains changements sur main reconstruisent et publient le jeu.

Le workflow télécharge Godot 4.5.1 et ses modèles officiels, importe le projet et exporte le jeu web sans threads. Aucun export manuel ni exécutable Windows à déposer dans ce dépôt.

## Développement
Ouvrir game/project.godot avec Godot 4.5.1. Pour exporter localement, installer ses modèles d’export puis exécuter `python scripts/export_web.py /chemin/vers/godot`.

## Commandes
Cliquer ou toucher une case explorée pour se déplacer ; toucher un objet pour l’examiner. Sac, journal, carte et pause sont accessibles par les boutons. La langue se choisit au menu. La sauvegarde reste dans le navigateur utilisé.

## Documents
Les cartes et solutions sont dans docs/ (attention aux révélations). Archives du projet : https://drive.google.com/drive/folders/1h3pAbUB9vy-9Ly24foVmbs8md3cSTqBJ

Le guide historique v0.6 décrit le ZIP avec export précompilé. Ce dépôt utilise désormais la compilation automatique décrite ci-dessus.

## Validation
Progression, navigation, interfaces et traductions vérifiées dans Godot. Le test réel sur Android/iPhone reste à effectuer.

Licences des composants tiers fournies à la racine.
