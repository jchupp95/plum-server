from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .recipe import RecipeSimpleRead

from pydantic import BaseModel


class IngredientBase(BaseModel):
    name: str


class IngredientCreate(IngredientBase):
    pass


class IngredientRead(IngredientBase):
    id: int
    recipes: list["RecipeSimpleRead"]

    class Config:
        from_attributes = True


from .recipe import RecipeSimpleRead  # noqa: E402

IngredientRead.model_rebuild()
