# Audit des fins de niveau — v0.20

Les coordonnées sont les cases `(x, y)` du jeu. Les fins sont définies dans `game/data/endings.json` : `LevelEndings.gd` les applique après le chargement des labyrinthes générés. Cette couche conserve les identifiants de progression et les exigences des énigmes.

| Chapitre / niveau | Repère | Point de fin | Décision et justification |
| --- | --- | --- | --- |
| 1 / 1 | 00 | Porte — (17, 34) | Vrai sas entre deux parois, au débouché du laboratoire. Pupitre, disques et code conservés. |
| 1 / 2 | 306 | Porte — (17, 34) | Seuil encadré donnant accès à la cabine de l’ascenseur. Alimentation et contrepoids conservés. |
| 1 / 3 | 306 | Porte — (17, 33) | Ancienne porte au centre du passage en T : déplacée contre le mur sud de la chambre d’observation. |
| 1 / 4 | 305 | Porte — (17, 33) | Sas adossé au mur sud ; le couloir est-ouest reste libre. |
| 1 / 5 | 405 | Folamour — (17, 1) | Démonstration de ZÉRO devant le docteur dans la galerie nord, après les rotors. Plus de porte ni de déplacement du docteur après la victoire. |
| 2 / 1 | 105 | Folamour — (17, 13) | Café remis directement au docteur au point de service central. Il se tient en retrait de 0,65 m contre le côté du couloir ; aucun obstacle transversal. |
| 2 / 2 | 101 | Folamour — (21, 19) | Remise en personne à l’accueil des bureaux ; le bac n’est plus une fausse porte. |
| 2 / 3 | 101 | Folamour — (27, 21) | Livraison au docteur à la réception est ; le guichet n’est plus une porte. |
| 2 / 4 | 105 | Folamour — (21, 21) | Annonce au président dans la salle centrale, après la préparation de la réunion. |
| 2 / 5 | 105 | Folamour — (21, 19) | Ouverture du dossier avec Folamour dans la salle des archives, et non sur une porte au milieu de la salle. |
| 3 / 1 | 900 | Folamour — (33, 25) | Compte rendu des prototypes dans la galerie est ; ce point n’est pas un seuil de bâtiment. |
| 3 / 2 | 900 | Folamour — (33, 33) | Bilan des incidents futurs dans l’angle sud-est ; une rencontre est cohérente avec cette aire de fin. |
| 3 / 3 | 900 | Folamour — (13, 33) | Rapport de surveillance dans la galerie sud, au lieu d’une porte isolée le long du mur. |
| 3 / 4 | 900 | Folamour — (33, 33) | Bilan du simulateur au poste sud-est ; le contrôle de crise précède la conversation. |
| 3 / 5 | 900 | Folamour — (29, 33) | Bilan du conseil de prévention dans la galerie sud ; transition de chapitre par dialogue. |
| 4 / 1 | 900 | Folamour — (33, 25) | Contrôles de régularisation présentés au docteur sur le palier est. |
| 4 / 2 | 900 | Folamour — (33, 23) | Rapport du quartier témoin dans la galerie est, sans couper le passage. |
| 4 / 3 | 900 | Folamour — (17, 19) | Discussion des preuves dans la salle centrale, après les trois expériences. |
| 4 / 4 | 900 | Folamour — (33, 19) | Rapport des machines dans la galerie est ; aucune porte décorative au débouché. |
| 4 / 5 | 900 | Folamour — (17, 3) | Discussion de MIROIR avec le docteur dans la salle nord. Les copies présentes ailleurs restent des personnages du décor. |
| 5 / 1 | 900 | Folamour — (33, 29) | Bilan des silos près de la zone de retour, à l’est, après les trois validations. |
| 5 / 2 | 900 | Folamour — (21, 15) | Discussion des preuves au cœur de l’observatoire ; aucun seuil artificiel dans cette salle. |
| 5 / 3 | 900 | Folamour — (29, 31) | Conversation avec le véritable docteur dans la salle sud-est ; les copies du conseil gardent leur rôle. |
| 5 / 4 | 900 | Folamour — (5, 27) | Confirmation de l’arrêt dans la zone d’évacuation sud-ouest. Aucun nouveau lancement ni compte à rebours. |
| 5 / 5 | 900 | Folamour — (17, 28) | Le docteur est placé en (17,28), près du bureau du dialogue (17,29). Lui parler ouvre le dernier raisonnement si nécessaire ; après validation, on lui propose de sortir ensemble. L’ancien passage (17,33) reste libre. |

## Interactions et continuité

- Un point de fin unique par niveau. Les niveaux 5–25 utilisent un personnage cliquable, le bouton **Parler**, une conversation et un repère **F** sur la carte. Aucun battant, verrou invisible ou voyant de machine sur le docteur.
- Chaque conversation rappelle les exigences manquantes. La fin exige toujours les mêmes énigmes et les mêmes objets ; les remises d’objets sont consommées une seule fois.
- Les dialogues, actions et objectifs sont traduits en français et en anglais, y compris les textes composés du HUD et du journal.
- Les points de fin 1–24 conservent leurs cases de découverte. Le point 25 se rapproche du bureau ; ses identifiants et validations restent inchangés. Les anciennes sauvegardes reconstruites retrouvent le nouveau point de fin.
- La présence du docteur est unique pour la conclusion de chaque niveau. Les copies narratives des chapitres 4–5 et la scène extérieure de l’épilogue sont conservées.

## Vérification

`verify_endings.gd` vérifie les 25 placements, les conditions manquantes, les remises, le déplacement automatique jusqu’au docteur, les conversations FR/EN et les sauvegardes avant/après conclusion. Les parcours physiques existants vérifient ensuite les énigmes, les passages et les transitions des chapitres. Le parcours final du niveau 25 vise désormais le bureau.
