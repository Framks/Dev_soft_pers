from fastapi import APIRouter, Depends, Query
from odmantic import AIOEngine

from src.models.client import Client
from database import get_engine
from src.services import client
from src.constants import constants

router = APIRouter(prefix="/clients", tags=["Clients"])

engine = get_engine()


@router.get("/")
async def list(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=constants.MAX_LENGTH_LIMIT),
    name_part: str = None,
):
    return await client.get_all(
        offset=offset, limit=limit, name_part=name_part, engine=engine
    )


@router.post("/")
async def create(client_post: Client):
    return await client.create(client_post, engine)


@router.get("/{client_id}", response_model=Client)
async def read_client(client_id: str):
    return await client.get_by_id(client_id=client_id, engine=engine)


@router.put("/{client_id}", response_model=Client)
async def update_client(client_id: str, client_put: Client):
    return await client.update(client_id, client_put, engine)


@router.delete("/{client_id}")
async def delete_client(client_id: str, engine: AIOEngine = Depends(get_engine)):
    return await client.delete(client_id, engine)
