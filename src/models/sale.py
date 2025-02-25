from datetime import datetime
from odmantic import Model, Reference
from .client import Client
from .sandal import Sandal
from typing import Optional, List


class SandalSale(Model):
    quantity: Optional[int]
    sandal: Sandal = Reference()


class Sale(Model):
    finished: Optional[bool]
    sale_date: Optional[datetime]
    valor_total: Optional[float]
    client: Client = Reference()
    sandalSales: List[SandalSale] = []
