# ============================================================
# 💸 CALCULATEUR DE BUDGET - VERSION COMPLÈTE
# ============================================================
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
from themes import THEMES  # ton fichier themes.py

# --------------------------------------------
# 🔧 CONFIGURATION DE BASE
# --------------------------------------------
st.set_page_config(page_title="💸 Calculateur de Budget", page_icon="💰", layout="centered")

# --- Mode mobile-friendly (PWA & responsive) ---
st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
    <style>
        input, textarea, select {
            width: 100% !important;
            max-width: 100% !important;
            font-size: 18px !important;
        }
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
        }
        div[data-testid="stForm"] {
            overflow-y: auto !important;
            max-height: 85vh !important;
        }
        button[kind="primary"] {
            height: 55px !important;
            font-size: 18px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------
# 🌈 Thème
# --------------------------------------------
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"

theme = THEMES.get(st.session_state.get("theme", "dark"), THEMES["dark"])


# --------------------------------------------
# 🔐 Connexion Supabase
# --------------------------------------------
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# --------------------------------------------
# 🧭 Navigation (barre simple)
# --------------------------------------------
st.markdown(f"""
    <div style="background-color:{theme['nav_bg']}; padding: 10px; border-radius: 10px; text-align:center;">
        <a href="#" style="color:{theme['text']}; font-size:22px; text-decoration:none;">🏠 Calculateur Budget Antonio</a>
    </div>
""", unsafe_allow_html=True)

# --------------------------------------------
# 👤 Gestion de la session utilisateur
# --------------------------------------------
if "user" not in st.session_state:
    st.session_state["user"] = None

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
# 🔑 Authentification
# --------------------------------------------
if not st.session_state["user"]:
    st.title("🔐 Connexion à ton espace budget")

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

# --------------------------------------------
# 💸 Tableau de bord principal
# --------------------------------------------
st.title("💼 Tableau de bord financier")
st.markdown(f"Bienvenue **{st.session_state['user'].email}** 👋")

if st.button("Se déconnecter"):
    logout()

# --- Ajouter une transaction ---
st.subheader("➕ Ajouter une transaction")
type_transac = st.radio("Type :", ["revenu", "dépense", "crédit", "voiture"], horizontal=True)
montant = st.number_input("Montant (€)", min_value=0.0, step=0.5)
description = st.text_input("Description")
categorie = st.selectbox("Catégorie", ["Autre", "Revenu", "Crédit", "Voiture", "Alimentation", "Loisirs"])

if st.button("Enregistrer la transaction"):
    if montant > 0 and description:
        user = st.session_state.get("user")
        user_email = getattr(user, "email", None)

        if not user_email:
            st.error("❌ Utilisateur non authentifié. Reconnecte-toi avant d’enregistrer.")
        else:
            response = supabase.table("transactions").insert({
                "type": type_transac,
                "montant": montant,
                "description": description,
                "user_email": user_email,
                "categorie": categorie,  # si tu l’as ajouté
                "date": datetime.now().isoformat(),
            }).execute()
            st.success("✅ Transaction enregistrée avec succès !")
            st.rerun()
    else:
        st.warning("⚠️ Remplis tous les champs avant d’enregistrer.")

# --------------------------------------------
# 📋 Historique des transactions
# --------------------------------------------
st.subheader("📋 Historique des transactions")

try:
    data = (
        supabase.table("transactions")
        .select("*")
        .eq("user_id", st.session_state["user"].id)
        .order("date", desc=True)
        .execute()
    )

    if data.data:
        for t in data.data:
            signe = "+" if t["type"] == "revenu" else "-"
            couleur = "green" if t["type"] == "revenu" else "red"
            st.markdown(
                f"<b style='color:{couleur};'>{signe}{t['montant']}€</b> — {t['description']} "
                f"({t.get('categorie','Autre')}) — <i>{t['date'][:10]}</i>",
                unsafe_allow_html=True,
            )
    else:
        st.info("Aucune transaction pour le moment.")
except Exception as e:
    st.error(f"Erreur lors du chargement : {e}")

# --------------------------------------------
# 💰 Solde et résumé
# --------------------------------------------
st.subheader("💰 Solde actuel")

if "data" in locals() and data.data:
    total_revenu = sum(t["montant"] for t in data.data if t["type"] == "revenu")
    total_depense = sum(t["montant"] for t in data.data if t["type"] in ["dépense", "crédit", "voiture"])
    solde = total_revenu - total_depense

    if solde >= 0:
        st.success(f"Ton solde actuel est de **{solde:.2f} €**")
    else:
        st.error(f"Tu es dans le négatif : **{solde:.2f} €** 😬")
else:
    st.info("Aucune donnée à afficher.")
