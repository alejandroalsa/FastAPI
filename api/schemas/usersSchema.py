# Importaciones

from typing import Union, List  # Indica que un campo puede ser de uno o varios tipos.

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    name: str
    email: str
    active: bool

class UserInSchema(BaseModel):
    username: str
    password: str

class UserCreateSchema(UserBase):
    password: str
    
class UserSchema(UserBase):
    id: int
