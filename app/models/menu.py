from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from .recipe import Recipe


class Menu(Base):
    __tablename__ = "menus"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    is_current: Mapped[bool] = mapped_column(default=False)
    recipes: Mapped[List["Recipe"]] = relationship(
        "Recipe",
        secondary="menu_recipe",
        back_populates="menus",
    )
