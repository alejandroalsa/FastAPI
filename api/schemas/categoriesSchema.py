# Importaciones

from typing import Union, List  # Indica que un campo puede ser de uno o varios tipos.

# BaseModel: Todos los esquemas deben heredar de esta clase.
# ConfigDict: Configuraciones adicionales para el esquema.
from pydantic import BaseModel, ConfigDict

# Esquema utilizado para validar y serializar los datos de un podcast, que se va a usar en el esquema CategoryPodcastsSchema.
from api import PodcastSchema

# Definición de esquemas

# Esquema base que define los campos comunes para la creación o actualización de una categoría.
# Este esquema no define un id porque no es necesario para la creación o actualización de una categoría.
# Simplemente es una base para los otros esquemas.
class CategoryBase(BaseModel):
    name: str

# Hereda de CategoryBase y no agrega ni modifica ningún campo.
# Se utiliza específicamente para la creación de categorías, y el hecho de que no se agregue nada más significa que se requiere el nombre y la nacionalidad para crear una nueva categoría.
class CategoryCreateSchema(CategoryBase):
    pass

# Hereda de CategoryBase y añade el campo id usado para la respuesta cuando se recupera información de una categoría
class CategorySchema(CategoryBase):
    id: int
    
# Un esquema especializado que incluye no solo la categoría, sino también los podcasts relacionados con esa categoría.
class CategoryPodcastsSchema(CategoryBase):
    id: int
    
    # Una lista de podcasts asociados a la categoría. Cada elemento de esta lista es validado utilizando el esquema PodcastSchema.
    podcasts: List[PodcastSchema]

    # Esta configuración indica a Pydantic que mapee los atributos del modelo (en lugar de los campos definidos en el esquema) a los atributos de los objetos.
    model_config = ConfigDict(from_attributes=True)



