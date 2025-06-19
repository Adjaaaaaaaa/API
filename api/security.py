from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dotenv import load_dotenv
import os
import secrets

load_dotenv()  # charge les variables d'environnement du fichier .env

security = HTTPBasic()

auth_users_str = os.getenv("AUTH_USERS", "")
# transforme "admin:admin123,user1:pass1" en dict
AUTHORIZED_USERS = dict(user.split(":", 1) for user in auth_users_str.split(",") if ":" in user)

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_password = AUTHORIZED_USERS.get(credentials.username)
    if not correct_password or not secrets.compare_digest(credentials.password, correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
