from typing import List, TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from .ingredient import Ingredient
    from .menu import Menu


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    image: Mapped[str] = mapped_column(String)
    ingredients: Mapped[str] = mapped_column(String)
    instructions: Mapped[str] = mapped_column(String)

    shopping_list: Mapped[List["Ingredient"]] = relationship(
        secondary="recipe_shoppinglist", back_populates="recipes"
    )

    menus: Mapped[List["Menu"]] = relationship(
        "Menu",
        secondary="menu_recipe",
        back_populates="recipes",
    )
