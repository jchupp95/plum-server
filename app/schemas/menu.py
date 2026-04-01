from typing import TYPE_CHECKING
from pydantic import BaseModel


if TYPE_CHECKING:
    from .recipe import RecipeSimpleRead


class MenuBase(BaseModel):
    name: str


class MenuCreate(MenuBase):
    pass


class MenuRead(MenuBase):
    id: int
    recipes: list["RecipeSimpleRead"] = []


from .recipe import RecipeSimpleRead  # noqa: E402

MenuRead.model_rebuild()
