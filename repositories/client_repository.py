from sqlmodel import Session, select
from typing_extensions import runtime

from models import Client


class ClientRepository:
    """
    Repositório de clientes que interage com um arquivo CSV para armazenar,
    recuperar, atualizar e excluir informações de clientes.

    Attributes:
        session (sqlmodel.Session): Caminho para o arquivo CSV onde os dados dos clientes são armazenados.
    """

    def __init__(self, session: Session):
        """
        Args:
            file_path (str): Caminho para o arquivo CSV onde os dados dos clientes serão lidos e escritos.
        """
        self.session = session

    def create(self, client: Client) -> Client:
        """
        Cria um novo cliente e persiste no arquivo CSV.

        Args:
            client (Client): Objeto `Client` com os dados do cliente a ser criado.

        Returns:
            Client: O cliente criado com um ID atribuído.
        """
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client

    def get_by_id(self, client_id: int) -> Client | None:
        """
        Busca um cliente pelo ID.

        Args:
            client_id (int): O ID do cliente a ser buscado.

        Returns:
            Client | None: O cliente encontrado, ou `None` se não encontrado.
        """
        try:
            return self.session.get(Client, client_id)
        except IndexError:
            return None

    def update(self, client: Client) -> Client:
        """
        Atualiza as informações de um cliente no arquivo CSV.

        Args:
            client (Client): Objeto `Client` contendo os dados atualizados do cliente.

        Returns:
            Client: O cliente atualizado.

        Raises:
            ValueError: Se o cliente não for encontrado.
        """
        client_before = self.get_by_id(client.id)
        if not client_before:
            raise runtime("nao encontrado")
        for key, value in client.model_dump().items():
            setattr(client_before, key, value)
        self.session.commit()
        return client_before

    def delete(self, client_id: int) -> Client:
        """
        Exclui um cliente pelo ID do arquivo CSV.

        Args:
            client_id (int): O ID do cliente a ser excluído.

        Returns:
            bool: `True` se o cliente foi excluído com sucesso, `False` caso contrário.
        """
        user = self.session.get(Client, client_id)
        if user:
            self.session.delete(user)
            self.session.commit()
        return user

    def list(self):
        """
        Lista todos os clientes armazenados no arquivo CSV.

        Returns:
            List[Client]: Lista de objetos `Client` com todos os clientes encontrados.
        """
        try:
            return self.session.exec(select(Client)).all()
        except FileNotFoundError:
            return []