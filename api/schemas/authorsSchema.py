# Importaciones

from typing import Union  # Indica que un campo puede ser de uno o varios tipos.

# BaseModel: Todos los esquemas deben heredar de esta clase.
# ConfigDict: Configuraciones adicionales para el esquema.
from pydantic import BaseModel, ConfigDict

# Definición de esquemas

# Esquema base que define los campos comunes para la creación o actualización de un autor.
# Este esquema no define un id porque no es necesario para la creación o actualización de un autor.
# Simplemente es una base para los otros esquemas.
class AuthorBase(BaseModel):
    name: str
    nationality: str

# Hereda de AuthorBase y no agrega ni modifica ningún campo.
# Se utiliza específicamente para la creación de autores, y el hecho de que no se agregue nada más significa que se requiere el nombre y la nacionalidad para crear un nuevo autor.
class AuthorCreateSchema(AuthorBase):
    pass

# Esquema utilizado para la actualización de autores.
class AuthorUpdateSchema(BaseModel):
    name: Union[str, None] = None  # Campo opcional de tipo texto
    nationality: Union[str, None] = None  # Campo opcional de tipo texto

# Hereda de AuthorBase y añade el campo id usado para la respuesta cuando se recupera información de un autor
class AuthorSchema(AuthorBase):
    id: int

    # Esta configuración indica a Pydantic que mapee los atributos del modelo (en lugar de los campos definidos en el esquema) a los atributos de los objetos.
    model_config = ConfigDict(from_attributes=True)
