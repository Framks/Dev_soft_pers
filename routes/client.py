from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from models.client import Client
from database import get_session

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)

@router.get("/")
def list(offset: int = 0, limit:int = 10, name_part:str = None, session: Session = Depends(get_session)):
    """
    Lista todos os clientes cadastrados no sistema.

    Args:
        offset (int): Quantidade de registros a pular no início da listagem.
        limit (int): Número máximo de registros a serem retornados.
        name_part (str, opcional): Parte do nome para filtrar os clientes. Padrão é None.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.

    Returns:
        list: Lista de objetos do tipo 'Client'.
    """
    return session.exec(select(Client)).all()

@router.post("/")
def create(client: Client,session: Session = Depends(get_session)):
    """
    Cria um novo cliente.

    Args:
        client (Client): Dados do cliente a ser criado.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.

    Returns:
        Client: Objeto do cliente criado.
    """
    session.add(client)
    session.commit()
    session.refresh(client)
    return client

@router.get("/{client_id}", response_model=Client)
def read_client(client_id: int, session: Session = Depends(get_session)):
    """
    Obtém os detalhes de um cliente pelo ID.

    Args:
        client_id (int): ID do cliente a ser consultado.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.

    Raises:
        HTTPException: Se o cliente não for encontrado.

    Returns:
        Client: Objeto do cliente encontrado.
    """
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{client_id}", response_model=Client)
def update_client(client_id: int, client: Client, session: Session = Depends(get_session)):
    """
    Atualiza as informações de um cliente existente.

    Args:
        client_id (int): ID do cliente a ser atualizado.
        client (Client): Dados atualizados do cliente.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.

    Raises:
        HTTPException: Se o cliente não for encontrado.

    Returns:
        Client: Objeto do cliente atualizado.
    """
    db_client = session.get(Client, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    for key, value in client.model_dump(exclude_unset=True).items():
        setattr(db_client, key, value)
    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client

@router.delete("/{client_id}")
def delete_client(client_id: int, session: Session = Depends(get_session)):
    """
    Exclui um cliente do banco de dados.

    Args:
        client_id (int): ID do cliente a ser excluído.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.

    Raises:
        HTTPException: Se o cliente não for encontrado.

    Returns:
        dict: Indica o sucesso da operação com `{"ok": True}`.
    """
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="client not found")
    session.delete(client)
    session.commit()
    return {"ok": True}