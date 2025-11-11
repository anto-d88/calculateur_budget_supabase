# ======================================================
# ⚡ DASHBOARD SPIRBOOST - Chargement Dragon Ball Z + Statistiques
# ======================================================

import streamlit as st
import time
import random
from supabase import create_client
from dotenv import load_dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ======================================================
# 🔐 SÉCURITÉ : UTILISATEUR CONNECTÉ
# ======================================================
if "user" not in st.session_state or st.session_state["user"] is None:
    st.warning("⚠️ Tu dois être connecté pour accéder au tableau de bord.")
    st.stop()

# ======================================================
# 🌀 ANIMATION DE CHARGEMENT - DRAGON BALL STYLE
# ======================================================
if "dashboard_loaded" not in st.session_state:
    st.session_state["dashboard_loaded"] = False

if not st.session_state["dashboard_loaded"]:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(
            """
            <div style="
                text-align:center;
                font-size:24px;
                color:#00f6ff;
                font-weight:bold;
                margin-top:50px;
                text-shadow: 0 0 15px #00f6ff, 0 0 25px #00f6ff;
                ">
                ⚡ Chargement du Ki... Concentration maximale...
            </div>
            <div style='display:flex;justify-content:center;margin-top:20px;'>
                <div style="
                    width:150px;
                    height:150px;
                    border-radius:50%;
                    background: radial-gradient(circle, #00f6ff, #001f33);
                    box-shadow: 0 0 40px #00f6ff, 0 0 80px #00f6ff, inset 0 0 20px #fff;
                    animation: pulse 1.2s infinite;
                "></div>
            </div>
            <style>
                @keyframes pulse {
                    0% { transform: scale(1); opacity: 0.9; }
                    50% { transform: scale(1.15); opacity: 1; }
                    100% { transform: scale(1); opacity: 0.9; }
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        progress = st.progress(0)
        for i in range(0, 101, 5):
            time.sleep(random.uniform(0.03, 0.08))
            progress.progress(i)
        placeholder.empty()
    st.session_state["dashboard_loaded"] = True

# ======================================================
# 🔧 CONNEXION SUPABASE
# ======================================================
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# ======================================================
# 📊 TABLEAU DE BORD FINANCIER
# ======================================================
st.title("📊 Tableau de bord financier SpirBoost")
st.markdown(f"Bienvenue **{st.session_state['user'].email}** 👋")

try:
    user_id = getattr(st.session_state["user"], "id", None)
    data = (
        supabase.table("transactions")
        .select("*")
        .eq("user_id", user_id)
        .order("date", desc=True)
        .execute()
    )

    if not data.data:
        st.info("Aucune transaction enregistrée pour le moment.")
        st.stop()

    df = pd.DataFrame(data.data)
    df["montant"] = df["montant"].astype(float)
    df["date"] = pd.to_datetime(df["date"]).dt.date

except Exception as e:
    st.error(f"Erreur lors du chargement des données : {e}")
    st.stop()

# ======================================================
# 💰 STATISTIQUES GLOBALES
# ======================================================
total_revenu = df.loc[df["type"] == "revenu", "montant"].sum()
total_depense = df.loc[df["type"] == "dépense", "montant"].sum()
solde = total_revenu - total_depense

col1, col2, col3 = st.columns(3)
col1.metric("💸 Revenu total", f"{total_revenu:.2f} €")
col2.metric("📉 Dépenses totales", f"{total_depense:.2f} €")
col3.metric("💰 Solde actuel", f"{solde:.2f} €")

st.markdown("---")

# ======================================================
# 📈 GRAPHIQUE Revenus vs Dépenses
# ======================================================
st.subheader("📅 Évolution mensuelle")
try:
    df["mois"] = pd.to_datetime(df["date"]).dt.to_period("M")
    grouped = df.groupby(["mois", "type"])["montant"].sum().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(8, 4))
    grouped.plot(kind="bar", ax=ax, color=["#00f6ff", "#ff4b4b"])
    plt.title("Revenus vs Dépenses mensuelles", color="white", fontsize=14)
    plt.xlabel("Mois", color="white")
    plt.ylabel("Montant (€)", color="white")
    plt.xticks(rotation=45, color="white")
    plt.yticks(color="white")
    plt.grid(alpha=0.3)
    plt.legend(["Revenus", "Dépenses"], loc="upper left")
    plt.gcf().patch.set_facecolor("#0e1117")
    ax.set_facecolor("#0e1117")
    st.pyplot(fig)
except Exception as e:
    st.warning(f"Pas assez de données pour le graphique : {e}")

# ======================================================
# 🥧 RÉPARTITION DES DÉPENSES
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
            colors=plt.cm.cool(np.linspace(0, 1, len(grouped_cat))),
        )
        plt.title("Répartition des dépenses par catégorie", color="white")
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
