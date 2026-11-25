
"""
Notification microservice - entry point.

Run: python -m uvicorn app.main:app --port 8084
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.routers import notification
import py_eureka_client.eureka_client as eureka_client


# Port du microservice
PORT = int(os.getenv("PORT", "8084"))


# Enregistrement et arrêt du client Eureka
@asynccontextmanager
async def lifespan(app: FastAPI):

    # Enregistrer NOTIFICATION dans Eureka
    await eureka_client.init_async(
        eureka_server="http://localhost:8761/eureka",
        app_name="NOTIFICATION",
        instance_port=PORT,
        instance_host="127.0.0.1",
        instance_id=f"notification:127.0.0.1:{PORT}",
        health_check_url=f"http://127.0.0.1:{PORT}/health",
        status_page_url=f"http://127.0.0.1:{PORT}/info"
    )

    print(f"NOTIFICATION enregistré dans Eureka sur le port {PORT}")

    try:
        yield
    finally:
        # Désenregistrer NOTIFICATION de Eureka
        await eureka_client.stop_async()
        print("NOTIFICATION arrêté dans Eureka")


# Création de l'application FastAPI
app = FastAPI(
    title="Notification Microservice API",
    version="1.0.0",
    description=(
        "Notification microservice (Python / FastAPI, no database). "
        "Only the hello endpoint is implemented; the notification "
        "logic is to be developed by students."
    ),
    contact={"name": "Badia Abouhdid"},
    servers=[
        {
            "url": f"http://localhost:{PORT}",
            "description": "Local"
        }
    ],
    docs_url="/swagger-ui",
    openapi_url="/v3/api-docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


# Vérification de l'état du microservice
@app.get("/health")
def health():
    return {"status": "UP"}


# Informations du microservice
@app.get("/info")
def info():
    return {
        "name": "Notification",
        "version": "1.0.0"
    }


# Conserver les routes existantes
app.include_router(notification.router)


print(">>> NOUVELLE VERSION MAIN.PY CHARGÉE <<<")


# Lancement direct du serveur
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True
    )
