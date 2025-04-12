# Importaciones principales

from fastapi import FastAPI  # Crea la instancia principal de la aplicación

# Importaciones de las rutas organizadas por recursos
from api import categoriesRouter
from api import podcastsRouter
from api import authorsRouter

from api import tags_metadata  # Documentación Swagger (más abajo se explica)
from fastapi.middleware.cors import (
    CORSMiddleware,
)  # Permite que la API sea accedida desde otros dominios

# CORS – Cross-Origin Resource Sharing
# Lista de dominios autorizados para hacer peticiones a la API
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Instancia de la aplicación FastAPI, que será el núcleo de la API.
app = FastAPI(
    title="Mastermaind Podcast API",
    description="APIRestFul para la gestión de los podcast realizados por Mastermind",
    version="0.1",
    contact={"name": "alejandroalsa", "url": "https://www.alejandroalsa.es"},
    openapi_tags=tags_metadata,  # Organiza las rutas por grupos con etiquetas amigables para la doc.
)

#  Middleware CORS
# Activa el middleware de CORS para permitir el acceso desde los dominios definidos, permitiendo todo tipo de métodos (GET, POST, PUT, DELETE, etc)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de Routers
app.include_router(categoriesRouter, tags=["categories"], prefix="/categories")
app.include_router(podcastsRouter, tags=["podcasts"], prefix="/podcasts")
app.include_router(authorsRouter, tags=["authors"], prefix="/authors")


# Ruta raíz
@app.get("/")
async def root():
    return {"title": app.title, "version": app.version}
