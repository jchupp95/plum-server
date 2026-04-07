# Plum

Plum is a small FastAPI service for planning meals. It lets you store ingredients, build recipes from those ingredients, and group recipes into menus so you can answer the recurring question: what's for dinner?

## What It Does

- Creates and reads ingredients
- Creates and reads recipes
- Creates menus and assigns recipes to them
- Exposes a "current" menu for the active meal plan
- Uses SQLite by default, so it runs locally with very little setup

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2.x
- SQLite
- `uv` for dependency management


## Getting Started

### 1. Install dependencies

```bash
uv sync
```

### 2. Start the API

```bash
uv run fastapi dev app/main.py
```

The app will usually be available at `http://127.0.0.1:8000`.

Interactive docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Configuration

The app reads settings from environment variables or a local `.env` file.

Default values:

```env
PROJECT_NAME=Plum API
DATABASE_URL=sqlite:///./app.db
DEBUG=True
```

Example `.env`:

```env
PROJECT_NAME=Plum API
DATABASE_URL=sqlite:///./app.db
IMAGES_DIR=images
DEBUG=True
```

## Database Notes

- Tables are created automatically on app startup
- The default database is a local SQLite file at `app.db`
- Recipes reference existing ingredients through a shopping list relationship
- Menus reference one or more recipes

## Seed Sample Data

To quickly load sample ingredients, recipes, and menus:

```bash
uv run python scripts/populate_test_db.py
```

This script clears the current SQLite data, recreates the tables, and inserts:

- 20 ingredients
- 10 recipes
- 3 menus

## API Overview

### Ingredients

- `POST /ingredient/` creates an ingredient
- `GET /ingredient/{ingredient_id}` fetches one ingredient

Example request:

```json
{
  "name": "Chicken"
}
```

### Recipes

- `POST /recipe/` creates a recipe
- `GET /recipe/{recipe_id}` fetches one recipe

Example request:

```json
{
  "name": "Chicken Stir Fry",
  "image": "chicken_stir_fry.jpg",
  "ingredients": "Chicken, Rice, Onion, Garlic, Carrot, Broccoli",
  "instructions": "Cook chicken, add veggies, serve with rice.",
  "shopping_list": [
    { "name": "Chicken" },
    { "name": "Rice" },
    { "name": "Onion" }
  ]
}
```

Note: recipe creation links to ingredients by name, so those ingredients should already exist in the database.

### Menus

- `POST /menu/` creates a menu
- `GET /menu/` lists non-current menus
- `GET /menu/current` fetches the current menu
- `GET /menu/{menu_id}` fetches one menu
- `PUT /menu/{menu_id}/recipes` replaces the menu's recipe list

Create menu example:

```text
POST /menu/?menu_name=Week%203
```

Update menu recipes example:

```text
PUT /menu/1/recipes?recipe_ids=1&recipe_ids=2&recipe_ids=3
```

## Typical Local Workflow

1. Start the API
2. Create a few ingredients
3. Create recipes that reference those ingredient names
4. Create a menu
5. Attach recipe IDs to that menu
6. Use `/menu/current` or `/menu/{id}` to read the result

## Development

Linting and tooling are managed in `pyproject.toml`.

Useful commands:

```bash
uv run ruff check .
uv run pre-commit run --all-files
```

## Docker

Build the image:

```bash
docker build -t plum-server .
```

Run it with external bind mounts for both the SQLite database file and recipe images:

```bash
docker run --rm -p 8444:8444 \
  -v /absolute/path/to/app.db:/data/app.db \
  -v /absolute/path/to/images:/data/images \
  plum-server
```

On Windows PowerShell from the repository root:

```powershell
docker run --rm -p 8444:8444 `
  -v "${PWD}\app.db:/data/app.db" `
  -v "${PWD}\images:/data/images" `
  plum-server
```

Container defaults:

```env
DATABASE_URL=sqlite:////data/app.db
IMAGES_DIR=/data/images
DEBUG=False
```

That means the API serves mounted images from `/images/...` and stores SQLite data in the mounted `app.db` file outside the container.
