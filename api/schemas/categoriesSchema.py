from typing import Union, List
from pydantic import BaseModel, ConfigDict

from api import PodcastSchema

# Esquemas Categoría

class CategoryBase(BaseModel):
    name: str

class CategoryCreateSchema(CategoryBase):
    pass

class CategorySchema(CategoryBase):
    id: int
    
class CategoryPodcastsSchema(CategoryBase):
    id: int
    podcasts: List[PodcastSchema]

    model_config = ConfigDict(from_attributes=True)



