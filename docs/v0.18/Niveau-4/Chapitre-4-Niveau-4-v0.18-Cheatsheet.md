# La fabrique du lendemain

Chapitre 4 / Niveau 4 / Version 0.18 / SPOILERS

## La fabrique du lendemain
Chapitre 4 / Niveau 4

### SPOILERS / VERSION 0.18

« Nous produisons aujourd’hui les solutions aux problèmes que nous annoncerons demain. Votre ascenseur est une commande mineure. Essayez de ne pas déranger les grandes. » — Folamour

Trois chaînes en tresses traversent le complexe : énergie à l’ouest, convoyeurs au centre, assemblage à l’est. Les passerelles changent de hauteur sur le plan ; les ateliers latéraux forment des boucles de retour.

### Parcours conseillé

Menu → Choisir un chapitre → Chapitre 4, puis choisir ce niveau. La transition depuis la mission précédente conserve les bilans. Le sac et le journal repartent à zéro à chaque nouveau niveau.

1. Ramasser la mallette 101 et l’installer au poste 203. Lire 201 et 202, puis résoudre 203 : L’énergie compte deux fois. Le sas 111 s’ouvre.

2. Lire 301 et 302, puis résoudre 303 : La pièce qui repasse. Le sas 112 s’ouvre.

3. Lire 401 et 402, puis résoudre 403 : Une petite pièce dans une grande machine. Rejoindre ensuite le passage 900.

Les notes secrètes 501, 502 et 503 sont facultatives. Leur lecture compte au bilan. Les 4 raccourcis demandent de marcher des deux côtés du mur ; la simple visibilité ne suffit pas.

### Commandes et sauvegarde

Clic ou toucher : marcher et examiner. WASD / ZQSD / flèches : marcher ; E : interagir ; I : sac ; J : journal ; M : carte. Aucune limite de temps. Les manipulations, mesures et programmes sont sauvegardés. Réinitialiser un essai restaure ses réglages sans rendre la mallette déjà installée. Après une simulation, modifier une commande exige un nouveau test.

### Indices graduels

Chaque poste propose une piste, une méthode, puis la solution complète. Ouvrir le panneau ne révèle rien automatiquement. Les indices consultés et les essais incorrects sont comptés au bilan.

## 01 / L’énergie compte deux fois

Poste 203 : (5, 9). Mallette 101 requise.

Répartir six unités entre A, B et C. Atteindre simultanément A+B=5, B+C=4 et A+C=3. Les jauges réagissent immédiatement.

### 201 / Consigne 201 / (1, 1)

Trois générateurs A, B, C distribuent six unités au total. La presse reçoit A+B et demande 5. Le refroidissement reçoit B+C et demande 4. Le guidage reçoit A+C et demande 3.

### 202 / Consigne 202 / (11, 33)

Une unité de générateur alimente deux postes par les circuits existants. Il ne faut pas additionner les besoins comme s’ils étaient indépendants. Les jauges affichent chaque somme.

### Solution exacte depuis la réinitialisation

A=2 ; B=3 ; C=1. Valider.

Comparer les sommes : A est une unité plus grand que C ; B est deux unités plus grand que C. Avec six unités, C=1, A=2, B=3.

Validation enregistrée. Le deuxième secteur est ouvert.

## 02 / La pièce qui repasse

Poste 303 : (19, 19). Validation 203 requise.

Régler les trois aiguillages. Le trajet doit visiter M → R → C → S. Les sorties possibles et les stations apparaissent sur le schéma. Tester fournit une trace et la cause d’un refus.

### 301 / Consigne 301 / (15, 1)

Le convoyeur part de D. À chaque case numérotée, l’aiguillage choisit sa sortie 0 ou 1. La pièce doit être moulée M, refroidie R, puis contrôlée C avant la sortie S.

### 302 / Consigne 302 / (23, 33)

Un passage à C avant R échoue ; R avant M échoue. La pièce peut repasser par un aiguillage, mais un circuit qui répète exactement le même état est une boucle. Les pièces d’essai sont toujours récupérées.

### Sorties du réseau

Nœud | Sortie 0 | Sortie 1
--- | --- | ---
1 | 3 | M
2 | R | 1
3 | 2 | C

Liaisons fixes : D → 1 ; M → 2 ; R → 3 ; C → S. Stations dans l’ordre : M (moulage), R (refroidissement), C (contrôle).

### Solution exacte depuis la réinitialisation

Aiguillages 1=1 ; 2=0 ; 3=1. Tester : D → 1 → M → 2 → R → 3 → C → S. Valider.

Le premier aiguillage doit entrer dans M. Le deuxième doit envoyer vers R. Le dernier rejoint C, qui mène à S. Les autres sorties recirculent ou sautent une opération.

Validation enregistrée. Le troisième secteur est ouvert.

## 03 / Une petite pièce dans une grande machine

Poste 403 : (29, 27). Validation 303 requise.

Programmer les six opérations selon les dépendances : socle avant moteur/guide ; moteur avant courroie ; guide et courroie avant capot ; capot avant contrôle. Tester puis valider.

### 401 / Consigne 401 / (27, 1)

Monter le socle avant le moteur et le guide. Le moteur doit précéder la courroie. Le guide doit précéder le capot. La courroie doit précéder le capot. Le contrôle clôt l’assemblage.

### 402 / Consigne 402 / (33, 33)

Le moteur et le guide peuvent être montés dans les deux ordres. Aucun ordre arbitraire n’est imposé si toutes les dépendances sont respectées. Tester indique la première dépendance manquante.

### Solution exacte depuis la réinitialisation

Socle → moteur → guide → courroie → capot → contrôle. Tester puis valider. Guide et moteur peuvent être inversés.

Le socle est premier, le contrôle dernier. Entre les deux, conserver les liens de dépendance ; plusieurs ordres intermédiaires sont acceptés.

Validation enregistrée. Le passage de fin de niveau est autorisé.

## Repères, secrets et raccourcis

Repère | Objet / poste | Coordonnées
--- | --- | ---
100 | Ordre de mission | (1, 31)
101 | Mallette de service | (3, 33)
111 | Sas de secteur 1 | (13, 27)
112 | Sas de secteur 2 | (25, 7)
201 | Consigne 201 | (1, 1)
202 | Consigne 202 | (11, 33)
203 | L’énergie compte deux fois | (5, 9)
301 | Consigne 301 | (15, 1)
302 | Consigne 302 | (23, 33)
303 | La pièce qui repasse | (19, 19)
401 | Consigne 401 | (27, 1)
402 | Consigne 402 | (33, 33)
403 | Une petite pièce dans une grande machine | (29, 27)
501 | Note confidentielle 1 | (11, 1)
502 | Note confidentielle 2 | (23, 1)
503 | Note confidentielle 3 | (27, 33)
900 | Passage de service | (33, 19)

### Raccourcis facultatifs

ID | Mur | Deux côtés à visiter | Gain minimal*
--- | --- | --- | ---
C41 | (5, 12) | (5, 11) ↔ (5, 13) | 12 pas
C42 | (3, 12) | (3, 11) ↔ (3, 13) | 12 pas
C43 | (9, 14) | (9, 13) ↔ (9, 15) | 20 pas
C44 | (6, 21) | (7, 21) ↔ (5, 21) | 28 pas

* Gain sur le trajet entre les deux côtés, même avec les autres raccourcis ouverts. Le parcours principal fonctionne sans ouvrir aucun raccourci.

## Archives confidentielles
et fin de mission

### 501 / (11, 1)

Commande : 1 pièce d’ascenseur. Emballage : 400 tonnes de matériel préventif.

### 502 / (23, 1)

Les capsules de tranquillité ne doivent jamais être secouées par le doute.

### 503 / (27, 33)

Objectif de production : suffisamment. Nouveau quota : davantage.

### Révélation de fin de niveau

L’ascenseur est réparé. Derrière sa pièce minuscule, les chaînes poursuivent des coques effilées, des systèmes de guidage et des capsules de tranquillité. La commande porte la mention HORIZON. Il manque seulement l’accord du directoire.

### La suite

Le bouton « Continuer la mission suivante » enchaîne le niveau suivant et conserve le bilan.

### Vérification du parcours

Le trajet de référence parcourt 493 cases de déplacement et visite les 15 points interactifs, dont les trois secrets. Les deux sas portent le total à 17 repères. Les solutions du guide sont utilisées par les tests des commandes réelles du jeu.
