from sqlalchemy.orm import Session
from app.models.menu import Menu
from app.models.recipe import Recipe
from app.schemas.menu import MenuBase


def get_menu(db: Session, menu_id: int):
    return db.query(Menu).filter(Menu.id == menu_id).first()


def get_current_menu(db: Session):
    return db.query(Menu).filter(Menu.is_current).first()


def get_menus(db: Session):
    return db.query(Menu).filter(~Menu.is_current).all()


def create_menu(db: Session, menu: MenuBase):
    db_menu = Menu(name=menu.name)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def update_menu_items(db: Session, menu_id: int, recipes: list[int]):
    db_menu = get_menu(db, menu_id)
    if not db_menu:
        return None

    # load Recipe objects for relationship assignment
    db_recipes = db.query(Recipe).filter(Recipe.id.in_(recipes)).all()

    db_menu.recipes = db_recipes
    db.commit()
    db.refresh(db_menu)
    return db_menu
