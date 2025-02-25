from fastapi import HTTPException
from odmantic import AIOEngine, ObjectId, query
from src.models.sandal import Sandal


async def list(offset, limit, name_part, engine: AIOEngine):
    query = {}

    if name_part:
        query = {"nome":{"$regex": f".*{name_part}.*", "$options": "i"}}

    sandals = await engine.find(Sandal, query, skip=offset, limit=limit)
    return sandals


async def create(sandal: Sandal, engine: AIOEngine):
    try:
        return await engine.save(sandal)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def get_by_id(sandal_id: str, engine: AIOEngine):
    id = ObjectId(sandal_id)
    sandal = await engine.find_one(Sandal, Sandal.id == id)
    if not sandal:
        raise HTTPException(status_code=404, detail="Sandal not found")
    return sandal


async def update(
        sandal_id: str, 
        sandal_put: Sandal, 
        engine: AIOEngine
        ) -> Sandal:
    try:
        sandal_before = await get_by_id(sandal_id, engine)
        sandal_before.codigo = sandal_put.codigo
        sandal_before.nome = sandal_put.nome
        sandal_before.valor = sandal_put.valor
        sandal_before.cor = sandal_put.cor
        sandal_before.tamanho = sandal_put.tamanho

        sandal_before = await engine.save(sandal_before)
        return sandal_before
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def delete(sandal_id: int, engine: AIOEngine):
    try:
        sandal = await get_by_id(sandal_id, engine)
        if not sandal:
            raise HTTPException(status_code=404, detail="Sandal not found")
        await engine.delete(Sandal, query.field("id") == sandal_id)
        return {"msg": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
