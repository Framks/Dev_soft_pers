from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .sale import SandalSale


class SandalBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    codigo: str
    nome: str
    valor: float
    cor: str
    tamanho: int


class Sandal(SandalBase, table=True):
    sandal_sales: list['SandalSale'] = Relationship(back_populates="sandal")
