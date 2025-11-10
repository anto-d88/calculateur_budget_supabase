import streamlit as st
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv
import os
import plotly.express as px

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

st.title("📊 Statistiques Financières")

data = supabase.table("transactions").select("*").execute()
if data.data:
    df = pd.DataFrame(data.data)
    fig = px.pie(df, values="montant", names="categorie", title="Répartition par catégorie (€)")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Aucune donnée à afficher.")
