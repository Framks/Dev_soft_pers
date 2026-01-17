from odmantic import Model
from typing import Optional


class Sandal(Model):
    codigo: Optional[str]
    nome: Optional[str]
    valor: Optional[float]
    cor: Optional[str]
    tamanho: Optional[int]
    marca: Optional[str]
