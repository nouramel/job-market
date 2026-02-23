# 🔑 Guide d'obtention des clés API

Ce document explique **étape par étape** comment obtenir gratuitement les clés API nécessaires au projet Job Market.

---

## 1️⃣ The Muse API

### Informations
- **URL:** https://www.themuse.com/developers/api/v2
- **Limite:** 500 requêtes/jour (gratuit)
- **Temps d'obtention:** ~5 minutes

### Étapes d'inscription

1. **Aller sur le site**
   - Ouvrir https://www.themuse.com/developers/api/v2
   
2. **Créer un compte**
   - Cliquer sur "Sign up" en haut à droite
   - Remplir le formulaire (email, nom, mot de passe)
   - Valider l'email

3. **Accéder à la section Developers**
   - Une fois connecté, aller sur https://www.themuse.com/developers/api/v2
   - Cliquer sur "Get API Key"

4. **Obtenir la clé**
   - Votre clé API s'affiche directement
   - Format : `public_key_xxxxxxxxxxxxx`
   - **Copier cette clé !**

5. **Tester la clé**
   ```bash
   # Exemple de requête
   curl "https://www.themuse.com/api/public/jobs?api_key=VOTRE_CLE&page=1"
   ```

6. **Ajouter au projet**
   - Ouvrir le fichier `config/.env`
   - Ajouter : `THEMUSE_API_KEY=votre_cle_ici`

---

## 2️⃣ Adzuna API

### Informations
- **URL:** https://developer.adzuna.com/
- **Limite:** 1000 appels/mois (gratuit)
- **Temps d'obtention:** ~5 minutes

### Étapes d'inscription

1. **Aller sur le site**
   - Ouvrir https://developer.adzuna.com/

2. **Créer un compte développeur**
   - Cliquer sur "Sign Up" en haut à droite
   - Remplir le formulaire
   - Valider l'email

3. **Créer une application**
   - Une fois connecté, aller sur "Dashboard"
   - Cliquer sur "Create New Application"
   - Remplir :
     * **Application Name:** Job Market
     * **Description:** Job market analysis platform for educational purposes
     * **Website:** https://github.com/nouramel/job-market

4. **Obtenir les credentials**
   - Après création, vous verrez :
     * **Application ID** (format : `12345678`)
     * **Application Key** (format : `abcdef1234567890abcdef1234567890`)
   - **Copier ces deux valeurs !**

5. **Tester les clés**
   ```bash
   # Exemple de requête (France)
   curl "https://api.adzuna.com/v1/api/jobs/fr/search/1?app_id=VOTRE_APP_ID&app_key=VOTRE_APP_KEY&what=data"
   ```

6. **Ajouter au projet**
   - Ouvrir le fichier `config/.env`
   - Ajouter :
     ```
     ADZUNA_APP_ID=votre_app_id_ici
     ADZUNA_APP_KEY=votre_app_key_ici
     ```

---

## 3️⃣ France Travail API (OAuth 2.0)

### Informations
- **URL:** https://francetravail.io/
- **Limite:** Illimitée (fair use)
- **Temps d'obtention:** ~10 minutes
- **Note:** Plus complexe (OAuth 2.0)

### Étapes d'inscription

1. **Aller sur Emploi Store Dev**
   - Ouvrir https://francetravail.io/inscription

2. **Créer un compte**
   - Remplir le formulaire d'inscription
   - **Type de compte:** Particulier (ou Entreprise si vous avez)
   - Valider l'email

3. **Se connecter**
   - Login sur https://francetravail.io/

4. **Créer une application**
   - Aller dans "Tableau de bord" → "Mes applications"
   - Cliquer sur "Créer une application"
   - Remplir :
     * **Nom:** Job Market Analysis
     * **Description:** Plateforme d'analyse du marché de l'emploi (projet éducatif)
     * **Type:** Application Web
     * **URL de redirection:** http://localhost:8000/callback (mettre n'importe quoi, on ne l'utilise pas)

5. **Sélectionner les APIs**
   - Cocher :
     * ✅ **Offres d'emploi v2**
     * ✅ **Référentiel ROME v1**
   - Valider

6. **Obtenir les credentials**
   - Une fois l'application créée, vous verrez :
     * **Client ID** (format : `PAR_jobmarketxxx_xxxxxxxxxxxxx`)
     * **Client Secret** (format : `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
   - **Copier ces deux valeurs !**
   - ⚠️ **IMPORTANT:** Le Client Secret n'est affiché qu'une seule fois !

7. **Tester les credentials**
   ```bash
   # Étape 1 : Obtenir un token
   curl -X POST "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire" \
     -d "grant_type=client_credentials" \
     -d "client_id=VOTRE_CLIENT_ID" \
     -d "client_secret=VOTRE_CLIENT_SECRET" \
     -d "scope=api_offresdemploiv2 o2dsoffre"
   
   # Étape 2 : Utiliser le token pour faire une requête
   # (Le token est dans la réponse : "access_token": "...")
   curl -X GET "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search?motsCles=data" \
     -H "Authorization: Bearer VOTRE_TOKEN"
   ```

8. **Ajouter au projet**
   - Ouvrir le fichier `config/.env`
   - Ajouter :
     ```
     FRANCETRAVAIL_CLIENT_ID=votre_client_id_ici
     FRANCETRAVAIL_CLIENT_SECRET=votre_client_secret_ici
     ```

---

## ✅ Vérification

Une fois que vous avez ajouté toutes les clés dans `config/.env`, votre fichier devrait ressembler à :

```env
# THE MUSE
THEMUSE_API_KEY=public_key_xxxxxxxxxxxxx

# ADZUNA
ADZUNA_APP_ID=12345678
ADZUNA_APP_KEY=abcdef1234567890abcdef1234567890

# FRANCE TRAVAIL
FRANCETRAVAIL_CLIENT_ID=PAR_jobmarketxxx_xxxxxxxxxxxxx
FRANCETRAVAIL_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🧪 Tester les clés

Maintenant que vous avez toutes vos clés, testez-les avec le notebook :

1. Ouvrir `notebooks/01_test_apis.ipynb`
2. Exécuter toutes les cellules
3. Vérifier que les 3 APIs retournent des données

**Si tout fonctionne, vous êtes prêt pour la collecte de données !** 🎉

---

## 🆘 Problèmes courants

### The Muse : "Invalid API key"
- ✅ Vérifiez que la clé commence par `public_key_`
- ✅ Pas d'espaces avant/après la clé

### Adzuna : "Unauthorized"
- ✅ Vérifiez que vous avez bien les deux valeurs (ID + Key)
- ✅ Vérifiez le format de l'URL (pays : `fr` pour France)

### France Travail : "Invalid client"
- ✅ Vérifiez que l'application est bien "Activée" dans votre dashboard
- ✅ Le Client Secret ne doit contenir aucun espace
- ✅ Si le token expire, il faut en redemander un nouveau (normal, ils durent 15 min)

---

## 📞 Support

Si vous bloquez :
1. Relire attentivement les documentations officielles
2. Vérifier les logs d'erreur dans le notebook
3. Vérifier que le fichier `.env` est bien dans `config/`

**Bon courage !** 💪
