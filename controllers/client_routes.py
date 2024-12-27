from fastapi import APIRouter, Depends
from sqlmodel import Session

from models import Client
from repositories import ClientRepository
from services import ClientService
from database.database import get_Session


def get_client_service(session: Session = Depends(get_Session)):
    return ClientService(ClientRepository(session))

router_client = router=APIRouter(prefix="/clients", tags=["clients"])

@router_client.post("/", response_model=Client)
def create_client( client: Client, service: ClientService = Depends(get_client_service)):
    """
    Cria um novo cliente.

    Args:
        client (Client): Objeto contendo os dados do cliente a ser criado.
        service

    Returns:
        object: Resultado da operação de criação.
    """
    return service.create(client)

@router_client.get("/")
def list_client(service: ClientService = Depends(get_client_service)):
    """
    Lista todos os clientes.

    Returns:
        List[object]: Lista de clientes cadastrados.
    """
    return service.list()

@router_client.get("/{client_id}", response_model=Client)
def search_client_id(client_id: int, service: ClientService = Depends(get_client_service)):
    """
    Busca um cliente pelo ID.

    Args:
        client_id (int): ID do cliente a ser buscado.

    Returns:
        object: Cliente encontrado ou `None` se não encontrado.
    """
    return service.search_client(client_id)

@router_client.put("/{client_id}", response_model=Client)
def update_client(client: Client, client_id: int, service: ClientService = Depends(get_client_service)):
    """
    Atualiza as informações de um cliente existente.

    Args:
        client (Client): Objeto contendo os dados atualizados do cliente.
        client_id (int): ID do cliente a ser atualizado.

    Returns:
        object: Resultado da operação de atualização.
    """
    return service.update(client_id, client)

@router_client.delete("/{client_id}", response_model=Client)
def delete_client(client_id: int, service: ClientService = Depends(get_client_service)):
    """
    Exclui um cliente pelo ID.

    Args:
        client_id (int): ID do cliente a ser excluído.

    Returns:
        object: Resultado da operação de exclusão.
    """
    return service.delete(client_id)
