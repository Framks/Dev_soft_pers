from datetime import datetime

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
        sale.sale_date = datetime.fromisoformat(sale.sale_date.rstrip("Z"))
        return self.repository.create(sale)

    def search_sale(self, sale_id: int) -> Sale | None:
        return self.repository.get_by_id(sale_id)

    def list(self, skip, limit) -> list[Sale]:
        return [sale.to_dict() for sale in self.repository.list(skip, limit)]

    def update(self, sale_id: int, sale: Sale) -> Sale:
        sale.id = sale_id
        return self.repository.update(sale)

    def delete(self, sale_id: int) -> bool:
        return self.repository.delete(sale_id)

    def count(self, init_date, fin_date):
        if init_date and fin_date:
            start_date = datetime.strptime(init_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(fin_date, "%Y-%m-%d").date()
            return self.repository.count_date(start_date, end_date)
        return self.repository.count()

    def sale_sandal_for_client(self, sale_id, sandal_id, client_id,quantity):
        sale = self.repository.get_by_id(sale_id)
        sandal = self.sandal_service.search_sandal(sandal_id)
        client = self.client_service.search_client(client_id)
        if not sale or not sandal or not client:
            raise InvalidArgumentException("ids", f"sale{sale_id}, sandal={sandal_id}, client={client_id}")
        sandal_sale = SandalSale(sandal_id=sandal_id, quantity=quantity, sale_id=sale_id)
        sale.valor_total = sale.valor_total + sandal.valor*quantity
        self.repository.update(sale)
        return self.repository.add_sandal(sandal_sale)

    def sandals_by_sale(self, sale_id):
        sale = self.repository.get_by_id(sale_id)
        if not sale:
            raise NotFoundException(f"Sale not found id={sale_id}")
        sandals = [self.sandal_service.search_sandal(sandalSale.sandal_id) for sandalSale in sale.sandalSales]
        return sandals

    def revomer_sandal_sale(self, sale_id: int, sandal_id:int):
        sale = self.repository.get_by_id(sale_id)
        sandal_sale = None
        for sandalSale in sale.sandalSales:
            if sandalSale.sandal_id == sandal_id:
                sandal_sale = sandalSale
                break
        sale.valor_total = sale.valor_total - (sandal_sale.sandal.valor * sandal_sale.quantity)
        self.repository.update(sale)
        return self.repository.delete_sandalSale(sandal_sale)

    def finished_sale(self, sale_id):
        sale = self.repository.get_by_id(sale_id)
        if not sale:
            raise NotFoundException(f"Sale not found id={sale_id}")
        if sale.finished:
            raise InvalidArgumentException("sale id","Sale already finished")
        sale.finished = True
        self.repository.update(sale)
        return sale

    def media_sale_date(self, start_date, end_date):
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            return self.repository.media_quantity_sale(start, end)
        except ValueError:
            raise InvalidArgumentException("Invalid date")

    def media_quantity_sandal(self, start_date, end_date):
        if start_date and end_date:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            return self.repository.media_quantity_sale(start, end)
        else:
            return self.repository.media_quantity_sale_all()