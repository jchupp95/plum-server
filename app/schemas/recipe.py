from typing import TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .ingredient import IngredientBase


class RecipeBase(BaseModel):
    name: str


class RecipeOverview(RecipeBase):
    id: int
    image: str

    class Config:
        from_attributes = True


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


class RecipeSimpleRead(RecipeBase):
    id: int


from .ingredient import IngredientBase  # noqa: E402

RecipeCreate.model_rebuild()
RecipeRead.model_rebuild()
