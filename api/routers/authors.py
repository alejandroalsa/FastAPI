# Importaciones

# Depends: Se utiliza para inyectar dependencias, como la base de datos.
# APIRouter: Crea un enrutador que contiene las rutas para el modelo Author.
# HTTPException: Para lanzar errores HTTP en caso de que algo falle.
from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy.orm import Session # Interacción con la base de datos

# Esquemas de Pydantic para validar los datos que se envían/reciben
# get_db: Es una dependencia que gestiona la conexión a la base de datos.
from api import authorController, get_db, AuthorSchema, AuthorCreateSchema, AuthorUpdateSchema, AuthorPodcastsSchema

# Creación del enrutador
router = APIRouter()

# Rutas

# Obtener todos los autores
# Ruta HTTP "/" con el método GET
# response_model=list[AuthorSchema]: Le indica a FastAPI que la respuesta debe ser una lista de objetos que siguen el esquema AuthorSchema
@router.get("/", response_model=list[AuthorSchema])
# Se define una función asíncrona usando una inyección de dependencias para obtener una sesión de la BD
async def read_authors(db: Session = Depends(get_db)):
  
  # Llama a la función get_authors del controlador authorController, pasándole la sesión de la base de datos
  # Esta función recupera todos los autores de la base de datos.
  authors=authorController.get_authors(db)
  
  # Si no se obtienen datos (es decir, authors es None), lanza un error HTTP 503
  if authors == None:
    raise HTTPException(status_code=503, detail="DB Unavailable")
  
  # Si todo ha ido bien, devuelve la lista de autores como respuesta JSON.
  return authors

# Obtener un autor por su ID
# Ruta HTTP "/{author_id}" donde añadimos un ID con el método GET
@router.get("/{author_id}", response_model=AuthorSchema)
# Se define una función asíncrona usando una inyección de dependencias para obtener una sesión de la BD, ademas pasamos el valor de author_id a un entero
async def read_authors(author_id:int, db: Session = Depends(get_db)):
  
  # Llama a la función get_author del controlador authorController, pasándole la sesión de la base de datos y el ID del autor
  author = authorController.get_author(db, author_id)
  
  # Si no se obtienen datos (es decir, authors es None), lanza un error HTTP 404
  if author == None:
    raise HTTPException(status_code=404, detail="Author not found")
  
  # Si todo ha ido bien, devuelve los datos del autor como respuesta JSON.
  return author

# Obtener los podcasts de un autor
# Ruta HTTP "/{author_id}/podcasts" donde añadimos un ID con el método GET
# Devuelve un AuthorPodcastsSchema, que incluye datos del autor y sus podcasts.
@router.get("/{author_id}/podcasts", response_model=AuthorPodcastsSchema)
# Igual que antes, obtenemos author_id e inyectamos la base de datos.
async def read_authors(author_id:int, db: Session = Depends(get_db)):
  
  # Llama a la función get_author del controlador authorController, pasándole la sesión de la base de datos y el ID del autor
  author = authorController.get_author(db, author_id)
  
  # Si no se obtienen datos (es decir, authors es None), lanza un error HTTP 404
  if author == None:
    raise HTTPException(status_code=404, detail="Author not found")
  
  # Si todo ha ido bien, devuelve los datos del autor con la lista de podcasts anidada como respuesta JSON.
  return author

# Crear un nuevo autor
# Ruta HTTP "/" con el método POST
# El modelo de respuesta es un solo AuthorSchema.
@router.post("/", response_model=AuthorSchema)
# Se define una función asíncrona usando una inyección de dependencias para obtener una sesión de la BD y donde le pasamos el schema para validar automáticamente los datos del cuerpo
async def write_author(author:AuthorCreateSchema, db: Session = Depends(get_db)):
  
  # Llama a la función que guarda el nuevo autor en la base de datos.
  authorResult = authorController.write_author(db, author)
  
  # Devuelve el autor creado.
  return authorResult

# Actualizar un autor existente
# Ruta HTTP "/{author_id}" con el método PUT
@router.put("/{author_id}", response_model=AuthorSchema)
# Se define una función asíncrona usando una inyección de dependencias para obtener una sesión de la BD, el ID del autor y donde le pasamos el schema para validar automáticamente los datos del cuerpo
async def update_authors(author_id:int, author:AuthorUpdateSchema, db: Session = Depends(get_db)):
  
  # Llama a la función que actualiza el autor en la base de datos.
  authorResult = authorController.update_author(db, author_id, author)
  
  # Si no se obtienen datos (es decir, author es None), lanza un error HTTP 404
  if authorResult == None:
    raise HTTPException(status_code=404, detail="Author not found")
  
  # Devuelve el autor actualizado.
  return authorResult

# Eliminar un autor
# Ruta HTTP "/{author_id}" con el método DELETE
@router.delete("/{author_id}", response_model=list[AuthorSchema])
# Se define una función asíncrona usando una inyección de dependencias para obtener una sesión de la BD y le pasamos el ID del autor y
async def delete_author(author_id:int, db: Session = Depends(get_db)):
  
  # Llama a la función que elimina el autor en la base de datos.
  author = authorController.delete_author(db, author_id)
  
  # Si no se obtienen datos (es decir, autho es None), lanza un error HTTP 404
  if author  == None:
    raise HTTPException(status_code=404, detail="Author not found")
   
  # Devuelve el autor eliminado
  return author
