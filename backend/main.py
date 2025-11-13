from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Imports locaux
from users import router as users_router
from roles import router as roles_router
from niveaux import router as niveaux_router
from sessions import router as sessions_router
from users.models import User
from niveaux.models import Niveau
from roles.models import Role
from agents.models import Agent
from sessions.models import SessionConversation
from database import engine, Base

# ============= CRÉATION DES TABLES =============
Base.metadata.create_all(bind=engine)

# ============= CONFIGURATION FASTAPI =============
app = FastAPI(
    title="Tonton Moustache API",
    description="API de gestion de recettes de cuisine",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ============= MIDDLEWARE CORS =============
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # URLs du frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= ROUTES PRINCIPALES =============
@app.get("/")
def read_root():
    """Page d'accueil de l'API"""
    return {
        "message": "Bienvenue sur l'API Tonton Moustache! 🍳",
        "version": "1.0.0",
        "endpoints": {
            "users": "/users/",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/health")
def health_check():
    """Vérification de l'état de l'API"""
    return {"status": "OK", "message": "API fonctionnelle"}

# ============= INCLUSION DES ROUTERS =============
app.include_router(
    users_router, 
    prefix="/users", 
    tags=["Utilisateurs"],
    responses={404: {"description": "Utilisateur non trouvé"}}
)

app.include_router(
    roles_router, 
    prefix="/roles", 
    tags=["Roles"],
    responses={404: {"description": "Role non trouvé"}}
)

app.include_router(
    niveaux_router, 
    prefix="/niveau", 
    tags=["Niveaux"],
    responses={404: {"description": "Niveau non trouvé"}}
)

app.include_router(
    sessions_router, 
    prefix="/sessions", 
    tags=["Sessions"],
    responses={404: {"description": "Session non trouvée"}}
)

# ============= DÉMARRAGE =============
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )
