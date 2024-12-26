from pydantic import BaseModel


class Client(BaseModel):
    """
    Modelo para representar um cliente.

    Attributes:
        id (int | None): Identificador único do cliente (opcional).
        nome (str): Nome do cliente.
        celular (str): Número de celular do cliente.
        endereco (str): Endereço do cliente.
    """

    id: int | None = None
    nome: str
    celular: str
    endereco: str

    @staticmethod
    def from_dict(data: dict):
        """
        Cria uma instância de `Client` a partir de um dicionário.

        Args:
            data (dict): Dicionário contendo os dados do cliente.

        Returns:
            Client: Instância do cliente criada com os dados fornecidos.
        """
        return Client(
            id=data.get("id"),
            nome=data.get("nome"),
            celular=str(data.get("celular")),
            endereco=data.get("endereco"),
        )
