# ============================================================
# 💸 CALCULATEUR DE BUDGET - VERSION AVEC NAVIGATION COMPLÈTE
# ============================================================

import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os

# --------------------------------------------
# 🔧 CONFIGURATION DE BASE
# --------------------------------------------
st.set_page_config(
    page_title="💸 Calculateur de Budget",
    page_icon="💰",
    layout="centered",
)

# --- Chargement du thème global (Dragon Ball par ex.)
st.markdown("""
    <style>
        /* Thème général */
        body {
            background-color: #0B0C10;
            color: #FFFFFF;
        }

        h1, h2, h3, h4, h5 {
            color: #F1C40F;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(255, 193, 7, 0.7);
        }

        /* Barre supérieure */
        .top-banner {
            background: linear-gradient(90deg, #111, #FFB300, #FF6F00);
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            font-size: 22px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 20px;
            box-shadow: 0 0 20px rgba(255, 183, 0, 0.6);
        }

        /* Liens rapides */
        button[kind="secondary"] {
            background-color: #222 !important;
            border: 1px solid #FFB300 !important;
            color: #FFD700 !important;
            font-weight: 600;
            border-radius: 10px !important;
            transition: all 0.3s ease-in-out;
        }

        button[kind="secondary"]:hover {
            background-color: #FFB300 !important;
            color: #111 !important;
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(255, 193, 7, 0.7);
        }

        .block-container {
            padding-top: 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------
# 🔐 CONNEXION SUPABASE
# --------------------------------------------
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# --------------------------------------------
# 🚀 BANNIÈRE D’ACCUEIL
# --------------------------------------------
st.markdown('<div class="top-banner">⚡ Calculateur de Budget - SpirBoost Dragon Ball ⚡</div>', unsafe_allow_html=True)

st.title("🏠 Accueil du Calculateur de Budget")
st.markdown("Bienvenue dans ton espace **SpirBoost Budget** 💰 – choisis une section ci-dessous :")

# --------------------------------------------
# 🔗 NAVIGATION RAPIDE (multi-pages)
# --------------------------------------------
st.markdown("## 🚀 Navigation rapide")

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.page_link("pages/1_Transactions.py", label="💳 Gérer mes transactions", icon="💰")

with col2:
    st.page_link("pages/2_Statistiques.py", label="📊 Statistiques détaillées", icon="📈")

with col3:
    st.page_link("pages/3_Paramètres.py", label="⚙️ Paramètres & Thèmes", icon="🧩")

with col4:
    st.page_link("pages/4_Dashboard.py", label="🔥 Tableau de bord visuel", icon="📊")

# --------------------------------------------
# 🧠 MESSAGE D’ACCUEIL
# --------------------------------------------
st.markdown("""
---
### 💡 Astuce :
Tu peux installer cette app sur ton **mobile Android** comme une vraie application (PWA) 📱  
➡️ Clique sur *“Ajouter à l’écran d’accueil”* quand tu ouvres ton app hébergée.
---
""")

# --------------------------------------------
# ✅ FIN
# --------------------------------------------
st.markdown("💫 *Propulsé par SpirBoost AI – version Dragon Ball Ultimate ⚡*")
