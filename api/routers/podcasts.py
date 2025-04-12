from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from api import podcastController, get_db
from api import PodcastSchema
from api import PodcastCreateSchema
from api import PodcastUpdateSchema
from api import PodcastAuthorsSchema, PodcastAuthorCreateSchema

# Enrutador donde definiremos los endpoints

router = APIRouter()

@router.get("/", response_model=list[PodcastSchema])
async def read_podcasts(db: Session = Depends(get_db)):
  podcasts=podcastController.get_podcasts(db)
  
  if podcasts == None:
    raise HTTPException(status_code=503, detail="DB Unavailable")
  return podcasts

@router.get("/{podcast_id}", response_model=PodcastSchema)
async def read_podcasts(podcast_id:int, db: Session = Depends(get_db)):
  podcast = podcastController.get_podcast(db, podcast_id)
  if podcast == None:
    raise HTTPException(status_code=404, detail="Podcast not found")
  return podcast

@router.get("/{podcast_id}/authors", response_model=PodcastAuthorsSchema)
async def read_podcasts(podcast_id:int, db: Session = Depends(get_db)):
  podcast = podcastController.get_podcast(db, podcast_id)
  if podcast == None:
    raise HTTPException(status_code=404, detail="Podcast not found")
  return podcast

@router.post("/", response_model=PodcastSchema)
async def write_podcasts(podcast:PodcastCreateSchema, db: Session = Depends(get_db)):
  podcastResult = podcastController.write_podcast(db, podcast)
  return podcastResult

@router.post("/{podcast_id}/authors", response_model=PodcastAuthorsSchema)
async def write_podcasts(podcast_id:int, podcast: PodcastAuthorsSchema, db: Session = Depends(get_db)):
  podcastResult = podcastController.write_podcast(db, podcast)
  if podcastResult == None:
    raise HTTPException(status_code=404, detail="Duplicated author-podcast")
  return podcastResult

@router.put("/{podcast_id}", response_model=PodcastSchema)
async def update_podcasts(podcast_id:int, podcast:PodcastUpdateSchema, db: Session = Depends(get_db)):
  podcastResult = podcastController.update_podcast(db, podcast_id, podcast)
  
  if podcastResult == None:
    raise HTTPException(status_code=404, detail="Podcast not found")
  return podcastResult

@router.delete("/{podcast_id}", response_model=list[PodcastSchema])
async def delete_podcasts(podcast_id:int, db: Session = Depends(get_db)):
  podcast = podcastController.delete_podcast(db, podcast_id)
  
  if podcast  == None:
    raise HTTPException(status_code=404, detail="Podcast not found")
   
  return podcast

@router.delete("/{podcast_id}/authors", response_model=PodcastAuthorsSchema)
async def delete_podcasts(podcast_id:int, podcast: PodcastAuthorCreateSchema, db: Session = Depends(get_db)):
  podcast = podcastController.delete_podcast(db, podcast_id, podcast)
  
  if podcast  == None:
    raise HTTPException(status_code=404, detail="Podcast not found")

  return podcast
