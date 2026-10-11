"""
Prévision du chiffre d'affaires 2005 — Sample Sales Data
Mehdi Graoui — octobre 2026

Les données s'arrêtent en mai 2005. Ce script estime le chiffre d'affaires
de juin à décembre 2005, puis l'année 2005 complète, avec deux méthodes
simples adaptées au peu d'historique disponible (29 mois) :

    Méthode 1 — Taux de croissance : on applique à juin-déc. 2004 la
                croissance observée sur janv.-mai 2005 vs janv.-mai 2004.
    Méthode 2 — Coefficients saisonniers : on estime la part de chaque mois
                dans l'année (moyenne 2003-2004) et on en déduit l'année
                complète à partir de janv.-mai 2005.
    Méthode 3 — Reconduction (naïve) : on reconduit juin-déc. 2004 sans
                croissance (scénario bas).

    Prévision retenue : la moyenne des trois méthodes, mois par mois. Les
    méthodes 1 et 2 ont tendance à surestimer, la méthode 3 à sous-estimer :
    leurs erreurs se compensent en partie.

Avant de prévoir 2005, chaque méthode est testée sur 2004 : on fait comme si
on était fin mai 2004 et on compare la prévision au réel de juin-déc. 2004.

Utilisation :
    1. Placer ce script dans le même dossier que sales_data_sample.csv
    2. Installer les bibliothèques :  pip install pandas matplotlib
    3. Lancer :                       python prevision_2005.py

Les résultats s'affichent dans la console. Les 2 figures sont enregistrées
en PNG dans le dossier du script (figure5 et figure6).
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# =============================================================================
# 0. PARAMÈTRES GÉNÉRAUX
# =============================================================================

DOSSIER = Path(__file__).resolve().parent
FICHIER = DOSSIER / "sales_data_sample.csv"

BLEU = "#152C73"            # réel
ORANGE = "#D9822B"          # méthode 1 (taux de croissance)
VERT = "#2E8B57"            # méthode 2 (coefficients saisonniers)
GRIS = "#8A8F99"            # méthode 3 (reconduction)
ROUGE = "#C0392B"           # prévision retenue (moyenne des 3 méthodes)
SOURCE = ("Source : Sample Sales Data, toutes commandes hors annulées "
          "(janv. 2003 – mai 2005). Prévisions : calculs de l'auteur.")

NOMS_MOIS = ["Janv.", "Févr.", "Mars", "Avr.", "Mai", "Juin",
             "Juil.", "Août", "Sept.", "Oct.", "Nov.", "Déc."]
MOIS_CONNUS = range(1, 6)       # janvier à mai : connus en 2005
MOIS_A_PREVOIR = range(6, 13)   # juin à décembre : à prévoir


# --- Petites fonctions d'affichage (format français) -------------------------

def dollars(valeur):
    """12345.6 -> '12 346 $'."""
    return f"{valeur:,.0f} $".replace(",", " ")


def millions(valeur):
    """6431000 -> '6,43 M$'."""
    return f"{valeur / 1e6:.2f} M$".replace(".", ",")


def pourcent(valeur, decimales=1, signe=False):
    """0.4935 -> '49,3 %'  (valeur donnée en proportion)."""
    valeur = round(valeur * 100, decimales) + 0.0
    texte = f"{valeur:+.{decimales}f} %" if signe else f"{valeur:.{decimales}f} %"
    return texte.replace(".", ",")


def titre(texte):
    print("\n" + "=" * 90)
    print(texte)
    print("=" * 90)


def finir_figure(fig, nom_fichier, legende):
    """Ajoute la légende « Figure X — ... / Source » et enregistre."""
    fig.text(0.5, 0.01, f"{legende}\n{SOURCE}", ha="center", va="bottom",
             fontsize=9, color="#555555", style="italic")
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig(DOSSIER / nom_fichier, dpi=150)
    print(f"   -> graphique enregistré : {nom_fichier}")


# =============================================================================
# 1. DONNÉES ET PÉRIMÈTRE
# =============================================================================

titre("1. DONNÉES ET PÉRIMÈTRE")

try:
    brut = pd.read_csv(FICHIER, encoding="utf-8", keep_default_na=False)
except UnicodeDecodeError:
    brut = pd.read_csv(FICHIER, encoding="cp850", keep_default_na=False)

# Pour l'analyse, l'étude retient les commandes expédiées ou résolues.
# Pour la prévision, ce périmètre est biaisé : en avril-mai 2005, une grande
# partie des commandes est encore « In Process », « On Hold » ou « Disputed »
# (pas encore expédiée). On prévoit donc la DEMANDE : toutes les commandes
# passées, sauf les commandes annulées.
commandes = brut[brut["STATUS"] != "Cancelled"].copy()

ca_mensuel = commandes.pivot_table(index="MONTH_ID", columns="YEAR_ID",
                                   values="SALES", aggfunc="sum")
ca_annee = ca_mensuel.sum()

expedie = brut[brut["STATUS"].isin(["Shipped", "Resolved"])]
ca_expedie_2005 = expedie[expedie["YEAR_ID"] == 2005]["SALES"].sum()

print("Périmètre de la prévision : toutes les commandes sauf « Cancelled »")
print(f"CA janv.-mai 2005, commandes passées (hors annulées) : {millions(ca_annee[2005])}")
print(f"CA janv.-mai 2005, commandes expédiées ou résolues   : {millions(ca_expedie_2005)}")
print(f"-> {millions(ca_annee[2005] - ca_expedie_2005)} de commandes 2005 pas encore "
      "expédiées : on les garde pour ne pas sous-estimer 2005.")

print("\nCA mensuel (commandes hors annulées) :")
affichage = ca_mensuel.copy()
affichage.index = NOMS_MOIS
print(affichage.apply(lambda col: col.map(lambda v: "" if pd.isna(v) else dollars(v))).to_string())


# =============================================================================
# 2. LES DEUX MÉTHODES (écrites une seule fois, réutilisées pour le test)
# =============================================================================

def methode_croissance(ca_mensuel, annee):
    """Méthode 1 — applique la croissance de janv.-mai à juin-déc. de l'année précédente.

    Renvoie (prévisions juin-déc., taux de croissance).
    """
    jan_mai = ca_mensuel.loc[MOIS_CONNUS, annee].sum()
    jan_mai_avant = ca_mensuel.loc[MOIS_CONNUS, annee - 1].sum()
    taux = jan_mai / jan_mai_avant
    prevision = ca_mensuel.loc[MOIS_A_PREVOIR, annee - 1] * taux
    return prevision, taux - 1


def methode_saisonniere(ca_mensuel, annee, annees_historique):
    """Méthode 2 — coefficients saisonniers (part de chaque mois dans l'année).

    Renvoie (prévisions juin-déc., part de janv.-mai dans l'année).
    """
    parts = ca_mensuel[annees_historique] / ca_mensuel[annees_historique].sum()
    part_moyenne = parts.mean(axis=1)                  # part moyenne de chaque mois
    part_jan_mai = part_moyenne[MOIS_CONNUS].sum()
    annee_complete = ca_mensuel.loc[MOIS_CONNUS, annee].sum() / part_jan_mai
    prevision = annee_complete * part_moyenne[MOIS_A_PREVOIR]
    return prevision, part_jan_mai


# =============================================================================
# 3. TEST SUR 2004 : SI ON AVAIT ÉTÉ FIN MAI 2004
# =============================================================================

titre("3. TEST DES MÉTHODES SUR 2004 (prévision de juin-déc. 2004)")

reel_2004 = ca_mensuel.loc[MOIS_A_PREVOIR, 2004]
test_m1, taux_test = methode_croissance(ca_mensuel, 2004)
test_m2, part_test = methode_saisonniere(ca_mensuel, 2004, [2003])

# Point de comparaison naïf : on reconduit juin-déc. 2003 sans croissance.
# Une bonne méthode doit au moins faire mieux que ça.
test_naif = ca_mensuel.loc[MOIS_A_PREVOIR, 2003]

print(f"Méthode 1 : croissance janv.-mai 2004 vs 2003 = {pourcent(taux_test, 0, signe=True)}")
print(f"Méthode 2 : part de janv.-mai dans l'année 2003 = {pourcent(part_test)}")
print("Remarque : avec une seule année d'historique (2003), les deux méthodes font le\n"
      "même calcul (CA 2003 du mois × janv.-mai 2004 / janv.-mai 2003) et donnent donc\n"
      "le même résultat. Elles diffèrent pour 2005, car la méthode 2 utilise alors la\n"
      "saisonnalité moyenne de 2003 ET 2004.")

test_moyenne = (test_naif + test_m1 + test_m2) / 3     # prévision retenue

test = pd.DataFrame({"Réel 2004": reel_2004,
                     "Méthode 3": test_naif,
                     "Méthode 1": test_m1,
                     "Méthode 2": test_m2,
                     "Moyenne": test_moyenne})
test.loc["Total juin-déc."] = test.sum()


def erreur_totale(prevision):
    """Écart du total juin-déc. prévu par rapport au réel (en proportion)."""
    return prevision.sum() / reel_2004.sum() - 1


def erreur_mensuelle_moyenne(prevision):
    """MAPE : erreur absolue moyenne mois par mois (en proportion)."""
    return ((prevision - reel_2004).abs() / reel_2004).mean()


print("\nPrévision de juin-déc. 2004 comparée au réel :")
affichage = test.copy()
affichage.index = NOMS_MOIS[5:] + ["Total juin-déc."]
print(affichage.apply(lambda col: col.map(dollars)).to_string())

print("\nQualité des méthodes sur 2004 :")
for nom, prevision in [("Méthode 3", test_naif), ("Méthode 1", test_m1), ("Méthode 2", test_m2),
                       ("Moyenne", test_moyenne)]:
    print(f"   {nom:<11} : erreur sur le total = {pourcent(erreur_totale(prevision), 1, signe=True)}"
          f" | erreur moyenne mois par mois (MAPE) = {pourcent(erreur_mensuelle_moyenne(prevision))}")
print("-> Les méthodes 1 et 2 surestiment 2004 : la croissance du début d'année (+51 %) ne\n"
      "   s'est pas maintenue sur toute l'année. La méthode 3 sous-estime. La moyenne des trois\n"
      "   méthodes est la plus précise : c'est elle qui est retenue pour 2005.")

# --- Figure 6 : test sur 2004 ---
fig, ax = plt.subplots(figsize=(10, 5.5))
x = list(MOIS_A_PREVOIR)
ax.plot(x, reel_2004 / 1000, marker="o", color=BLEU, linewidth=2.5, label="Réel 2004")
ax.plot(x, test_naif / 1000, marker="o", linestyle="--", color=GRIS, linewidth=1.3, alpha=0.75,
        label=f"Méthode 3 — 2003 reconduit (total {pourcent(erreur_totale(test_naif), 0, signe=True)})")
ax.plot(x, test_m1 / 1000, marker="s", linestyle="--", color=ORANGE, linewidth=1.3, alpha=0.75,
        label=f"Méthodes 1 et 2 — identiques sur ce test (total {pourcent(erreur_totale(test_m1), 0, signe=True)})")
ax.plot(x, test_moyenne / 1000, marker="D", color=ROUGE, linewidth=2.8,
        label=f"Moyenne des 3 méthodes — retenue (total {pourcent(erreur_totale(test_moyenne), 0, signe=True)})")
ax.set_xticks(x, NOMS_MOIS[5:])
ax.set_ylabel("Chiffre d'affaires (milliers de $)")
ax.legend(frameon=False)
ax.grid(axis="y", color="#E6E9F2")
ax.spines[["top", "right"]].set_visible(False)
finir_figure(fig, "figure6_test_prevision_2004.png",
             "Figure 6 — Test des méthodes : prévision de juin-déc. 2004 faite fin mai 2004, comparée au réel")


# =============================================================================
# 4. PRÉVISION DE 2005
# =============================================================================

titre("4. PRÉVISION DE JUIN-DÉCEMBRE 2005 ET DE L'ANNÉE 2005")

prev_m1, taux_2005 = methode_croissance(ca_mensuel, 2005)
prev_m2, part_2005 = methode_saisonniere(ca_mensuel, 2005, [2003, 2004])

print(f"Méthode 1 : croissance janv.-mai 2005 vs 2004 = {pourcent(taux_2005, 0, signe=True)}")
print(f"Méthode 2 : part moyenne de janv.-mai dans l'année (2003-2004) = {pourcent(part_2005)}")

# Méthode 3 : juin-déc. 2004 reconduit sans croissance (le « naïf » du test).
# En 2004, le réel est tombé entre le naïf (-21 %) et les méthodes 1-2 (+20 %).
prev_m3 = ca_mensuel.loc[MOIS_A_PREVOIR, 2004]

prevision = pd.DataFrame({"Méthode 1": prev_m1, "Méthode 2": prev_m2, "Méthode 3": prev_m3})
prevision["Retenue"] = prevision.mean(axis=1)          # moyenne des trois méthodes
affichage = prevision.copy()
affichage.index = NOMS_MOIS[5:]
affichage.loc["Total juin-déc."] = prevision.sum()
print("\nPrévision mensuelle de juin à décembre 2005 :")
print(affichage.apply(lambda col: col.map(dollars)).to_string())

jan_mai_2005 = ca_annee[2005]
print(f"\nCA réel janv.-mai 2005 : {millions(jan_mai_2005)}")
print("\nCA 2005 complet estimé (janv.-mai réel + juin-déc. prévu) :")
totaux = {}
for nom in prevision.columns:
    totaux[nom] = jan_mai_2005 + prevision[nom].sum()
    print(f"   {nom:<12}: {millions(totaux[nom])}  "
          f"(soit {pourcent(totaux[nom] / ca_annee[2004] - 1, 0, signe=True)} vs 2004)")
bas = min(totaux["Méthode 1"], totaux["Méthode 2"], totaux["Méthode 3"])
haut = max(totaux["Méthode 1"], totaux["Méthode 2"], totaux["Méthode 3"])
print(f"\nFourchette 2005 : de {millions(bas)} (méthode 3, sans croissance) "
      f"à {millions(haut)} (méthode 2)")
print(f"PRÉVISION RETENUE (moyenne des 3 méthodes) : {millions(totaux['Retenue'])} "
      f"(soit {pourcent(totaux['Retenue'] / ca_annee[2004] - 1, 0, signe=True)} vs 2004)")

# --- Figure 5 : réel 2003-2005 et prévisions juin-déc. 2005 ---
dates = pd.date_range("2003-01-01", "2005-12-01", freq="MS")
reel = pd.Series([ca_mensuel.loc[d.month, d.year] for d in dates], index=dates).dropna()
dates_prev = pd.date_range("2005-06-01", "2005-12-01", freq="MS")
dernier = reel.index[-1]        # mai 2005 : on relie les prévisions au dernier point réel

fig, ax = plt.subplots(figsize=(11, 5.5))
ax.plot(reel.index, reel / 1000, marker="o", markersize=4, color=BLEU, linewidth=2,
        label="Réel (hors commandes annulées)")
for nom, couleur, marqueur, libelle in [("Méthode 3", GRIS, "o", "Méthode 3 — 2004 reconduit"),
                                         ("Méthode 1", ORANGE, "s", "Méthode 1 — taux de croissance"),
                                         ("Méthode 2", VERT, "^", "Méthode 2 — coefficients saisonniers")]:
    serie = pd.Series(prevision[nom].values, index=dates_prev)
    serie = pd.concat([reel[[dernier]], serie])
    ax.plot(serie.index, serie / 1000, marker=marqueur, markersize=4, linestyle="--",
            color=couleur, linewidth=1.3, alpha=0.75,
            label=f"{libelle} (2005 : {millions(totaux[nom])})")
# Prévision retenue : moyenne des trois méthodes, en trait plein et plus épais
serie = pd.concat([reel[[dernier]], pd.Series(prevision["Retenue"].values, index=dates_prev)])
ax.plot(serie.index, serie / 1000, marker="D", markersize=5, color=ROUGE, linewidth=2.8,
        label=f"Prévision retenue — moyenne des 3 méthodes (2005 : {millions(totaux['Retenue'])})")
ax.axvspan(pd.Timestamp("2005-05-16"), pd.Timestamp("2005-12-31"), color="#F2F4F8", zorder=0)
ax.text(pd.Timestamp("2005-06-05"), ax.get_ylim()[1] * 0.95, "prévision", fontsize=10,
        color=GRIS, style="italic")
graduations = pd.date_range("2003-01-01", "2005-12-01", freq="4MS")
ax.set_xticks(graduations, [f"{NOMS_MOIS[d.month - 1]} {d.year}" for d in graduations])
ax.set_ylabel("Chiffre d'affaires (milliers de $)")
ax.legend(frameon=False, loc="upper left")
ax.grid(axis="y", color="#E6E9F2")
ax.spines[["top", "right"]].set_visible(False)
finir_figure(fig, "figure5_prevision_2005.png",
             "Figure 5 — Chiffre d'affaires mensuel réel (2003 – mai 2005) et prévision de juin à décembre 2005")

print("\nFin du script.")
