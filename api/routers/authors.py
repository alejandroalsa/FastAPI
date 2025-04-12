from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from api import authorController, get_db
from api import AuthorSchema
from api import AuthorCreateSchema
from api import AuthorUpdateSchema
from api import AuthorPodcastsSchema

# Enrutador donde definiremos los endpoints

router = APIRouter()

@router.get("/", response_model=list[AuthorSchema])
async def read_authors(db: Session = Depends(get_db)):
  authors=authorController.get_authors(db)
  
  if authors == None:
    raise HTTPException(status_code=503, detail="DB Unavailable")
  return authors

@router.get("/{author_id}", response_model=AuthorSchema)
async def read_authors(author_id:int, db: Session = Depends(get_db)):
  author = authorController.get_author(db, author_id)
  if author == None:
    raise HTTPException(status_code=404, detail="Author not found")
  return author

@router.get("/{author_id}/podcasts", response_model=AuthorPodcastsSchema)
async def read_authors(author_id:int, db: Session = Depends(get_db)):
  author = authorController.get_author(db, author_id)
  if author == None:
    raise HTTPException(status_code=404, detail="Author not found")
  return author

@router.post("/", response_model=AuthorSchema)
async def write_author(author:AuthorCreateSchema, db: Session = Depends(get_db)):
  authorResult = authorController.write_author(db, author)
  return authorResult

@router.put("/{author_id}", response_model=AuthorSchema)
async def update_authors(author_id:int, author:AuthorUpdateSchema, db: Session = Depends(get_db)):
  authorResult = authorController.update_author(db, author_id, author)
  
  if authorResult == None:
    raise HTTPException(status_code=404, detail="Author not found")
  return authorResult

@router.delete("/{author_id}", response_model=list[AuthorSchema])
async def delete_author(author_id:int, db: Session = Depends(get_db)):
  author = authorController.delete_author(db, author_id)
  
  if author  == None:
    raise HTTPException(status_code=404, detail="Author not found")
   
  return author
