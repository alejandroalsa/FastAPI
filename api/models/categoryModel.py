# Importaciones

# List de typing es utilizado para indicar que el atributo podcasts sera una lista de objetos Podcast
from typing import List

# Tipos de datos que se utilizan para definir las columnas en SQLAlchemy.
from sqlalchemy import Integer, String, ForeignKey

# Herramientas de SQLAlchemy que permiten establecer las relaciones y columnas en el modelo.
from sqlalchemy.orm import Mapped, relationship, mapped_column

# Base: Para definir el modelo, ya definida en el archivo /database/database.py
from api import Base

# Podcast: El modelo Podcast que se importa para poder establecer la relación.
from api.models.podcastModel import Podcast


# Definición de la clase Category
class Category(Base):
    __tablename__ = "categories"  # Define el nombre de la tabla en la base de datos.

    # Definición de columnas
    # Las columnas se definen utilizando Mapped, lo que indica que estas son columnas de mapeo de la base de datos.
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    # Relación One-To-Many (Uno a Muchos) con Category
    # podcasts: Esto indica que esta relación está asociada con la clase Podcast (SQLAlchemy maneja las relaciones utilizando el nombre de la clase como un string).
    """
    El argumento cascade define el comportamiento de la relación cuando se realizan operaciones como insertar, actualizar o eliminar:
    
    all: Aplica todas las operaciones de cascada (como guardar, eliminar) a los objetos relacionados.
    
    delete-orphan: Si un objeto relacionado (en este caso, un Podcast) ya no está asociado a la categoría, se elimina automáticamente.
    """
    podcasts: Mapped[List["Podcast"]] = relationship(
        "Podcast", cascade="all, delete-orphan"
    )
