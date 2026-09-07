# Le Labyrinthe du Docteur Folamour - version 0.6

Deux niveaux d’exploration et d’énigmes, en français ou en anglais.
Version Windows et version web préparée pour GitHub Pages.

## Jouer

Sur Windows, ouvrir `Labyrinthe-Folamour.exe` dans le kit Windows.
Sur téléphone, ouvrir le lien GitHub Pages une fois le dépôt publié. Aucune
installation n’est nécessaire. Le premier chargement transfère le moteur et les
ressources du jeu ; patienter jusqu’au menu.

- Cliquer ou toucher un passage découvert : le personnage s’y rend.
- Cliquer ou toucher un objet : le personnage s’approche pour l’examiner.
- Le bouton **Examiner / Ramasser** agit sur l’élément à proximité.
- **Sac**, **Journal**, **Carte** et **Pause** restent accessibles à l’écran.
- Les fenêtres défilent verticalement si leur contenu dépasse l’écran.
- Un pavé numérique permet de saisir les codes sur téléphone et dans la version web.
- Sur PC, les touches WASD / ZQSD / flèches et E restent utilisables.
- Le clavier interrompt un déplacement automatique. Ouvrir un menu l’arrête aussi.
- **Langue / Language** permet de passer du français à l’anglais.

Le déplacement automatique ne traverse ni murs, ni portes fermées, ni sas.
Il ne planifie pas de trajet à travers les zones encore inconnues. Pour aller plus
loin, avancer vers une case visible, puis choisir une nouvelle destination.
Le franchissement d’un sas reste une action explicite, dans le sens autorisé.

La sauvegarde web appartient au navigateur et à l’adresse du jeu. Elle n’est pas
synchronisée avec Windows ou avec un autre appareil. Conserver le même navigateur
et la même adresse pour reprendre. Les sauvegardes Windows 0.4 / 0.5 restent compatibles.

## Changements 0.6

- Déplacement au clic et au toucher, avec recherche de chemin et repère de destination.
- Interface adaptée aux écrans étroits, fenêtres défilantes et pavé numérique.
- Références visibles dans le sac et les entrées du journal, y compris les anciennes.
- Témoins des mécanismes : rouge = inactif, ambre = pièces installées mais réglage à faire,
  vert = activé. Les emplacements remplis prennent une teinte dorée.
- Objets, indices, mécanismes et portes mieux distingués sur la carte et dans le décor.
- Accessoires muraux et ambiances sonores discrètes par secteur, désactivables dans Pause.
- Sons au format WAV et export web sans threads ; ombres désactivées sur le web.
- Départ du niveau 2 décalé à la case (1, 2), devant le terminal 100, pour éviter que
  le personnage soit superposé au terminal. Les énigmes et leurs solutions sont inchangées.

## Publier sur GitHub Pages

L’archive GitHub contient les sources **game/**, l’export jouable **web/**, les
documents **docs/** et le workflow **.github/workflows/pages.yml**.
Le jeu web est déjà exporté : aucune compilation n’est nécessaire pour ce premier déploiement.

1. Créer un dépôt GitHub destiné à ce projet, ou utiliser un dépôt existant approprié.
2. Extraire l’archive GitHub. Envoyer tout son contenu avec Git ou GitHub Desktop,
   en conservant `.github/workflows/pages.yml`. Le fichier WASM dépasse la limite
   d’envoi de l’interface web GitHub : utiliser Git / GitHub Desktop.
3. Dans le dépôt : **Settings > Pages > Build and deployment > Source : GitHub Actions**.
4. Pousser sur la branche **main**. Si le premier envoi précédait l’activation de Pages,
   ouvrir **Actions > Publish playable web build > Run workflow**.
5. Attendre la réussite du workflow. Ouvrir l’URL indiquée par le déploiement
   `github-pages`, puis partager cette URL avec l’ami qui testera le jeu.

Exemple de commandes, depuis le dossier extrait (remplacer le nom du dépôt) :

```sh
git init
git add .
git commit -m "Prototype Folamour 0.6 - click and touch"
git branch -M main
git remote add origin https://github.com/VOTRE-COMPTE/VOTRE-DEPOT.git
git push -u origin main
```

Ce kit n’a pas été poussé sur un dépôt et n’a pas encore d’URL publique de jeu.
Aucun compte GitHub de joueur n’est nécessaire pour visiter une publication Pages accessible.

## Refaire l’export après une modification

Installer Godot **4.5.1 standard** et les modèles d’exportation officiels de la même version.
Modifier le projet dans `game/`, puis lancer :

```sh
python scripts/export_web.py /chemin/vers/Godot
```

Sous Windows, remplacer ce chemin par celui du moteur Godot. Puis envoyer les sources
et les nouveaux fichiers `web/` sur GitHub. Le workflow publie **web/** ; il ne recompile
pas les sources. Une modification de `game/` seule ne met donc pas à jour le jeu en ligne.

Pour un essai local du web : `python -m http.server 8000 --directory web`, puis ouvrir
`http://localhost:8000`. Ne pas ouvrir `index.html` par double-clic.

## Test avec un nouveau joueur

Faire le premier essai sans montrer les solutions. Ne pas expliquer immédiatement
un mécanisme : demander d’abord « Qu’est-ce que tu essaies de faire ? ».

Noter : modèle du téléphone, navigateur, langue, portrait/paysage et niveau testé.
Pour chaque difficulté, relever le repère du jeu ou les coordonnées et le comportement attendu.

1. Commencer une partie et comprendre le déplacement sans explication orale.
2. Toucher un passage, changer de destination, essayer une case derrière une porte fermée.
3. Ramasser un objet, lire un indice, retrouver leurs références dans le journal.
4. Sur le niveau 1, saisir puis corriger un code avec le pavé numérique.
5. Tourner le téléphone. Le menu Pause apparaît ; reprendre et vérifier la progression.
6. Activer un mécanisme. Demander au joueur ce qui lui indique que l’action a réussi.
7. Au niveau 2, retrouver comment fabriquer le relais sans montrer la cheatsheet.
8. Ouvrir un raccourci après avoir visité physiquement les deux côtés du mur.
9. Changer de langue, revenir au menu, recharger la page et reprendre la partie.
10. Noter les passages répétitifs, les hésitations et les éventuels ralentissements.

Retour à recopier :

- Appareil / navigateur / langue :
- Niveau / repère / coordonnées :
- Action tentée :
- Ce qui s’est produit :
- Ce qui était attendu :
- Capture facultative :
- Durée approximative du niveau :
- Énigme préférée / moins intéressante :

Le test humain n’a pas été réalisé par un nouveau joueur à ce stade.

## Validation effectuée

- Parcours niveau 1 : collisions, portes, sas, raccourcis, objets et sauvegarde/reprise.
- Parcours niveau 2 : 897 cases, assemblages, molettes, transition et fin de campagne.
- Parcours automatique du niveau 2 : chemin vers les objets, interactions et sortie.
- Refus des destinations inconnues, des portes fermées et des sas en navigation automatique.
- Saisie du code 4726 par les boutons du pavé numérique puis ouverture de la porte.
- Français / anglais, anciens journaux, préférence de langue et conservation des états.
- Touches tactiles synthétiques dans Godot, clic projeté vers le sol et captures aux
  dimensions 390 x 844, 844 x 390 et sur PC.

Tests réalisés avec Godot sous Linux. Le navigateur distant ne peut pas ouvrir le
serveur local de cet environnement : l’exécution de l’export web dans un navigateur,
la sauvegarde web réelle, les performances Android/iPhone et le lancement Windows
restent à confirmer après publication / sur les appareils cibles.

## Solutions rapides - SPOILERS

### Niveau 1

1. Lire les fragments 38 et 02. Saisir **4726** à l’accès 03.
2. Utiliser la clé 33 dans la réserve 29 ; récupérer le disque S (Soleil = 6).
3. Lire 53 et 54. À la porte 87 : CUVE, BOBINE, FILTRE, LENTILLE = **8512**.
   Récupérer le disque E (Étoile = 9).
4. Utiliser l’artéfact 93 dans la chambre 19 ; récupérer le disque L (Lune = 4).
5. Lire la calibration 20 : LUNE, SOLEIL, ÉTOILE.
6. Franchir un sas 50 depuis le nord avec les trois disques et la fiche 20 archivée.
7. Installer le fusible F dans le tableau 65.
8. Installer les trois disques au pupitre 00, puis saisir **469**.

### Niveau 2

1. 101 + 102, assemblés à 103 : clé à douille. Utiliser cette clé à 104 pour ouvrir 105.
2. Installer le volant 201 au collecteur 206.
3. Lire 202, 203, 204 et 205. RETOUR = CUVE = 2, DÉPART = POMPE = 3,
   PURGE = FILTRE = 1. Régler **2 / 3 / 1** : ouverture de 207.
4. 208 + 209, assemblés à 210 : relais de puissance.
5. 301 + 302, installés à 303 : contrepoids opérationnel.
6. Installer le relais à 304 ; actionner 306. Aucun code supplémentaire.

Documents de référence classés dans le Drive du projet, dossier **Version 0.6 - Cheatsheets et test web**.
Les exécutables n’y sont pas déposés.

## Références techniques et crédits

- Godot 4.5, export web : https://docs.godotengine.org/en/4.5/tutorials/export/exporting_for_web.html
- GitHub Pages, workflow : https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- Moteur Godot et police DejaVu : licences tierces incluses dans le kit.
