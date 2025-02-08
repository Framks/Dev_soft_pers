from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

from .sandal import Sandal

class SandalSaleBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    quantity: int

class SandalSale(SandalSaleBase, table=True):
    sale_id: int = Field(default=None, foreign_key="sale.id")
    sandal_id: int = Field(default=None, foreign_key="sandal.id")
    sandal: 'Sandal' =