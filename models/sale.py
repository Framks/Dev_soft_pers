from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship

from .client import Client, ClientBase
from .sandal import Sandal, SandalBase


class SandalSaleBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    quantity: int = Field(default=1)
    
    
class SandalSale(SandalSaleBase, table=True):
    sale_id: int = Field(default=None, foreign_key="sale.id",)
    sandal_id: int = Field(default=None, foreign_key="sandal.id")
    sandal: 'Sandal' = Relationship(back_populates="sandal_sales")
    sale: 'Sale' = Relationship(back_populates="sandal_sales")


class SandalSaleWithSandal(SandalSaleBase):
    sandal: SandalBase | None




class SaleBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    finished: bool
    sale_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    valor_total: float
    

class Sale(SaleBase, table=True):
    client_id: int = Field(foreign_key="client.id")
    client: 'Client' = Relationship(back_populates="sales")
    sandal_sales: list[SandalSale] = Relationship(back_populates="sale")


class SaleWithClientSandals(SaleBase):
    client: ClientBase | None
    sandal_sales: list[SandalSaleWithSandal]