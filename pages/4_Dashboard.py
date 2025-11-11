# ======================================================
# 📊 DASHBOARD FINANCIER - Budget Antonio Z
# ======================================================

import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt

# ======================================================
# 🔐 CONNEXION SUPABASE
# ======================================================
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# ======================================================
# 👤 VÉRIFICATION UTILISATEUR
# ======================================================
if "user" not in st.session_state or st.session_state["user"] is None:
    st.warning("⚠️ Tu dois être connecté pour voir ton tableau de bord.")
    st.page_link("app.py", label="🔐 Retour à la connexion", icon="➡️")
    st.stop()

user = st.session_state.get("user")
user_id = getattr(user, "id", None)
user_email = getattr(user, "email", None)

st.title("📊 Tableau de bord financier")
st.markdown(f"Bienvenue **{user_email}** 👋")

# ======================================================
# 📥 RÉCUPÉRATION DES DONNÉES
# ======================================================
try:
    data = (
        supabase.table("transactions")
        .select("*")
        .eq("user_id", user_id)
        .order("date", desc=True)
        .execute()
    )

    if not data.data:
        st.info("Aucune transaction enregistrée pour l’instant.")
        st.stop()

    df = pd.DataFrame(data.data)
    df["montant"] = df["montant"].astype(float)
    df["date"] = pd.to_datetime(df["date"]).dt.date

except Exception as e:
    st.error(f"Erreur lors du chargement des données : {e}")
    st.stop()

# ======================================================
# 💰 CALCULS GLOBAUX
# ======================================================
total_revenu = df.loc[df["type"] == "revenu", "montant"].sum()
total_depense = df.loc[df["type"] == "dépense", "montant"].sum()
solde = total_revenu - total_depense

col1, col2, col3 = st.columns(3)
col1.metric("💸 Revenu total", f"{total_revenu:.2f} €")
col2.metric("📉 Dépenses totales", f"{total_depense:.2f} €")
col3.metric(
    "💰 Solde actuel",
    f"{solde:.2f} €",
    delta=f"{solde - total_depense:.2f} €" if total_depense else None,
)

st.markdown("---")

# ======================================================
# 📈 GRAPHIQUE Revenus vs Dépenses (par mois)
# ======================================================
st.subheader("📅 Évolution mensuelle")

try:
    df["mois"] = pd.to_datetime(df["date"]).dt.to_period("M")
    grouped = df.groupby(["mois", "type"])["montant"].sum().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(8, 4))
    grouped.plot(kind="bar", ax=ax)
    plt.title("Revenus vs Dépenses mensuelles")
    plt.xlabel("Mois")
    plt.ylabel("Montant (€)")
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.legend(["Revenus", "Dépenses"])
    st.pyplot(fig)
except Exception as e:
    st.warning(f"Pas assez de données pour le graphique mensuel : {e}")

# ======================================================
# 🥧 GRAPHIQUE Répartition par catégorie
# ======================================================
st.subheader("🥧 Répartition des dépenses par catégorie")

try:
    depenses = df[df["type"] == "dépense"]
    if not depenses.empty:
        grouped_cat = depenses.groupby("categorie")["montant"].sum()

        fig2, ax2 = plt.subplots(figsize=(5, 5))
        ax2.pie(
            grouped_cat,
            labels=grouped_cat.index,
            autopct="%1.1f%%",
            startangle=90,
            textprops={"color": "white"},
        )
        plt.title("Répartition des dépenses par catégorie")
        st.pyplot(fig2)
    else:
        st.info("Aucune dépense enregistrée pour le moment.")
except Exception as e:
    st.warning(f"Erreur dans la création du graphique : {e}")

# ======================================================
# 📆 FILTRE PAR PÉRIODE
# ======================================================
st.markdown("---")
st.subheader("📆 Filtrer les transactions")

min_date = df["date"].min()
max_date = df["date"].max()
date_range = st.slider(
    "Choisis une période",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
)

filtered = df[(df["date"] >= date_range[0]) & (df["date"] <= date_range[1])]
st.write(f"📅 Transactions du **{date_range[0]}** au **{date_range[1]}**")

st.dataframe(
    filtered[["date", "type", "description", "categorie", "montant"]]
    .sort_values("date", ascending=False)
    .reset_index(drop=True)
)
