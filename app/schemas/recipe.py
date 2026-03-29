from typing import TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .ingredient import IngredientBase


class RecipeBase(BaseModel):
    name: str


class RecipeCreate(RecipeBase):
    image: str
    ingredients: str
    instructions: str
    shopping_list: list["IngredientBase"]


class RecipeRead(RecipeBase):
    id: int
    image: str
    ingredients: str
    instructions: str
    shopping_list: list["IngredientBase"]

    class Config:
        from_attributes = True


from .ingredient import IngredientBase  # noqa: E402

RecipeCreate.model_rebuild()
RecipeRead.model_rebuild()
