from fastapi import APIRouter, Depends, Query
from odmantic import AIOEngine

from src.models.sandal import Sandal
from database import get_engine
from src.constants import constants
from src.services import sandal

router = APIRouter(prefix="/sandals", tags=["Sandals"])


@router.get("/")
async def list(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=constants.MAX_LENGTH_LIMIT),
    name_part: str = None,
    engine: AIOEngine = Depends(get_engine),
):
    return await sandal.list(
        offset=offset, limit=limit, name_part=name_part, engine=engine
    )


@router.post("/")
async def create(sandal_post: Sandal,engine: AIOEngine = Depends(get_engine)):
    return await sandal.create(sandal_post, engine)


@router.get("/{sandal_id}", response_model=Sandal)
async def read_sandal(sandal_id: str, engine: AIOEngine = Depends(get_engine)):
    return await sandal.get_by_id(sandal_id=sandal_id, engine=engine)


@router.put("/{sandal_id}", response_model=Sandal)
async def update_sandal(
    sandal_id: str, sandal_put: Sandal, engine: AIOEngine = Depends(get_engine)
):
    return await sandal.update(
        sandal_id=sandal_id, sandal_put=sandal_put, engine=engine
    )


@router.delete("/{sandal_id}")
async def delete_sandal(sandal_id: str, engine: AIOEngine = Depends(get_engine)):
    return await sandal.delete(sandal_id=sandal_id, engine=engine)
