from sqlalchemy.orm import Session, selectinload

from app.models.ingredient import Ingredient
from app.schemas.shopping_list import ShoppingListBase, ShoppingListItem


def get_shopping_list(db: Session) -> ShoppingListBase:
    ingredients = (
        db.query(Ingredient)
        .options(selectinload(Ingredient.recipes))
        .order_by(Ingredient.name)
        .all()
    )

    items = [
        ShoppingListItem(
            ingredient=ingredient.name,
            recipes=[recipe.name for recipe in ingredient.recipes],
        )
        for ingredient in ingredients
    ]

    return ShoppingListBase(items=items)
