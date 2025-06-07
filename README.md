# GMB_CODEX

Cette application Flask permet de se connecter à l'API Google Business Profile via OAuth2 et d'afficher la liste de vos fiches dans un tableau de bord minimal.

## Installation

1. Créez un projet Google Cloud et activez l'API *Google Business Profile*.
2. Configurez un identifiant OAuth 2.0 de type "Application Web" et téléchargez le fichier `client_secret.json` à placer à la racine du projet. Vous pouvez aussi définir les variables d'environnement `GOOGLE_CLIENT_ID` et `GOOGLE_CLIENT_SECRET` à la place du fichier.
3. Installez les dépendances :

```bash
pip install -r requirements.txt
```

4. Lancez l'application :

```bash
python app/app.py
```

L'application s'exécute sur [http://localhost:5000](http://localhost:5000).

## Fonctionnement

Au premier lancement, un bouton de connexion Google s'affiche. Une fois l'utilisateur autorisé, l'application récupère les locations associées au compte et les présente dans le dashboard.

Ce projet sert de base pour ajouter d'autres KPIs : note moyenne, nombre d'avis, etc.
