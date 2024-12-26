from models.client import Client
from repositories import ClientRepository
from fastapi import HTTPException


class ClientService:
    """
    Serviço que fornece funcionalidades para gerenciar clientes,
    utilizando um repositório de clientes.

    Attributes:
        repository (ClientRepository): O repositório utilizado para persistir os dados dos clientes.
    """

    def __init__(self, repository: ClientRepository):
        """
        Inicializa o serviço de clientes com o repositório fornecido.

        Args:
            repository (ClientRepository): Instância do repositório que será utilizado para manipular dados de clientes.
        """
        self.repository = repository

    def create(self, client: Client) -> Client:
        """
        Cria um novo cliente.

        Args:
            client (Client): Objeto `Client` contendo os dados do cliente a ser criado.

        Returns:
            Client: O cliente criado com o ID atribuído.
        """

        try:
            return self.repository.create(client)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Arquivo não encontrado: {str(e)}" )

    def search_client(self, client_id: int) -> Client | None:
        """
        Busca um cliente pelo ID.

        Args:
            client_id (int): O ID do cliente a ser buscado.

        Returns:
            Client | None: O cliente encontrado, ou `None` se o cliente não for encontrado.
        """
        try:
            return self.repository.search_por_id(client_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Arquivo não encontrado: {str(e)}" )

    def list(self) -> list[Client]:
        """
        Lista todos os clientes.

        Returns:
            list[Client]: Lista de objetos `Client` com todos os clientes cadastrados.
        """
        try:
            return self.repository.list()
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Arquivo não encontrado: {str(e)}")

    def update(self, client_id: int, client: Client) -> Client:
        """
        Atualiza os dados de um cliente existente.

        Args:
            client_id (int): O ID do cliente a ser atualizado.
            client (Client): Objeto `Client` contendo os dados atualizados do cliente.

        Returns:
            Client: O cliente atualizado.

        Raises:
            ValueError: Se o cliente não for encontrado no repositório.
        """
        
        try:
            client.id = client_id
            return self.repository.update(client)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Arquivo não encontrado: {str(e)}")


    def delete(self, client_id: int) -> bool:
        """
        Exclui um cliente pelo ID.

        Args:
            client_id (int): O ID do cliente a ser excluído.

        Returns:
            bool: `True` se o cliente foi excluído com sucesso, `False` caso contrário.
        """ 
        try:
            return self.repository.delete(client_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Arquivo não encontrado: {str(e)}")
