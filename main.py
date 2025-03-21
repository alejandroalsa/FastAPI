from fastapi import FastAPI, Response, status
from fooddata import FoodData
from models import Ingrediente

# Objeto para trabajar con los datos de prueba
food = FoodData()

tags_metadata = [
    {
        "name": "Ingredientes",
        "description": "Operaciones relacionadas con el CRUD de ingredientes",
    },
    {
        "name": "Platos",
        "description": "Operaciones relacionadas con el CRUD de platos",
    }
]

# Objeto app de tipo FastAPI
app = FastAPI(
    title="DIWES ADVANCED",
    description="API de DIWES ADVANCED",
    summary="Esta es la API privada de DIWES ADVANCED orientada al uso exclusivo del software",
    version="1.0.0",
    terms_of_service="https://diwesadvanced.com/api/terms",
    contact={
        "name": "DIWES ADVANCED",
        "url": "https://support.diwesadvanced.com",
        "email": "api@diwesadvanced.com",
    },
    openapi_tags=tags_metadata,
)


# Entrada GET http://localhost:8000/ ó Endpoint GET /
@app.get("/")
def read_root():
    return {"api": "DIWES ADVANCED API"}


# Ingredientes
# Entrada GET http://localhost:8000/ingredientes
@app.get("/ingredientes", tags=["ingredientes"])
async def read_ingredientes(skip:int=0,total:int=10, all: bool | None = None):
    # await pedir datos
    
    if(all):
        return await food.get_allIngredientes()
    else:
        return await food.get_ingredientes(skip,total)


@app.get("/ingredientes/{ingrediente_id}", tags=["ingredientes"], status_code=status.HTTP_200_OK)
async def red_ingrediente(ingrediente_id: int,response: Response):
    ingrediente = await food.get_ingrediente(ingrediente_id)
    # Si encontramos el ingrediente lo devolvemos
    if (ingrediente):
        return ingrediente
    # Si el ingrediente es nulo
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Error, el ID: " + str(ingrediente_id) + " no se ha encontrado"}


@app.post("/ingredientes", tags=["ingredientes"])
async def write_ingredients(ingrediente:Ingrediente):
    return await food.write_ingrediente(ingrediente)

@app.put("/ingredientes/{ingrediente_id}", tags=["ingredientes"])
async def update_ingredients(ingrediente_id:int,ingrediente:Ingrediente):
    return await food.update_ingrediente(ingrediente_id, ingrediente)

# Platos

@app.get("/platos", tags=["platos"])
async def read_platos(skip:int=0,total:int=2,all:bool | None = None):
    
    if(all):
        return await food.get_allPlatos()
    else:
        return await food.get_platos(skip,total)
    
@app.get("/platos/{plato_id}", tags=["platos"], status_code=status.HTTP_200_OK)
async def read_plato(plato_id:int, response:Response):
    plato = await food.get_plato(plato_id)
    if(plato):
        return plato
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Error, el ID: " + str(plato_id) + " no se ha encontrado"}

@app.get("/platos/{palto_id}/ingredientes/{ingrediente_id}", tags=["platos", "ingredientes"], status_code=status.HTTP_200_OK)
async def red_platoIngrediente(plato_id:int, ingrediente_id:int, response:Response):
    
    ingrediente = await food.get_ingredientePlato(plato_id, ingrediente_id)
    if(ingrediente):
        return ingrediente
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"Error, el ID: " + str(ingrediente_id) + " no se ha encontrado"}
