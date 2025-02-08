from sqlmodel import Session, select
from fastapi import HTTPException

from models.client import Sandal

def list(offset, limit, name_part, session: Session):
    """
    Lista todas as sandálias, com suporte para paginação e busca parcial pelo nome.

    Args:
        offset (int): Número de registros a serem ignorados (para paginação).
        limit (int): Número máximo de registros retornados.
        name_part (str): Parte do nome para busca (opcional).
        session (Session): Sessão do banco de dados.

    Returns:
        list[Sandal]: Lista de sandálias encontradas.
    """
    if name_part:
        search_term = f"%{name_part}%"
        return session.exec(select(Sandal).where(Sandal.name.like(search_term)).offset(offset).limit(limit)).all()
    else:
        return session.exec(select(Sandal).offset(offset).limit(limit)).all()

def create(client: Sandal,session: Session):
    """
    Cria uma nova sandália.

    Args:
        client (Sandal): Objeto Sandal contendo os dados da nova sandália.
        session (Session): Sessão do banco de dados.

    Returns:
        Sandal: Sandália criada.

    Raises:
        HTTPException: Caso ocorra um erro durante a criação.
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
    Obtém uma sandália pelo ID.

    Args:
        client_id (int): ID da sandália.
        session (Session): Sessão do banco de dados.

    Returns:
        Sandal: Sandália correspondente ao ID, ou None se não encontrada.
    """
    return session.get(Sandal, client_id)

def update(client: Sandal,session: Session) -> Sandal:
    """
    Atualiza uma sandália existente.

    Args:
        client (Sandal): Objeto Sandal com os dados atualizados.
        session (Session): Sessão do banco de dados.

    Returns:
        Sandal: Sandália atualizada.

    Raises:
        HTTPException: Caso ocorra um erro durante a atualização.
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
    Remove uma sandália pelo ID.

    Args:
        client_id (int): ID da sandália a ser removida.
        session (Session): Sessão do banco de dados.

    Returns:
        Sandal: Sandália removida.

    Raises:
        HTTPException: Caso ocorra um erro durante a exclusão.
    """
    try:
        user = session.get(Sandal, client_id)
        session.delete(user)
        session.commit()
        return user
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
