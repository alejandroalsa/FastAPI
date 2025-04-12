# Conexión a la base de datos y utilidades relacionadas
"""
engine: motor de conexión de SQLAlchemy
get_db: función para obtener una sesión en endpoints
SessionLocal: clase para crear sesiones de base de datos
"""
from api.database.database import engine, get_db, SessionLocal

# Configuración de etiquetas y metadatos para la documentación OpenAPI
from api.configdoc import tags_metadata

# Base de datos - modelos y relaciones
"""
Base: clase base declarativa para los modelos
podcast_authors: tabla intermedia de relación many-to-many (muchos a muchos)
"""
from api.database.database import Base
from api.database.database import podcast_authors

# Modelos de SQLAlchemy (ORM)
from api.models.categoryModel import Category as CategoryModel
from api.models.podcastModel import Podcast as PodcastModel
from api.models.authorModel import Author as AuthorModel

# Esquemas de Pydantic (validación y serialización)
from api.schemas.authorsSchema import AuthorSchema, AuthorCreateSchema, AuthorUpdateSchema
from api.schemas.podcastsSchema import PodcastSchema, PodcastCreateSchema, PodcastUpdateSchema, PodcastAuthorCreateSchema
from api.schemas.podcastsSchema import PodcastAuthorsSchema, AuthorPodcastsSchema
from api.schemas.categoriesSchema import CategorySchema, CategoryPodcastsSchema, CategoryCreateSchema


# Lógica de la API (controladores)
from api.controllers import categoryController
from api.controllers import podcastController
from api.controllers import authorController

# Rutas (routers agrupados por recurso)
from api.routers.categories import router as categoriesRouter
from api.routers.podcasts import router as podcastsRouter
from api.routers.authors import router as authorsRouter

# Instancia principal de la aplicación
from api.main import app
