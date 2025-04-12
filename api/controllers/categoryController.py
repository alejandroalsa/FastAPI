from sqlalchemy import select
from api import CategoryModel
from api import CategoryCreateSchema
from sqlalchemy.exc import NoResultFound, OperationalError, IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

# Controller de categorias
def get_categories(db):
  try:
    #Crearia la consulta SELECT * from categories
    stmt = select(CategoryModel)
    #Lista de categorias
    result = db.scalars(stmt)
    categories=result.all()
  
  except OperationalError:
    categories = None
  
  return categories

def get_category(db, category_id:int):
  try:
    #Crearia la consulta SELECT * from categories
    result = db.execute(select(CategoryModel).filter_by(id=category_id))
    categoryModel = result.scalar_one()   
  except NoResultFound:
    categoryModel = None

  #Lista de categorias
  return categoryModel


def write_category(db, category:CategoryCreateSchema):
  # Creamos el modelo ORM en base al schema
  categoryModel = CategoryModel(name=category.name)

  # Insertamos en la BD
  db.add(categoryModel)
  db.commit()
  db.refresh(categoryModel)
  return categoryModel

def update_category(db, category_id:int, category:CategoryCreateSchema):
  
  try:
    # Select del modelo ORM
    result = db.execute(select(CategoryModel).filter_by(id=category_id))
    categoryModel = result.scalar_one()
    # Modificamos el name
    categoryModel.name=category.name

    # Actualizamos en la BD
    db.add(categoryModel)
    db.commit()
    db.refresh(categoryModel)
  
  except NoResultFound:
    categoryModel = None
  
  return categoryModel

def delete_category(db, category_id:int):
  
  try:
    # Select del modelo ORM
    category = db.get(CategoryModel,category_id)

    # Eliminamos en la BD
    db.delete(category)
    db.commit()
    category = get_categories(db)
  except UnmappedInstanceError:
    category = None
  except IntegrityError:
    category = -1
  return category
