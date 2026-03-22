from sqlalchemy import Integer, Table, Column, ForeignKey
from app.core.database import Base

recipe_ingredient = Table(
    "recipe_shoppinglist",
    Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipes.id"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredients.id"), primary_key=True),
)