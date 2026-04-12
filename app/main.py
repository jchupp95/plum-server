from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.database import Base, engine
from app.routers import menu, recipe, ingredient, shopping_list, stock_item
from app.core.config import settings

Base.metadata.create_all(bind=engine)
images_dir = Path(settings.IMAGES_DIR)
images_dir.mkdir(parents=True, exist_ok=True)

app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/images", StaticFiles(directory=images_dir), name="images")

app.include_router(ingredient.router, prefix="/ingredient", tags=["Ingredients"])
app.include_router(recipe.router, prefix="/recipe", tags=["Recipes"])
app.include_router(menu.router, prefix="/menu", tags=["Menus"])
app.include_router(
    shopping_list.router, prefix="/shopping-list", tags=["Shopping List"]
)
app.include_router(stock_item.router, prefix="/stock-item", tags=["Stock Items"])
