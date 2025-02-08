from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from models.sandal import Sandal
from database import get_session

router = APIRouter(
    prefix="/sandals",
    tags=["Sandals"]
)

@router.get("/")
def list(offset: int = 0, limit:int = 10, name_part:str = None, session: Session = Depends(get_session)):
    """
    Lista as sandálias, com paginação e opção de filtro parcial por nome.

    Args:
        offset (int): Quantidade de registros a pular. Padrão: 0.
        limit (int): Quantidade máxima de registros a retornar. Padrão: 10.
        name_part (str, opcional): Parte do nome para buscar.
        session (Session): Sessão do banco de dados.

    Returns:
        list: Lista de sandálias.
    """
    return session.exec(select(Sandal)).all()

@router.post("/")
def create(sandal: Sandal,session: Session = Depends(get_session)):
    """
    Cria uma nova sandália.

    Args:
        sandal (Sandal): Dados da sandália a ser criada.
        session (Session): Sessão do banco de dados.

    Returns:
        Sandal: A sandália criada.
    """
    session.add(sandal)
    session.commit()
    session.refresh(sandal)
    return sandal

@router.get("/{sandal_id}", response_model=Sandal)
def read_sandal(sandal_id: int, session: Session = Depends(get_session)):
    """
    Obtém os detalhes de uma sandália pelo ID.

    Args:
        sandal_id (int): ID da sandália.
        session (Session): Sessão do banco de dados.

    Returns:
        Sandal: A sandália encontrada.
    """
    sandal = session.get(Sandal, sandal_id)
    if not sandal:
        raise HTTPException(status_code=404, detail="Sandal not found")
    return sandal

@router.put("/{sandal_id}", response_model=Sandal)
def update_sandal(sandal_id: int, sandal: Sandal, session: Session = Depends(get_session)):
    """
    Atualiza os dados de uma sandália.

    Args:
        sandal_id (int): ID da sandália a ser atualizada.
        sandal (Sandal): Dados atualizados.
        session (Session): Sessão do banco de dados.

    Returns:
        Sandal: Sandália atualizada.
    """
    db_sandal = session.get(Sandal, sandal_id)
    if not db_sandal:
        raise HTTPException(status_code=404, detail="Sandal not found")
    for key, value in sandal.model_dump(exclude_unset=True).items():
        setattr(db_sandal, key, value)
    session.add(db_sandal)
    session.commit()
    session.refresh(db_sandal)
    return db_sandal

@router.delete("/{sandal_id}")
def delete_sandal(sandal_id: int, session: Session = Depends(get_session)):
    """
    Remove uma sandália pelo ID.

    Args:
        sandal_id (int): ID da sandália a ser removida.
        session (Session): Sessão do banco de dados.

    Returns:
        dict: Indicação de sucesso com `{"ok": True}`.
    """
    sandal = session.get(Sandal, sandal_id)
    if not sandal:
        raise HTTPException(status_code=404, detail="sandal not found")
    session.delete(sandal)
    session.commit()
    return {"ok": True}