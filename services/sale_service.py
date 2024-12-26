from models import Sale
from repositories import SaleRepository


class SaleService:
    """
    Serviço que gerencia operações relacionadas a vendas, incluindo a criação, pesquisa,
    listagem, atualização e exclusão de vendas.

    Attributes:
        repository (SaleRepository): O repositório responsável pela persistência de dados das vendas.
    """

    def __init__(self, repository: SaleRepository):
        """
        Args:
            repository (SaleRepository): O repositório onde as vendas são armazenadas.
        """
        self.repository = repository

    def create(self, sale: Sale) -> Sale:
        """
        Cria uma nova venda no repositório.

        Args:
            sale (Sale): A venda a ser criada.

        Returns:
            Sale: A venda criada, incluindo seu ID atribuído.

        """
        return self.repository.create(sale)

    def search_sale(self, sale_id: int) -> Sale | None:
        """
        Busca uma venda pelo seu ID.

        Args:
            sale_id (int): O ID da venda a ser buscada.

        Returns:
            Sale | None: A venda correspondente ao ID fornecido, ou None se não encontrada.
        """
        return self.repository.search_por_id(sale_id)

    def list(self) -> list[Sale]:
        """
        Lista todas as vendas.

        Returns:
            list[Sale]: Uma lista de todas as vendas no repositório.
        """
        return self.repository.list()

    def update(self, sale_id: int, sale: Sale) -> Sale:
        """
        Atualiza os dados de uma venda existente.

        Args:
            sale_id (int): O ID da venda a ser atualizada.
            sale (Sale): Os novos dados da venda.

        Returns:
            Sale: A venda atualizada.

        Raises:
            ValueError: Se a venda não for encontrada.
        """
        return self.repository.update(sale)

    def delete(self, sale_id: int) -> bool:
        """
        Exclui uma venda pelo seu ID.

        Args:
            sale_id (int): O ID da venda a ser excluída.

        Returns:
            bool: True se a venda foi excluída com sucesso, False caso contrário.
        """
        return self.repository.delete(sale_id)

    def count(self):
        """
        Conta o número total de vendas no repositório.

        Returns:
            int: O número total de vendas.
        """
        return self.repository.count()
