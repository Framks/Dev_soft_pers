from fastapi import APIRouter, Depends
from sqlmodel import Session

from database.database import get_Session
from models import Sale
from repositories import SaleRepository, SandalRepository, ClientRepository
from services import SaleService, SandalService, ClientService


def get_sale_service(session: Session = Depends(get_Session)) -> SaleService:
    return SaleService(SaleRepository(session), ClientService(ClientRepository(session)), SandalService(SandalRepository(session)))

sale_router = APIRouter(prefix="/sales", tags=["sales"])

@sale_router.post("/")
def create_sale( sale: Sale,service = Depends(get_sale_service)):
    """
    Cria uma nova venda.

    Args:
        sale (Sale): Objeto contendo os dados da venda.

    Returns:
        object: Resultado da operação de criação.
    """
    return service.create(sale)

@sale_router.get("/")
def list_sale(service = Depends(get_sale_service)):
    """
    Lista todas as vendas.

    Returns:
        List[object]: Lista de vendas cadastradas.
    """
    return service.list()

@sale_router.get("/{sale_id}")
def search_sale_id( sale_id: int,service = Depends(get_sale_service)):
    """
    Busca uma venda pelo ID.

    Args:
        sale_id (int): ID da venda a ser buscada.

    Returns:
        object: Venda encontrada ou `None` se não encontrada.
    """
    return service.search_sale(sale_id)

@sale_router.put("/{sale_id}")
def update_sale(sale: Sale, sale_id: int,service = Depends(get_sale_service)):
    """
    Atualiza as informações de uma venda existente.

    Args:
        sale (Sale): Objeto contendo os dados atualizados da venda.
        sale_id (int): ID da venda a ser atualizada.

    Returns:
        object: Resultado da operação de atualização.
    """
    return service.update(sale_id, sale)

@sale_router.delete("/{sale_id}")
def delete_sale(sale_id: int, service = Depends(get_sale_service)):
    """
    Exclui uma venda pelo ID.

    Args:
        sale_id (int): ID da venda a ser excluída.

    Returns:
        object: Resultado da operação de exclusão.
    """
    return service.delete(sale_id)

@sale_router.get("/total")
def count_sales(service = Depends(get_sale_service)):
    """
    Conta o número total de vendas registradas.

    Returns:
        int: Total de vendas registradas.
    """
    return service.count()

@sale_router.post("/{sale_id}/sandals/{sandal_id}/client/{client_id}")
def sale_sandal_for_client(sale_id: int,sandal_id: int,  client_id: int,quantity: int, service = Depends(get_sale_service)):
    return service.sale_sandal_for_client(sale_id, sandal_id, client_id,quantity)

@sale_router.get("/{sale_id}/sandals/")
def sandals_by_sale(sale_id: int, service = Depends(get_sale_service)):
    return service.sandals_by_sale(sale_id)
