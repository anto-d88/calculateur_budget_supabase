# ============================================================
# 💸 CALCULATEUR DE BUDGET — version corrigée
# ============================================================
import os
from datetime import datetime, timezone

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client
from themes import THEMES

# ------------------------------
# ⚙️ CONFIG DE PAGE + MOBILE
# ------------------------------
st.set_page_config(page_title="💸 Calculateur de Budget", page_icon="💰", layout="centered")
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<style>
  input, textarea, select { width:100% !important; max-width:100% !important; font-size:18px !important;}
  .block-container { padding-top:1rem !important; padding-bottom:2rem !important; padding-left:.8rem !important; padding-right:.8rem !important;}
  div[data-testid="stForm"] { overflow-y:auto !important; max-height:85vh !important;}
  button[kind="primary"] { height:55px !important; font-size:18px !important;}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# 🎨 THÈME
# ------------------------------
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"
theme = THEMES.get(st.session_state.get("theme", "dark"), THEMES["dark"])

# ------------------------------
# 🔐 SUPABASE
# ------------------------------
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# ------------------------------
# 🧭 NAV SIMPLE
# ------------------------------
st.markdown(
    f"""
    <div style="background-color:{theme['nav_bg']}; padding:10px; border-radius:10px; text-align:center;">
        <span style="color:{theme['text']}; font-size:22px;">🏠 Calculateur Budget Antonio</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------
# 👤 SESSION UTILISATEUR
# ------------------------------
if "user" not in st.session_state:
    st.session_state["user"] = None

def login(email: str, password: str):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return res.user
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")
        return None

def signup(email: str, password: str):
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

# ------------------------------
# 🏠 DASHBOARD
# ------------------------------
user = st.session_state["user"]
user_id = getattr(user, "id", None)
user_email = getattr(user, "email", None)

st.title("💼 Tableau de bord financier")
st.markdown(f"Bienvenue **{user_email}** 👋")

if st.button("Se déconnecter"):
    logout()

# -------- Ajouter une transaction --------
st.subheader("➕ Ajouter une transaction")
type_transac = st.radio("Type :", ["revenu", "dépense", "crédit", "voiture"], horizontal=True)
montant = st.number_input("Montant (€)", min_value=0.0, step=0.5)
description = st.text_input("Description")
categorie = st.selectbox("Catégorie", ["Autre", "Revenu", "Crédit", "Voiture", "Alimentation", "Loisirs"])

if st.button("💾 Enregistrer la transaction"):
    if montant > 0 and description:
        if not user_id or not user_email:
            st.error("❌ Utilisateur non authentifié. Reconnecte-toi avant d’enregistrer.")
        else:
            try:
                supabase.table("transactions").insert({
                    "user_id": user_id,              # ✅ on enregistre l'ID
                    "user_email": user_email,        # ✅ et l'email
                    "type": type_transac,
                    "montant": montant,
                    "description": description,
                    "categorie": categorie,
                    "date": datetime.now(timezone.utc).isoformat()
                }).execute()
                st.success("✅ Transaction enregistrée avec succès !")
                st.rerun()
            except Exception as e:
                st.error(f"Erreur d'enregistrement : {e}")
    else:
        st.warning("⚠️ Remplis tous les champs avant d’enregistrer.")

# -------- Récupération des transactions --------
st.subheader("📋 Historique des transactions")

df = pd.DataFrame()
try:
    # ✅ filtre principal par user_id (RLS standard)
    q = supabase.table("transactions").select("*").order("date", desc=True)
    if user_id:
        q = q.eq("user_id", user_id)
    elif user_email:
        # fallback si la table n'a pas encore user_id partout
        q = q.eq("user_email", user_email)
    data = q.execute()

    if data.data:
        df = pd.DataFrame(data.data)
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

# -------- Cartes Résumé --------
st.subheader("📊 Résumé")

if not df.empty:
    total_revenu = df.loc[df["type"] == "revenu", "montant"].sum()
    total_depense = df.loc[df["type"].isin(["dépense", "crédit", "voiture"]), "montant"].sum()
    solde = float(total_revenu) - float(total_depense)

    st.markdown(
        f"""
        <div style="display:flex;gap:16px;flex-wrap:wrap;">
            <div style="background:{theme['nav_bg']};padding:18px 22px;border-radius:14px;min-width:220px;box-shadow:0 4px 10px rgba(0,0,0,.2);">
                <h4 style="margin:0 0 8px 0;">💰 Solde</h4>
                <h2 style="color:{'limegreen' if solde >= 0 else 'tomato'};margin:0;">{solde:.2f} €</h2>
            </div>
            <div style="background:{theme['nav_bg']};padding:18px 22px;border-radius:14px;min-width:220px;box-shadow:0 4px 10px rgba(0,0,0,.2);">
                <h4 style="margin:0 0 8px 0;">📈 Revenus</h4>
                <h2 style="color:limegreen;margin:0;">+{total_revenu:.2f} €</h2>
            </div>
            <div style="background:{theme['nav_bg']};padding:18px 22px;border-radius:14px;min-width:220px;box-shadow:0 4px 10px rgba(0,0,0,.2);">
                <h4 style="margin:0 0 8px 0;">📉 Dépenses</h4>
                <h2 style="color:tomato;margin:0;">-{total_depense:.2f} €</h2>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.info("Aucune donnée à afficher pour le résumé.")
