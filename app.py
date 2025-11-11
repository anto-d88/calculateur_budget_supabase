# ============================================================
# 💸 BUDGET ANTONIO Z - PAGE PRINCIPALE (Connexion + Dashboard)
# ============================================================

import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os
import time
from datetime import datetime

# --------------------------------------------
# ⚙️ CONFIGURATION
# --------------------------------------------
st.set_page_config(page_title="💸 Budget Antonio Z", page_icon="💰", layout="centered")

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# --------------------------------------------
# ⚡ ANIMATION DRAGON BALL STYLE
# --------------------------------------------
def show_loading_screen():
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <style>
                .loading-container {
                    background-color: black;
                    background-image: radial-gradient(circle at center, #1a1a1a 0%, #000 100%);
                    height: 100vh;
                    width: 100vw;
                    position: fixed;
                    top: 0; left: 0;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    z-index: 9999;
                    color: #fff;
                    font-family: 'Orbitron', sans-serif;
                    overflow: hidden;
                }
                .energy-bar {
                    width: 80%;
                    height: 14px;
                    border-radius: 10px;
                    background: linear-gradient(90deg, #333 0%, #555 100%);
                    overflow: hidden;
                    margin-top: 30px;
                    box-shadow: 0 0 15px #00f6ff88;
                }
                .energy-fill {
                    height: 100%;
                    width: 0%;
                    background: linear-gradient(90deg, #00f6ff, #1aff00, #ffcc00);
                    box-shadow: 0 0 15px #00f6ff;
                    border-radius: 10px;
                    animation: fillEnergy 3.5s ease-in-out forwards;
                }
                @keyframes fillEnergy {
                    0% { width: 0%; filter: brightness(0.8); }
                    25% { width: 40%; filter: brightness(1.2); }
                    50% { width: 60%; filter: brightness(1.5); }
                    75% { width: 85%; filter: brightness(1.8); }
                    100% { width: 100%; filter: brightness(2); }
                }
                .loading-text {
                    font-size: 1.5rem;
                    margin-top: 10px;
                    color: #00f6ff;
                    text-shadow: 0 0 8px #00f6ff;
                    animation: pulse 1s ease-in-out infinite;
                }
                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
                }
            </style>
            <div class="loading-container">
                <div class="loading-text">⚡ CHARGEMENT DU KI FINANCIER...</div>
                <div class="energy-bar"><div class="energy-fill"></div></div>
            </div>
        """, unsafe_allow_html=True)
    time.sleep(3.5)
    placeholder.empty()


# --------------------------------------------
# 🧠 CHARGEMENT INITIAL
# --------------------------------------------
if "user" not in st.session_state:
    st.session_state["user"] = None

show_loading_screen()

# --------------------------------------------
# 🔐 AUTHENTIFICATION
# --------------------------------------------
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
            st.success("✅ Compte créé ! Confirme ton e-mail avant de te connecter.")
    except Exception as e:
        st.error(f"Erreur : {e}")

def logout():
    st.session_state["user"] = None
    st.rerun()

# --------------------------------------------
# 🔑 PAGE DE CONNEXION
# --------------------------------------------
if not st.session_state["user"]:
    st.title("🔐 Connexion à ton espace financier")

    tab1, tab2 = st.tabs(["Se connecter", "Créer un compte"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Mot de passe", type="password")
        if st.button("Connexion"):
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

# --------------------------------------------
# 💼 TABLEAU DE BORD
# --------------------------------------------
user = st.session_state["user"]
st.title(f"💼 Tableau de bord - {user.email}")

if st.button("🚪 Se déconnecter"):
    logout()

st.markdown("---")
st.write("📊 Accède à tes outils :")
st.page_link("transactions", label="💳 Gérer mes transactions", icon="💸")
st.page_link("dashboard", label="📊 Tableau de bord", icon="📈")

