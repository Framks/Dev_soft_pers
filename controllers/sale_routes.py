from fastapi import APIRouter

from models import Sale
from services import SaleService


class SalesRoutes:
    """
    Classe responsável por definir as rotas relacionadas às vendas.

    Attributes:
        router (APIRouter): Objeto para gerenciar as rotas do FastAPI.
        service (SaleService): Serviço responsável por implementar a lógica das operações.
    """

    def __init__(self, service: SaleService):
        """
        Args:
            service (SaleService): Instância do serviço responsável pelas operações
                relacionadas às vendas.
        """
        self.router = APIRouter()
        self.service = service
        self._add_routes()

    def _add_routes(self):
        """
        Registra as rotas da API relacionadas às vendas.
        """
        self.router.add_api_route("/sales", self.create_sale, methods=["POST"])
        self.router.add_api_route("/sales", self.list_sale, methods=["GET"])
        self.router.add_api_route(
            "/sales/{sale_id}", self.search_sale_id, methods=["GET"]
        )
        self.router.add_api_route("/sales/{sale_id}", self.update_sale, methods=["PUT"])
        self.router.add_api_route(
            "/sales/{sale_id}", self.delete_sale, methods=["DELETE"]
        )
        self.router.add_api_route("/sales/total/", self.count_sales, methods=["GET"])

    def create_sale(self, sale: Sale):
        """
        Cria uma nova venda.

        Args:
            sale (Sale): Objeto contendo os dados da venda.

        Returns:
            object: Resultado da operação de criação.
        """
        return self.service.create(sale)

    def list_sale(self):
        """
        Lista todas as vendas.

        Returns:
            List[object]: Lista de vendas cadastradas.
        """
        return self.service.list()

    def search_sale_id(self, sale_id: int):
        """
        Busca uma venda pelo ID.

        Args:
            sale_id (int): ID da venda a ser buscada.

        Returns:
            object: Venda encontrada ou `None` se não encontrada.
        """
        return self.service.search_sale(sale_id)

    def update_sale(self, sale: Sale, sale_id: int):
        """
        Atualiza as informações de uma venda existente.

        Args:
            sale (Sale): Objeto contendo os dados atualizados da venda.
            sale_id (int): ID da venda a ser atualizada.

        Returns:
            object: Resultado da operação de atualização.
        """
        return self.service.update(sale_id, sale)

    def delete_sale(self, sale_id: int):
        """
        Exclui uma venda pelo ID.

        Args:
            sale_id (int): ID da venda a ser excluída.

        Returns:
            object: Resultado da operação de exclusão.
        """
        return self.service.delete(sale_id)

    def count_sales(self):
        """
        Conta o número total de vendas registradas.

        Returns:
            int: Total de vendas registradas.
        """
        return self.service.count()
