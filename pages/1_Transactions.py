import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os
from datetime import datetime

# --------------------------
# 🔐 Connexion Supabase
# --------------------------
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# --------------------------
# 🎨 Interface principale
# --------------------------
st.title("💳 Gérer les Transactions")

# --------------------------
# ➕ Ajouter une transaction
# --------------------------
st.subheader("➕ Ajouter une transaction")

type_transac = st.radio("Type :", ["revenu", "dépense"], horizontal=True, key="type_new")
montant = st.number_input("Montant (€)", min_value=0.0, step=0.5, key="montant_new")
description = st.text_input("Description", key="desc_new")
categorie = st.selectbox("Catégorie", ["Autre", "Crédit", "Voiture", "Revenu"], key="cat_new")

if st.button("💾 Enregistrer"):
    try:
        supabase.table("transactions").insert({
            "type": type_transac,
            "montant": montant,
            "description": description,
            "categorie": categorie,
            "date": datetime.now().isoformat()
        }).execute()
        st.success("✅ Transaction ajoutée avec succès !")
        st.rerun()
    except Exception as e:
        st.error(f"Erreur : {e}")

st.markdown("---")

# --------------------------
# 🧾 Liste + Modification
# --------------------------
st.subheader("🧾 Historique et modifications")

try:
    data = supabase.table("transactions").select("*").order("date", desc=True).execute()
    if not data.data:
        st.info("Aucune transaction enregistrée.")
    else:
        for t in data.data:
            with st.expander(f"📅 {t['date'][:10]} | {t['description']} | {t['montant']} € | {t['categorie']}"):
                new_type = st.radio("Type :", ["revenu", "dépense"], index=0 if t["type"] == "revenu" else 1, key=f"type_{t['id']}")
                new_montant = st.number_input("Montant (€)", min_value=0.0, value=t["montant"], step=0.5, key=f"montant_{t['id']}")
                new_description = st.text_input("Description", value=t["description"], key=f"desc_{t['id']}")
                new_categorie = st.selectbox("Catégorie", ["Autre", "Crédit", "Voiture", "Revenu"], index=["Autre", "Crédit", "Voiture", "Revenu"].index(t["categorie"]) if t["categorie"] in ["Autre", "Crédit", "Voiture", "Revenu"] else 0, key=f"cat_{t['id']}")

                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("✏️ Modifier", key=f"edit_{t['id']}"):
                        try:
                            supabase.table("transactions").update({
                                "type": new_type,
                                "montant": new_montant,
                                "description": new_description,
                                "categorie": new_categorie
                            }).eq("id", t["id"]).execute()
                            st.success("✅ Transaction modifiée avec succès !")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erreur de modification : {e}")

                with col2:
                    if st.button("🗑️ Supprimer", key=f"delete_{t['id']}"):
                        try:
                            supabase.table("transactions").delete().eq("id", t["id"]).execute()
                            st.warning("🗑️ Transaction supprimée.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erreur de suppression : {e}")
except Exception as e:
    st.error(f"Erreur d’affichage : {e}")
