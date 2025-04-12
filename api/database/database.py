# Importación de los componentes clave de SQLAlchemy, necesarios para:
"""
Column: Crear columnas
ForeignKey: Crear claves foráneas
Table: Definir tablas
create_engine: Crear el motor de conexión a la BD
sessionmaker: Crear sesiones
DeclarativeBase: Definir una base declaravita para los modelos
"""
from sqlalchemy import Column, ForeignKey, Table, create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# URL de conexión a la base de datos, en este caso para MySQL
"""
diwesadvanced_admin: usuario de la base de datos
password_admin: contraseña del usuario
localhost: servidor de la base de datos
masterpodcast: nombre de la base de datos
"""
SQLALCHEMY_DATABASE_URL = (
  "mysql+pymysql://diwesadvanced_admin:password_admin@localhost/masterpodcast"
)

# Creación del objeto "engine" que representa la conexión a la base de datos.
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True) # echo=True -> activa el modo debug, y se verán las consultas SQL ejecutadas en consola (solo para desarrollo)

# Sesiones
"""
SessionLocal es una clase que crea sesiones de base de datos.
autocommit=False: forzar el uso de escribir db.commit() explícitamente para aplicar los cambios en la BD.
autoflush=False: evita que SQLAlchemy sincronice automáticamente los datos en cada cambio.
bind=engine: enlaza la sesión al motor de conexión.
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para modelos: Esto define una clase base a partir de la cual heredan todos tus modelos (Author, Podcast, etc.)
class Base(DeclarativeBase):
    pass
  
# Tabla de asociación entre Podcasts y Authors
# Como vimos antes, esta tabla no tiene un model propio porque no necesitas añadirle campos extra. Es una tabla intermedia entre podcasts y authors par el many-to-many.
# Cada vez que tengamos una relación muchos a muchos (many-to-many) sin atributos adicionales necesitamos definir esto:
podcast_authors = Table(
    "podcast_authors",
    Base.metadata,
    Column("podcast_id", ForeignKey("podcasts.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)

# Dependencia de sesión. Esto es una dependencia de FastAPI.
def get_db():
  db = SessionLocal() # Se crea la sesión
  # Se intenta devolver la sesión
  try:
    yield db # Devolvemos la sesión con yield
  finally:
    db.close() # No devolvemos la sesión
