from odmantic import AIOEngine
from fastapi import HTTPException
from typing import Optional, List
from odmantic import ObjectId

from src.models.client import Client


async def get_all(
    offset: int, 
    limit: int, 
    name_part: Optional[str], 
    engine: AIOEngine
    ) -> List[Client]:
    query = {}
    if name_part:
        query = {"name": {"$regex": f".*{name_part}.*", "$options": "i"}}  # Regex case-insensitive

    clients = await engine.find(Client, query, skip=offset, limit=limit)
    return clients


async def create(client: Client, engine: AIOEngine) -> Client:
    try:
        client = await engine.save(client)
        return client
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def get_by_id(client_id: str, engine: AIOEngine) -> Optional[Client]:
    obj_id = ObjectId(client_id)
    return await engine.find_one(Client, Client.id == obj_id)


async def update(client_id: str, client_data: Client, engine: AIOEngine) -> Client:
    client = await get_by_id(client_id, engine)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    client.name = client_data.name
    client.email = client_data.email

    try:
        await engine.save(client)
        return client
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def delete(client_id: str, engine: AIOEngine):
    try:
        client = await get_by_id(client_id, engine)
        if not client:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        await engine.delete(client)
        return client
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
