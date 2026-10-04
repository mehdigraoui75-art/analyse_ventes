# Analyse des ventes et des prix — Sample Sales Data

Étude de cas *Sales Analysis* sur les ventes B2B d'un distributeur de modèles réduits (janvier 2003 – mai 2005) : chiffre d'affaires, saisonnalité, marchés, clients, gammes, références et écart au prix catalogue.

👉 **[Voir le projet en ligne](https://mehdigraoui75-art.github.io/analyse_ventes/)** : étude, tableau de bord interactif, rapport Power BI et code Python.

## Principaux résultats

- **9,44 M$** de chiffre d'affaires, **+31 %** en 2004 et **+12 %** sur janvier-mai 2005.
- Le **4e trimestre** pèse **44 à 52 %** du CA annuel (pic de novembre, préparation de Noël).
- Les **voitures classiques** (39,5 % du CA) se vendent de plus en plus sous le prix catalogue : −0,8 % en 2003, −5,6 % en 2004, **−8,1 %** en 2005, soit **161 k$** de manque à gagner.
- Clientèle concentrée : les 20 premiers clients font **43 %** du CA, et aucun nouveau client n'a été recruté sur janvier-mai 2005.

## Contenu du dépôt

| Fichier | Description |
|---|---|
| `index.html` | Page d'accueil du projet en ligne |
| `tableau-de-bord.html` | Tableau de bord interactif (3 pages, filtres par année, territoire et gamme) |
| `analyse_sample_sales_graoui.pdf` | Étude complète : analyse, tableaux, graphiques et recommandations |
| `analyse_sample_sales_graoui.py` | Script Python qui reproduit tous les chiffres et graphiques de l'étude |
| `analyse_sample_sales_graoui.pbix` | Rapport Power BI (Power Query, DAX) |
| `analyse_sample_sales_powerBI.pdf` | Export PDF du rapport Power BI |
| `sales_data_sample.csv` | Données sources ([Sample Sales Data, Kaggle](https://www.kaggle.com/datasets/kyanyoga/sample-sales-data)) |

## Lancer le script Python

```bash
pip install -r requirements.txt
python analyse_sample_sales_graoui.py
```

Le script affiche les résultats dans la console, section par section, et enregistre les 4 graphiques en PNG.

## Méthode

- **Périmètre** : commandes expédiées (*Shipped*) ou résolues (*Resolved*), soit 94 % des ventes.
- **Écart au prix catalogue** = CA ÷ (quantité × prix catalogue MSRP) − 1. Un écart négatif signifie une vente sous le prix catalogue.
- **Panier moyen** = CA ÷ nombre de commandes.

## Outils

Python (pandas, matplotlib) · Power BI (Power Query, DAX) · HTML / JavaScript

---
Mehdi Graoui · Sales Analyst
