from fastapi import FastAPI
from routes import router

"""
This module initializes a FastAPI application for managing filtered users.
- Imports FastAPI for creating the web application.
- Imports the API router from the 'routes' module.
- Creates a FastAPI app instance with the title "API Utilisateurs GitHub".
- Includes the router to register API endpoints.
Usage:
    Run this module to start the FastAPI server and expose the user filtering API endpoints.
"""


app = FastAPI(title="API Utilisateurs GitHub")

app.include_router(router)
