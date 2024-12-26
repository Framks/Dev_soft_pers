from fastapi import APIRouter

from models import Client


class ClientRoutes:
    """
    Classe responsável por definir as rotas relacionadas ao gerenciamento de clientes.

    Attributes:
        router (APIRouter): Objeto para gerenciar as rotas do FastAPI.
        service (object): Serviço responsável por implementar a lógica das operações.
    """

    def __init__(self, client_service):
        """W
        Args:
            client_service (object): Instância do serviço responsável pelas operações.
        """
        self.router = APIRouter()
        self.service = client_service
        self._add_routes()

    def _add_routes(self):
        """Registra as rotas da API no roteador."""
        self.router.add_api_route("/clients", self.create_client, methods=["POST"])
        self.router.add_api_route("/clients", self.list_client, methods=["GET"])
        self.router.add_api_route(
            "/clients/{client_id}", self.search_client_id, methods=["GET"]
        )
        self.router.add_api_route(
            "/clients/{client_id}", self.update_client, methods=["PUT"]
        )
        self.router.add_api_route(
            "/clients/{client_id}", self.delete_client, methods=["DELETE"]
        )

    def create_client(self, client: Client):
        """
        Cria um novo cliente.

        Args:
            client (Client): Objeto contendo os dados do cliente a ser criado.

        Returns:
            object: Resultado da operação de criação.
        """
        return self.service.create(client)

    def list_client(self):
        """
        Lista todos os clientes.

        Returns:
            List[object]: Lista de clientes cadastrados.
        """
        return self.service.list()

    def search_client_id(self, client_id: int):
        """
        Busca um cliente pelo ID.

        Args:
            client_id (int): ID do cliente a ser buscado.

        Returns:
            object: Cliente encontrado ou `None` se não encontrado.
        """
        return self.service.search_client(client_id)

    def update_client(self, client: Client, client_id: int):
        """
        Atualiza as informações de um cliente existente.

        Args:
            client (Client): Objeto contendo os dados atualizados do cliente.
            client_id (int): ID do cliente a ser atualizado.

        Returns:
            object: Resultado da operação de atualização.
        """
        return self.service.update(client_id, client)

    def delete_client(self, client_id: int):
        """
        Exclui um cliente pelo ID.

        Args:
            client_id (int): ID do cliente a ser excluído.

        Returns:
            object: Resultado da operação de exclusão.
        """
        return self.service.delete(client_id)
