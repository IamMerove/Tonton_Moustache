#!/bin/bash

echo "🚀 Démarrage de Tonton Moustache Backend..."

# Exécuter le script d'initialisation
echo "📦 Initialisation de la base de données..."
python init_admin.py

# Lancer le serveur uvicorn
echo "🌐 Démarrage du serveur FastAPI..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
