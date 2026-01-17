from odmantic import AIOEngine, ObjectId
from fastapi import HTTPException
from datetime import datetime

from src.models.sale import Sale, SandalSale
from src.models.sandal import Sandal


async def list(offset: int, limit: int, engine: AIOEngine):
    sales = await engine.find(Sale, skip=offset, limit=limit)
    return sales


async def create(sale: Sale, engine: AIOEngine):
    sale_new = await engine.save(sale)
    return sale_new


async def get_by_id(sale_id: int, engine: AIOEngine):
    obj_id = ObjectId(sale_id)
    return await engine.find(Sale, Sale.id == obj_id)


async def update(sale_id, sale: Sale, engine: AIOEngine):
    db_sale = await get_by_id(sale_id, engine)
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")

    db_sale.finished = sale.finished
    db_sale.valor_total = sale.valor_total
    db_sale.sale_date = sale.sale_date

    await engine.save(db_sale)
    return db_sale


async def delete(sale_id: int, engine: AIOEngine):
    sale = await get_by_id(sale_id, engine)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")

    await engine.delete(sale)
    return {"ok": True}


async def add_sandal(
        sale_id: str, 
        sandal_id: str, 
        quantity: int, 
        engine: AIOEngine
        ):
    sale = await engine.find_one(Sale, Sale.id == ObjectId(sale_id))
    sandal = await engine.find_one(Sandal, Sandal.id == ObjectId(sandal_id))

    if not sale or not sandal:
        raise HTTPException(status_code=404, detail="Venda ou sandália não encontrada")

    sandal_sale = SandalSale(sandal=sandal, quantity=quantity)
    sale.sandalSales.append(sandal_sale)
    sale.valor_total += sandal.valor * quantity

    await engine.save(sale)
    return sale


async def delete_sandalSale(engine: AIOEngine, sale_id, sandal_id):
    try:
        sale = await engine.find_one(Sale, Sale.id == ObjectId(sale_id))
        if not sale:
            raise HTTPException(detail="Sale not found", status_code=404)
        sandal_sale = next(
            (s for s in sale.sandalSales if str(s.sandal.id) == sandal_id), None
        )
        if not sale:
            raise HTTPException(detail="SandalSale not found", status_code=404)
        sale.sandalSales.remove(sandal_sale)
        sale.valor_total -= sandal_sale.quantity * sandal_sale.sandal.valor
        return await engine.save(sale)
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


async def count_date(init_date, fin_date, engine: AIOEngine):
    try:
        result = None

        if init_date and fin_date:
            start = (
                init_date
                if isinstance(init_date, datetime)
                else datetime.strptime(init_date, "%Y-%m-%d")
            )
            end = (
                fin_date
                if isinstance(fin_date, datetime)
                else datetime.strptime(fin_date, "%Y-%m-%d")
            )

            result = await engine.count(
                Sale, Sale.sale_date >= start, Sale.sale_date <= end
            )
        else:
            result = await engine.count(Sale)

        return {"count": result}

    except Exception as e:
        print(e)
        raise HTTPException(detail=str(e), status_code=400)


async def media_quantity_sandal(
    engine: AIOEngine
):
    try:
        pipeline = [
            {"$project": {"total_quantity": {"$sum": "$sandalSales.quantity"}}},
            {"$group": {"_id": None, "average_quantity": {"$avg": "$total_quantity"}}},
            {"$project": {"_id": 0, "average_quantity": 1}},
        ]
        result = await engine.get_collection(Sale).aggregate(pipeline).to_list()
        return result[0]
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)


async def finished_sale(sale_id, engine: AIOEngine):
    sale = await engine.find_one(Sale, Sale.id == ObjectId(sale_id))

    if not sale:
        raise HTTPException(detail=f"Sale not found id={sale_id}", status_code=404)

    if sale.finished:
        raise HTTPException(detail="Sale already finished", status_code=400)

    sale.finished = True
    sale.sale_date = datetime.now()
    await engine.save(sale)
    return sale
