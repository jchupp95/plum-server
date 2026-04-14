from sqlalchemy.orm import Session
from app.models.stock_item import StockItem
from app.schemas.stock_item import StockItemCreate


def get_stock_items(db: Session) -> list[StockItem]:
    return db.query(StockItem).all()


def get_stock_item_by_name(db: Session, name: str) -> StockItem | None:
    return db.query(StockItem).filter(StockItem.name == name).first()


def create_stock_item(db: Session, stock_item: StockItemCreate):
    db_stock_item = StockItem(name=stock_item.name)
    db.add(db_stock_item)
    db.commit()
    db.refresh(db_stock_item)
    return db_stock_item


def delete_stock_item(db: Session, stock_item_id: int):
    db_stock_item = db.query(StockItem).filter(StockItem.id == stock_item_id).first()
    if db_stock_item:
        db.delete(db_stock_item)
        db.commit()
        return True
    return False
