from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    celular: str
    endereco: str
    sales: List["Sale"] = Relationship(back_populates="client")