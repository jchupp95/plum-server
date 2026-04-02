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


def create_recipe(db: Session, recipe: RecipeCreate):
    shopping_list = (
        db.query(Ingredient)
        .filter(
            Ingredient.name.in_(
                [ingredient.name for ingredient in recipe.shopping_list]
            )
        )
        .all()
    )

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

        shopping_list = (
            db.query(Ingredient)
            .filter(
                Ingredient.name.in_(
                    [ingredient.name for ingredient in recipe.shopping_list]
                )
            )
            .all()
        )
        db_recipe.shopping_list = shopping_list

        db.commit()
        db.refresh(db_recipe)
        return db_recipe
    return None
