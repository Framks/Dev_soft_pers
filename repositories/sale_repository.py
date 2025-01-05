from datetime import datetime

from sqlalchemy.sql.functions import count
from sqlmodel import Session, select, func
from random import randint, sample, choice, uniform
from datetime import datetime, timedelta

from exceptions import OperationalException, NotFoundException
from models import Sale, SandalSale, Sandal, Client


class SaleRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, sale: Sale) -> Sale:
        try:
            self.session.add(sale)
            self.session.commit()
            self.session.refresh(sale)
            return sale
        except Exception as e:
            self.session.rollback()
            raise OperationalException(str(e))

    def get_by_id(self, sale_id: int) -> Sale | None:
        try:
            return self.session.get(Sale, sale_id)
        except Exception as e:
            raise NotFoundException(str(e))

    def update(self, sale: Sale) -> Sale | None:
        try:
            sale_before = self.get_by_id(sale.id)
            for key, value in sale.model_dump().items():
                setattr(sale_before, key,value)
            self.session.commit()
            self.session.refresh(sale)
            return sale
        except Exception as e:
            self.session.rollback()
            raise NotFoundException(str(e))

    def delete(self, sale_id: int) -> bool:
        try:
            sale = self.get_by_id(sale_id)
            self.session.delete(sale)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise NotFoundException(str(e))

    def list(self, skip, limit):
        try:
            return self.session.exec(select(Sale).offset(skip).limit(limit)).all()
        except Exception as e:
            raise OperationalException(str(e))

    def add_sandal(self, sandal_sale: SandalSale):
        try:
            self.session.add(sandal_sale)
            self.session.commit()
            self.session.refresh(sandal_sale)
            return sandal_sale
        except Exception as e:
            self.session.rollback()
            raise OperationalException(str(e))

    def count(self):
        try:
            return self.session.exec(select(count(Sale.id))).one()
        except Exception as e:
            raise OperationalException(str(e))

    def delete_sandalSale(self, sandal_sale: SandalSale):
        try:
            self.session.delete(sandal_sale)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise OperationalException(str(e))

    def get_sandalSale(self, sandalSale_id: int):
        return self.session.get(SandalSale, sandalSale_id)

    def count_date(self, init_date, fin_date):
        return self.session.exec(select(count(Sale.id)).where((Sale.sale_date >= init_date) & (Sale.sale_date <= fin_date))).one()

    def media_quantity_sale(self, start_date: datetime, end_date: datetime):
        sub_search= (
            select(SandalSale.sale_id, func.sum(SandalSale.quantity).label("quantity_sale"))
            .join(Sale, Sale.id == SandalSale.sale_id)
            .where(Sale.sale_date.between(start_date, end_date))
            .group_by(SandalSale.sale_id)
            .subquery()
        )
        result = self.session.exec(select(func.avg(sub_search.c.quantity_sale).label("media_quantity_sale"))).first()
        return result

    def media_quantity_sale_all(self):
        sub_search= (
            select(SandalSale.sale_id, func.sum(SandalSale.quantity).label("quantity_sale"))
            .join(Sale, Sale.id == SandalSale.sale_id)
            .group_by(SandalSale.sale_id)
            .subquery()
        )
        result = self.session.exec(select(func.avg(sub_search.c.quantity_sale).label("media_quantity_sale"))).first()
        return result