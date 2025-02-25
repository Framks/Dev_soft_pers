from fastapi import APIRouter, Depends, Query
from odmantic import AIOEngine

from src.models.sale import Sale
from database import get_engine
from src.services import sale
from src.constants.constants import MAX_LENGTH_LIMIT
from datetime import date

router = APIRouter(prefix="/sales", tags=["sales"])


@router.get("/")
async def list(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=MAX_LENGTH_LIMIT),
    session: AIOEngine = Depends(get_engine),
):
    return await sale.list(offset, limit, session)


@router.post("/")
async def create(sale_create: Sale, session: AIOEngine = Depends(get_engine)):
    return await sale.create(sale_create, session)


@router.get("/{sale_id}")
async def read_sale(sale_id: str, session: AIOEngine = Depends(get_engine)):
    return await sale.get_by_id(sale_id, session)


@router.put("/{sale_id}")
async def update_sale(
    sale_id: int, sale_update: Sale, session: AIOEngine = Depends(get_engine)
):
    return await sale.update(sale_id, sale_update, session)


@router.delete("/{sale_id}")
async def delete_sale(sale_id: int, session: AIOEngine = Depends(get_engine)):
    return await sale.delete(sale_id, session)


@router.post("/{sale_id}/sandals/{sandal_id}/")
async def add_sandal_sale(
    sale_id: str,
    sandal_id: str,
    quantity: int = 1,
    session: AIOEngine = Depends(get_engine),
):
    return await sale.add_sandal(sale_id, sandal_id, quantity, session)


@router.delete("/{sale_id}/sandals/{sandal_id}/")
async def remove_sandal_sale(
    sale_id: str, sandal_id: str, engine: AIOEngine = Depends(get_engine)
):
    return await sale.delete_sandalSale(
        engine=engine, sale_id=sale_id, sandal_id=sandal_id
    )


@router.put("/{sale_id}/finished")
async def finished_sale(sale_id: str, engine=Depends(get_engine)):
    return await sale.finished_sale(sale_id, engine=engine)


@router.get("/media_quantity/sandals")
async def media_quantity_sandal(
    start_date: date = Query(None, ge=date(2023, 1, 1), le=date(2024, 12, 31)),
    end_date: date = Query(None, ge=date(2023, 1, 1), le=date(2024, 12, 31)),
    engine=Depends(get_engine),
):
    """
    Calcula a quantidade média de sandálias por venda em um intervalo de tempo.

    Args:
        start_date (str, opcional): Data de início no formato YYYY-MM-DD.
        end_date (str, opcional): Data de término no formato YYYY-MM-DD.
        session (AIOEngine): Sessão do banco de dados, injetada automaticamente pelo FastAPI.

    Returns:
        Quantidade média de sandálias por venda.
    """
    return await sale.media_quantity_sandal(start_date, end_date, engine)


@router.get("/count/total")
async def count(
    start_date=None, end_date=None, engine: AIOEngine = Depends(get_engine)
):
    return await sale.count_date(start_date, end_date, engine)
