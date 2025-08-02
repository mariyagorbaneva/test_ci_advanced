from pydantic import BaseModel
from typing import Optional
# Блюдо
class RecipeIn(BaseModel):
    title: str
    cooking_time: float
    ingredients: str
    description: Optional[str] = None

class RecipeOut(BaseModel):
    recipe_id: int
    title: str
    views: int
    cooking_time: float
    ingredients: str
    description: Optional[str] = None

    class Config:
        from_attributes = True
