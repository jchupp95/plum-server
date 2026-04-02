from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.menu import MenuBase, MenuRead
import app.crud.menu as crud

router = APIRouter()


@router.post("/", response_model=MenuBase)
def create_menu(menu_name: str, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_by_name(db, menu_name)
    if db_menu:
        raise HTTPException(status_code=400, detail="Menu already registered")
    return crud.create_menu(db, menu_name)


@router.get("/current", response_model=MenuRead)
def read_current_menu(db: Session = Depends(get_db)):
    db_menu = crud.get_current_menu(db)
    if not db_menu:
        raise HTTPException(status_code=404, detail="Current menu not found")
    return db_menu


@router.get("/{menu_id}", response_model=MenuRead)
def read_menu(menu_id: int, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return db_menu


@router.get("/", response_model=list[MenuRead])
def read_menus(db: Session = Depends(get_db)):
    menus = crud.get_menus(db)
    return menus


@router.put("/{menu_id}/recipes", response_model=MenuRead)
def update_menu_recipes(
    menu_id: int, recipe_ids: list[int], db: Session = Depends(get_db)
):
    db_menu = crud.update_menu_items(db, menu_id, recipe_ids)
    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return db_menu


@router.delete("/{menu_id}", response_model=bool)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    success = crud.delete_menu(db, menu_id)
    if not success:
        raise HTTPException(status_code=404, detail="Menu not found")
    return success
