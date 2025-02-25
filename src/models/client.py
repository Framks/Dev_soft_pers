from odmantic import Model
from typing import Optional


class Client(Model):
    name: Optional[str] = None
    email: Optional[str] = None
    rua: Optional[str] = None
    numero: Optional[int] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    telefone: Optional[str] = None
    celular: Optional[str] = None
