from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.shopping_list import ShoppingListBase
import app.crud.shopping_list as crud

router = APIRouter()


@router.get("/", response_model=ShoppingListBase)
def read_shopping_list(db: Session = Depends(get_db)):
    return crud.get_shopping_list(db)
