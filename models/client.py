from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


class Client(SQLModel, table=True):
    """
    Modelo para representar um cliente.

    Attributes:
        id (int | None): Identificador único do cliente (opcional).
        nome (str): Nome do cliente.
        celular (str): Número de celular do cliente.
        endereco (str): Endereço do cliente.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    celular: str
    endereco: str
    sales: List["Sale"] = Relationship(back_populates="client")