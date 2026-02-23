# 🚀 Job Market - Plateforme d'Analyse du Marché de l'Emploi

> **Projet de fin d'études - Data Engineering**  
> *Par Nour Amel SERIR - Liora ex DataScientest (Mars 2025 - Mars 2026)*

## 📋 Description

Plateforme d'analyse du marché de l'emploi combinant collecte de données en temps réel, analyses prédictives et recommandations personnalisées pour aider les professionnels en reconversion et les étudiants dans leur orientation.

### 🎯 Objectifs

- Collecter et analyser **5 000+ offres d'emploi** via APIs et web scraping
- Identifier les **secteurs porteurs** et **compétences recherchées**
- Proposer des **recommandations personnalisées** basées sur le profil utilisateur
- Visualiser les **tendances du marché** via un dashboard interactif

---

## 🏗️ Architecture

```
job-market/
├── README.md                   # Ce fichier
├── requirements.txt            # Dépendances Python
├── config/
│   ├── config.yaml            # Configuration générale
│   └── .env.example           # Template pour clés API
├── data/
│   ├── raw/                   # Données brutes collectées
│   ├── processed/             # Données nettoyées
│   └── models/                # Modèles ML sauvegardés
├── notebooks/
│   ├── 01_test_apis.ipynb    # Tests de connexion APIs
│   ├── 02_data_exploration.ipynb
│   └── 03_nlp_skills.ipynb
├── src/
│   ├── __init__.py
│   ├── collectors/            # Scripts de collecte
│   │   ├── __init__.py
│   │   ├── themuse.py
│   │   ├── adzuna.py
│   │   └── francetravail.py
│   ├── etl/                   # Pipeline ETL
│   │   ├── __init__.py
│   │   ├── cleaner.py
│   │   └── transformer.py
│   ├── nlp/                   # Extraction NLP
│   │   ├── __init__.py
│   │   └── skills_extractor.py
│   ├── ml/                    # Modèles ML
│   │   ├── __init__.py
│   │   └── recommender.py
│   └── utils/                 # Utilitaires
│       ├── __init__.py
│       └── logger.py
├── database/
│   ├── schema.sql             # Schéma PostgreSQL
│   └── init_db.py            # Script initialisation BDD
├── api/
│   ├── main.py               # FastAPI app
│   └── routes/
├── dashboard/
│   └── app.py                # Streamlit dashboard
├── tests/
│   └── test_collectors.py
└── docs/
    └── discovery.md          # Document Discovery

```

---

## 🔧 Stack Technique

| Composant | Technologie | Justification |
|-----------|-------------|---------------|
| **Langage** | Python 3.11+ | Écosystème data science riche |
| **Collecte APIs** | `requests` | HTTP client simple et fiable |
| **Web scraping** | `Scrapy`, `BeautifulSoup4` | Scraping structuré et parsing HTML |
| **NLP** | `spaCy` + `fr_core_news_md` | NLP français performant |
| **ML** | `scikit-learn` | Algorithmes de recommandation |
| **BDD relationnelle** | PostgreSQL 16 | Open source, robuste |
| **BDD NoSQL** | MongoDB Community | Documents JSON |
| **API Backend** | FastAPI | Moderne, auto-documentation |
| **Dashboard** | Streamlit | Prototypage rapide |
| **Visualisations** | Plotly | Graphiques interactifs |

---

## 🚀 Installation

### Option A : Environnement local

```bash
# 1. Cloner le repository
git clone https://github.com/nouramel/job-market.git
cd job-market

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer les clés API
cp config/.env.example config/.env
# Éditer config/.env avec vos clés API
```

### Option B : Google Colab (100% en ligne)

1. Ouvrir le notebook `notebooks/01_test_apis.ipynb` dans Colab
2. Suivre les instructions du notebook

---

## 🔑 Configuration des APIs

### 1. The Muse API

- **URL:** https://www.themuse.com/developers/api/v2
- **Inscription:** Gratuite
- **Limite:** 500 requêtes/jour
- **Documentation:** https://www.themuse.com/developers/api/v2

**Obtenir la clé :**
1. Créer un compte sur The Muse
2. Accéder à la section Developers
3. Générer une clé API
4. Ajouter dans `config/.env` : `THEMUSE_API_KEY=your_key`

### 2. Adzuna API

- **URL:** https://developer.adzuna.com/
- **Inscription:** Gratuite
- **Limite:** 1000 appels/mois
- **Documentation:** https://developer.adzuna.com/docs

**Obtenir les clés :**
1. Créer un compte sur Adzuna Developer
2. Créer une nouvelle application
3. Récupérer `App ID` et `App Key`
4. Ajouter dans `config/.env` :
   ```
   ADZUNA_APP_ID=your_app_id
   ADZUNA_APP_KEY=your_app_key
   ```

### 3. France Travail API (ex-Pôle Emploi)

- **URL:** https://francetravail.io/
- **Inscription:** Gratuite (OAuth 2.0)
- **Limite:** Illimitée (fair use)
- **Documentation:** https://francetravail.io/data/api

**Obtenir les credentials :**
1. Créer un compte sur France Travail Emploi Store Dev
2. Créer une application
3. Récupérer `Client ID` et `Client Secret`
4. Ajouter dans `config/.env` :
   ```
   FRANCETRAVAIL_CLIENT_ID=your_client_id
   FRANCETRAVAIL_CLIENT_SECRET=your_client_secret
   ```

---

## 📖 Usage

### Collecter des données

```bash
# Collecter 100 offres depuis The Muse
python src/collectors/themuse.py --limit 100

# Collecter depuis Adzuna (France)
python src/collectors/adzuna.py --country fr --limit 100

# Collecter depuis France Travail
python src/collectors/francetravail.py --limit 100
```

### Lancer le dashboard

```bash
streamlit run dashboard/app.py
```

### Lancer l'API

```bash
uvicorn api.main:app --reload
# Accéder à la doc : http://localhost:8000/docs
```

---

## 📅 Roadmap

**Mars 2025** ✅
- [x] Discovery document
- [x] Veille technologique
- [x] Architecture définie

**Avril 2025** 🔄
- [ ] Setup environnement
- [ ] Tests APIs
- [ ] Premiers scripts de collecte

**Mai-Juin 2025**
- [ ] Collecte de 3000+ offres
- [ ] Création bases de données
- [ ] Pipeline ETL

**Juillet-Septembre 2025**
- [ ] Extraction NLP compétences
- [ ] Analyses et visualisations
- [ ] Dashboard Streamlit v1

**Octobre-Décembre 2025**
- [ ] Algorithme de recommandation
- [ ] API REST FastAPI
- [ ] Tests et optimisations

**Janvier-Février 2026**
- [ ] Déploiement en production
- [ ] Documentation finale
- [ ] Soutenance

---

## 🤝 Contribution

Ce projet est développé dans le cadre d'un projet de fin d'études. Les contributions externes ne sont pas acceptées pour l'instant.

---

## 📄 Licence

Ce projet est réalisé à des fins éducatives dans le cadre du Master Data Engineering de DataScientest.

---

## 👤 Auteur

**Nour Amel SERIR**
- GitHub: [@nouramel](https://github.com/nouramel)
- LinkedIn: [Nour Serir](https://www.linkedin.com/in/nour-serir/)
- Email: serirna@gmail.com

**Encadrement :** DataScientest - Formation Data Engineering & Product Management (Mars 2025 - Février 2026)

---

## 📚 Ressources

- [Document Discovery](docs/discovery.md)
- [Architecture détaillée](docs/architecture.md)
- [Guide de déploiement](docs/deployment.md)
