from sqlalchemy import Integer, Table, Column, ForeignKey
from app.core.database import Base

menu_recipe = Table(
    "menu_recipe",
    Base.metadata,
    Column("menu_id", Integer, ForeignKey("menus.id"), primary_key=True),
    Column("recipe_id", Integer, ForeignKey("recipes.id"), primary_key=True),
)
