# 🎮 CareerQuest — RPG Développement Carrière

Application gamifiée de développement professionnel — B3PRJ2 Hackathon

---

## 🚀 Démarrage rapide

### Prérequis
- Docker & Docker Compose installés
- Git

### Lancer l'application

```bash
git clone <url-du-repo>
cd careerquest
docker compose up --build
```

Puis ouvrir :
- **Frontend** → http://localhost:3000
- **Backend API** → http://localhost:8000/api
- **Admin Django** → http://localhost:8000/admin

---

## 🗄️ Initialiser la base de données

```bash
# Migrations
docker exec careerquest_backend python manage.py migrate

# Charger les données initiales (quêtes + compétences)
docker exec careerquest_backend python manage.py loaddata api/fixtures/initial_data.json

# Créer un superuser pour l'admin
docker exec -it careerquest_backend python manage.py createsuperuser
```

---

## 🏗️ Architecture

```
careerquest/
├── docker-compose.yml
├── .gitlab-ci.yml
├── backend/                  ← Django REST API
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── careerquest/          ← Config Django
│   │   ├── settings.py
│   │   └── urls.py
│   └── api/                  ← App principale
│       ├── models.py         ← User, Compétences, Quêtes
│       ├── views.py          ← Endpoints API
│       ├── serializers.py
│       ├── urls.py
│       └── fixtures/
│           └── initial_data.json
└── frontend/                 ← React
    ├── Dockerfile
    ├── package.json
    └── src/
        ├── App.js
        ├── App.css
        ├── pages/
        │   ├── Login.js
        │   ├── Register.js
        │   ├── Dashboard.js
        │   ├── Profil.js
        │   ├── Quetes.js
        │   └── Classement.js
        ├── components/
        │   ├── Navbar.js
        │   ├── Avatar.js
        │   └── ProgressBar.js
        └── services/
            └── api.js        ← Appels HTTP axios
```

---

## 📡 API Endpoints

| Méthode | URL | Description | Auth |
|---------|-----|-------------|------|
| POST | `/api/auth/register/` | Créer un compte | ❌ |
| POST | `/api/token/` | Login → JWT token | ❌ |
| GET | `/api/profil/` | Mon profil | ✅ |
| PUT | `/api/profil/` | Modifier profil | ✅ |
| GET | `/api/competences/` | Liste compétences | ❌ |
| GET | `/api/competences/mes/` | Mes compétences | ✅ |
| POST | `/api/competences/mes/` | Ajouter compétence | ✅ |
| GET | `/api/quetes/` | Mes quêtes | ✅ |
| POST | `/api/quetes/:id/done/` | Compléter quête | ✅ |
| GET | `/api/classement/` | Top 10 | ❌ |
| GET | `/api/github/:username/` | Repos GitHub | ✅ |

---

## 🎮 Système de progression

| Avatar | Niveau | Condition |
|--------|--------|-----------|
| 🧑‍💻 Étudiant | 1-5 | 0-499 XP |
| 👨‍🔬 Junior | 6-15 | 500-1499 XP |
| 🧙‍♂️ Senior | 16-30 | 1500-2999 XP |
| 🦸 Expert | 31+ | 3000+ XP |

**Gains XP :**
- Compléter une quête : +50 à +200 XP
- Ajouter une compétence : +20 XP
- Connecter GitHub : +10 XP par repo

---

## 👥 Équipe

| Rôle | Responsabilité |
|------|---------------|
| Frontend | React, pages, CSS |
| Backend | Django, API REST |
| DevOps | Docker, GitLab CI, déploiement |
