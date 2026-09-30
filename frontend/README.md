# User Access Security App

Application web sécurisée développée dans le cadre d'un projet de transition vers la cybersécurité.

L'objectif de ce projet est de construire progressivement une application web complète et de mettre en pratique des concepts de **sécurité applicative**, **authentification**, **autorisation**, **tests de sécurité**, **CI/CD**, **DevSecOps**, **conteneurs**, **Infrastructure as Code** et **AWS**.

Le projet est volontairement construit étape par étape afin de comprendre et de documenter chaque mécanisme de sécurité.

---

## 🎯 Objectifs

Les principaux objectifs sont de :

* construire une application web avec un frontend et une API ;
* mettre en place une authentification sécurisée ;
* protéger les mots de passe avec Argon2 ;
* utiliser des JWT pour l'authentification ;
* gérer les rôles et les autorisations ;
* protéger les endpoints sensibles ;
* limiter les risques de BOLA/IDOR et BFLA ;
* valider les entrées côté backend ;
* écrire des tests automatisés de sécurité ;
* automatiser les contrôles avec GitHub Actions ;
* intégrer progressivement des outils DevSecOps ;
* conteneuriser l'application avec Docker ;
* décrire l'infrastructure avec Terraform ;
* préparer un déploiement AWS sécurisé ;
* utiliser OIDC entre GitHub Actions et AWS afin d'éviter les clés AWS statiques.

---

# 🏗️ Architecture de l'application

L'architecture actuelle est composée de trois couches principales :

```text
┌──────────────────────────────┐
│          Angular 22          │
│           Frontend           │
│                              │
│  Login                       │
│  Dashboard                   │
│  Auth Guard                  │
│  HTTP Interceptor            │
└──────────────┬───────────────┘
               │
               │ HTTP + JWT
               ▼
┌──────────────────────────────┐
│           FastAPI            │
│           Backend            │
│                              │
│  Authentication              │
│  JWT validation              │
│  Authorization               │
│  API endpoints               │
└──────────────┬───────────────┘
               │
               │ SQLAlchemy
               ▼
┌──────────────────────────────┐
│         PostgreSQL           │
│                              │
│  users                       │
│  email                       │
│  password_hash               │
│  role                        │
└──────────────────────────────┘
```

---

# 🛠️ Technologies

## Frontend

* Angular 22
* TypeScript
* SCSS
* Angular Reactive Forms
* Angular Router
* Angular HTTP Client

## Backend

* Python 3.12
* FastAPI
* SQLAlchemy
* Pydantic
* PyJWT
* pwdlib
* Argon2

## Base de données

* PostgreSQL

## Tests

* pytest
* FastAPI TestClient

## Versioning

* Git
* GitHub

## CI/CD et DevSecOps — prévus

* GitHub Actions
* SAST
* SCA
* Secret scanning
* Docker
* Trivy
* Terraform
* AWS IAM
* AWS STS
* GitHub Actions OIDC

---

# 🔐 Sécurité de l'application

## Hachage des mots de passe

Les mots de passe ne sont jamais stockés en clair.

Ils sont hachés avec **Argon2** via `pwdlib`.

```text
Mot de passe
      │
      ▼
    Argon2
      │
      ▼
password_hash
      │
      ▼
 PostgreSQL
```

La base de données contient uniquement le hash du mot de passe.

---

## Authentification JWT

Lorsqu'un utilisateur fournit des identifiants valides, le backend génère un JWT.

Le token contient notamment :

* l'identité de l'utilisateur (`sub`) ;
* le rôle ;
* la date d'expiration (`exp`).

La durée de validité actuelle du token est de **30 minutes**.

Le frontend stocke actuellement le token dans `sessionStorage`.

---

## Validation du JWT

Les endpoints protégés vérifient :

1. la présence du header `Authorization` ;
2. le format `Bearer <token>` ;
3. la validité de la signature ;
4. l'expiration du token ;
5. la présence de l'identité utilisateur ;
6. l'existence de l'utilisateur en base de données.

---

# 👤 Authentification et autorisation

Une distinction est faite entre :

```text
Authentification
      │
      ▼
Qui est l'utilisateur ?
```

et :

```text
Autorisation
      │
      ▼
Que peut-il faire ?
```

Un utilisateur authentifié ne possède donc pas automatiquement les droits administrateur.

---

## Autorisation administrateur

L'endpoint :

```http
GET /admin
```

est réservé aux utilisateurs ayant actuellement le rôle :

```text
admin
```

Le backend récupère l'utilisateur depuis PostgreSQL avant de vérifier son rôle.

Le rôle actuellement présent en base de données est donc utilisé pour prendre la décision d'autorisation.

Cela permet notamment de ne pas considérer le rôle contenu dans un ancien JWT comme l'unique source de vérité pour les permissions.

---

# 🛡️ Protection du frontend

Le dashboard est protégé par un **Angular Auth Guard**.

Lorsqu'un utilisateur ne possède pas de token dans sa session, il est redirigé vers :

```text
/login
```

---

## HTTP Interceptor

Un interceptor Angular ajoute automatiquement le JWT aux requêtes API :

```http
Authorization: Bearer <JWT>
```

Cela permet aux endpoints protégés de récupérer l'identité de l'utilisateur.

---

# 🚨 Gestion des erreurs

Le backend distingue notamment :

### 401 Unauthorized

Utilisé lorsque l'authentification est absente ou invalide.

Exemples :

```text
Identifiants incorrects
Token invalide
Token manquant
```

### 403 Forbidden

Utilisé lorsque l'utilisateur est authentifié mais ne possède pas les permissions nécessaires.

Exemple :

```text
Accès réservé aux administrateurs
```

---

# 🧪 Tests de sécurité

Le projet contient actuellement **6 tests automatisés**.

Les tests couvrent :

## Mots de passe

* création d'un hash ;
* vérification d'un mot de passe correct ;
* rejet d'un mauvais mot de passe.

## JWT

* création d'un JWT ;
* décodage d'un JWT valide ;
* vérification des claims ;
* rejet d'un JWT invalide.

## Autorisation

* accès administrateur autorisé ;
* accès utilisateur standard refusé ;
* rejet d'un token invalide.

Lancer les tests :

```bash
python -m pytest
```

Résultat actuel :

```text
6 passed
```

---

# 🔎 Endpoints

## Publics

```http
GET /
POST /login
```

## Authentifié

```http
GET /users/me
```

## Administrateur

```http
GET /admin
```

---

# 👥 Utilisateurs de test

## Utilisateur standard

```text
Email : alice@example.com
Rôle  : user
```

## Administrateur

```text
Email : admin@example.com
Rôle  : admin
```

Les mots de passe de test ne sont volontairement pas documentés dans ce README.

Ils sont uniquement destinés à l'environnement local.

---

# 🔒 Gestion des secrets

Les secrets locaux sont stockés dans un fichier :

```text
.env
```

Ce fichier est exclu du dépôt Git.

Il ne doit jamais contenir de secrets qui seraient commités dans GitHub.

Exemple de structure :

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost/user_access_db
JWT_SECRET=CHANGE_ME
```

Les valeurs réelles ne doivent jamais être publiées.

---

# 🔄 Pipeline CI/CD et DevSecOps

La pipeline CI/CD constitue une partie importante du projet.

L'objectif est de faire évoluer progressivement le pipeline afin qu'un `git push` déclenche automatiquement différents contrôles.

L'architecture cible est :

```text
                    Git push
                       │
                       ▼
              ┌─────────────────┐
              │ GitHub Actions  │
              └────────┬────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
       Tests          SAST         SCA
          │            │            │
          └────────────┼────────────┘
                       │
                       ▼
               Secret scanning
                       │
                       ▼
                 Docker build
                       │
                       ▼
                   Trivy
                       │
                       ▼
                Déploiement
                       │
                       ▼
                     AWS
```

---

## 1. Tests automatisés

La première étape de la pipeline sera l'exécution automatique des tests Python.

```text
git push
   │
   ▼
GitHub Actions
   │
   ▼
pytest
   │
   ├── succès → pipeline continue
   │
   └── échec  → pipeline arrêtée
```

L'objectif est d'empêcher une modification cassant les mécanismes de sécurité de passer silencieusement dans la branche principale.

---

## 2. SAST

Le **Static Application Security Testing** permettra d'analyser le code source afin de rechercher des problèmes de sécurité.

Exemples de contrôles possibles :

* mauvaises pratiques Python ;
* problèmes liés aux entrées utilisateur ;
* erreurs de sécurité courantes ;
* utilisation dangereuse de certaines fonctions.

Le SAST sera intégré progressivement à GitHub Actions.

---

## 3. SCA

Le **Software Composition Analysis** permettra d'analyser les dépendances du projet.

L'objectif est notamment d'identifier les dépendances présentant des vulnérabilités connues.

Les dépendances Python seront ainsi contrôlées automatiquement dans la CI.

---

## 4. Secret scanning

Le pipeline devra également rechercher les secrets accidentellement présents dans le dépôt.

Exemples :

* tokens ;
* clés API ;
* credentials ;
* secrets AWS ;
* mots de passe.

Le fichier `.env` est déjà exclu du dépôt grâce au `.gitignore`, mais le pipeline ajoutera une seconde couche de protection.

---

## 5. Docker

L'application sera ensuite conteneurisée.

La cible est notamment :

```text
Frontend
   │
   ▼
Docker

Backend
   │
   ▼
Docker

PostgreSQL
   │
   ▼
Docker / environnement contrôlé
```

Docker permettra d'obtenir un environnement reproductible entre développement, CI et déploiement.

---

## 6. Trivy

Les images Docker seront analysées avec **Trivy**.

L'objectif sera de rechercher :

* vulnérabilités système ;
* vulnérabilités de packages ;
* problèmes dans les images ;
* éventuellement des secrets détectables dans les artefacts.

La pipeline pourra être configurée pour bloquer le déploiement lorsque certaines vulnérabilités dépassent un niveau défini.

---

# ☁️ Infrastructure as Code

L'infrastructure cloud sera progressivement décrite avec **Terraform**.

L'objectif est d'éviter de créer manuellement toute l'infrastructure et de conserver sa configuration dans Git.

Architecture cible :

```text
Terraform
    │
    ▼
AWS
```

Les ressources AWS seront ainsi versionnées avec le code.

---

# 🔐 GitHub Actions → AWS

Une partie importante du projet sera la sécurisation de l'accès entre GitHub Actions et AWS.

L'objectif est d'éviter :

```text
GitHub Actions
      │
      ▼
Clé AWS statique
```

et de mettre en place :

```text
GitHub Actions
      │
      │ OIDC
      ▼
AWS IAM Role
      │
      ▼
AWS STS
      │
      ▼
Credentials temporaires
      │
      ▼
AWS
```

## Pourquoi OIDC ?

OIDC permettra à GitHub Actions d'obtenir des credentials temporaires auprès d'AWS sans stocker une clé d'accès AWS longue durée dans les secrets GitHub.

Le rôle IAM pourra également être configuré avec des permissions minimales.

---

# 🔑 Principe du moindre privilège

Le projet appliquera progressivement le principe :

> Donner uniquement les permissions nécessaires.

Cela concernera notamment :

* les rôles applicatifs ;
* les endpoints administrateurs ;
* les permissions IAM ;
* GitHub Actions ;
* les ressources AWS ;
* les credentials utilisés dans la CI/CD.

---

# 📁 Structure du projet

```text
user-access-security-app/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── create_user.py
│
├── frontend/
│   └── src/
│       └── app/
│           ├── guards/
│           ├── interceptors/
│           ├── pages/
│           └── services/
│
├── tests/
│   ├── test_auth.py
│   └── test_security.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .gitignore
├── README.md
└── requirements.txt
```

> Le fichier `ci.yml` sera ajouté lors de la mise en place de la pipeline GitHub Actions.

---

# 🚀 Installation locale

## Prérequis

* Python 3.12+
* Node.js
* npm
* PostgreSQL
* Angular CLI

---

## Backend

Créer l'environnement virtuel :

```bash
python3 -m venv .venv
```

Activer l'environnement :

```bash
source .venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Créer le fichier `.env` à la racine du projet :

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost/user_access_db
JWT_SECRET=CHANGE_ME
```

Démarrer FastAPI :

```bash
uvicorn app.main:app --reload
```

API :

```text
http://127.0.0.1:8000
```

Documentation :

```text
http://127.0.0.1:8000/docs
```

---

# 🅰️ Frontend

Entrer dans le dossier frontend :

```bash
cd frontend
```

Installer les dépendances :

```bash
npm install
```

Démarrer Angular :

```bash
ng serve --poll 1000
```

Application :

```text
http://localhost:4200
```

---

# 🧪 Vérification locale

Lancer les tests backend :

```bash
python -m pytest
```

Démarrer le backend :

```bash
uvicorn app.main:app --reload
```

Démarrer le frontend :

```bash
cd frontend
ng serve --poll 1000
```

Puis ouvrir :

```text
http://localhost:4200
```

---

# 📋 État du projet

## Implémenté

* [ ] Application Angular
* [ ] API FastAPI
* [ ] PostgreSQL
* [ ] SQLAlchemy
* [ ] Hachage des mots de passe avec Argon2
* [ ] Authentification JWT
* [ ] Expiration des JWT
* [ ] Auth Guard Angular
* [ ] HTTP Interceptor
* [ ] Endpoint `/users/me`
* [ ] Gestion des rôles
* [ ] Autorisation administrateur
* [ ] Vérification du rôle actuel en base
* [ ] Gestion des réponses HTTP 401/403
* [ ] Tests automatisés
* [ ] Git
* [ ] GitHub
* [ ] Protection du fichier `.env`

## CI/CD / DevSecOps à implémenter

* [ ] GitHub Actions
* [ ] Pipeline de tests automatique
* [ ] SAST
* [ ] SCA
* [ ] Secret scanning
* [ ] Docker
* [ ] Scan Docker avec Trivy
* [ ] Pipeline de build
* [ ] Pipeline de déploiement

## Cloud à implémenter

* [ ] Terraform
* [ ] AWS
* [ ] IAM
* [ ] STS
* [ ] GitHub Actions OIDC
* [ ] Déploiement automatisé AWS
* [ ] Principe du moindre privilège côté cloud

---

# 🎓 Compétences travaillées

Ce projet permet de mettre en pratique :

### Sécurité applicative

* authentification ;
* autorisation ;
* JWT ;
* hachage des mots de passe ;
* gestion des sessions ;
* contrôle des accès ;
* BOLA/IDOR ;
* BFLA ;
* validation des entrées.

### Développement

* Angular ;
* TypeScript ;
* Python ;
* FastAPI ;
* SQLAlchemy ;
* PostgreSQL ;
* API REST.

### DevSecOps

* Git ;
* GitHub ;
* GitHub Actions ;
* tests automatisés ;
* SAST ;
* SCA ;
* secret scanning ;
* Docker ;
* Trivy.

### Cloud Security

* Terraform ;
* AWS ;
* IAM ;
* STS ;
* OIDC ;
* gestion des permissions ;
* credentials temporaires ;
* principe du moindre privilège.

---

# 📌 Statut

Projet personnel de formation et de portfolio orienté **cybersécurité applicative et DevSecOps**.

Le projet est développé progressivement, avec une priorité donnée à la compréhension des mécanismes de sécurité, aux tests et à l'automatisation.
