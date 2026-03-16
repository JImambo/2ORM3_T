# 🗄️ Database Manager Pro v2.0

Une application desktop moderne de gestion d'utilisateurs construite avec **Python**, **CustomTkinter** et **SQLAlchemy**.

## ✨ Fonctionnalités
- **Interface Moderne** : Design "Dark Mode" avec composants arrondis (CustomTkinter).
- **CRUD Complet** : Ajouter, Lire, Modifier et Supprimer des entrées dans une base SQLite.
- **Recherche Live** : Filtrage instantané des résultats pendant la saisie.
- **Auto-remplissage** : Cliquez sur une ligne du tableau pour charger les données dans le formulaire.
- **ORM SQLAlchemy** : Gestion propre et sécurisée de la base de données.

## 🛠️ Installation

1. **Cloner le projet** :
   ```bash
   git clone https://github.com/JImambo/2ORM3_T.git
   cd 2ORM3_T

2. **Créer un environnement virtuel** :
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate

3. **Installer les dépendances** :
    ```bash
    pip install sqlalchemy customtkinter darkdetect packaging


**📂 Structure du Projet**

database.py : Le script principal contenant l'interface et la logique SQL.

demo.db : La base de données SQLite (générée automatiquement au premier lancement).


**🚀 Utilisation**
Lancez l'application avec :
   ```bash
   python3 database.py

* Pour Ajouter : Remplissez les champs et cliquez sur "AJOUTER".

* Pour Modifier : Sélectionnez un utilisateur dans la liste, modifiez ses infos dans les champs, puis cliquez sur "MODIFIER".

* Pour Supprimer : Sélectionnez un utilisateur et cliquez sur "SUPPRIMER".

**📝 Licence**
* Ce projet est sous licence MIT.