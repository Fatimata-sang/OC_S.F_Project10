Résumé

Ce projet consiste à développer pour SoftDesk, une entreprise éditrice de logiciels,
une API REST sécurisée de suivi des problèmes (issue tracking).

L’application de suivi couvre les trois plateformes (Web, Android et iOS) et permet aux utilisateurs de :

créer des projets (projects),

ajouter des utilisateurs (users) comme contributeurs (contributors)à un projet,

créer des tickets (issues) dans un projet (projects),

ajouter des commentaires (comments) à un ticket (issues).

Les Fonctionnalités

Authentification et Autorisation : accès sécurisé basé sur les rôles et les propriétés.

Endpoints API : prise en charge complète du CRUD (create, read, update, and delete).

Technologies utilisées

Langage de programmation : Python

Framework : Django REST

Base de données : SQLite

Authentification back-end : JWT (JSON Web Token)

Tâches du projet

Concevoir les modèles Django à partir du schéma de base de données.

Créer des serializers pour la validation et la transformation des données.

Créer des vues pour gérer la logique de l’API.

Définir les routes URL de l’API.

Appliquer des permissions aux vues pour garantir un accès autorisé.
| Endpoint API                                | Méthode HTTP | URl                                     | Permission                    |
| ------------------------------------------- | ------------ | ---------------------------------------- | ----------------------------- |
| Inscription utilisateur                     | POST         | /signup/                                 | Toute personne ≥ 18 ans       |
| Connexion utilisateur                       | POST         | /login/                                  | Utilisateurs enregistrés      |
| Liste des projets de l’utilisateur connecté | GET          | /projects/                               | Propriétaire et contributeurs |
| Créer un nouveau projet                     | POST         | /projects/                               | Utilisateurs enregistrés      |
| Obtenir un projet                           | GET          | /projects/{id}/                          | Propriétaire et contributeurs |
| Mettre à jour un projet                     | PUT          | /projects/{id}/                          | Propriétaire du projet        |
| Supprimer un projet et ses issues           | DELETE       | /projects/{id}/                          | Propriétaire du projet        |
| Ajouter un contributeur à un projet         | POST         | /projects/{id}/contributors/             | Propriétaire du projet        |
| Lister les utilisateurs d’un projet         | GET          | /projects/{id}/contributors/             | Propriétaire du projet        |
| Supprimer un utilisateur d’un projet        | DELETE       | /projects/{id}/contributors/{id}         | Propriétaire du projet        |
| Obtenir les issues d’un projet              | GET          | /projects/{id}/issues/                   | Propriétaire et contributeurs |
| Créer une issue dans un projet              | POST         | /projects/{id}/issues/                   | Propriétaire et contributeurs |
| Mettre à jour une issue                     | PUT          | /projects/{id}/issues/{id}               | Propriétaire de l’issue       |
| Supprimer une issue                         | DELETE       | /projects/{id}/issues/{id}               | Propriétaire de l’issue       |
| Créer un commentaire sur une issue          | POST         | /projects/{id}/issues/{id}/comments/     | Propriétaire et contributeurs |
| Lister les commentaires d’une issue         | GET          | /projects/{id}/issues/{id}/comments/     | Propriétaire et contributeurs |
| Modifier un commentaire                     | PUT          | /projects/{id}/issues/{id}/comments/{id} | Propriétaire du commentaire   |
| Supprimer un commentaire                    | DELETE       | /projects/{id}/issues/{id}/comments/{id} | Propriétaire du commentaire   |
| Obtenir un commentaire spécifique           | GET          | /projects/{id}/issues/{id}/comments/{id} | Propriétaire et contributeurs |

Développement local
Ce project a été fait avec : 
Python 3.10 

Installation sur macOS/Linux

Cloner le dépôt

cd /chemin/vers/le/projet
git clone https://github.com/Fatimata-sang/OC_S.F_Project10.git


Se déplacer dans le dossier

cd SoftDesk

Créer un environnement virtuel

python -m venv venv


Activer l’environnement

source venv/bin/activate


Mettre à jour pip de manière sécurisée

python -m pip install --upgrade pip


Installer les dépendances

pip install -r requirements.txt


Désactiver l’environnement

deactivate

Installation sur Windows

Suivre les mêmes étapes ci-dessus.

Pour activer l’environnement :

.\venv\Scripts\Activate

Lancer l’application

Démarrer le serveur

cd SoftDesk

python manage.py runserver


Accès via le navigateur

Pour l’inscription :

http://localhost:8000/api/signup


Pour la connexion :

http://localhost:8000/api/login

Interface d’administration et les users qui sont deja dans la base de donnée

admin :
user : admin
password : ADMIn12345

users :
user : toto
password : titi2025

user : fatim
password : fatim2025


Accéder à :

http://localhost:8000/admin


Se connecter avec le superuser.

Tests :

Les endpoints d’inscription et de connexion ne nécessitent pas de token.

Tous les autres endpoints nécessitent un token d’accès.

Tous les endpoints peuvent être testés avec Postman
, cURL ou le serveur local Django REST.