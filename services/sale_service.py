from exceptions import NotFoundException, InvalidArgumentException
from models import Sale, SandalSale
from repositories import SaleRepository
from services import ClientService, SandalService


class SaleService:

    def __init__(self, repository: SaleRepository, client_service: ClientService, sandal_service: SandalService):
        self.repository = repository
        self.client_service = client_service
        self.sandal_service = sandal_service

    def create(self, sale: Sale) -> Sale:
        return self.repository.create(sale)

    def search_sale(self, sale_id: int) -> Sale | None:
        return self.repository.get_by_id(sale_id)

    def list(self) -> list[Sale]:
        return [sale.to_dict() for sale in self.repository.list()]

    def update(self, sale_id: int, sale: Sale) -> Sale:
        return self.repository.update(sale)

    def delete(self, sale_id: int) -> bool:
        return self.repository.delete(sale_id)

    def count(self):
        """
        Conta o número total de vendas no repositório.

        Returns:
            int: O número total de vendas.
        """
        return self.repository.count()

    def sale_sandal_for_client(self, sale_id, sandal_id, client_id,quantity):
        sale = self.repository.get_by_id(sale_id)
        sandal = self.sandal_service.search_sandal(sandal_id)
        client = self.client_service.search_client(client_id)
        if not sale or not sandal or not client:
            raise InvalidArgumentException("ids", f"sale{sale_id}, sandal={sandal}, client={client_id}")
        sandal_sale = SandalSale(sandal_id=sandal_id, quantity=quantity, sale_id=sale_id)
        return self.repository.add_sandal(sandal_sale)

    def sandals_by_sale(self, sale_id):
        sale = self.repository.get_by_id(sale_id)
        if not sale:
            raise NotFoundException(f"Sale not found id={sale_id}")
        sandals = [self.sandal_service.search_sandal(sandalSale.sandal_id) for sandalSale in sale.sandalSales]
        return sandals