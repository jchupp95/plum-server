import os
import sys
from sqlalchemy import text
from sqlalchemy.orm import Session

# Ensure project root is on sys.path when script is executed directly
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.core.database import Base, SessionLocal, engine  # noqa: E402
from app.models.ingredient import Ingredient  # noqa: E402
from app.models.recipe import Recipe  # noqa: E402
from app.models.menu import Menu  # noqa: E402


def _clear_database(db: Session):
    db.execute(text("PRAGMA foreign_keys=OFF;"))
    for tbl in reversed(Base.metadata.sorted_tables):
        db.execute(tbl.delete())
    db.execute(text("PRAGMA foreign_keys=ON;"))
    db.commit()


def create_ingredients(db: Session):
    ingredient_names = [
        "Chicken",
        "Beef",
        "Pork",
        "Salmon",
        "Rice",
        "Pasta",
        "Tomato",
        "Lettuce",
        "Cheese",
        "Egg",
        "Milk",
        "Onion",
        "Garlic",
        "Potato",
        "Carrot",
        "Broccoli",
        "Mushroom",
        "Olive oil",
        "Salt",
        "Pepper",
    ]

    ingredients = []
    for name in ingredient_names:
        existing = db.query(Ingredient).filter(Ingredient.name == name).first()
        if not existing:
            item = Ingredient(name=name)
            db.add(item)
            ingredients.append(item)

    db.commit()
    for item in ingredients:
        db.refresh(item)

    return db.query(Ingredient).all()


def create_recipes(db: Session, ingredients):
    recipes_data = [
        {
            "name": "Chicken Stir Fry",
            "image": "chicken_stir_fry.jpg",
            "ingredients": "Chicken, Rice, Onion, Garlic, Carrot, Broccoli",
            "instructions": "Cook chicken, add veggies, serve with rice.",
            "ingredient_names": [
                "Chicken",
                "Rice",
                "Onion",
                "Garlic",
                "Carrot",
                "Broccoli",
            ],
        },
        {
            "name": "Pasta al Pomodoro",
            "image": "pasta_pomodoro.jpg",
            "ingredients": "Pasta, Tomato, Olive oil, Garlic, Cheese",
            "instructions": "Boil pasta, stir in tomato sauce, top with cheese.",
            "ingredient_names": ["Pasta", "Tomato", "Olive oil", "Garlic", "Cheese"],
        },
        {
            "name": "Beef Tacos",
            "image": "beef_tacos.jpg",
            "ingredients": "Beef, Lettuce, Tomato, Cheese, Onion, Pepper",
            "instructions": "Cook beef, assemble with veggies in tacos.",
            "ingredient_names": [
                "Beef",
                "Lettuce",
                "Tomato",
                "Cheese",
                "Onion",
                "Pepper",
            ],
        },
        {
            "name": "Salmon Rice Bowl",
            "image": "salmon_rice_bowl.jpg",
            "ingredients": "Salmon, Rice, Lettuce, Olive oil",
            "instructions": "Bake salmon, serve over rice with lettuce.",
            "ingredient_names": ["Salmon", "Rice", "Lettuce", "Olive oil"],
        },
        {
            "name": "Veggie Omelette",
            "image": "veggie_omelette.jpg",
            "ingredients": "Egg, Milk, Cheese, Mushroom, Onion, Tomato",
            "instructions": "Whisk eggs, cook with veggies and cheese.",
            "ingredient_names": [
                "Egg",
                "Milk",
                "Cheese",
                "Mushroom",
                "Onion",
                "Tomato",
            ],
        },
        {
            "name": "Roast Pork and Potatoes",
            "image": "roast_pork_potatoes.jpg",
            "ingredients": "Pork, Potato, Olive oil, Garlic, Salt, Pepper",
            "instructions": "Roast pork and potatoes with seasoning.",
            "ingredient_names": [
                "Pork",
                "Potato",
                "Olive oil",
                "Garlic",
                "Salt",
                "Pepper",
            ],
        },
        {
            "name": "Mushroom Risotto",
            "image": "mushroom_risotto.jpg",
            "ingredients": "Rice, Mushroom, Onion, Garlic, Cheese",
            "instructions": "Cook rice slowly with mushrooms and cheese.",
            "ingredient_names": ["Rice", "Mushroom", "Onion", "Garlic", "Cheese"],
        },
        {
            "name": "Potato Soup",
            "image": "potato_soup.jpg",
            "ingredients": "Potato, Carrot, Onion, Garlic, Milk",
            "instructions": "Simmer vegetables and blend with milk.",
            "ingredient_names": ["Potato", "Carrot", "Onion", "Garlic", "Milk"],
        },
        {
            "name": "Salad Bowl",
            "image": "salad_bowl.jpg",
            "ingredients": "Lettuce, Tomato, Olive oil, Cheese",
            "instructions": "Toss all salad ingredients together.",
            "ingredient_names": ["Lettuce", "Tomato", "Olive oil", "Cheese"],
        },
        {
            "name": "Egg Fried Rice",
            "image": "egg_fried_rice.jpg",
            "ingredients": "Rice, Egg, Onion, Garlic, Carrot, Soy sauce",
            "instructions": "Fry rice with eggs and veggies.",
            "ingredient_names": ["Rice", "Egg", "Onion", "Garlic", "Carrot"],
        },
    ]

    recipe_list = []
    for data in recipes_data:
        db_recipe = db.query(Recipe).filter(Recipe.name == data["name"]).first()
        if db_recipe:
            recipe_list.append(db_recipe)
            continue

        recipe_ingredients = (
            db.query(Ingredient)
            .filter(Ingredient.name.in_(data["ingredient_names"]))
            .all()
        )

        db_recipe = Recipe(
            name=data["name"],
            image=data["image"],
            ingredients=data["ingredients"],
            instructions=data["instructions"],
            shopping_list=recipe_ingredients,
        )
        db.add(db_recipe)
        recipe_list.append(db_recipe)

    db.commit()
    for item in recipe_list:
        db.refresh(item)

    return recipe_list


def create_menus(db: Session, recipes):
    menu_definitions = [
        {"name": "Menu", "is_current": True, "recipe_indices": [0, 1, 2, 3]},
        {"name": "Week 1", "is_current": False, "recipe_indices": [1, 4, 5]},
        {"name": "Week 2", "is_current": False, "recipe_indices": [6, 7, 8, 9]},
    ]

    menus = []
    for data in menu_definitions:
        db_menu = db.query(Menu).filter(Menu.name == data["name"]).first()
        if not db_menu:
            db_menu = Menu(name=data["name"], is_current=data["is_current"])
            db.add(db_menu)

        db_menu.recipes = [
            recipes[i] for i in data["recipe_indices"] if i < len(recipes)
        ]
        menus.append(db_menu)

    db.commit()
    for m in menus:
        db.refresh(m)
    return menus


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        _clear_database(db)
        ingredients = create_ingredients(db)
        recipes = create_recipes(db, ingredients)
        menus = create_menus(db, recipes)

        print(f"Created {len(ingredients)} ingredients")
        print(f"Created {len(recipes)} recipes")
        print(f"Created {len(menus)} menus")
        print("Menu list:")
        for m in menus:
            print(
                f"- {m.name} (current={m.is_current}) -> {[r.name for r in m.recipes]}"
            )
    finally:
        db.close()


if __name__ == "__main__":
    main()
