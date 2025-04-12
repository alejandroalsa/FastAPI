from sqlalchemy import select
from api import AuthorModel
from api import AuthorCreateSchema
from api import AuthorUpdateSchema
from sqlalchemy.exc import NoResultFound, OperationalError
from sqlalchemy.orm.exc import UnmappedInstanceError

# Controller de categorias
def get_authors(db):
  try:
    #Crearia la consulta SELECT * from authors
    stmt = select(AuthorModel)
    #Lista de categorias
    result = db.scalars(stmt)
    authors=result.all()
  
  except OperationalError:
    authors = None
  
  return authors

def get_author(db, author_id:int):
  try:
    #Crearia la consulta SELECT * from authors
    result = db.execute(select(AuthorModel).filter_by(id=author_id))
    authorModel = result.scalar_one()   
  except NoResultFound:
    authorModel = None

  #Lista de categorias
  return authorModel


def write_author(db, author:AuthorCreateSchema):
  # Creamos el modelo ORM en base al schema
  authorModel = AuthorModel(name=author.name, nationality=author.nationality)

  # Insertamos en la BD
  db.add(authorModel)
  db.commit()
  db.refresh(authorModel)
  return authorModel

def update_author(db, author_id:int, author:AuthorUpdateSchema):
  
  try:
    # Select del modelo ORM
    result = db.execute(select(AuthorModel).filter_by(id=author_id))
    authorModel = result.scalar_one()

    for key, value in author:
      if value is not None: setattr(authorModel, key, value)

    # Actualizamos en la BD
    db.commit()
    db.refresh(authorModel)
  
  except NoResultFound:
    authorModel = None
  
  return authorModel

def delete_author(db, author_id:int):
  
  try:
    # Select del modelo ORM
    author = db.get(AuthorModel,author_id)

    # Eliminamos en la BD
    db.delete(author)
    db.commit()
    author = get_authors(db)
  except UnmappedInstanceError:
    author = None
  return author
