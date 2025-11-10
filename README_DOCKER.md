# 🐳 Docker - Tonton Moustache

## 🚀 Démarrage rapide

### Lancer l'application complète
```bash
docker-compose up
```

### Lancer en arrière-plan
```bash
docker-compose up -d
```

### Reconstruire les images
```bash
docker-compose up --build
```

## 📝 Commandes utiles

### Voir les logs
```bash
# Tous les services
docker-compose logs -f

# Backend uniquement
docker-compose logs -f backend

# Frontend uniquement
docker-compose logs -f frontend
```

### Arrêter les conteneurs
```bash
docker-compose down
```

### Arrêter et supprimer les volumes
```bash
docker-compose down -v
```

### Accéder à un conteneur
```bash
# Backend
docker-compose exec backend bash

# Frontend
docker-compose exec frontend sh
```

## 🌐 URLs d'accès

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentation API**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📦 Structure

```
Tonton_Moustache/
├── docker-compose.yml      # Orchestration des services
├── backend/
│   ├── Dockerfile         # Image Docker du backend
│   └── requirements.txt   # Dépendances Python
└── frontend/
    └── Dockerfile         # Image Docker du frontend
```

## 🔧 Développement

Les volumes sont montés pour permettre le **hot-reload** :
- Modifications du backend → Uvicorn redémarre automatiquement
- Modifications du frontend → Vite recharge automatiquement

## ⚠️ Notes importantes

1. La base de données SQLite est stockée dans un volume Docker nommé `backend_db`
2. Les `node_modules` du frontend sont dans un volume anonyme pour de meilleures performances
3. Le backend est accessible depuis le frontend via le réseau Docker `tonton_network`
