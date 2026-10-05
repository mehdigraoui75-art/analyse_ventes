# Prompter le MVP « Enchères Emprunteur »

## Le prompt qui aurait produit la v1

> Crée une page web statique (un seul fichier HTML/CSS/JS, sans backend, mobile OK) pour un MVP de
> marketplace d'**assurance emprunteur (ADI)**.
> **Cible** : particuliers qui prennent un crédit immobilier et veulent une assurance moins chère que celle de leur banque.
> **Fonctionnalité unique** : le client remplit son profil (âge, capital, durée, objet du prêt, profession, fumeur, sport à risque, motif),
> la fiche anonymisée est « envoyée » à 5 assureurs fictifs qui font des **enchères descendantes pendant 48 h**
> (simulées : 48 h accélérées en 45 s). Afficher le compte à rebours, le classement en direct, la meilleure offre,
> la référence banque et l'économie estimée sur la durée du prêt.
> **Contraintes** : style sobre et professionnel, français, aucune donnée envoyée (localStorage seulement), prix qui ne font que baisser.
> **Hors périmètre** : comptes, paiement, vrais assureurs, questionnaire de santé.
> **Vérifie** que le JS fonctionne dans un navigateur avant de conclure.

### Pourquoi ça marche
| Élément | Rôle |
|---|---|
| Cible | Oriente le vocabulaire et les champs du formulaire |
| Fonctionnalité unique | Garde le MVP petit |
| Contraintes (statique, simulé) | Évite que l'IA invente un back-end |
| Hors périmètre | Empêche la dérive (comptes, paiement…) |
| Vérification demandée | Oblige à tester plutôt qu'à supposer |

## Modèle réutilisable

> Contexte : [produit en une phrase] pour [cible].
> Objectif de cette itération : [un seul changement].
> Contraintes : [techniques, style, langue].
> Ne touche pas à : [ce qui marche déjà].
> Critère de réussite : [comment je saurai que c'est bon].

## Prompts pour la suite (un par itération)

1. **Barème réaliste** : « Remplace le barème fictif de `tauxBase()` par une grille par tranche d'âge et de durée que je te fournis (CSV). Garde la même interface. »
2. **Vue assureur** : « Ajoute une page `assureur.html` qui affiche la fiche anonymisée et permet de baisser son prix (jamais de le monter). Stockage localStorage pour l'instant. »
3. **Vrai back-end** : « Propose l'architecture minimale (Supabase ou Firebase) pour stocker les fiches et les offres, avec clôture automatique à 48 h. Ne code rien avant que je valide. »
4. **Conformité** : « Liste ce qu'il faut vérifier avant de lancer en France (courtier/ORIAS, RGPD, loi Lemoine, données de santé). Signale ce qui relève d'un juriste. »
5. **Test utilisateur** : « Rédige 5 questions à poser à 5 emprunteurs pour savoir s'ils utiliseraient ce service et à quel prix. »

## Conseils
- **Un changement par prompt.** Plus c'est ciblé, moins il y a de régressions.
- **Donne un critère de réussite**, sinon l'IA décide seule de ce qui est « fini ».
- **Demande de lister les hypothèses** quand tu ne connais pas le métier : le barème de prix est ici inventé.
- **Relis ce qui est simulé** avant de montrer le MVP à quelqu'un.
