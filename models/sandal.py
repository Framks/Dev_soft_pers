from pydantic import BaseModel


class Sandal(BaseModel):
    """
    Modelo para representar uma sandália.

    Attributes:
        id (int): Identificador único da sandália.
        codigo (str): Código único da sandália.
        nome (str): Nome da sandália.
        quantidade (int): Quantidade de sandálias em estoque.
        valor (float): Preço da sandália.
        cor (str): Cor da sandália.
        tamanho (int): Tamanho da sandália.
    """

    id: int
    codigo: str
    nome: str
    quantidade: int
    valor: float
    cor: str
    tamanho: int
