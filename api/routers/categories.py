from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from api import categoryController, get_db
from api import CategorySchema
from api import CategoryCreateSchema
from api import CategoryPodcastsSchema
from api.controllers import securityController
from api.schemas.usersSchema import UserSchema

# Enrutador donde definiremos los endpoints

router = APIRouter()

@router.get("/", response_model=list[CategorySchema])
async def read_categories(db: Session = Depends(get_db)):
  categories=categoryController.get_categories(db)
  
  if categories == None:
    raise HTTPException(status_code=503, detail="DB Unavailable")
  return categories

@router.get("/{category_id}", response_model=CategorySchema)
async def read_categories(category_id:int, db: Session = Depends(get_db)):
  category = categoryController.get_category(db, category_id)
  if category == None:
    raise HTTPException(status_code=404, detail="Category not found")
  return category

@router.get("/{category_id}/podcasts", response_model=CategoryPodcastsSchema)
async def read_categories(category_id:int, db: Session = Depends(get_db)):
  category = categoryController.get_category(db, category_id)
  if category == None:
    raise HTTPException(status_code=404, detail="Category not found")
  return category

@router.post("/", response_model=CategorySchema)
async def write_categories(category:CategoryCreateSchema, db: Session = Depends(get_db)):
  categoryResult = categoryController.write_category(db, category)
  return categoryResult

@router.put("/{category_id}", response_model=CategorySchema)
async def update_categories(category_id:int, category:CategoryCreateSchema, db: Session = Depends(get_db)):
  categoryResult = categoryController.update_category(db, category_id, category)
  
  if categoryResult == None:
    raise HTTPException(status_code=404, detail="Category not found")
  return categoryResult

@router.delete("/{category_id}", response_model=list[CategorySchema])
async def delete_category(category_id: int, db: Session = Depends(get_db),
user: UserSchema = Depends(securityController.check_token)):

    categories = categoryController.delete_category(db, category_id)
    if categories == None:
        raise HTTPException(status_code=404, detail="Category not found")
    elif categories == -1:
        raise HTTPException(status_code=404, detail="Podcasts not empty")
    return categories
