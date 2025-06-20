from fastapi import FastAPI
from routes import router
from fastapi.responses import RedirectResponse

"""
This module initializes a FastAPI application for interacting with GitHub user data.
- Imports and includes API routes from the `routes` module.
- Sets up application metadata such as title, description, and version.
- Redirects the root URL ("/") to the automatic API documentation ("/docs").
Endpoints:
    - "/" (GET): Redirects to the Swagger UI documentation.
    - All endpoints defined in the included router.
Usage:
    Run this module to start the FastAPI server and access the API documentation at "/docs".
"""


app = FastAPI(
    title="API Utilisateurs GitHub",
    description="""
## 🎉 **Bienvenue sur l'API des utilisateurs GitHub !**

**Pour interagir avec les endpoints, authentifiez-vous**.
""",
    version="1.0.0",
)
app.include_router(router)

@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")


