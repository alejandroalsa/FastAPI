# Importaciones

# List de typing es utilizado para indicar que el atributo podcasts sera una lista de objetos Podcast
from typing import List

# Tipos de datos que se utilizan para definir las columnas en SQLAlchemy.
from sqlalchemy import Integer, String, ForeignKey

# Herramientas de SQLAlchemy que permiten establecer las relaciones y columnas en el modelo.
from sqlalchemy.orm import Mapped, relationship, mapped_column

# Base: Para definir el modelo, ya definida en el archivo /database/database.py
# podcast_authors: Es la tabla intermedia, usada para la relación muchos a muchos (many-to-many) entre Podcast y Author.
from api import Base, podcast_authors


# Definición de la clase Author
class Author(Base):
    __tablename__ = "authors"  # Define el nombre de la tabla en la base de datos.

    # Definición de columnas
    # Las columnas se definen utilizando Mapped, lo que indica que estas son columnas de mapeo de la base de datos.
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    nationality: Mapped[str]

    # Relación muchos a muchos (many-to-many)
    """
    podcasts: Este es el atributo que define la relación muchos a muchos entre Author y Podcast
    La relación es bidireccional, lo que significa que desde un autor se puede acceder a los podcasts en los que ha participado, y desde un podcast se puede acceder a sus autores
    
    relationship: Función de SQLAlchemy usada para definir cómo las tablas están relacionadas
    En este caso se está indicando que un autor puede estar relacionado con muchos podcasts
    
    secondary=podcast_authors: Esta es la tabla intermedia podcast_authors
    Es la que conecta Author con Podcast en una relación de muchos a muchos
    
    back_populates="authors": Esto indica que en el modelo Podcast, hay un atributo authors que apunta de vuelta a los autores relacionados con ese podcast
    Establece una relación bidireccional entre Author y Podcast
    """
    podcasts: Mapped[List["Podcast"]] = relationship(
        secondary=podcast_authors, back_populates="authors"
    )
