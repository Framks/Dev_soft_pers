from fastapi import APIRouter

from models import Sandal
from services import SandalService


class SandalRoutes:
    """
    Classe responsável por definir as rotas relacionadas a sandálias.

    Attributes:
        router (APIRouter): Objeto para gerenciar as rotas do FastAPI.
        service (SandalService): Serviço responsável por implementar a lógica das operações.
    """

    def __init__(self, sandal_service: SandalService):
        """
        Args:
            sandal_service (SandalService): Instância do serviço responsável pelas operações
                relacionadas a sandálias.
        """
        self.router = APIRouter()
        self.service = sandal_service
        self._add_routes()

    def _add_routes(self):
        """
        Registra as rotas da API relacionadas a sandálias.
        """
        self.router.add_api_route("/sandals", self.create_sandal, methods=["POST"])
        self.router.add_api_route("/sandals", self.list_sandal, methods=["GET"])
        self.router.add_api_route(
            "/sandals/{sandal_id}", self.search_sandal_id, methods=["GET"]
        )
        self.router.add_api_route(
            "/sandals/{sandal_id}", self.update_sandal, methods=["PUT"]
        )
        self.router.add_api_route(
            "/sandals/{sandal_id}", self.delete_sandal, methods=["DELETE"]
        )

    def create_sandal(self, sandal: Sandal):
        """
        Cria uma nova sandália.

        Args:
            sandal (Sandal): Objeto contendo os dados da sandália.

        Returns:
            object: Resultado da operação de criação.
        """
        return self.service.create(sandal)

    def list_sandal(self):
        """
        Lista todas as sandálias.

        Returns:
            List[object]: Lista de sandálias cadastradas.
        """
        return self.service.list()

    def search_sandal_id(self, sandal_id: int):
        """
        Busca uma sandália pelo ID.

        Args:
            sandal_id (int): ID da sandália a ser buscada.

        Returns:
            object: Sandália encontrada ou `None` se não encontrada.
        """
        return self.service.search_sandal(sandal_id)

    def update_sandal(self, sandal: Sandal, sandal_id: int):
        """
        Atualiza as informações de uma sandália existente.

        Args:
            sandal (Sandal): Objeto contendo os dados atualizados da sandália.
            sandal_id (int): ID da sandália a ser atualizada.

        Returns:
            object: Resultado da operação de atualização.
        """
        return self.service.update(sandal_id, sandal)

    def delete_sandal(self, sandal_id: int):
        """
        Exclui uma sandália pelo ID.

        Args:
            sandal_id (int): ID da sandália a ser excluída.

        Returns:
            object: Resultado da operação de exclusão.
        """
        return self.service.delete(sandal_id)
