from sqlalchemy.orm import Session
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient
from app.schemas.recipe import RecipeCreate


def get_recipe(db: Session, recipe_id: int):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()


def get_recipe_by_name(db: Session, name: str):
    return db.query(Recipe).filter(Recipe.name == name).first()


def get_recipes(db: Session):
    return db.query(Recipe).all()


def build_shopping_list(db: Session, recipe: RecipeCreate) -> list[Ingredient]:
    ingredient_names: list[str] = []
    for ingredient in recipe.shopping_list:
        if ingredient.name not in ingredient_names:
            ingredient_names.append(ingredient.name)

    if not ingredient_names:
        return []

    existing_ingredients = (
        db.query(Ingredient).filter(Ingredient.name.in_(ingredient_names)).all()
    )
    ingredients_by_name = {
        ingredient.name: ingredient for ingredient in existing_ingredients
    }

    for ingredient_name in ingredient_names:
        if ingredient_name not in ingredients_by_name:
            new_ingredient = Ingredient(name=ingredient_name)
            db.add(new_ingredient)
            db.flush()
            ingredients_by_name[ingredient_name] = new_ingredient

    return [ingredients_by_name[name] for name in ingredient_names]


def create_recipe(db: Session, recipe: RecipeCreate):
    shopping_list = build_shopping_list(db, recipe)

    db_recipe = Recipe(
        name=recipe.name,
        image=recipe.image,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions,
        shopping_list=shopping_list,
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def delete_recipe(db: Session, recipe_id: int):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if db_recipe:
        db.delete(db_recipe)
        db.commit()
        return True
    return False


def update_recipe(db: Session, recipe_id: int, recipe: RecipeCreate):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if db_recipe:
        db_recipe.name = recipe.name
        db_recipe.image = recipe.image
        db_recipe.ingredients = recipe.ingredients
        db_recipe.instructions = recipe.instructions
        db_recipe.shopping_list = build_shopping_list(db, recipe)

        db.commit()
        db.refresh(db_recipe)
        return db_recipe
    return None
