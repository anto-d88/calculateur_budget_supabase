# ============================================================
# 💸 CALCULATEUR DE BUDGET - VERSION COMPLÈTE
# ============================================================

import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os
import pandas as pd
from themes import THEMES

# ============================================================
# ⚙️ CONFIGURATION GÉNÉRALE
# ============================================================

st.set_page_config(page_title="💸 Calculateur de Budget", page_icon="💰", layout="wide")

# --- Charger les variables d'environnement (.env) ---
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# ============================================================
# 🎨 GESTION DES THÈMES
# ============================================================

if "theme_name" not in st.session_state:
    st.session_state["theme_name"] = "Sombre"

theme_name = st.sidebar.selectbox("🎨 Choisir un thème :", list(THEMES.keys()),
                                  index=list(THEMES.keys()).index(st.session_state["theme_name"]))
st.session_state["theme_name"] = theme_name
theme = THEMES[theme_name]

# --- Appliquer le style global ---
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {theme["background"]};
            color: {theme["text"]};
            font-family: 'Segoe UI', sans-serif;
        }}
        header[data-testid="stHeader"] {{
            background-color: transparent;
        }}
        .block-container {{
            padding-top: 1rem;
            padding-bottom: 2rem;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# 💼 TABLEAU DE BORD FINANCIER
# ============================================================

st.title("💼 Tableau de bord financier")

try:
    data = supabase.table("transactions").select("*").execute()

    if not data.data:
        st.info("Aucune transaction enregistrée pour le moment.")
    else:
        df = pd.DataFrame(data.data)
        total_revenu = df[df["type"] == "revenu"]["montant"].sum()
        total_depense = df[df["type"] == "dépense"]["montant"].sum()
        solde = total_revenu - total_depense

        st.markdown(
            f"""
            <div style="display:flex;justify-content:space-around;flex-wrap:wrap;gap:20px;">
                <div style="background-color:{theme["card"]};padding:20px;border-radius:15px;min-width:250px;text-align:center;box-shadow:0 4px 10px rgba(0,0,0,0.2);">
                    <h3>💰 Solde</h3>
                    <h2 style="color:{'limegreen' if solde >= 0 else 'tomato'};">{solde:.2f} €</h2>
                </div>
                <div style="background-color:{theme["card"]};padding:20px;border-radius:15px;min-width:250px;text-align:center;box-shadow:0 4px 10px rgba(0,0,0,0.2);">
                    <h3>📈 Revenus</h3>
                    <h2 style="color:limegreen;">+{total_revenu:.2f} €</h2>
                </div>
                <div style="background-color:{theme["card"]};padding:20px;border-radius:15px;min-width:250px;text-align:center;box-shadow:0 4px 10px rgba(0,0,0,0.2);">
                    <h3>📉 Dépenses</h3>
                    <h2 style="color:tomato;">-{total_depense:.2f} €</h2>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

except Exception as e:
    st.error(f"Erreur de chargement : {e}")

# ============================================================
# 🚨 SYSTÈME DE NOTIFICATIONS INTELLIGENT
# ============================================================

def afficher_notification(type_msg, message):
    """Affiche une alerte stylée dans Streamlit avec couleur adaptée"""
    couleurs = {
        "erreur": "#ff4d4d",          # rouge vif
        "avertissement": "#ffb84d",   # orange chaud
        "succès": "#4CAF50",          # vert
        "info": "#2196F3"             # bleu clair
    }

    bg_color = couleurs.get(type_msg, "#2196F3")

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(90deg, {bg_color}, {bg_color}cc);
            color: white;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: 12px;
            padding: 15px 20px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0px 3px 10px rgba(0,0,0,0.25);
            animation: slideDown 0.5s ease-out;
        ">
            🔔 {message}
        </div>

        <style>
            @keyframes slideDown {{
                from {{ opacity: 0; transform: translateY(-15px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# 🔍 DÉTECTION AUTOMATIQUE D'ÉTAT FINANCIER
# ============================================================

if "data" in locals() and data.data:

    # Solde négatif
    if solde < 0:
        afficher_notification("erreur", f"⚠️ Attention Antonio ! Ton solde est négatif ({solde:.2f} €) 💸")

    # Grosse dépense
    grosses_depenses = [t for t in data.data if t["type"] == "dépense" and t["montant"] > 300]
    if grosses_depenses:
        afficher_notification("avertissement", "💰 Grosse dépense détectée ! Pense à vérifier ton budget 🧾")

    # Gros solde positif
    if solde >= 1000:
        afficher_notification("succès", "🎉 Bravo ! Tu as dépassé 1000 € de solde positif 💪")

else:
    afficher_notification("info", "Ajoute des transactions pour commencer ton suivi budgétaire 📊")
