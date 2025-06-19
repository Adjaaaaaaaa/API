from fastapi import FastAPI
from routes import router

app = FastAPI(title="API Utilisateurs Filtrés")

app.include_router(router)
