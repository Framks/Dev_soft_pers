from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


class Sale(SQLModel, table=True):
    """
    Modelo para representar uma venda.

    Attributes:
        id (int): Identificador único da venda.
        client (Client): Cliente associado à venda.
        valor_total (float): Valor total da venda.
        produtos (List[Sandal]): Lista de sandálias (produtos) associadas à venda.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id")
    valor_total: float
    sandalSales: List["SandalSale"] = Relationship(back_populates="sale")
    client: "Client" = Relationship(back_populates="sales")