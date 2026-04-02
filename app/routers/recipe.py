import json
import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import TypeAdapter, ValidationError
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.ingredient import IngredientBase
from app.schemas.recipe import RecipeRead, RecipeCreate, RecipeOverview
import app.crud.recipe as crud

router = APIRouter()
IMAGES_DIR = Path("images")
SHOPPING_LIST_ADAPTER = TypeAdapter(list[IngredientBase])


def parse_shopping_list(shopping_list: str | None) -> list[IngredientBase]:
    if shopping_list is None:
        return []

    try:
        return SHOPPING_LIST_ADAPTER.validate_json(shopping_list)
    except (ValidationError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status_code=422,
            detail="shopping_list must be valid JSON matching IngredientBase[]",
        ) from exc


def save_image(image: UploadFile | None) -> str:
    if image is None or not image.filename:
        return ""

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    image_filename = f"{uuid4()}.png"
    image_path = IMAGES_DIR / image_filename

    try:
        with image_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    finally:
        image.file.close()

    return f"/images/{image_filename}"


def delete_image(image_url: str | None) -> None:
    if not image_url or not image_url.startswith("/images/"):
        return

    image_path = IMAGES_DIR / image_url.removeprefix("/images/")
    if image_path.exists():
        image_path.unlink()


@router.post("/", response_model=RecipeRead)
def create_recipe(
    name: str = Form(...),
    ingredients: str | None = Form(None),
    instructions: str | None = Form(None),
    shopping_list: str | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    db_recipe = crud.get_recipe_by_name(db, name)
    if db_recipe:
        raise HTTPException(status_code=400, detail="Recipe already exists")

    parsed_shopping_list = parse_shopping_list(shopping_list)
    image_url = save_image(image)

    recipe = RecipeCreate(
        name=name,
        image=image_url,
        ingredients=ingredients,
        instructions=instructions or "",
        shopping_list=parsed_shopping_list,
    )
    return crud.create_recipe(db, recipe)


@router.put("/{recipe_id}", response_model=RecipeRead)
def update_recipe(
    recipe_id: int,
    name: str = Form(...),
    ingredients: str = Form(...),
    instructions: str | None = Form(None),
    shopping_list: str | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    db_recipe = crud.get_recipe(db, recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    existing_recipe = crud.get_recipe_by_name(db, name)
    if existing_recipe and existing_recipe.id != recipe_id:
        raise HTTPException(status_code=400, detail="Recipe already exists")

    parsed_shopping_list = parse_shopping_list(shopping_list)
    old_image_url = db_recipe.image
    image_url = save_image(image) or old_image_url

    recipe = RecipeCreate(
        name=name,
        image=image_url,
        ingredients=ingredients,
        instructions=instructions or "",
        shopping_list=parsed_shopping_list,
    )
    updated_recipe = crud.update_recipe(db, recipe_id, recipe)
    if not updated_recipe:
        delete_image(image_url)
        raise HTTPException(status_code=404, detail="Recipe not found")

    if image is not None and image.filename:
        delete_image(old_image_url)
    return updated_recipe


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
    db_recipe = crud.get_recipe(db, recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    success = crud.delete_recipe(db, recipe_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recipe not found")

    delete_image(db_recipe.image)
    return success
