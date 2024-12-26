from pydantic import BaseModel
from typing import List

from models.client import Client
from models.sandal import Sandal


class Sale(BaseModel):
    """
    Modelo para representar uma venda.

    Attributes:
        id (int): Identificador único da venda.
        client (Client): Cliente associado à venda.
        valor_total (float): Valor total da venda.
        produtos (List[Sandal]): Lista de sandálias (produtos) associadas à venda.
    """

    id: int
    client: Client
    valor_total: float
    produtos: List[Sandal]
