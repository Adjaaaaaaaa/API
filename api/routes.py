import json
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from .security import verify_credentials

router = APIRouter()
"""
API Routes for User Management
This module defines FastAPI routes for managing and retrieving user information
from a pre-filtered JSON file. All endpoints require authentication via the
`verify_credentials` dependency.
Routes:
    - GET /users/:
        Returns the complete list of filtered users.
        
        Searches for users whose login contains the specified keyword.
        Query Parameters:
            - q (str): The keyword to search for in user logins.
        
    - GET /users/{login}:
        Returns the details of a user identified by their login.
        Path Parameters:
            - login (str): The login of the user to retrieve.
Dependencies:
    - verify_credentials: Ensures that the user is authenticated before accessing any endpoint.
Raises:
    - HTTPException 404: If a user with the specified login is not found.
"""

# Charger le fichier JSON une fois au démarrage
DATA_FILE = Path(__file__).parent.parent / "data" / "filtered_users.json"
with open(DATA_FILE, "r", encoding="utf-8") as f:
    USERS = json.load(f)

@router.get("/users/", summary="Liste des utilisateurs filtrés", description="Retourne la liste complète des utilisateurs filtrés.")
def get_users(username: str = Depends(verify_credentials)):
    return USERS

@router.get("/users/search", summary="Recherche d’utilisateurs", description="Recherche les utilisateurs dont le login contient le mot-clé spécifié.")
def search_users(q: str, username: str = Depends(verify_credentials)):
    results = [user for user in USERS if q.lower() in user["login"].lower()]
    return results

@router.get("/users/{login}", summary="Détails d’un utilisateur", description="Retourne les détails d’un utilisateur donné par son login.")
def get_user(login: str, username: str = Depends(verify_credentials)):
    for user in USERS:
        if user["login"].lower() == login.lower():
            return user
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")


