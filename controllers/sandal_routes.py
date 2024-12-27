from fastapi import APIRouter, Depends
from sqlmodel import Session

from database.database import get_Session
from models import Sandal
from repositories import SandalRepository
from services import SandalService


def get_sandal_service(session: Session = Depends(get_Session)):
    return SandalService(SandalRepository(session))

sandal_router = APIRouter(prefix="/sandals", tags=["sandals"])

@sandal_router.post("/", response_model=Sandal)
def create_sandal(sandal: Sandal, service = Depends(get_sandal_service)):
    """
    Cria uma nova sandália.

    Args:
        sandal (Sandal): Objeto contendo os dados da sandália.

    Returns:
        object: Resultado da operação de criação.
    """
    return service.create(sandal)

@sandal_router.get("/")
def list_sandal(service: SandalService = Depends(get_sandal_service)):
    """
    Lista todas as sandálias.

    Returns:
        List[object]: Lista de sandálias cadastradas.
    """
    return service.list()

@sandal_router.get("/{sandal_id}")
def search_sandal_id(sandal_id: int, service: SandalService = Depends(get_sandal_service)):
    """
    Busca uma sandália pelo ID.

    Args:
        sandal_id (int): ID da sandália a ser buscada.

    Returns:
        object: Sandália encontrada ou `None` se não encontrada.
    """
    return service.search_sandal(sandal_id)

@sandal_router.put("/{sandal_id}")
def update_sandal(sandal: Sandal, sandal_id: int, service: SandalService = Depends(get_sandal_service)):
    """
    Atualiza as informações de uma sandália existente.

    Args:
        sandal (Sandal): Objeto contendo os dados atualizados da sandália.
        sandal_id (int): ID da sandália a ser atualizada.

    Returns:
        object: Resultado da operação de atualização.
    """
    return service.update(sandal_id, sandal)

@sandal_router.delete("/{sandal_id}")
def delete_sandal(sandal_id: int, service: SandalService = Depends(get_sandal_service)):
    """
    Exclui uma sandália pelo ID.

    Args:
        sandal_id (int): ID da sandália a ser excluída.

    Returns:
        object: Resultado da operação de exclusão.
    """
    return service.delete(sandal_id)
