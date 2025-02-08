from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .sale import Sale


class ClientBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str


class Client(ClientBase, table=True):
    sales: list['Sale'] = Relationship(back_populates="client")