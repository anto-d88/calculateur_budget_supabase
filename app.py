# ======================================================
# 💸 APP PRINCIPALE SPIRBOOST - Connexion / Authentification
# ======================================================

import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os

# ======================================================
# 🔧 CONFIGURATION GLOBALE STREAMLIT
# ======================================================
st.set_page_config(page_title="💸 SpirBoost Budget", page_icon="💰", layout="centered")

# Design responsive + style global
st.markdown("""
<style>
.block-container {padding-top:1rem;padding-bottom:2rem;}
button[kind="primary"] {height:50px !important;font-size:18px !important;}
</style>
""", unsafe_allow_html=True)

# ======================================================
# 🔐 CONNEXION À SUPABASE
# ======================================================
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# ======================================================
# 🧠 GESTION DE SESSION
# ======================================================
if "user" not in st.session_state:
    st.session_state["user"] = None

if "dashboard_loaded" not in st.session_state:
    st.session_state["dashboard_loaded"] = False  # pour reset la barre Dragon Ball

# ======================================================
# 🧩 FONCTIONS D’AUTHENTIFICATION
# ======================================================
def login(email, password):
    """Connexion utilisateur"""
    try:
        result = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return result.user
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
        return None

def signup(email, password):
    """Création d’un nouveau compte"""
    try:
        result = supabase.auth.sign_up({"email": email, "password": password})
        if result.user:
            st.success("✅ Compte créé ! Vérifie ton e-mail avant de te connecter.")
    except Exception as e:
        st.error(f"Erreur : {e}")

def logout():
    """Déconnexion complète"""
    st.session_state["user"] = None
    st.session_state["dashboard_loaded"] = False  # Rejoue la barre au prochain accès Dashboard
    st.success("Déconnexion réussie ✅")
    st.rerun()

# ======================================================
# 🔑 PAGE D’AUTHENTIFICATION
# ======================================================
if not st.session_state["user"]:
    st.title("🔐 Connexion à ton espace SpirBoost")

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
                st.warning("⚠️ Remplis tous les champs avant de créer ton compte.")
    st.stop()

# ======================================================
# 🏠 ACCUEIL APRÈS CONNEXION
# ======================================================
st.title("🏠 Accueil SpirBoost Budget")
st.markdown(f"Bienvenue **{st.session_state['user'].email}** 👋")

if st.button("🚪 Se déconnecter"):
    logout()

st.markdown("---")
st.subheader("📲 Accès rapide")

# 💡 Menu automatique : Streamlit détecte les pages du dossier /pages
st.info("👉 Utilise le menu latéral (à gauche ou via le bouton ☰ sur mobile) pour accéder à :\n\n"
        "💳 1_Transactions\n"
        "📊 2_Statistiques\n"
        "⚙️ 3_Paramètres\n"
        "⚡ 4_Dashboard (barre Dragon Ball Z)")

st.markdown("---")
st.markdown("""
<div style='text-align:center;'>
    <h4 style='color:#00f6ff;'>SpirBoost ⚡ Intelligence & Budget</h4>
    <p style='color:gray;'>Version 2025 — Créée avec passion par Antonio</p>
</div>
""", unsafe_allow_html=True)
