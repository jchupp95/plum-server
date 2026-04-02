from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.stock_item import StockItemCreate, StockItemRead
import app.crud.stock_item as crud

router = APIRouter()


@router.get("/", response_model=list[StockItemRead])
def read_stock_items(db: Session = Depends(get_db)):
    return crud.get_stock_items(db)


@router.post("/", response_model=StockItemRead)
def create_stock_item(stock_item: StockItemCreate, db: Session = Depends(get_db)):
    db_stock_item = crud.get_stock_item_by_name(db, stock_item.name)
    if db_stock_item:
        raise HTTPException(status_code=400, detail="Stock item already exists")
    return crud.create_stock_item(db, stock_item)


@router.delete("/{stock_item_id}", response_model=bool)
def delete_stock_item(stock_item_id: int, db: Session = Depends(get_db)):
    success = crud.delete_stock_item(db, stock_item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Stock item not found")
    return success
