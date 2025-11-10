import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

st.title("💳 Gérer les Transactions")

type_transac = st.radio("Type :", ["revenu", "dépense"], horizontal=True)
montant = st.number_input("Montant (€)", min_value=0.0, step=0.5)
description = st.text_input("Description")
categorie = st.selectbox("Catégorie", ["Autre", "Crédit", "Voiture", "Revenu"])

if st.button("💾 Enregistrer"):
    try:
        supabase.table("transactions").insert({
            "type": type_transac,
            "montant": montant,
            "description": description,
            "categorie": categorie
        }).execute()
        st.success("Transaction ajoutée avec succès ✅")
        st.rerun()
    except Exception as e:
        st.error(f"Erreur : {e}")

st.markdown("---")

try:
    data = supabase.table("transactions").select("*").order("date", desc=True).execute()
    if data.data:
        for t in data.data:
            st.write(f"📅 {t['date'][:10]} | {t['description']} | {t['montant']}€ | {t['categorie']}")
    else:
        st.info("Aucune transaction.")
except Exception as e:
    st.error(f"Erreur d’affichage : {e}")
