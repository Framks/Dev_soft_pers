from fastapi import APIRouter

from services import DataService


class DataRoutes:
    """
    Classe responsável por definir as rotas relacionadas ao processamento de dados.

    Attributes:
        service (DataService): Serviço responsável por realizar as operações de criação de zip e hash.
        router (APIRouter): Roteador do FastAPI para gerenciar as rotas.
    """

    def __init__(self, service: DataService):
        """
        Args:
            service (DataService): Instância do serviço responsável pelas operações
                de criação de zip e cálculo de hash.
        """
        self.service = service
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        """
        Registra as rotas da API relacionadas ao processamento de dados.
        """
        self.router.add_api_route("/zip/create/", self.create_zip, methods=["POST"])
        self.router.add_api_route("/zip/hash/", self.create_hash, methods=["POST"])

    def create_zip(self):
        """
        Gera um arquivo zip.

        Este endpoint delega a lógica de criação do zip ao serviço associado.

        Returns:
            object: Resultado da operação de criação do arquivo zip.
        """
        return self.service.create_zip()

    def create_hash(self):
        """
        Calcula o hash de dados.

        Este endpoint delega a lógica de cálculo de hash ao serviço associado.

        Returns:
            object: Resultado do cálculo de hash.
        """
        return self.service.create_hash()
