import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Connexion à Supabase
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

print("=== Calculateur de budget connecté à Supabase 💸 ===")

def ajouter_transaction():
    type_transac = input("Type (revenu/dépense) : ").lower()
    montant = float(input("Montant (€) : "))
    description = input("Description : ")

    supabase.table("transactions").insert({
        "type": type_transac,
        "montant": montant,
        "description": description
    }).execute()

    print("✅ Transaction enregistrée avec succès !\n")

def afficher_solde():
    data = supabase.table("transactions").select("*").execute()
    total_revenu = sum(t["montant"] for t in data.data if t["type"] == "revenu")
    total_depense = sum(t["montant"] for t in data.data if t["type"] == "dépense")
    solde = total_revenu - total_depense

    print("=== RÉCAPITULATIF ===")
    print(f"Revenus totaux : {total_revenu} €")
    print(f"Dépenses totales : {total_depense} €")
    print(f"💰 Solde actuel : {solde} €\n")

while True:
    print("1️⃣ Ajouter une transaction")
    print("2️⃣ Voir le solde")
    print("3️⃣ Quitter\n")

    choix = input("Choix : ")

    if choix == "1":
        ajouter_transaction()
    elif choix == "2":
        afficher_solde()
    elif choix == "3":
        print("👋 À bientôt Antonio !")
        break
    else:
        print("Option invalide, réessaye.\n")
