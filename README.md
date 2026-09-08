# Lab-mazing — Le Labyrinthe de Folamour

Version 0.14 : jeu solo 3D isométrique, chapitre 1 complet et trois missions du chapitre 2, français/anglais, déplacement au clic et au toucher.

Jouer dans le navigateur : https://jfeffe.github.io/lab-mazing/

## Publication
Dans Settings → Pages → Build and deployment, sélectionner **GitHub Actions**. Ensuite lancer le workflow **Build and publish game** depuis Actions. Les prochains changements sur main reconstruisent et publient le jeu.

Le workflow télécharge Godot 4.5.1 et ses modèles officiels, importe le projet et exporte le jeu web sans threads. Aucun export manuel ni exécutable Windows à déposer dans ce dépôt.

## Développement
Ouvrir game/project.godot avec Godot 4.5.1. Pour exporter localement, installer ses modèles d’export puis exécuter `python scripts/export_web.py /chemin/vers/godot`.

## Nouveautés v0.14
**Le courrier interne** est le niveau 3 du chapitre 2 (numéro interne 8). Folamour confie une livraison : identifier le seul colis plus lourd parmi six, acheminer une capsule par trois aiguillages, puis reconstituer une adresse à partir d’une étiquette, d’un annuaire et d’un avis de déménagement.

Le nouveau circuit entoure deux entrepôts et une aile d’expédition. Il compte 19 repères, trois secrets et six raccourcis sans contournement des portes verrouillées. Parcours de référence : 661 → 633 pas avec révélation progressive des raccourcis.

Le réseau utilise un schéma 2D animé uniquement pendant les essais. Pesées libres, capsule réutilisable, commandes réversibles et sauvegardes partielles. Les réglages de netteté mobile, les corrections audio et la vitesse +30 % sont conservés.

Le menu sépare désormais les chapitres et leurs niveaux. Les trois missions du chapitre 2 sont accessibles directement. Les sauvegardes et confirmations reprennent ces noms. Après les photocopies, « Passer au courrier interne » conserve les bilans.

Données : `python scripts/build_level8.py`. Vérification : `python game/tests/validate_level8.py`, puis Godot `--headless --path game --fixed-fps 60 --script res://tests/verify_level8.gd`. Documents : `python scripts/document_level8.py /chemin/de/sortie`.

[Carte et cheatsheet v0.14](https://drive.google.com/drive/folders/1W1RC8XbgvQnBSvdAy9-I0HZruYXrlkQn).

## Nouveautés v0.13
Le service des photocopies est la deuxième mission du chapitre 2 (niveau global 7). L’accueil central dessert trois ailes : préparation, archives et copies. Trois mécanismes distincts permettent de superposer des calques, classer des dossiers selon une directive validée et transformer une image par rotation ou miroir. Folamour introduit la mission et termine sur sa demande de recto verso.

Les six raccourcis évitent 88 pas sur le parcours de référence (747 → 659), après visite physique de leurs deux côtés. Les deux portes ne peuvent pas être contournées. Trois archives secrètes, objectifs et indices progressifs FR/EN, sauvegardes des essais et bilans des missions précédentes.

La vitesse passe de 7 à 9,1 unités/s (+30 %) dans tous les niveaux, au clavier et sur les trajets au clic/toucher. Les corrections audio et les réglages de netteté/stabilité mobiles de v0.12.4 sont conservés ; aucun bruit de pas.

Accès : après la mission des serres, « Passer aux photocopies », ou menu de test → Niveau 7. La troisième mission reste à venir.

Données : `python scripts/build_level7.py`. Validation : `python game/tests/validate_level7.py` et Godot `--headless --path game --fixed-fps 60 --script res://tests/verify_level7.gd`. Documents : `python scripts/document_level7.py /chemin/de/sortie`.

[Cartes et solutions v0.13](https://drive.google.com/drive/folders/1Xt0fg-rjPgT0MS-oH0x1QC_dWd52Rj8p).

## Nouveautés v0.12
Le chapitre 2 commence avec **Les serres expérimentales**, première mission du stage non rémunéré. Folamour demande un café : le joueur rétablit l’irrigation avec quatre coudes orientables, fait pousser une liane-pont, récolte quatre ingrédients et compose un mélange selon trois propriétés. Le nouveau labyrinthe possède une serre centrale, quatre branches, des parois vitrées, 20 repères, trois secrets et six raccourcis de retour.

Accès depuis « Choisir un chapitre » ou « Accepter le stage — Chapitre 2 » à la fin du niveau 5. Les bilans précédents sont conservés en poursuivant l’aventure. La sélection de test utilise le numéro global 6. La suite du chapitre 2 reste annoncée comme indisponible.

Les trois nouvelles manipulations sont réversibles et sauvegardées, avec objectifs et indices progressifs FR/EN. Le parcours de référence passe de 741 à 653 pas avec les raccourcis révélés au fil de la marche ; chaque lien économise encore au moins 12 pas avec les autres ouverts. Aucun ne contourne la passerelle verrouillée.

Données : `python scripts/build_level6.py`. Vérification : `python game/tests/validate_level6.py`, puis Godot `--headless --path game --fixed-fps 60 --script res://tests/verify_level6.gd`. Documents : `python scripts/document_level6.py /chemin/de/sortie`.

Cartes, solutions et résumé v0.12 : https://drive.google.com/drive/folders/1NI13ExWbDG9bNK3Hkqd6PydEJkyuQezn

## Nouveautés v0.11
Les cinq niveaux proposent des indices facultatifs en trois paliers : piste, méthode, puis solution annoncée. L’objectif actuel est consultable depuis le jeu, le journal et la pause ; les deux ailes du niveau 5 restent explorables dans les deux ordres. Les aides révélées sont sauvegardées sans modifier les énigmes.

Une composition originale de 48 secondes accompagne l’exploration à faible volume : piano électrique, basse et cloches légèrement étranges. Des sons ponctuent les pas, les portes, les machines et la fin du chapitre. Les réglages séparés (général, musique, effets, machines) sont persistants, avec coupure générale et interruption en arrière-plan. La musique s’atténue pendant la lecture. `scripts/compose_audio.py` permet de recréer les assets avec NumPy et ffmpeg, sans échantillons tiers.

Le dossier de candidature final additionne temps d’exploration, énigmes, raccourcis et aides des niveaux terminés. Les bilans historiques sans ces détails sont signalés comme partiels. Validation supplémentaire : `verify_chapter_polish.gd` (aides, objectifs, sauvegardes, anciens bilans, audio et disposition mobile FR/EN).

Documents v0.11 : https://drive.google.com/drive/folders/1zHdNMZROgU8dtWD_6bY5QsWSrvqi2HBO

## Nouveautés v0.10
Les 32 raccourcis des cinq niveaux sont réévalués pour réduire les retours dans les couloirs déjà explorés. Chaque passage économise au moins 12 pas entre ses deux côtés, même lorsque les autres raccourcis de sa zone sont ouverts. Les trajets de référence sont plus courts pour chacun des cinq niveaux ; `game/tests/shortcut_audit.json` conserve le détail avant/après et les conditions de mesure.

L’apparition conserve sa règle : passage physique des deux côtés du mur. Les liens ne contournent aucun verrou d’énigme ni sas à sens unique. À la reprise, les anciens identifiants sont recalculés à partir des cases réellement parcourues ; une position dans un ancien raccourci redevenu mur est replacée sur le sol connu le plus proche.

Validation : `python game/tests/validate_shortcuts.py` et Godot avec `--headless --path game --fixed-fps 60 --script res://tests/verify_shortcuts.gd`. Les cartes et guides complets des cinq niveaux sont générés avec `python scripts/document_campaign.py /chemin/de/sortie`. Les documents historiques restent archivés sous leurs versions.

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

### Correctif mobile v0.12.1

Partage des BoxMesh (serres : 4031 blocs / 54 ressources), limitation à 30 FPS sur écran tactile, résolution 3D plafonnée indépendamment des textes, décor distant masqué sans effacer la carte et verre opaque sur le Web. Énigmes, sauvegardes et solutions v0.12 conservées. Validation headless : parcours niveau 6, confort mobile, raccourcis, bilan de chapitre et partage des ressources des six niveaux. Les performances et les fermetures du navigateur restent à confirmer sur appareil réel.

### Correctif mobile v0.12.2

Suppression complète du bruit des pas. Sur appareil à pointeur tactile, plafonnement du ratio de pixels du canvas WebGL à 1, pour réduire aussi la mémoire des tampons 2D et intermédiaires que la baisse de résolution 3D seule ne limitait pas. Les commandes tactiles utilisent le même ratio que le dessin. La cause exacte du plantage navigateur signalé reste à confirmer sur le téléphone ; ces mesures réduisent sa charge mémoire.

### Correctif v0.12.3 — transitions audio Web

Les commandes de pause/reprise audio étaient envoyées à chaque image. Dans le backend samples de Godot 4.5.1, chaque reprise recrée une source Web Audio, même si elle joue déjà. Reproduction sur la classe JavaScript exportée : 600 reprises identiques créent 600 sources. Les commandes sont désormais envoyées uniquement lors d’un changement d’état ; le volume d’ambiance à zéro ne provoque plus une reprise immédiatement suivie d’une pause. Test de régression : 108000 mises à jour / deux transitions. La stabilité réelle du navigateur reste à confirmer sur les appareils concernés.

### Ajustement v0.12.4 — netteté mobile

Ratio de pixels tactile plafonné à 1,5 au lieu de 1 pour améliorer les textes et le décor. Résolution 3D à 85 % maximum et grand côté visé de 1152 pixels (contre 75 % / 960). Limite de 30 FPS, partage des modèles et correctif audio conservés.
