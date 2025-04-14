# Importaciones principales

from fastapi import FastAPI, status, Depends, HTTPException  # Crea la instancia principal de la aplicación
# Importaciones de las rutas organizadas por recursos
from api import categoriesRouter
from api import podcastsRouter
from api import authorsRouter
from sqlalchemy.orm import Session
from api import get_db, securityController

from dotenv import load_dotenv
import os

load_dotenv()

from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta

from passlib.context import CryptContext

from api.schemas.usersSchema import UserCreateSchema, UserInSchema, UserSchema 

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
    title=os.getenv('API_NAME'),
    description=os.getenv('API_DESCRIPTION'),
    version=os.getenv('API_VERSION'),
    contact={"name": os.getenv('API_DEVELOPER'), "url": "https://www.alejandroalsa.es", "email": os.getenv('EMAIL_SUPPORT')},
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

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Ruta raíz
@app.get("/")
async def root():
    return {"title": app.title, "version": app.version}

@app.post("/signup/", response_model=UserSchema)
async def singup(user: UserCreateSchema, db: Session = Depends(get_db)):
    user.password=pwd_context.hash(user.password)
    return securityController.write_user(db,user)

@app.post("/signin/")
async def login(user: UserInSchema, db: Session = Depends(get_db)):
    user = securityController.authenticate_user(db, user.username, user.password, pwd_context)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username o password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return  {"access_token": securityController.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    ), "token_type": "bearer"}
