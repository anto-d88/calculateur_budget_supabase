# 💸 SpirBoost Budget — Calculateur de Budget Intelligent

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-ff4b4b?logo=streamlit)
![Supabase](https://img.shields.io/badge/Database-Supabase-3ECF8E?logo=supabase)
![Made by Antonio](https://img.shields.io/badge/Made%20with%20❤️%20by-Antonio-orange)

---

## 🚀 Présentation

Bienvenue sur **SpirBoost Budget**, une application développée par **Antonio** pour t’aider à **reprendre le contrôle sur ton argent** — avec style, puissance et motivation ⚡  

Inspirée par l’univers de **Dragon Ball Z**, cette app transforme la gestion financière en un **jeu d’évolution personnelle**.  
Chaque dépense, chaque revenu devient un pas de plus vers ta transformation en **Super Saiyan de la finance 💥**.

---

## 💡 Objectif

> “Donner à chacun la puissance d’un Super Saiyan pour maîtriser ses finances.”

SpirBoost Budget te permet de :
- 💳 **Ajouter, modifier et suivre** tes revenus et dépenses  
- 📊 **Visualiser ton solde** et ton **historique en temps réel**  
- ☁️ **Sauvegarder tes données** en ligne via **Supabase**  
- 🔐 **Créer un compte sécurisé** avec authentification intégrée  
- 🎨 **Changer le thème visuel** (Dragon Ball, Dark, Light...)  
- 📱 **Utiliser l’application sur mobile comme une PWA installable**

---

## 🧠 Structure du projet

Voici l’organisation complète du projet 👇

calculateur_budget_supabase/
│
├── app.py # Page principale (connexion et navigation)
│
├── pages/
│ ├── 1_Transactions.py # Gestion des transactions (ajout, édition, suppression)
│ ├── 2_Statistiques.py # Statistiques et graphiques dynamiques (en développement)
│ ├── 3_Paramètres.py # Thèmes, préférences utilisateur et design
│ ├── 4_Dashboard.py # Tableau de bord visuel et résumé général
│
├── .env # Variables d’environnement (SUPABASE_URL, SUPABASE_KEY)
├── .streamlit/config.toml # Configuration du thème global Streamlit
├── themes.py # Dictionnaire de thèmes dynamiques
├── requirements.txt # Dépendances Python (Streamlit, Supabase, Pandas, etc.)
└── README.md # Ce fichier ✨


---

## 🧩 Mode d’emploi — Comment utiliser SpirBoost Budget

### 🪪 1. Connexion / Inscription
- Crée ton compte en quelques secondes avec ton email et ton mot de passe.  
- Une fois connecté, ton tableau de bord s’active automatiquement.  
- Tu restes connecté même après fermeture du navigateur grâce à Supabase 🔐

### 💸 2. Ajout de transactions
- Sélectionne le **type** : revenu, dépense, crédit, voiture, etc.  
- Indique le **montant**, la **description** et la **catégorie**.  
- Clique sur **“Enregistrer”** pour sauvegarder ta transaction.  
✅ Toutes tes données sont stockées dans Supabase, liées à ton compte personnel.

### 📊 3. Consultation du solde et de l’historique
- Ton **solde actuel** se calcule automatiquement (revenus - dépenses).  
- Tu vois l’historique complet de tes opérations, trié par date.  
- Les **couleurs et symboles** indiquent le type de transaction (+ ou -).

### 🎨 4. Personnalisation
- Va dans **Paramètres** pour changer ton thème visuel :  
  - `Dark mode`, `Dragon Ball`, `Saiyan Gold`, etc.  
- Le thème s’applique instantanément à toute l’application.

### 🔥 5. Tableau de bord (Dashboard)
- Accède à une **vue globale** de ton budget.  
- Visualise tes totaux par catégorie.  
- Des **graphes dynamiques** arrivent bientôt pour afficher ton évolution dans le temps 📈

---

## 🛠️ Installation locale

### 1️⃣ Clone le dépôt :
```bash
git clone https://github.com/anto-d88/calculateur_budget_supabase.git
cd calculateur_budget_supabase

python -m venv venv
venv\Scripts\activate   # sous Windows
source venv/bin/activate   # sous Mac/Linux

pip install -r requirements.txt

SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxx

streamlit run app.py

🌍 Accès en ligne

L’application est hébergée sur Streamlit Cloud :
🔗 https://calculateur-budget-antonio.streamlit.app

💡 Astuce mobile :
Tu peux installer l’app comme une application Android (PWA) depuis ton navigateur mobile !

Ouvre le lien → Menu ⋮ → “Ajouter à l’écran d’accueil”

🧠 Philosophie du projet

“J’ai voulu créer un outil simple, inspirant et accessible à tous.
Gérer ton argent ne doit pas être une corvée, mais une aventure motivante.
SpirBoost Budget t’aide à progresser, un peu plus fort chaque jour.”

— Antonio, créateur de SpirBoost ⚡

💬 Donne ton avis & participe à l’aventure !

Ton avis compte énormément 🙏
Tu peux :

💡 Suggérer une amélioration

🐞 Signaler un bug

🌈 Proposer une nouvelle idée

❤️ Laisser un message d’encouragement

➡️ 👉 Donner mon avis sur GitHub

ou contacte-moi directement : contactantodev.inte@gmail.com

Chaque idée, même petite, aide à rendre SpirBoost encore plus fort 💪

🔮 Prochaines évolutions

🚧 En cours de développement :

🤖 Assistant IA Budget : analyse automatique des dépenses, alertes et conseils personnalisés

🗣️ Voix-off interactive : un mode vocal pour gérer ton budget à la parole

📈 Graphiques détaillés : histogrammes et comparatifs mensuels dynamiques

💾 Mode hors-ligne (PWA avancé) : accès à tes données même sans Internet

💰 Export PDF / Excel de ton tableau de bord

🔔 Notifications automatiques : rappels d’objectifs financiers

🧩 Multi-comptes : gérer plusieurs portefeuilles à la fois (perso, pro, famille…)

📘 Licence

Projet libre pour usage personnel, éducatif et communautaire.
Toute utilisation commerciale doit mentionner l’auteur original — Antonio (SpirBoost).

🌟 Merci d’avoir pris le temps de découvrir SpirBoost Budget.
Continue d’apprendre, de créer, et de booster ton avenir —
comme un vrai Saiyan de la finance 💥 !