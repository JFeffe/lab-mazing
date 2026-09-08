# Lab-Mazing v0.18 — Le complexe de la certitude

Cinq niveaux jouables, quinze nouveaux essais, quinze notes secrètes et seize raccourcis. Français / anglais.

[Jouer](https://jfeffe.github.io/lab-mazing/)

## Les cinq missions

### 1. Bienvenue, vous habitez ici

Une gare en éventail : trois guichets au nord, un hall commun, puis deux labyrinthes de maintenance au sud. Les badges commandent les trois guichets ; le sas 111 mène aux dossiers et le sas 112 aux tubes.

- Depuis 203 : résident → lire 210 → retour ; technicien → lire 211 → retour ; inspecteur → lire 212 → retour. Choisir inspecteur et valider.
- Dossier D ; clé triangle ; quai C ; tampon ajourné. Valider.
- A → B ; B → X ; C → Y ; D → C. Tester puis valider.

### 2. Le quartier témoin

Une rue verticale dessert trois maisons à horaires décalés, à l’ouest d’un jardin inaccessible. Deux quartiers labyrinthiques occupent le nord-est et le sud-est, reliés par une ruelle étroite.

- Matin → lire 210 → retour ; midi → lire 211 → retour ; soir → lire 212 → retour. Régler MIDI et valider.
- Ada 12 ; Boris 14 ; Cyril 8 ; Daria 10. Valider.
- Ada ; conserver pluviomètre et vitre réelle ; écarter radio et rapport de Boris. Valider.

### 3. Le ministère des regards

Deux anneaux de surveillance entourent une tour centrale. Depuis l’anneau extérieur, trois niches à l’est se ferment selon les caméras. Un pont ouest mène aux montages ; une entrée nord mène aux sources.

- A EST ; B SUD (ou NORD/EST) ; C NORD. Visiter 210, 211 et 212. Retour au 203, tester puis valider.
- B → D → A → C → E. Tester puis valider.
- R1-R3 : MIROIR ; R4-R5 : capteur ; familles physiques : 1. Valider.

### 4. La fabrique du lendemain

Trois chaînes en tresses traversent le complexe : énergie à l’ouest, convoyeurs au centre, assemblage à l’est. Les passerelles changent de hauteur sur le plan ; les ateliers latéraux forment des boucles de retour.

- A=2 ; B=3 ; C=1. Valider.
- Aiguillages 1=1 ; 2=0 ; 3=1. Tester : D → 1 → M → 2 → R → 3 → C → S. Valider.
- Socle → moteur → guide → courroie → capot → contrôle. Tester puis valider. Guide et moteur peuvent être inversés.

### 5. L’unanimité absolue

Une salle de décision centrale dessert cinq bureaux : un au nord, deux à l’ouest et deux à l’est. Les couloirs latéraux contournent les bureaux, tandis que les deux sas gardent les réseaux du conseil.

- Habitat : dossier ; météo : pluviomètre ; sécurité : film ; industrie : commande ; transport : ascenseur. Valider.
- A → X ; B → A ; C → Y ; D → E ; E → C. Tester puis valider.
- A+B aller (2), A retour (1), C+D aller (8), B retour (2), A+B aller (2). Total 15. Valider.

## Validation et recherches

Les parcours physiques, les quinze solutions via les commandes, les sauvegardes partielles, les indices et les transitions sont vérifiés dans Godot 4.5.1. Les panneaux sont contrôlés en 390×844 et 844×390, en français et en anglais. Les contraintes combinatoires sont également vérifiées indépendamment. Test sur appareil réel à effectuer.

Inspirations méthodologiques : [Matthew VanDevander, concepteur de Taiji](https://taiji-game.com/2022/02/23/84-how-i-design-puzzles/) — construire autour d’une déduction, accepter les solutions alternatives qui préservent l’idée ; [Clara Fernandez-Vara, GDC](https://gdcvault.com/play/1013851/Puzzle-Writing-Best) — fournir les indices nécessaires et relier les énigmes au récit. Les données, textes et plans de ce chapitre sont originaux ; le passage du sceau adapte le classique problème du pont et de la lampe.

## Progression narrative

La cité souterraine confond les prévisions de MIROIR et le réel. Les badges, les routines, les caméras et les usines forment une administration toujours plus démesurée. Le joueur remplace les copies par des observations. La perte de certitude déclenche le protocole de sérénité maximale et révèle les silhouettes du programme HORIZON, futur chapitre 5.

## Contenu

Chaque dossier de niveau contient la carte exacte en PNG et PDF A3, ainsi que le guide détaillé en PDF A4 et Markdown. Les documents contiennent les solutions. Les versions précédentes restent archivées.
