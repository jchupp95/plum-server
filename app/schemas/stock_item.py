from pydantic import BaseModel


class StockItemBase(BaseModel):
    name: str
    quantity: float
    unit: str


class StockItemCreate(StockItemBase):
    pass


class StockItemRead(StockItemBase):
    id: int

    class Config:
        from_attributes = True
