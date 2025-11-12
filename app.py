# ============================================================
# 💸 CALCULATEUR DE BUDGET SPIRBOOST - VERSION COMPLÈTE (STABLE)
# ============================================================

import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os

# ============================================================
# ⚙️ CONFIGURATION DE BASE
# ============================================================
st.set_page_config(
    page_title="💸 SpirBoost Budget",
    page_icon="💰",
    layout="centered",
)

# 🎨 STYLE DRAGON BALL Z
st.markdown("""
<style>
body { background-color:#0b0c10; color:white; }
h1, h2, h3 { color:#ffcc00; text-shadow:0 0 10px #ffaa00; font-weight:700; }
button[kind="secondary"] {
    background-color:#111 !important;
    border:1px solid #ffaa00 !important;
    color:#ffaa00 !important;
    border-radius:10px !important;
    font-weight:600;
    transition:all 0.25s;
}
button[kind="secondary"]:hover {
    background-color:#ffaa00 !important;
    color:#111 !important;
    transform:scale(1.05);
    box-shadow:0 0 20px #ffaa00;
}
.top-banner {
    background:linear-gradient(90deg,#111,#ffb300,#ff6f00);
    padding:15px;
    border-radius:12px;
    text-align:center;
    font-size:22px;
    font-weight:700;
    color:#fff;
    margin-bottom:20px;
    box-shadow:0 0 25px rgba(255,183,0,0.6);
}
.block-container { padding-top:1rem !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 🔐 CONNEXION À SUPABASE
# ============================================================
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# --- Restauration automatique de session (version Python compatible)
try:
    if "user" in st.session_state and st.session_state["user"]:
        current_session = supabase.auth.get_session()
        if not current_session or not current_session.user:
            st.session_state["user"] = None
except Exception:
    st.session_state["user"] = None

# ============================================================
# 🧠 SESSION STATE
# ============================================================
if "user" not in st.session_state:
    st.session_state["user"] = None
if "dashboard_loaded" not in st.session_state:
    st.session_state["dashboard_loaded"] = False

# ============================================================
# 🔑 FONCTIONS D’AUTHENTIFICATION
# ============================================================
def login(email, password):
    try:
        result = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return result.user
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
        return None

def signup(email, password):
    try:
        result = supabase.auth.sign_up({"email": email, "password": password})
        if result.user:
            st.success("✅ Compte créé ! Vérifie ton e-mail avant de te connecter.")
    except Exception as e:
        st.error(f"Erreur : {e}")

def logout():
    """Déconnexion complète"""
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    st.session_state["user"] = None
    st.session_state["dashboard_loaded"] = False
    st.success("✅ Déconnexion réussie")
    st.switch_page("app.py")

# ============================================================
# 🔒 PAGE DE CONNEXION
# ============================================================
if not st.session_state["user"]:
    st.markdown('<div class="top-banner">⚡ SpirBoost Budget - Connexion ⚡</div>', unsafe_allow_html=True)
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
                st.warning("⚠️ Remplis tous les champs.")
    st.stop()

# ============================================================
# 🏠 PAGE D’ACCUEIL APRÈS CONNEXION
# ============================================================
st.markdown('<div class="top-banner">💸 SpirBoost Budget - Accueil</div>', unsafe_allow_html=True)
st.title("🏠 Tableau principal")
st.markdown(f"Bienvenue **{st.session_state['user'].email}** 👋")

if st.button("🚪 Se déconnecter"):
    logout()

# ------------------------------------------------------------
# 🔗 LIENS RAPIDES
# ------------------------------------------------------------
st.markdown("## 🚀 Navigation rapide")

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.page_link("pages/1_Transactions.py", label="💳 Transactions", icon="💰")

with col2:
    st.page_link("pages/2_Statistiques.py", label="📈 Statistiques", icon="📊")

with col3:
    st.page_link("pages/3_Paramètres.py", label="⚙️ Paramètres", icon="🧩")

with col4:
    st.page_link("pages/4_Dashboard.py", label="🔥 Tableau de bord", icon="📊")

# ------------------------------------------------------------
# 🔙 REVENIR À LA CONNEXION (optionnel)
# ------------------------------------------------------------
if st.button("🔐 Revenir à la connexion"):
    st.session_state["user"] = None
    st.switch_page("app.py")

# ------------------------------------------------------------
# 🧠 FOOTER
# ------------------------------------------------------------
st.markdown("""
---
<div style='text-align:center;'>
    <h4 style='color:#ffcc00;'>SpirBoost ⚡ Intelligence & Budget</h4>
    <p style='color:gray;'>Version 2025 – Créée par Antonio</p>
</div>
""", unsafe_allow_html=True)
