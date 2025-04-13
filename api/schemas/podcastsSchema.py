# Importaciones

from typing import Union, List  # Indica que un campo puede ser de uno o varios tipos.

# BaseModel: Todos los esquemas deben heredar de esta clase.
# ConfigDict: Configuraciones adicionales para el esquema.
from pydantic import BaseModel, ConfigDict

# Definición de esquemas

# Esquema base que define los campos comunes para la creación o actualización de un podcasts.
# Este esquema no define un id porque no es necesario para la creación o actualización de un podcasts.
# Simplemente es una base para los otros esquemas.
class PodcastBaseSchema(BaseModel):
    title: str
    description: str
    url: str
    category_id: int

# Esquema utilizado para la actualización de podcasts.
class PodcastUpdateSchema(BaseModel):
    title: Union[str, None] = None # Campo opcional de tipo texto
    description: Union[str, None] = None # Campo opcional de tipo texto
    url: Union[str, None] = None # Campo opcional de tipo texto


# Hereda de AuthorBase y añade el campo id usado para la respuesta cuando se recupera información de un autor
class PodcastSchema(PodcastBaseSchema):
    id: int
    
    # Esta configuración indica a Pydantic que mapee los atributos del modelo (en lugar de los campos definidos en el esquema) a los atributos de los objetos.
    model_config = ConfigDict(from_attributes=True)


# AuthorBase y Author  son esquemas para representar a los autores de los podcasts.
class AuthorBase(BaseModel):
    id: int

class Author(AuthorBase):
    name: str
    nationality: str

# Este esquema se utiliza cuando se crean o asocian autores a un podcast. Recibe una lista de autores (solo con sus id).
class PodcastAuthorCreateSchema(BaseModel):
    authors: List[AuthorBase]

# Este esquema se utiliza cuando se crea un podcast, con la diferencia de que incluye la lista de autores. Los autores se pasan como una lista de objetos AuthorBase, representando los id de los autores.
class PodcastCreateSchema(PodcastBaseSchema):
    authors: List[AuthorBase]
    
# La diferencia entre estos dos últimos es que PodcastAuthorCreateSchema asocia autores a podcasts ya creados y PodcastCreateSchema se usa cuando creamos un podcasts desde 0 y necesitamos asignarles un autor

# Este esquema es una versión extendida de PodcastSchema, en la cual se incluyen los autores del podcast. Se utiliza cuando necesitas devolver información completa de los autores asociados al podcast.
class PodcastAuthorsSchema(PodcastSchema):
    authors: List[Author]

# Este esquema extiende Author y agrega una lista de podcasts asociados al autor. Se utiliza para mostrar todos los podcasts en los que un autor ha participado.
class AuthorPodcastsSchema(Author):
    podcasts: List[PodcastSchema]
