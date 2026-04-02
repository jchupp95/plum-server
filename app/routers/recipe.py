from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.recipe import RecipeRead, RecipeCreate, RecipeOverview
import app.crud.recipe as crud

router = APIRouter()


@router.post("/", response_model=RecipeRead)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = crud.get_recipe_by_name(db, recipe.name)
    if db_recipe:
        raise HTTPException(status_code=400, detail="Recipe already exists")
    return crud.create_recipe(db, recipe)


@router.get("/", response_model=list[RecipeRead])
def read_recipes(db: Session = Depends(get_db)):
    return crud.get_recipes(db)


@router.get("/overview", response_model=list[RecipeOverview])
def read_recipes_overview(db: Session = Depends(get_db)):
    return crud.get_recipes(db)


@router.get("/{recipe_id}", response_model=RecipeRead)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = crud.get_recipe(db, recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe


@router.delete("/{recipe_id}", response_model=bool)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    success = crud.delete_recipe(db, recipe_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return success
