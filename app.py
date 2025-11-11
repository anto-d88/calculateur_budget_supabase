# ============================================================
# 💸 CALCULATEUR DE BUDGET — DASHBOARD DESIGN + GRAPHIQUES
# ============================================================
import os
from datetime import datetime, timezone
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client
import matplotlib.pyplot as plt
from themes import THEMES

# ------------------------------
# ⚙️ CONFIG DE PAGE + MOBILE
# ------------------------------
st.set_page_config(page_title="💸 Calculateur de Budget", page_icon="💰", layout="wide")

st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<style>
    body {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    header {visibility: hidden;} /* Supprime le header Streamlit par défaut */

    .main-title {
        font-size: 2.3rem;
        font-weight: bold;
        margin-top: 60px;
        margin-bottom: 30px;
        text-align: center;
        color: #4CAF50;
    }

    /* Barre supérieure sombre */
    .top-bar {
        background-color: #1C1C1E;
        color: #F5F5F5;
        padding: 14px;
        position: fixed;
        top: 0;
        width: 100%;
        z-index: 100;
        text-align: center;
        border-bottom: 1px solid #333;
    }

    .card {
        background-color: #1E1E2F;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        min-width: 300px;
        text-align: center;
    }

    .card h2 {
        margin: 0;
        color: #4CAF50;
    }

    .metric-value {
        font-size: 2.3rem;
        font-weight: 600;
        margin-top: 10px;
    }

    .metric-label {
        color: #B0B0B0;
        font-size: 1rem;
        margin-top: 5px;
    }

</style>
""", unsafe_allow_html=True)

# ------------------------------
# 🔐 SUPABASE
# ------------------------------
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# ------------------------------
# 👤 SESSION UTILISATEUR
# ------------------------------
if "user" not in st.session_state:
    st.session_state["user"] = None

def login(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return res.user
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
        return None

def signup(email, password):
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        if res.user:
            st.success("✅ Compte créé ! Confirme ton e-mail avant de te connecter.")
    except Exception as e:
        st.error(f"Erreur : {e}")

def logout():
    st.session_state["user"] = None
    st.rerun()

# ------------------------------
# 🔑 AUTH
# ------------------------------
if not st.session_state["user"]:
    st.markdown('<div class="top-bar">💰 Calculateur Budget Antonio</div>', unsafe_allow_html=True)
    st.markdown("<h1 class='main-title'>🔐 Connexion à ton espace budget</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Se connecter", "Créer un compte"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter"):
            user = login(email, password)
            if user:
                st.session_state["user"] = user
                st.success("Connexion réussie ✅")
                st.rerun()

    with tab2:
        new_email = st.text_input("Nouvel email")
        new_password = st.text_input("Nouveau mot de passe", type="password")
        if st.button("Créer le compte"):
            if new_email and new_password:
                signup(new_email, new_password)
            else:
                st.warning("Remplis tous les champs.")
    st.stop()

# ------------------------------
# 🏠 DASHBOARD
# ------------------------------
user = st.session_state["user"]
user_id = getattr(user, "id", None)
user_email = getattr(user, "email", None)

st.markdown('<div class="top-bar">💰 Calculateur Budget Antonio</div>', unsafe_allow_html=True)
st.markdown(f"<h1 class='main-title'>Bienvenue {user_email} 👋</h1>", unsafe_allow_html=True)

if st.button("Se déconnecter"):
    logout()

# -------- Récupération des transactions --------
df = pd.DataFrame()
try:
    q = supabase.table("transactions").select("*").order("date", desc=True)
    if user_id:
        q = q.eq("user_id", user_id)
    elif user_email:
        q = q.eq("user_email", user_email)
    data = q.execute()
    if data.data:
        df = pd.DataFrame(data.data)
except Exception as e:
    st.error(f"Erreur lors du chargement : {e}")

# -------- Calcul des totaux --------
total_revenu = df.loc[df["type"] == "revenu", "montant"].sum() if not df.empty else 0
total_depense = df.loc[df["type"].isin(["dépense", "crédit", "voiture"]), "montant"].sum() if not df.empty else 0
solde = float(total_revenu) - float(total_depense)

# ------------------------------
# 📊 CARTES + GRAPHIQUES
# ------------------------------
col1, col2, col3 = st.columns(3, gap="large")

# 💰 SOLDE
with col1:
    st.markdown(
        f"""
        <div class="card">
            <h2>💰 Solde</h2>
            <div class="metric-value" style="color:{'limegreen' if solde >= 0 else 'tomato'};">{solde:.2f} €</div>
            <div class="metric-label">Solde total actuel</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if not df.empty:
        fig, ax = plt.subplots(figsize=(3, 1.5))
        df["date"] = pd.to_datetime(df["date"])
        ax.plot(df["date"], df["montant"].cumsum(), color="limegreen")
        ax.set_xticks([]); ax.set_yticks([]); ax.set_facecolor("#1E1E2F")
        st.pyplot(fig)

# 📈 REVENUS
with col2:
    st.markdown(
        f"""
        <div class="card">
            <h2>📈 Revenus</h2>
            <div class="metric-value" style="color:limegreen;">+{total_revenu:.2f} €</div>
            <div class="metric-label">Somme totale des revenus</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if not df.empty:
        fig, ax = plt.subplots(figsize=(3, 1.5))
        revenus = df[df["type"] == "revenu"]
        if not revenus.empty:
            ax.bar(revenus["date"].dt.strftime("%m-%d"), revenus["montant"], color="#4CAF50")
        ax.set_xticks([]); ax.set_yticks([]); ax.set_facecolor("#1E1E2F")
        st.pyplot(fig)

# 📉 DÉPENSES
with col3:
    st.markdown(
        f"""
        <div class="card">
            <h2>📉 Dépenses</h2>
            <div class="metric-value" style="color:tomato;">-{total_depense:.2f} €</div>
            <div class="metric-label">Total des dépenses</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if not df.empty:
        fig, ax = plt.subplots(figsize=(3, 1.5))
        dep = df[df["type"].isin(["dépense", "crédit", "voiture"])]
        if not dep.empty:
            ax.bar(dep["date"].dt.strftime("%m-%d"), dep["montant"], color="tomato")
        ax.set_xticks([]); ax.set_yticks([]); ax.set_facecolor("#1E1E2F")
        st.pyplot(fig)
