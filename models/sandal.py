from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


class Sandal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    codigo: str
    nome: str
    valor: float
    cor: str
    tamanho: int
    sandalSales: List["SandalSale"] = Relationship(back_populates="sandal")
