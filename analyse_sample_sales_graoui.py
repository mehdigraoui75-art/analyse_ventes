"""
Analyse des ventes et des prix — Sample Sales Data
Mehdi Graoui — octobre 2026

Ce script reproduit, à partir du fichier sales_data_sample.csv, tous les
chiffres, tableaux et graphiques du document « analyse_sample_sales_graoui.pdf ».

Utilisation :
    1. Placer ce script dans le même dossier que sales_data_sample.csv
    2. Installer les bibliothèques :  pip install pandas matplotlib
    3. Lancer :                       python analyse_sample_sales_graoui.py

Les résultats s'affichent dans la console, section par section (même ordre
que le PDF). Les 4 figures sont enregistrées en PNG dans le dossier du script.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# =============================================================================
# 0. PARAMÈTRES GÉNÉRAUX
# =============================================================================

DOSSIER = Path(__file__).resolve().parent          # dossier du script
FICHIER = DOSSIER / "sales_data_sample.csv"

BLEU = "#152C73"                                   # bleu marine (titres et 2005)
BLEU_MOYEN = "#5A72B5"                             # 2004
BLEU_CLAIR = "#A9B6DC"                             # 2003
GRIS = "#C9CED9"
COULEURS_ANNEES = {2003: BLEU_CLAIR, 2004: BLEU_MOYEN, 2005: BLEU}
SOURCE = "Source : Sample Sales Data, commandes expédiées et résolues (janv. 2003 – mai 2005)."

ANNEES = [2003, 2004, 2005]
LIBELLES_ANNEES = {2003: "2003", 2004: "2004", 2005: "2005 (janv.-mai)"}

# Traductions en français (comme dans le rapport)
NOMS_GAMMES = {"Classic Cars": "Voitures classiques", "Vintage Cars": "Voitures vintage",
               "Motorcycles": "Motos", "Trucks and Buses": "Camions et bus",
               "Planes": "Avions", "Ships": "Bateaux", "Trains": "Trains"}
NOMS_PAYS = {"USA": "États-Unis", "Spain": "Espagne", "France": "France",
             "Australia": "Australie", "UK": "Royaume-Uni", "Italy": "Italie",
             "Finland": "Finlande", "Norway": "Norvège", "Singapore": "Singapour",
             "Canada": "Canada", "Denmark": "Danemark", "Germany": "Allemagne",
             "Austria": "Autriche", "Japan": "Japon", "Sweden": "Suède",
             "Switzerland": "Suisse", "Belgium": "Belgique",
             "Philippines": "Philippines", "Ireland": "Irlande"}
NOMS_TERRITOIRES = {"EMEA": "Europe, Moyen-Orient, Afrique (EMEA)",
                    "NA": "Amérique du Nord (NA)",
                    "APAC": "Asie-Pacifique (APAC)", "Japan": "Japon"}


# --- Petites fonctions d'affichage (format français) -------------------------

def dollars(valeur):
    """12345.6 -> '12 346 $' (espace comme séparateur de milliers)."""
    return f"{valeur:,.0f} $".replace(",", " ")


def pourcent(valeur, decimales=1, signe=False):
    """0.4935 -> '49,3 %'  (valeur donnée en proportion, pas en %)."""
    valeur = round(valeur * 100, decimales) + 0.0      # + 0.0 évite d'afficher « -0,0 »
    texte = f"{valeur:+.{decimales}f} %" if signe else f"{valeur:.{decimales}f} %"
    if signe and valeur == 0:
        texte = texte.replace("+", "")
    return texte.replace(".", ",")


def titre(texte):
    print("\n" + "=" * 90)
    print(texte)
    print("=" * 90)


def afficher_tableau(tableau, colonnes_dollars=(), colonnes_pourcent=()):
    """Affiche un DataFrame avec les montants en $ et les parts en %."""
    copie = tableau.copy()
    for col in colonnes_dollars:
        copie[col] = copie[col].map(dollars)
    for col in colonnes_pourcent:
        copie[col] = copie[col].map(pourcent)
    print(copie.to_string())


def tableau_par_annee(donnees, colonne, top=None, libelle_total="Total"):
    """
    Tableau « CA par catégorie et par année » (Tableaux 1, 2, 3, 5 et 6 du PDF) :
    une ligne par catégorie, une colonne par année, puis Total et Part du CA.
    Si top est donné, on ne garde que les N premières lignes et le total
    porte sur ces N lignes.
    """
    pivot = donnees.pivot_table(index=colonne, columns="YEAR_ID", values="SALES",
                                aggfunc="sum", fill_value=0)
    pivot["Total"] = pivot[ANNEES].sum(axis=1)
    pivot["Part du CA"] = pivot["Total"] / donnees["SALES"].sum()
    pivot = pivot.sort_values("Total", ascending=False)
    if top is not None:
        pivot = pivot.head(top)
    pivot.loc[libelle_total] = pivot.sum()
    pivot = pivot.rename(columns=LIBELLES_ANNEES)
    pivot.columns.name = None
    return pivot


def finir_figure(fig, nom_fichier, legende):
    """Ajoute la légende « Figure X — ... / Source », enregistre et affiche."""
    fig.text(0.5, 0.01, f"{legende}\n{SOURCE}", ha="center", va="bottom",
             fontsize=9, color="#555555", style="italic")
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig(DOSSIER / nom_fichier, dpi=150)
    print(f"   -> graphique enregistré : {nom_fichier}")


# =============================================================================
# 1. PRÉSENTATION DES DONNÉES
# =============================================================================

titre("1. PRÉSENTATION DES DONNÉES")

# Le fichier Kaggle d'origine est encodé en CP850 ; s'il a été réenregistré en
# UTF-8 (par exemple avec VS Code), on le lit en UTF-8. On essaie les deux.
# keep_default_na=False : sinon pandas lit le territoire « NA » (Amérique du
# Nord) comme une valeur manquante.
try:
    brut = pd.read_csv(FICHIER, encoding="utf-8", keep_default_na=False)
except UnicodeDecodeError:
    brut = pd.read_csv(FICHIER, encoding="cp850", keep_default_na=False)

print(f"Taille du fichier d'origine : {brut.shape[0]} lignes et {brut.shape[1]} colonnes")

# Colonnes supprimées : coordonnées et noms de contacts (données personnelles)
COLONNES_SUPPRIMEES = ["PHONE", "ADDRESSLINE1", "ADDRESSLINE2", "POSTALCODE",
                       "CONTACTLASTNAME", "CONTACTFIRSTNAME"]
df = brut.drop(columns=COLONNES_SUPPRIMEES)
print(f"Après suppression de {len(COLONNES_SUPPRIMEES)} colonnes : {df.shape[1]} colonnes")

print(f"Nombre de commandes (ORDERNUMBER)        : {df['ORDERNUMBER'].nunique()}")
print(f"Nombre maximum de lignes par commande    : {df['ORDERLINENUMBER'].max()}")
print(f"Statuts possibles ({df['STATUS'].nunique()})                     : {', '.join(df['STATUS'].unique())}")
print(f"Gammes de produits                       : {df['PRODUCTLINE'].nunique()}")
print(f"Références produits                      : {df['PRODUCTCODE'].nunique()}")
print(f"Clients                                  : {df['CUSTOMERNAME'].nunique()}")
print(f"Pays                                     : {df['COUNTRY'].nunique()}")

# --- Qualité des données ---
print("\nQualité des données")
vides = (df == "").sum()
print("Colonnes contenant des cases vides :")
print(vides[vides > 0].to_string())
print(f"Lignes avec TERRITORY = 'NA' (Amérique du Nord, pas une valeur manquante) : "
      f"{(df['TERRITORY'] == 'NA').sum()}")
part_plafond = (df["PRICEEACH"] == 100).mean()
print(f"PRICEEACH plafonné à 100 sur {pourcent(part_plafond, 0)} des lignes "
      f"-> prix unitaire réel recalculé = SALES / QUANTITYORDERED")
df["PRIX_UNITAIRE_REEL"] = df["SALES"] / df["QUANTITYORDERED"]

# --- Périmètre de l'étude : commandes expédiées et résolues ---
ventes = df[df["STATUS"].isin(["Shipped", "Resolved"])].copy()
part_perimetre = ventes["SALES"].sum() / df["SALES"].sum()
print(f"\nPérimètre : commandes Shipped + Resolved = {pourcent(part_perimetre, 0)} du CA total")

# Colonnes utiles pour la suite
ventes["GAMME"] = ventes["PRODUCTLINE"].map(NOMS_GAMMES)
ventes["PAYS"] = ventes["COUNTRY"].map(NOMS_PAYS)
ventes["TERRITOIRE"] = ventes["TERRITORY"].map(NOMS_TERRITOIRES)
ventes["CA_CATALOGUE"] = ventes["QUANTITYORDERED"] * ventes["MSRP"]   # CA au prix catalogue
ventes["DATE"] = pd.to_datetime(ventes["ORDERDATE"], format="%m/%d/%Y %H:%M")


# =============================================================================
# 2. ÉVOLUTION DU CHIFFRE D'AFFAIRES
# =============================================================================

titre("2. ÉVOLUTION DU CHIFFRE D'AFFAIRES")

ca_annee = ventes.groupby("YEAR_ID")["SALES"].sum()
for annee in ANNEES:
    print(f"CA {LIBELLES_ANNEES[annee]:<17}: " + f"{ca_annee[annee] / 1e6:.2f} M$".replace(".", ","))
print(f"Croissance 2004 vs 2003 : {pourcent(ca_annee[2004] / ca_annee[2003] - 1, 0, signe=True)}")

# 2005 ne couvre que janvier à mai : on compare à la même période de 2004
jan_mai = ventes[ventes["MONTH_ID"] <= 5].groupby("YEAR_ID")["SALES"].sum()
print(f"Croissance janv.-mai 2005 vs janv.-mai 2004 : "
      f"{pourcent(jan_mai[2005] / jan_mai[2004] - 1, 0, signe=True)}")

# Saisonnalité : poids du 4e trimestre
print("\nPart du 4e trimestre dans le CA annuel :")
for annee in [2003, 2004]:
    t4 = ventes[(ventes["YEAR_ID"] == annee) & (ventes["QTR_ID"] == 4)]["SALES"].sum()
    print(f"   {annee} : {pourcent(t4 / ca_annee[annee], 0)}")

ca_mensuel = ventes.pivot_table(index="MONTH_ID", columns="YEAR_ID", values="SALES", aggfunc="sum")
mois_pic = ca_mensuel[[2003, 2004]].idxmax()
print(f"Mois le plus fort : novembre (mois n°{mois_pic[2003]} en 2003, n°{mois_pic[2004]} en 2004)")

# --- Figure 1 : CA par année ---
fig, ax = plt.subplots(figsize=(9, 5.5))
etiquettes = [LIBELLES_ANNEES[a].replace(" (", "\n(") for a in ANNEES]
barres = ax.bar(etiquettes, ca_annee[ANNEES] / 1e6, color=BLEU, width=0.6)
for barre, valeur in zip(barres, ca_annee[ANNEES] / 1e6):
    ax.text(barre.get_x() + barre.get_width() / 2, valeur + 0.08,
            f"{valeur:.2f} M$".replace(".", ","), ha="center", fontsize=12)
ax.set_ylabel("Chiffre d'affaires (millions de $)")
ax.spines[["top", "right"]].set_visible(False)
finir_figure(fig, "figure1_ca_par_annee.png", "Figure 1 — Chiffre d'affaires par année")

# --- Figure 2 : CA mensuel, une courbe par année ---
NOMS_MOIS = ["Janv.", "Févr.", "Mars", "Avr.", "Mai", "Juin",
             "Juil.", "Août", "Sept.", "Oct.", "Nov.", "Déc."]
fig, ax = plt.subplots(figsize=(10, 5.5))
for annee in ANNEES:
    serie = ca_mensuel[annee].dropna() / 1000
    ax.plot(serie.index, serie.values, marker="o", color=COULEURS_ANNEES[annee],
            linewidth=2.5 if annee == 2005 else 2, label=LIBELLES_ANNEES[annee])
ax.set_xticks(range(1, 13), NOMS_MOIS)
ax.set_ylabel("Chiffre d'affaires (milliers de $)")
ax.legend(frameon=False)
ax.grid(axis="y", color="#E6E9F2")
ax.spines[["top", "right"]].set_visible(False)
finir_figure(fig, "figure2_ca_mensuel.png", "Figure 2 — Chiffre d'affaires mensuel, une courbe par année")


# =============================================================================
# 3. MARCHÉS ET TERRITOIRES
# =============================================================================

titre("3. MARCHÉS ET TERRITOIRES")

print("Tableau 1 — Chiffre d'affaires par territoire")
tableau1 = tableau_par_annee(ventes, "TERRITOIRE")
afficher_tableau(tableau1, colonnes_dollars=list(tableau1.columns[:-1]),
                 colonnes_pourcent=["Part du CA"])

pays_emea = ventes[ventes["TERRITORY"] == "EMEA"]["PAYS"].nunique()
print(f"\nPays dans la zone EMEA (tous européens) : {pays_emea}")
part_eu_na = tableau1.loc[[NOMS_TERRITOIRES["EMEA"], NOMS_TERRITOIRES["NA"]], "Part du CA"].sum()
print(f"Europe + Amérique du Nord : {pourcent(part_eu_na, 0)} des ventes")

print("\nTableau 2 — Top 10 des pays par chiffre d'affaires")
tableau2 = tableau_par_annee(ventes, "PAYS", top=10, libelle_total="Total (10 pays)")
afficher_tableau(tableau2, colonnes_dollars=list(tableau2.columns[:-1]),
                 colonnes_pourcent=["Part du CA"])

part_pays = ventes.groupby("PAYS")["SALES"].sum().sort_values(ascending=False) / ventes["SALES"].sum()
print(f"\nÉtats-Unis : {pourcent(part_pays.iloc[0], 0)} du CA")
print(f"États-Unis + Espagne + France : {pourcent(part_pays.iloc[:3].sum(), 0)}")
print(f"10 premiers pays : {pourcent(part_pays.iloc[:10].sum(), 0)} "
      f"| {len(part_pays) - 10} autres pays : {pourcent(part_pays.iloc[10:].sum(), 0)}")

# Point d'alerte : la Norvège
norvege = ventes[ventes["COUNTRY"] == "Norway"]
print("\nPoint d'alerte : la Norvège")
print(f"   CA 2003 : {dollars(norvege[norvege['YEAR_ID'] == 2003]['SALES'].sum())}"
      f" | CA 2004 : {dollars(norvege[norvege['YEAR_ID'] == 2004]['SALES'].sum())}"
      f" | CA 2005 : {dollars(norvege[norvege['YEAR_ID'] == 2005]['SALES'].sum())}")
print(f"   Nombre de clients : {norvege['CUSTOMERNAME'].nunique()}"
      f" | dernière commande : {norvege['DATE'].max():%d/%m/%Y}")


# =============================================================================
# 4. CLIENTS
# =============================================================================

titre("4. CLIENTS")

ventes["CLIENT (PAYS)"] = ventes["CUSTOMERNAME"] + " (" + ventes["PAYS"] + ")"
print("Tableau 3 — Top 20 des clients par chiffre d'affaires")
tableau3 = tableau_par_annee(ventes, "CLIENT (PAYS)", top=20, libelle_total="Total (20 clients)")
afficher_tableau(tableau3, colonnes_dollars=list(tableau3.columns[:-1]),
                 colonnes_pourcent=["Part du CA"])

part_clients = ventes.groupby("CUSTOMERNAME")["SALES"].sum().sort_values(ascending=False) / ventes["SALES"].sum()
print(f"\nNombre de clients : {len(part_clients)}")
print(f"10 premiers clients : {pourcent(part_clients.iloc[:10].sum(), 0)} du CA")
print(f"20 premiers clients : {pourcent(part_clients.iloc[:20].sum(), 0)} du CA")
print(f"2 premiers clients ({', '.join(part_clients.index[:2])}) : "
      f"{pourcent(part_clients.iloc[:2].sum(), 0)} du CA")

# Les 20 premiers clients sans commande en 2005
top20 = part_clients.index[:20]
clients_2005 = set(ventes[ventes["YEAR_ID"] == 2005]["CUSTOMERNAME"])
sans_2005 = [c for c in top20 if c not in clients_2005]
print(f"\nClients du top 20 sans commande en 2005 : {len(sans_2005)}")
for client in sans_2005:
    print(f"   - {client}")

# Poids du 4e trimestre dans leurs achats de 2004
achats_2004 = ventes[(ventes["YEAR_ID"] == 2004) & (ventes["CUSTOMERNAME"].isin(sans_2005))]
part_ca_t4 = achats_2004[achats_2004["QTR_ID"] == 4]["SALES"].sum() / achats_2004["SALES"].sum()
part_cmd_t4 = (achats_2004.drop_duplicates("ORDERNUMBER")["QTR_ID"] == 4).mean()
print(f"Part de leur CA 2004 réalisée au 4e trimestre        : {pourcent(part_ca_t4, 0)}")
print(f"Part de leurs commandes 2004 passées au 4e trimestre : {pourcent(part_cmd_t4, 0)}")


# =============================================================================
# 5. FIDÉLISATION CLIENTS
# =============================================================================

titre("5. FIDÉLISATION CLIENTS")

clients_par_annee = {a: set(ventes[ventes["YEAR_ID"] == a]["CUSTOMERNAME"]) for a in ANNEES}
indicateurs = {}
for i, annee in enumerate(ANNEES):
    donnees_annee = ventes[ventes["YEAR_ID"] == annee]
    ca = donnees_annee["SALES"].sum()
    nb_commandes = donnees_annee["ORDERNUMBER"].nunique()
    nb_clients = len(clients_par_annee[annee])
    colonne = {
        "Chiffre d'affaires": dollars(ca),
        "Nombre de commandes": nb_commandes,
        "Clients actifs": nb_clients,
        "Panier moyen (CA / commande)": dollars(ca / nb_commandes),
        "Commandes par client": f"{nb_commandes / nb_clients:.1f}".replace(".", ","),
    }
    if i == 0:
        # 2003 est la première année : pas de comparaison possible
        colonne.update({"Nouveaux clients": "—", "Part du CA des nouveaux clients": "—",
                        "Clients perdus (vs année précédente)": "—", "Taux de rétention": "—"})
    else:
        # Nouveau client = n'a jamais commandé les années précédentes
        deja_clients = set().union(*[clients_par_annee[a] for a in ANNEES[:i]])
        nouveaux = clients_par_annee[annee] - deja_clients
        ca_nouveaux = donnees_annee[donnees_annee["CUSTOMERNAME"].isin(nouveaux)]["SALES"].sum()
        colonne["Nouveaux clients"] = len(nouveaux)
        colonne["Part du CA des nouveaux clients"] = pourcent(ca_nouveaux / ca, 0)
        if annee == 2004:
            # Rétention : clients de 2003 qui ont recommandé en 2004
            # (non calculée pour 2005, année incomplète)
            annee_prec = clients_par_annee[ANNEES[i - 1]]
            perdus = annee_prec - clients_par_annee[annee]
            colonne["Clients perdus (vs année précédente)"] = len(perdus)
            colonne["Taux de rétention"] = pourcent(1 - len(perdus) / len(annee_prec), 0)
        else:
            colonne["Clients perdus (vs année précédente)"] = "—"
            colonne["Taux de rétention"] = "—"
    indicateurs[LIBELLES_ANNEES[annee]] = colonne

print("Tableau 4 — Indicateurs de fidélisation clients par année")
print(pd.DataFrame(indicateurs).to_string())

# Commandes annulées ou en litige (hors périmètre de l'étude)
annulees = df[df["STATUS"].isin(["Cancelled", "Disputed"])]["SALES"].sum()
print(f"\nCommandes annulées ou en litige : {dollars(annulees)}, "
      f"soit {pourcent(annulees / df['SALES'].sum())} du CA total")


# =============================================================================
# 6. GAMMES DE PRODUITS
# =============================================================================

titre("6. GAMMES DE PRODUITS")

print("Tableau 5 — Chiffre d'affaires par gamme de produits")
tableau5 = tableau_par_annee(ventes, "GAMME")
afficher_tableau(tableau5, colonnes_dollars=list(tableau5.columns[:-1]),
                 colonnes_pourcent=["Part du CA"])

part_voitures = tableau5.loc[["Voitures classiques", "Voitures vintage"], "Part du CA"].sum()
print(f"\nVoitures classiques + vintage : {pourcent(part_voitures, 0)} des ventes")

print("\nCroissance 2004 vs 2003 par gamme :")
croissance = (tableau5["2004"] / tableau5["2003"] - 1).sort_values(ascending=False)
for gamme, valeur in croissance.items():
    print(f"   {gamme:<20} {pourcent(valeur, 0, signe=True)}")


# =============================================================================
# 7. RÉFÉRENCES PRODUITS
# =============================================================================

titre("7. RÉFÉRENCES PRODUITS")

ventes["RÉFÉRENCE (GAMME)"] = ventes["PRODUCTCODE"] + " (" + ventes["GAMME"] + ")"
print("Tableau 6 — Top 20 des références produits par chiffre d'affaires")
tableau6 = tableau_par_annee(ventes, "RÉFÉRENCE (GAMME)", top=20, libelle_total="Total (20 références)")
afficher_tableau(tableau6, colonnes_dollars=list(tableau6.columns[:-1]),
                 colonnes_pourcent=["Part du CA"])

top20_refs = (ventes.groupby(["PRODUCTCODE", "GAMME"])["SALES"].sum()
              .sort_values(ascending=False).head(20).reset_index())
print(f"\nNombre de références : {ventes['PRODUCTCODE'].nunique()}")
print(f"Part du CA des 20 premières : {pourcent(top20_refs['SALES'].sum() / ventes['SALES'].sum(), 0)}")
print("Répartition du top 20 par gamme :")
print(top20_refs["GAMME"].value_counts().to_string())
autres = top20_refs[top20_refs["GAMME"] != "Voitures classiques"]
print("Références d'autres gammes dans le top 20 :")
for _, ligne in autres.iterrows():
    print(f"   - {ligne['PRODUCTCODE']} ({ligne['GAMME']})")


# =============================================================================
# 8. ANALYSE DES PRIX
# =============================================================================

titre("8. ANALYSE DES PRIX")
print("Écart au prix catalogue = CA réel / (QUANTITYORDERED x MSRP) - 1  (moyenne pondérée)")

# --- Figure 3 : écart par gamme, toutes années confondues ---
par_gamme = ventes.groupby("GAMME")[["SALES", "CA_CATALOGUE"]].sum()
ecart_gamme = (par_gamme["SALES"] / par_gamme["CA_CATALOGUE"] - 1).sort_values()
print("\nÉcart au prix catalogue par gamme (janv. 2003 – mai 2005) :")
for gamme, valeur in ecart_gamme.items():
    print(f"   {gamme:<20} {pourcent(valeur, signe=True)}")

fig, ax = plt.subplots(figsize=(10, 5.5))
couleurs = [BLEU if v < 0 else GRIS for v in ecart_gamme.values]
barres = ax.barh(ecart_gamme.index, ecart_gamme.values * 100, color=couleurs, height=0.6)
ax.axvline(0, color="black", linewidth=1)
ax.text(0.2, len(ecart_gamme) - 0.45, "prix catalogue", fontsize=9, color="#555555", style="italic")
for barre, valeur in zip(barres, ecart_gamme.values * 100):
    ax.text(valeur + (0.3 if valeur >= 0 else -0.3), barre.get_y() + barre.get_height() / 2,
            f"{valeur:+.1f} %".replace(".", ","), va="center",
            ha="left" if valeur >= 0 else "right", fontsize=10,
            weight="bold" if valeur < 0 else "normal", color=BLEU if valeur < 0 else "black")
ax.set_xlim(ecart_gamme.min() * 100 - 3, ecart_gamme.max() * 100 + 3)
ax.set_ylim(-0.6, len(ecart_gamme) - 0.2)
ax.set_xlabel("Écart par rapport au prix catalogue (MSRP), en %")
ax.spines[["top", "right"]].set_visible(False)
finir_figure(fig, "figure3_ecart_prix_par_gamme.png", "Figure 3 — Écart moyen au prix catalogue par gamme")

# --- Figure 4 : écart par gamme et par année ---
par_gamme_annee = ventes.groupby(["GAMME", "YEAR_ID"])[["SALES", "CA_CATALOGUE"]].sum()
ecart_ga = (par_gamme_annee["SALES"] / par_gamme_annee["CA_CATALOGUE"] - 1).unstack("YEAR_ID")
ecart_ga = ecart_ga.sort_values(2005, ascending=False)     # le plus négatif en haut
print("\nÉcart au prix catalogue par gamme et par année :")
print(ecart_ga.rename(columns=LIBELLES_ANNEES).map(lambda v: pourcent(v, signe=True)).to_string())

fig, ax = plt.subplots(figsize=(10, 6.5))
hauteur = 0.26
positions = range(len(ecart_ga))
for j, annee in enumerate(ANNEES):
    y = [p + (1 - j) * hauteur for p in positions]      # 2003 en haut de chaque groupe
    valeurs = ecart_ga[annee] * 100
    ax.barh(y, valeurs, height=hauteur, color=COULEURS_ANNEES[annee], label=LIBELLES_ANNEES[annee])
    for yy, v in zip(y, valeurs):
        ax.text(v + (0.3 if v >= 0 else -0.3), yy, f"{v:+.1f} %".replace(".", ","),
                va="center", ha="left" if v >= 0 else "right", fontsize=7)
ax.set_yticks(list(positions), ecart_ga.index)
ax.set_xlim(ecart_ga.min().min() * 100 - 3, ecart_ga.max().max() * 100 + 5)
ax.axvline(0, color="black", linewidth=1)
ax.set_xlabel("Écart par rapport au prix catalogue (MSRP), en %  —  0 = prix catalogue")
ax.legend(title="Année", frameon=False, loc="upper right")
ax.spines[["top", "right"]].set_visible(False)
finir_figure(fig, "figure4_ecart_prix_par_gamme_annee.png",
             "Figure 4 — Écart moyen au prix catalogue par gamme et par année")

# --- Focus voitures classiques : manque à gagner ---
classiques = ventes[ventes["GAMME"] == "Voitures classiques"]
manque = (classiques.groupby("YEAR_ID")["CA_CATALOGUE"].sum()
          - classiques.groupby("YEAR_ID")["SALES"].sum())
print("\nVoitures classiques — manque à gagner par rapport au prix catalogue :")
for annee in ANNEES:
    print(f"   {LIBELLES_ANNEES[annee]:<17}: {manque[annee] / 1000:.0f} k$")
print(f"   Total             : {manque.sum() / 1000:.0f} k$")

lignes_2005 = classiques[classiques["YEAR_ID"] == 2005]
part_sous = (lignes_2005["SALES"] < lignes_2005["CA_CATALOGUE"]).mean()
print(f"Lignes de commande 2005 vendues sous le prix catalogue : {pourcent(part_sous, 0)}")


# =============================================================================
# 9. RECOMMANDATIONS — chiffres utilisés
# =============================================================================

titre("9. RECOMMANDATIONS — chiffres utilisés")
print(f"1. Récupérer la moitié de l'écart 2004 sur les voitures classiques : "
      f"environ {manque[2004] / 2 / 1000:.0f} k$ par an")
print(f"2. Poids du 4e trimestre : 44 à 52 % du CA annuel (voir section 2)")
print(f"3. Clients du top 20 sans commande en 2005 : {len(sans_2005)} ; Norvège sans commande "
      f"depuis le {norvege['DATE'].max():%d/%m/%Y}")
print(f"5. Euro Shopping Channel + Mini Gifts Distributors : {pourcent(part_clients.iloc[:2].sum(), 0)} des ventes")

plt.show()   # affiche les 4 graphiques à la fin
