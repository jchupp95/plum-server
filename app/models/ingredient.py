from typing import List, TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.recipe import Recipe
from app.core.database import Base
  

class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)

    recipes: Mapped[List["Recipe"]] = relationship(
        secondary="recipe_shoppinglist",
        back_populates="shopping_list"
    )