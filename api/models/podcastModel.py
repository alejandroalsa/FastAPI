# Importaciones

# List de typing es utilizado para indicar que el atributo authors sera una lista de objetos Author
from typing import List

# Tipos de datos que se utilizan para definir las columnas en SQLAlchemy.
from sqlalchemy import Integer, String, ForeignKey

# Herramientas de SQLAlchemy que permiten establecer las relaciones y columnas en el modelo.
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column

# Base: Para definir el modelo, ya definida en el archivo /database/database.py
# podcast_authors: Es la tabla intermedia, usada para la relación muchos a muchos (many-to-many) entre Podcast y Author.
from api import Base, podcast_authors

# Author: El modelo Author que se importa para poder establecer la relación.
from api.models.authorModel import Author


# Definición de la clase Podcast
class Podcast(Base):
    __tablename__ = "podcasts"  # Define el nombre de la tabla en la base de datos.

    # Definición de columnas
    # Las columnas se definen utilizando Mapped, lo que indica que estas son columnas de mapeo de la base de datos.
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    url: Mapped[str]

    # Relación One-To-Many (Uno a Muchos) con Category
    # category_id: Esta columna define una relación de uno a muchos con la tabla categories. Un podcast puede pertenecer a una categoría, por lo que la columna category_id es una clave foránea que referencia la columna id de la tabla categories.
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    # Relación muchos a muchos (many-to-many)
    """
    authors: Este es el atributo que define la relación muchos a muchos entre Author y Podcast
    La relación es bidireccional, lo que significa que desde un autor se puede acceder a los podcasts en los que ha participado, y desde un podcast se puede acceder a sus autores
    
    relationship: Función de SQLAlchemy usada para definir cómo las tablas están relacionadas
    En este caso se está indicando que un autor puede estar relacionado con muchos podcasts
    
    secondary=podcast_authors: Esta es la tabla intermedia podcast_authors
    Es la que conecta Author con Podcast en una relación de muchos a muchos
    
    back_populates="authors": Esto indica que en el modelo Author, hay un atributo podcasts que apunta de vuelta a los podcasts relacionados con ese author
    Establece una relación bidireccional entre Author y Podcast
    """
    authors: Mapped[List["Author"]] = relationship(
        secondary=podcast_authors, back_populates="podcasts"
    )
