from typing import Union
from pydantic import BaseModel, ConfigDict

# Esquemas Categoría

class AuthorBase(BaseModel):
    name: str
    nationality: str

class AuthorCreateSchema(AuthorBase):
    pass

class AuthorUpdateSchema(BaseModel):
    name: Union[str, None] = None
    nationality: Union[str, None] = None

class AuthorSchema(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
