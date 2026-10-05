# Enchères Emprunteur — mode d'emploi

> Idée personnelle, non publiée. Tout est simulé : assureurs fictifs, barème de prix inventé, aucune donnée envoyée.

## Où est quoi ?

```
mvp-assurance-emprunteur/
├── index.html          ← LA page client + « Jouer l'assureur » (tout-en-un)
├── assureur.html       ← la vue assureur dans un 2e onglet (nécessite un petit serveur)
├── QUESTIONS_TEST.md   ← 5 questions pour tester l'idée auprès d'emprunteurs
├── PROMPTS.md          ← les prompts qui ont produit le MVP + ceux pour la suite
└── LISEZMOI.md         ← ce fichier
```

Où se règle quoi dans le code (`index.html`) :
| Je veux changer… | Où |
|---|---|
| le barème de prix | fonction `tauxBase()` |
| la liste / agressivité des assureurs | tableau `ASSUREURS` (`f` = niveau de prix, `plancher` = prix minimum) |
| la durée de l'enchère simulée | constante `DUREE_SIM_S` (45 s = « 48 h ») |
| les couleurs | variables `:root` en haut du fichier |

## Tester seul — méthode 1 (la plus simple, sans rien installer)
1. Enregistre les fichiers dans un même dossier.
2. **Double-clique sur `index.html`** (il s'ouvre dans ton navigateur).
3. Clique « Lancer les enchères » et regarde le classement bouger pendant 45 s.
4. Dans le bloc « Jouer l'assureur », propose un prix.

## Méthode 2 — deux onglets (client + assureur)
1. Ouvre un terminal dans le dossier et lance : `python3 -m http.server 8000`
   (sous Windows : `python -m http.server 8000`).
2. Onglet 1 : http://localhost:8000/index.html — onglet 2 : http://localhost:8000/assureur.html
3. Lance l'enchère dans l'onglet 1, puis joue l'assureur dans l'onglet 2.
4. Arrête le serveur avec Ctrl+C.

## Check-list de test (résultat attendu)
| # | Action | Attendu |
|---|---|---|
| 1 | Lancer avec les valeurs par défaut | Compte à rebours qui descend, 5 assureurs classés, prix qui baissent |
| 2 | Renseigner « 130 » comme coût banque | Économie estimée = (130 − meilleure offre) × nb de mois |
| 3 | Envoyer un prix puis un prix **plus haut** | Le 2e est refusé (« ne peut que baisser ») |
| 4 | « Battre la meilleure de 1 € » | Vous passez 1er, au moins momentanément |
| 5 | Attendre 45 s | « Gagnant » affiché, boutons désactivés, message « Enchère close » |
| 6 | « Nouvelle simulation » | Retour au formulaire ; `assureur.html` affiche « Aucune enchère en cours » |
| 7 | Changer âge / fumeur / métier | Les prix montent (fumeur +30 %, âge, métier à risque) |
| 8 | Ouvrir sur téléphone (méthode 2, même réseau) | Mise en page lisible sur petit écran |
