# Analyse des ventes et des prix — Sample Sales Data

Étude de cas *Sales Analysis* sur les ventes B2B d'un distributeur de modèles réduits (janvier 2003 – mai 2005) : chiffre d'affaires, saisonnalité, marchés, clients, gammes, références et écart au prix catalogue.

👉 **[Voir le projet en ligne](https://mehdigraoui75-art.github.io/analyse_ventes/)** : étude, tableau de bord interactif, rapport Power BI et code Python.

## Principaux résultats

- **9,44 M$** de chiffre d'affaires, **+31 %** en 2004 et **+12 %** sur janvier-mai 2005.
- Le **4e trimestre** pèse **44 à 52 %** du CA annuel (pic de novembre, préparation de Noël).
- Les **voitures classiques** (39,5 % du CA) se vendent de plus en plus sous le prix catalogue : −0,8 % en 2003, −5,6 % en 2004, **−8,1 %** en 2005, soit **161 k$** de manque à gagner.
- Clientèle concentrée : les 20 premiers clients font **43 %** du CA, et aucun nouveau client n'a été recruté sur janvier-mai 2005.
- **Prévision 2005** : **6,16 M$** (+35 %), moyenne de trois méthodes simples, dans une fourchette de 5,10 à 6,90 M$. Testée sur 2004, la moyenne n'a fait que 6 % d'erreur.

## Contenu du dépôt

| Fichier | Description |
|---|---|
| `index.html` | Page d'accueil du projet en ligne |
| `tableau-de-bord.html` | Tableau de bord interactif (3 pages, filtres par année, territoire et gamme) |
| `analyse_sample_sales_graoui.pdf` | Étude complète : analyse, tableaux, graphiques et recommandations |
| `analyse_sample_sales_graoui.py` | Script Python qui reproduit tous les chiffres et graphiques de l'étude |
| `analyse_sample_sales_graoui.pbix` | Rapport Power BI (Power Query, DAX) |
| `analyse_sample_sales_powerBI.pdf` | Export PDF du rapport Power BI |
| `prevision_2005.pdf` | Note de prévision du chiffre d'affaires 2005 : méthodes, test sur 2004, prévision retenue |
| `prevision_2005.py` | Script Python qui reproduit les chiffres et graphiques de la prévision |
| `sales_data_sample.csv` | Données sources ([Sample Sales Data, Kaggle](https://www.kaggle.com/datasets/kyanyoga/sample-sales-data)) |

## Lancer le script Python

```bash
pip install -r requirements.txt
python analyse_sample_sales_graoui.py   # étude : 4 graphiques
python prevision_2005.py                # prévision 2005 : 2 graphiques
```

Chaque script affiche les résultats dans la console, section par section, et enregistre ses graphiques en PNG.

## Méthode

- **Périmètre** : commandes expédiées (*Shipped*) ou résolues (*Resolved*), soit 94 % des ventes.
- **Écart au prix catalogue** = CA ÷ (quantité × prix catalogue MSRP) − 1. Un écart négatif signifie une vente sous le prix catalogue.
- **Panier moyen** = CA ÷ nombre de commandes.
- **Prévision 2005** : périmètre élargi à toutes les commandes hors annulées (en avril-mai 2005, une partie des commandes n'est pas encore expédiée). Prévision retenue = moyenne de trois méthodes (taux de croissance, coefficients saisonniers, reconduction de 2004).

## Outils

Python (pandas, matplotlib) · Power BI (Power Query, DAX) · HTML / JavaScript · IA générative (Claude)

---
Mehdi Graoui · Sales Analyst
