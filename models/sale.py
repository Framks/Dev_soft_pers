from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


class Sale(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id")
    finished: bool
    valor_total: float
    sale_date : datetime
    sandalSales: List["SandalSale"] = Relationship(back_populates="sale")
    client: "Client" = Relationship(back_populates="sales")

    def to_dict(self):
        """Converte o objeto Sale para um dicionário incluindo relacionamentos."""
        return {
            "id": self.id,
            "client_id": self.client_id,
            "sade_date":self.sale_date.strftime("%d/%m/%Y"),
            "valor_total": self.valor_total,
            "sandalSales": [
                {
                    "id": sandal_sale.id,
                    "sandal_id": sandal_sale.sandal_id,
                    "quantity": sandal_sale.quantity,
                }
                for sandal_sale in self.sandalSales
            ],
            "client": {
                "id": self.client.id,
                "nome": self.client.nome,
                "celular": self.client.celular,
                "endereco": self.client.endereco,
            } if self.client else None,
        }