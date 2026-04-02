from pydantic import BaseModel


class ShoppingListItem(BaseModel):
    ingredient: str
    recipes: list[str]


class ShoppingListBase(BaseModel):
    items: list[ShoppingListItem]
