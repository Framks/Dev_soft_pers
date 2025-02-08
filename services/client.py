from sqlmodel import Session, select
from fastapi import HTTPException

from models.client import Client

def list(offset, limit, name_part, session: Session):
    """
    Lista os clientes com suporte a paginação e filtro parcial pelo nome.

    Args:
        offset (int): Número de registros a pular no início da listagem.
        limit (int): Número máximo de registros a retornar.
        name_part (str): Parte do nome para busca. Se None, retorna todos os clientes.
        session (Session): Sessão do banco de dados.

    Returns:
        list[Client]: Lista de clientes encontrados.
    """
    if name_part:
        search_term = f"%{name_part}%"
        return session.exec(select(Client).where(Client.name.like(search_term)).offset(offset).limit(limit)).all()
    else:
        return session.exec(select(Client).offset(offset).limit(limit)).all()

def create(client: Client,session: Session):
    """
    Cria um novo cliente.

    Args:
        client (Client): Dados do cliente a ser criado.
        session (Session): Sessão do banco de dados.

    Returns:
        Client: Cliente criado.

    Raises:
        HTTPException: Em caso de erro ao salvar o cliente.
    """
    try:
        session.add(client)
        session.commit()
        session.refresh(client)
        return client
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_by_id(client_id: int,session: Session):
    """
    Busca um cliente pelo ID.

    Args:
        client_id (int): ID do cliente a ser buscado.
        session (Session): Sessão do banco de dados.

    Returns:
        Client: Cliente encontrado, ou None se não existir.
    """
    return session.get(Client, client_id)

def update(client: Client,session: Session) -> Client:
    """
    Atualiza os dados de um cliente existente.

    Args:
        client (Client): Dados atualizados do cliente.
        session (Session): Sessão do banco de dados.

    Returns:
        Client: Cliente atualizado.

    Raises:
        HTTPException: Em caso de erro ao atualizar o cliente.
    """
    try:
        client_before = get_by_id(client.id)
        for key, value in client.model_dump().items():
            setattr(client_before, key, value)
        session.commit()
        return client_before
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def delete(client_id: int, session: Session):
    """
    Remove um cliente pelo ID.

    Args:
        client_id (int): ID do cliente a ser removido.
        session (Session): Sessão do banco de dados.

    Returns:
        Client: Cliente removido.

    Raises:
        HTTPException: Em caso de erro ao remover o cliente.
    """
    try:
        user = session.get(Client, client_id)
        session.delete(user)
        session.commit()
        return user
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
