from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class SandalSale(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sale_id: Optional[int] = Field(default=None, foreign_key="sale.id")
    sandal_id: Optional[int] = Field(default=None, foreign_key="sandal.id")
    quantity: int
    sandal: Optional["Sandal"] = Relationship(back_populates="sandalSales")
    sale: Optional["Sale"] = Relationship(back_populates="sandalSales")