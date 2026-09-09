# Lab-mazing — Le Labyrinthe de Folamour

**[▶ Jouer au Labyrinthe de Folamour dans le navigateur](https://jfeffe.github.io/lab-mazing/)**

Version 0.22 : jeu solo 3D isométrique, cinq chapitres complets et vingt-cinq niveaux, français/anglais, déplacement au clic et au toucher.

## Publication
Pour chaque annonce de version sur GitHub, placer le lien **Jouer** en première ligne du corps de la publication, avant les nouveautés. Utiliser le [modèle d’annonce](.github/RELEASE_TEMPLATE.md) et conserver le lien juste sous le titre de ce README.

Dans Settings → Pages → Build and deployment, sélectionner **GitHub Actions**. Ensuite lancer le workflow **Build and publish game** depuis Actions. Les prochains changements sur main reconstruisent et publient le jeu.

Le workflow télécharge Godot 4.5.1 et ses modèles officiels, importe le projet et exporte le jeu web sans threads. Aucun export manuel ni exécutable Windows à déposer dans ce dépôt.

## Développement
Générer les ambiances originales avec `python3 scripts/compose_finale_audio.py`, puis ouvrir game/project.godot avec Godot 4.5.1. Pour exporter localement, installer ses modèles d’export puis exécuter `python scripts/export_web.py /chemin/vers/godot`.

## Nouveautés v0.22 — Retours utiles et audit complet

- 43 portes secrètes ajoutées sur 20 niveaux : 155 passages au total. Chaque ajout évite au moins 20 pas, jusqu’à 72, même avec les autres raccourcis et verrous ouverts. Les exemples documentés mènent à un poste permanent, une commande ou Folamour.
- Les 112 portes précédentes gardent leurs positions et leurs identifiants. Une nouvelle porte se révèle après visite physique des deux côtés, y compris à la reprise si les deux cases avaient déjà été parcourues.
- Clic sur une sortie murale : le personnage avance désormais assez près du modèle pour interagir. Un clic sur un objet inaccessible annule la destination précédente.
- Les 25 niveaux, les accès variables, les énigmes, les sauvegardes et les 250 souvenirs ont été revérifiés. Les grilles et les conditions de progression restent inchangées.
- Contrôle visuel natif des 25 niveaux et des interfaces portrait/paysage. Le navigateur de contrôle ne fournit pas WebGL 2 ; la fluidité sur téléphone physique reste à vérifier.

[Cheatsheets et cartes v0.22](docs/v0.22/INDEX.md) · [Dossier v0.22 sur Drive](https://drive.google.com/drive/folders/1N2W2Mz7kKlehyW2VMztWtzykcsEGqMHr).

Documents : `python3 scripts/document_campaign_audit.py /chemin/de/sortie`. Mesures des retours et conservation des placements publiés : `python3 scripts/audit_return_links.py --write`. Les générateurs historiques peuvent reconstruire leurs anciens passages ; réappliquer ensuite cet audit conserve la sélection v0.22.

Validation : `python3 game/tests/validate_return_links.py`, puis les tests Godot `verify_shortcuts`, `verify_return_saves` et `verify_interaction_approaches`. La suite complète comprend 27 tests Godot et les validations indépendantes des chapitres. [Mesures des 155 portes](game/tests/return_links_audit.json).

## Nouveautés v0.21 — Dossier du sujet 16

- Dossier accessible depuis le HUD, la pause et les bilans : progression, collection, quinze archives et observations de Folamour.
- Dix souvenirs facultatifs par niveau (250) : ampoules témoins, tampons de service, rouages de prévoyance, prismes MIROIR et capsules de retour. Ils ne consomment aucune place dans le sac et ne conditionnent jamais la fin.
- Collection persistante pendant la campagne et lors des reprises. Rejouer un niveau terminé depuis le dossier conserve la collection et les bilans ; les énigmes et la progression du niveau actuel sont remplacées après confirmation explicite. Une nouvelle aventure réinitialise le dossier.
- Folamour suit le sujet du regard, respire et gesticule doucement. Répliques liées aux rencontres, réussites, tentatives et collections ; animations et commentaires désactivables séparément en pause.
- Palettes, lumière et objets décoratifs spécifiques à chaque chapitre. Les cinq silhouettes se distinguent aussi sans la couleur.
- Aucun changement aux 25 grilles, énigmes ou passages. Placement : 196 fonds d’impasse et 54 recoins éloignés, avec dix récompenses par niveau, cinq pas au minimum des interactions et huit pas entre récompenses.

Placement reproductible : `python3 scripts/place_collectibles.py`. Contrôles : `python3 game/tests/validate_collectibles.py` et Godot `--headless --path game --fixed-fps 60 --script res://tests/verify_subject16.gd`. Ces contrôles s’ajoutent à la suite complète dans GitHub Actions.

[Cheatsheets v0.21 — les 25 niveaux](docs/v0.21/INDEX.md). Le ZIP complet remis avec cette version contient les cartes PNG/PDF, les guides PDF/Markdown et le rapport de recherche. [Documents v0.21 dans Drive](https://drive.google.com/drive/folders/1_2Sa00T5YCT2QCgQap1IADQbYPzGb_ms) : cinq dossiers de chapitre, 25 guides PDF, une archive pour chaque chapitre, l’archive complète, le rapport de recherche et l’index des 250 souvenirs. [Recherche et audit](docs/v0.21/Recherche-et-audit-v0.21.md). Régénération : `python3 scripts/document_subject16.py /chemin/de/sortie`.

Vérification : les 250 ramassages physiques et les 23 régressions Godot passent, ainsi que la publication GitHub Actions. Le paquet web publié contient bien les 25 collections. Le navigateur de contrôle ne fournit pas WebGL 2 : l’appréciation du rendu 3D et la fluidité sur téléphone réel restent à confirmer.

## Fins de niveau v0.20

Les 25 points de fin ont été audités. Les niveaux 1–2 gardent leurs vrais seuils ; les sorties 3–4 sont fixées au mur. Dans les niveaux 5–25, parler à Folamour remplace la porte artificielle, avec une remise d’objet ou un bilan adapté à la mission. Au niveau 25, le docteur reste auprès du bureau du dialogue final.

Les objectifs, le bouton **Parler**, les repères **F** sur la carte et les conversations existent en français et en anglais. Les énigmes, objets requis et identifiants de sauvegarde sont conservés.

La présentation canonique des fins se trouve dans `game/data/endings.json`, appliquée aux données générées par `LevelEndings.gd`. Elle n’est pas écrasée par les générateurs de labyrinthes. [Audit des 25 fins](docs/endings-audit-v020.md).

## Ajustements v0.19.1

- Recul maximal du zoom augmenté de 36 à 48.
- Clic droit sur un passage découvert et accessible dans la carte : elle se ferme et le personnage s’y rend.
- Boutons Examiner / Ramasser à 16 px, sur une seule ligne.
- Sas 305 du chapitre 1, niveau 4, monté contre le mur sud pour dégager le couloir.

## Nouveautés v0.19

**Pour votre tranquillité définitive** conclut l’aventure en cinq niveaux. HORIZON, révélé à la fin du chapitre 4, transforme la protection en obsession : fusées gigantesques, fausses preuves de MIROIR et copies qui ont oublié le droit de refuser. Le joueur rétablit ce droit et conduit Folamour à accepter un avenir incertain.

| Niveau | Labyrinthe | Trois défis |
| --- | --- | --- |
| 1 — Le département des petites précautions | Épine de maintenance, trois baies de silos, deux ailes | Ponts couplés avec inspections physiques, manifeste, capsule de retour |
| 2 — L’observatoire des intentions hostiles | Trois enceintes imbriquées | Décalages horaires, chronologie causale, copies circulaires |
| 3 — Le docteur a toujours raison | Bureaux autour du conseil et archives en deux ailes | Quorum contradictoire, mandat fragmenté, droit d’arrêt |
| 4 — Tout est sous contrôle | Galerie de commandement et réseau d’évacuation | Procédure d’arrêt, relais de reprise, deux capsules en miroir |
| 5 — Un avenir légèrement incertain | Terrasses successives vers un petit bureau | Faits/hypothèses/inconnues, intervalles, dialogue final |

- Quinze énigmes et quinze secrets, seize raccourcis sans contournement des sas, trois accès physiques variables.
- Compte à rebours par étapes : seules les trois validations du niveau 4 font avancer la procédure. Les essais restent réversibles et aucun temps réel ne provoque d’échec.
- Fusées monumentales, balayages de surveillance, cinq copies au conseil, ambiances mécaniques originales, annonces archivées et silence au dernier niveau. Une scène extérieure conclut l’aventure.
- Reprise des sauvegardes des vingt anciens niveaux, transition depuis le chapitre 4, accès direct par chapitre, bilans conservés. Toutes les nouvelles consignes et interfaces sont en français/anglais.
- Vérifications : parcours physiques complets, quinze solutions via les boutons, sauvegardes partielles/finales, indices, 27 configurations de ponts, 64 graphes de preuves, trajets de capsules, dispositions portrait/paysage et régressions. Le contrôle visuel Web local n’a pas abouti dans cet environnement ; un essai sur téléphone physique reste à effectuer.

[Cartes et cheatsheets v0.19 — cinq dossiers de niveau](https://drive.google.com/drive/folders/1lTndQ60RtFyScCaPx2RVO_1fgic_vX5f).

Données : `python3 scripts/build_chapter5.py`. Audio : `python3 scripts/compose_finale_audio.py`. Documents : `python3 scripts/document_chapter5.py /chemin/de/sortie`.

Tests : `python3 game/tests/validate_chapter5.py`, puis Godot `--headless --path game --fixed-fps 60 --script res://tests/verify_chapter5.gd` et `res://tests/verify_finale_states.gd`. Ces contrôles sont inclus dans la publication GitHub Actions.

## Nouveautés v0.18

Le chapitre 4, **Le complexe de la certitude**, prolonge directement la v0.17 : cinq niveaux dans une cité souterraine où les prédictions de MIROIR remplacent les observations. Le programme HORIZON est annoncé à la conclusion ; le chapitre 5 reste à venir.

| Niveau | Labyrinthe | Défis |
| --- | --- | --- |
| 1 — Bienvenue, vous habitez ici | Gare en éventail et deux ailes de maintenance | Badges et visites physiques, identité croisée, deux capsules dans un réseau |
| 2 — Le quartier témoin | Rue verticale, maisons à horaires variables, deux quartiers | Phases matin/midi/soir, planning de livraisons, témoin et preuves indépendantes |
| 3 — Le ministère des regards | Deux anneaux et tour centrale | Portes liées aux caméras, raccords d’un film, origine des rapports |
| 4 — La fabrique du lendemain | Trois bandes de production, passerelles alternées | Alimentation partagée, convoyeur, dépendances d’assemblage |
| 5 — L’unanimité absolue | Cinq branches autour du conseil | Affectation des preuves, réseau de confiance, traversées avec un sceau commun |

- Quinze énigmes, quinze secrets, seize raccourcis et neuf accès variables. Les anneaux du niveau 3 offrent déjà des retours directs, sans raccourcis cachés.
- Les badges, phases et orientations modifient les portes physiques, la carte et les trajets au clic/toucher. Les changements se font au pupitre pour éviter tout enfermement ; les trois registres doivent être visités. Une fois validé, le secteur reste accessible.
- États et observations sauvegardés, essais réversibles, temps du dernier casse-tête avancé uniquement par les traversées. Plusieurs assemblages valides sont acceptés.
- Menus distincts par chapitre, accès direct aux cinq niveaux, transition depuis le chapitre 3 et reprise des sauvegardes existantes. Textes et indices FR/EN, réglages mobiles et audio conservés.
- Vérifications : parcours physiques complets, quinze solutions via les boutons réels, sauvegardes partielles/finales, indices, portes dans les deux sens, configurations des réseaux, annulation, variantes d’assemblage, interface portrait/paysage et régressions des anciens chapitres. Un essai sur téléphone réel reste à faire.

[Cartes et cheatsheets v0.18 — cinq dossiers de niveau](https://drive.google.com/drive/folders/1QZKSCzC91o7R5nYe43ddt9DZUd3X6jYj).

Données : `python3 scripts/build_chapter4.py`. Documents : `python3 scripts/document_chapter4.py /chemin/de/sortie`.
Tests : `python3 game/tests/validate_chapter4.py`, puis Godot 4.5.1 `--headless --path game --fixed-fps 60 --script res://tests/verify_chapter4.gd` et `res://tests/verify_certainty_states.gd`. Les nouveaux tests et les contrôles mobiles sont intégrés au workflow de publication.

Les principes de conception et les sources consultées figurent dans [le résumé](docs/v0.18/Resume-v0.18.md).

## Nouveautés v0.17

Le chapitre 3, **Le département de la prévoyance**, est jouable du début à la fin. Après MIROIR, Folamour transforme la prévention en problème administratif : les prédictions se copient, la surveillance le dénonce et le conseil réclame un complexe souterrain.

| Niveau | Plan original | Trois défis |
| --- | --- | --- |
| 1 — Le magasin des prototypes | Entrepôts en peigne et galerie de livraison | Mesurer les appareils, ranger les prototypes, programmer un chariot |
| 2 — Le bureau des incidents futurs | Bureaux en trois terrasses | Synchroniser les horloges, retrouver la causalité, prévenir sans étouffer la ventilation |
| 3 — La centrale de surveillance | Trois cours autour d’un vide | Orienter les caméras, remonter un film, identifier le visiteur |
| 4 — Le simulateur de crise | Plateformes et passerelles autour des bassins | Répartir douze unités, équilibrer trois cuves, évacuer deux équipes aux commandes opposées |
| 5 — Le conseil de prévention | Amphithéâtre annulaire et coulisses | Écarter les preuves copiées, résoudre les quatre voix, stabiliser les échos retardés |

- Quinze nouveaux essais, quinze secrets et vingt raccourcis, avec indices graduels en français et en anglais.
- Mesures et programmes conservés ; simulations sans temps réel ; annulation des ordres et des transvasements ; remise à zéro sans perte du matériel installé.
- Transition archives → chapitre 3, cinq missions enchaînées, reprise des essais partiels et bilan du chapitre. Le chapitre 4 est annoncé, sans accès jouable.
- Panneaux vérifiés en portrait et paysage ; déplacements, collisions, solutions, sauvegardes et raccourcis couverts par les tests Godot.

[Cartes et cheatsheets v0.17 — cinq dossiers de niveau](https://drive.google.com/drive/folders/1tSsCdJEI-DX_fy_I0nd6jUn9xzBYUkn0).

Les données sont générées avec `python3 scripts/build_chapter3.py`. Les guides français (cartes PNG/PDF A3, solutions PDF A4/Markdown) sont générés avec `python3 scripts/document_chapter3.py /chemin/de/sortie`. Vérification : `python3 game/tests/validate_chapter3.py`, puis Godot avec `--headless --path game --fixed-fps 60 --script res://tests/verify_chapter3.gd`.

## Nouveautés v0.16
**Le service des archives**, niveau 5 du chapitre 2 (numéro interne 10), poursuit le projet MIROIR : rayonnages à commandes couplées, authentification de rapports par trois preuves indépendantes, puis reproduction de quatre états dans une salle jumelle physique.

17 repères, trois archives secrètes et quatre raccourcis à découvrir. Les 27 configurations des rayonnages laissent une issue ; une sécurité interdit leur déplacement si le personnage est à l’intérieur. La carte et les déplacements au clic/toucher suivent leurs ouvertures réelles. Les indices restent consultables dans le journal.

Accès direct **Chapitre 2 · Niveau 5 — Le service des archives**, ou « Passer au service des archives » après la réunion, avec conservation des bilans. Commandes, objectifs, indices et histoire FR/EN. Les essais partiels, tests de la copie, rayonnages et raccourcis sont sauvegardés. Netteté mobile, vitesse +30 % et audio conservés.

Validation : parcours physique complet, porte verrouillée, sécurité des rayonnages, deux ordres d’exploration, reprise des essais, sauvegarde finale et panneaux portrait/paysage. Le secteur des prototypes est annoncé à la conclusion mais n’est pas encore un niveau jouable.

Données : `python scripts/build_level10.py`. Tests : `python game/tests/validate_level10.py`, puis Godot `--headless --path game --fixed-fps 60 --script res://tests/verify_level10.gd`. Documents : `python scripts/document_level10.py /chemin/de/sortie`.

[Carte et cheatsheet v0.16](https://drive.google.com/drive/folders/1HoAb0Sl6SiNdCjGv-oFSRIIqAsvMKovn).

## Nouveautés v0.15
**La salle de réunion**, niveau 4 du chapitre 2 (numéro interne 9), poursuit le stage : placer six invités selon leurs contraintes, organiser quatre interventions en une heure et brancher les circuits image/son. Folamour présente son comité et prépare la suite autour du projet MIROIR.

Grande salle centrale, quatre ailes de bureaux, 20 repères et trois archives facultatives. Le placement ouvre les bureaux est ; le planning ouvre trois accès à la salle. Six raccourcis évitent 166 pas sur le parcours de référence (753 → 587), après visite physique des deux côtés, sans contourner les portes.

Accès direct **Chapitre 2 · Niveau 4 — La salle de réunion**, ou « Passer à la salle de réunion » après le courrier, avec conservation des bilans. Commandes, objectifs et indices FR/EN ; places, horaires et branchements sauvegardés. Déplacement +30 %, réglages de netteté mobile et corrections audio conservés ; aucun bruit de pas. Six portraits simples, sans rendu vidéo supplémentaire.

Validation : solutions uniques, parcours physique complet, quatre barrières, reprises partielles, transition depuis le courrier et affichage FR/EN en portrait/paysage. Les quinze suites de tests ont réussi ; aucun essai sur appareil réel n’a été effectué dans cette livraison.

Données : `python scripts/build_level9.py`. Vérification : `python game/tests/validate_level9.py`, puis Godot `--headless --path game --fixed-fps 60 --script res://tests/verify_level9.gd`. Documents : `python scripts/document_level9.py /chemin/de/sortie`.

[Carte et cheatsheet v0.15](https://drive.google.com/drive/folders/1NUGzcN74ws1MmmJIdCcqbLfzREa1iyhz).

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

Une composition originale de 48 secondes accompagne l’exploration à faible volume : piano électrique, basse et cloches légèrement étranges. Des sons ponctuent les portes, les machines et la fin du chapitre ; les bruits de pas ont été retirés. Les réglages séparés (général, musique, effets, machines) sont persistants, avec coupure générale et interruption en arrière-plan. La musique s’atténue pendant la lecture. `scripts/compose_audio.py` permet de recréer les assets avec NumPy et ffmpeg, sans échantillons tiers.

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
