from sqlalchemy import select
from api import PodcastModel
from api import PodcastCreateSchema
from api import PodcastUpdateSchema, PodcastAuthorCreateSchema
from api import AuthorModel
from sqlalchemy.exc import NoResultFound, OperationalError, IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

# Controller de categorias
def get_podcasts(db):
  try:
    #Crearia la consulta SELECT * from podcasts
    stmt = select(PodcastModel)
    #Lista de categorias
    result = db.scalars(stmt)
    podcasts=result.all()
  
  except OperationalError:
    podcasts = None
  
  return podcasts

def get_podcast(db, podcast_id:int):
  try:
    #Crearia la consulta SELECT * from podcasts
    result = db.execute(select(PodcastModel).filter_by(id=podcast_id))
    podcastModel = result.scalar_one()   
  except NoResultFound:
    podcastModel = None

  #Lista de categorias
  return podcastModel


def write_podcast(db, podcast:PodcastCreateSchema):
  # Creamos el modelo ORM en base al schema
  podcastModel = PodcastModel(title=podcast.title, description=podcast.description, url=podcast.url, category_id=podcast.category_id)
  
  # Recorremos los autores que no llegan en el JSON
  for author in podcast.authors:
    authorModel = db.query(AuthorModel).filter(AuthorModel.id == author.id).first()
    podcastModel.authors.append(authorModel)

  # Insertamos en la BD
  db.add(podcastModel)
  db.commit()
  db.refresh(podcastModel)
  return podcastModel

def write_podcastauthors(db, podcast_id: int, podcast:PodcastAuthorCreateSchema):

  try:
    podcastModel = db.query(PodcastModel).filter(PodcastModel.id == podcast_id).first()
    # Recorremos los autores que no llegan en el JSON
    for author in podcast.authors:
      authorModel = db.query(AuthorModel).filter(AuthorModel.id == author.id).first()
      podcastModel.authors.append(authorModel)

    # Insertamos en la BD
    db.add(podcastModel)
    db.commit()
    db.refresh(podcastModel)
  except IntegrityError:
    podcastModel = None
  return podcastModel
  


def update_podcast(db, podcast_id:int, podcast:PodcastUpdateSchema):
  
  try:
    # Select del modelo ORM
    result = db.execute(select(PodcastModel).filter_by(id=podcast_id))
    podcastModel = result.scalar_one()

    for key, value in podcast:
      if value is not None: setattr(podcastModel, key, value)

    # Actualizamos en la BD
    db.commit()
    db.refresh(podcastModel)
  
  except NoResultFound:
    podcastModel = None
  
  return podcastModel

def delete_podcast(db, podcast_id:int):
  
  try:
    # Select del modelo ORM
    podcast = db.get(PodcastModel,podcast_id)

    # Eliminamos en la BD
    db.delete(podcast)
    db.commit()
    podcast = get_podcasts(db)
  except UnmappedInstanceError:
    podcast = None
  return podcast

def delete_podcastauthors(db, podcast_id: int, podcast: PodcastAuthorCreateSchema):
    try:
        # Buscamos el podcast
        podcastModel = db.query(PodcastModel).filter(PodcastModel.id == podcast_id).first()
        # Recorremos todos los authors si existen y los añadimos
        for author in podcast.authors:
            authorModel = db.query(AuthorModel).filter(AuthorModel.id == author.id).first()
            podcastModel.authors.remove(authorModel)
        # Commit
        db.commit()
        db.refresh(podcastModel)
    except UnmappedInstanceError:
        podcastModel = None
    except ValueError:
        podcastModel = None
    return podcastModel