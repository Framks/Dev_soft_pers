from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class SandalSale(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sale_id: int = Field(default=None, foreign_key="sale.id")
    sandal_id: int = Field(default=None, foreign_key="sandal.id")
    quantity: int
    sandal: "Sandal" = Relationship(back_populates="sandalSales")
    sale: "Sale" = Relationship(back_populates="sandalSales")