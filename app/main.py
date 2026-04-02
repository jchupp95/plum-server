from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import menu, recipe, ingredient, shopping_list
from app.core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)

app.include_router(ingredient.router, prefix="/ingredient", tags=["Ingredients"])
app.include_router(recipe.router, prefix="/recipe", tags=["Recipes"])
app.include_router(menu.router, prefix="/menu", tags=["Menus"])
app.include_router(
    shopping_list.router, prefix="/shopping-list", tags=["Shopping List"]
)
