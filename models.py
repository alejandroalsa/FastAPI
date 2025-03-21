from pydantic import BaseModel


class Ingrediente(BaseModel):
    nombre: str
    calorias: int
    carbohidratos: float | None = None
    proteinas: float | None = None
    grases: float | None = None
    fibra: float | None = None
