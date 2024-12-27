from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


class Sandal(SQLModel, table=True):
    """
    Modelo para representar uma sandália.

    Attributes:
        id (int): Identificador único da sandália.
        codigo (str): Código único da sandália.
        nome (str): Nome da sandália.
        valor (float): Preço da sandália.
        cor (str): Cor da sandália.
        tamanho (int): Tamanho da sandália.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    codigo: str
    nome: str
    valor: float
    cor: str
    tamanho: int
    sandalSales: List["SandalSale"] = Relationship(back_populates="sandal")
