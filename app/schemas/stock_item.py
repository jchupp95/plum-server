from pydantic import BaseModel


class StockItemBase(BaseModel):
    name: str


class StockItemCreate(StockItemBase):
    pass


class StockItemRead(StockItemBase):
    id: int
