from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.ingredient import IngredientRead, IngredientCreate
import app.crud.ingredient as crud

router = APIRouter()


@router.post("/", response_model=IngredientRead)
def create_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    db_ingredient = crud.get_ingredient_by_name(db, ingredient.name)
    if db_ingredient:
        raise HTTPException(status_code=400, detail="Ingredient already registered")
    return crud.create_ingredient(db, ingredient)


@router.get("/{ingredient_id}", response_model=IngredientRead)
def read_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    db_ingredient = crud.get_ingredient(db, ingredient_id)
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return db_ingredient
