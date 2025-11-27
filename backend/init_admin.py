"""
Script d'initialisation de la base de données
Crée les rôles de base et un compte administrateur
"""

import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
import bcrypt

# Importer database en premier
from database import SessionLocal, engine, Base

# Puis importer les modèles dans l'ordre des dépendances
from roles.models import Role
from niveaux.models import Niveau
from matieres.models import Matiere
from agents.models import Agent
from users.models import User
from sessions.models import SessionConversation
from messages.models import Message

def hash_password(password: str) -> str:
    """Hasher un mot de passe avec bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def init_database():
    """Initialiser la base de données avec les données de base"""
    
    # Créer toutes les tables
    print("🔧 Création des tables...")
    Base.metadata.create_all(bind=engine)
    
    # Créer une session
    db = SessionLocal()
    
    try:
        # ============= CRÉATION DES RÔLES =============
        print("\n👥 Création des rôles...")
        
        # Vérifier si les rôles existent déjà
        role_admin = db.query(Role).filter(Role.nom_role == "Administrateur").first()
        role_etudiant = db.query(Role).filter(Role.nom_role == "Etudiant").first()
        
        if not role_admin:
            role_admin = Role(nom_role="Administrateur")
            db.add(role_admin)
            print("   ✅ Rôle 'Administrateur' créé")
        else:
            print("   ⚠️  Rôle 'Administrateur' existe déjà")
        
        if not role_etudiant:
            role_etudiant = Role(nom_role="Etudiant")
            db.add(role_etudiant)
            print("   ✅ Rôle 'Etudiant' créé")
        else:
            print("   ⚠️  Rôle 'Etudiant' existe déjà")
        
        db.commit()
        db.refresh(role_admin)
        db.refresh(role_etudiant)
        
        # ============= CRÉATION DES NIVEAUX =============
        print("\n📚 Création des niveaux scolaires...")
        
        niveaux = ["6ème", "5ème", "4ème", "3ème", "Seconde", "Première", "Terminale"]
        
        for niveau_nom in niveaux:
            niveau_exists = db.query(Niveau).filter(Niveau.nom_niveau == niveau_nom).first()
            if not niveau_exists:
                niveau = Niveau(nom_niveau=niveau_nom)
                db.add(niveau)
                print(f"   ✅ Niveau '{niveau_nom}' créé")
            else:
                print(f"   ⚠️  Niveau '{niveau_nom}' existe déjà")
        

        db.commit()

        # ============= CRÉATION DES MATIÈRES =============
        print("\n📚 Création des matières principales...")
        matieres = [
            ("Français", "Cours de français collège/lycée"),
            ("Mathématiques", "Cours de mathématiques collège/lycée"),
            ("Histoire-Géo", "Cours d'histoire-géographie"),
            ("Biologie", "Cours de SVT/biologie"),
            ("Physique", "Cours de physique-chimie"),
            ("Anglais", "Cours d'anglais")
        ]
        for nom, desc in matieres:
            matiere_exists = db.query(Matiere).filter(Matiere.nom_matieres == nom).first()
            if not matiere_exists:
                matiere = Matiere(nom_matieres=nom, description_matiere=desc)
                db.add(matiere)
                print(f"   ✅ Matière '{nom}' créée")
            else:
                print(f"   ⚠️  Matière '{nom}' existe déjà")
        db.commit()

        # Récupérer le premier niveau pour l'admin
        premier_niveau = db.query(Niveau).first()

        # ============= CRÉATION DU COMPTE ADMIN =============
        print("\n🔐 Création du compte administrateur...")

        # Informations du compte admin
        admin_email = "admin@tontonmoustache.com"
        admin_password = "Admin123!"

        # Vérifier si l'admin existe déjà
        admin_exists = db.query(User).filter(User.email == admin_email).first()

        if not admin_exists:
            # Hasher le mot de passe
            hashed_password = hash_password(admin_password)
            # Créer le compte admin
            admin = User(
                nom="Administrateur",
                prenom="Principal",
                email=admin_email,
                passwordhash=hashed_password,
                consentement_rgpd=True,
                id_niveau=premier_niveau.id_niveau,
                id_role=role_admin.id_role
            )
            db.add(admin)
            db.commit()
            print("   ✅ Compte administrateur créé avec succès!")
            print(f"\n📧 Email: {admin_email}")
            print(f"🔑 Mot de passe: {admin_password}")
            print("\n⚠️  IMPORTANT: Changez ce mot de passe après la première connexion!")
        else:
            print("   ⚠️  Un compte admin existe déjà")

        print("\n✨ Initialisation terminée avec succès!\n")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'initialisation: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("🎓 TONTON MOUSTACHE - Initialisation de la base de données")
    print("=" * 60)
    init_database()
