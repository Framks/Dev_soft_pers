from fastapi import APIRouter, Depends
from sqlmodel import Session

from models.sale import Sale,  SaleWithClientSandals
from database import get_session
from services import sale

router = APIRouter(
    prefix="/sales",
    tags=["sales"]
)

@router.get("/", response_model=list[SaleWithClientSandals])
def list(offset: int = 0, limit:int = 10, session: Session = Depends(get_session)):
    """
    Lista as vendas realizadas.

    Args:
        offset (int, opcional): Quantidade de registros a pular no início da listagem. Padrão é 0.
        limit (int, opcional): Número máximo de registros a serem retornados. Padrão é 10.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.

    Returns:
        list: Lista de vendas, incluindo clientes e sandálias.
    """
    return sale.list(offset, limit, session)

@router.post("/", response_model=SaleWithClientSandals)
def create(sale_create: Sale,session: Session = Depends(get_session)):
    """
    Cria uma nova venda.

    Args:
        sale_create (Sale): Dados da venda a ser criada.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.

    Returns:
        SaleWithClientSandals: Objeto da venda criada com detalhes de cliente e sandálias.
    """
    return sale.create(sale_create, session)

@router.get("/{sale_id}", response_model=SaleWithClientSandals)
def read_sale(sale_id: int, session: Session = Depends(get_session)):
    """
    Obtém os detalhes de uma venda pelo ID.

    Args:
        sale_id (int): ID da venda a ser consultada.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.

    Returns:
        SaleWithClientSandals: Detalhes da venda encontrada.
    """
    return sale.get_by_id(sale_id, session)

@router.put("/{sale_id}", response_model=SaleWithClientSandals)
def update_sale(sale_id: int, sale_update: Sale, session: Session = Depends(get_session)):
    """
    Atualiza os dados de uma venda existente.

    Args:
        sale_id (int): ID da venda a ser atualizada.
        sale_update (Sale): Dados atualizados da venda.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.

    Returns:
        SaleWithClientSandals: Venda atualizada.
    """
    return sale.update(sale_id, sale_update, session)

@router.delete("/{sale_id}")
def delete_sale(sale_id: int, session: Session = Depends(get_session)):
    """
    Remove uma venda.

    Args:
        sale_id (int): ID da venda a ser removida.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.

    Returns:
        dict: Indica o sucesso da operação com `{"ok": True}`.
    """
    return sale.delete(sale_id, session)

@router.post("/{sale_id}/sandals/{sandal_id}/", response_model=SaleWithClientSandals)
def add_sandal_sale(sale_id:int, sandal_id:int, quantity: int = 1, session: Session = Depends(get_session)):
    """
    Adiciona sandálias a uma venda.

    Args:
        sale_id (int): ID da venda.
        sandal_id (int): ID da sandália.
        quantity (int, opcional): Quantidade de sandálias a serem adicionadas. Padrão é 1.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.

    Returns:
        SaleWithClientSandals: Venda atualizada com as sandálias adicionadas.
    """
    return sale.add_sandal(sale_id, sandal_id, quantity, session)

@router.delete("/{sale_id}/sandals/{sandal_id}/", response_model=SaleWithClientSandals)
def remove_sandal_sale(sale_id:int, sandal_id:int, session: Session = Depends(get_session)):
    """
    Remove uma sandália de uma venda.

    Args:
        sale_id (int): ID da venda.
        sandal_id (int): ID da sandália.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.

    Returns:
        SaleWithClientSandals: Venda atualizada com a sandália removida.
    """
    return sale.delete_sandalSale(session, sale_id, sandal_id)

@router.put("/{sale_id}/finished")
def finished_sale(sale_id: int, session = Depends(get_session)):
    """
    Finaliza uma venda.

    Args:
        sale_id (int): ID da venda a ser finalizada.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.

    Returns:
        dict: Indica o sucesso da operação com `{"ok": True}`.
    """
    return sale.finished_sale(sale_id, session)

@router.get("/media_quantity/sandals")
def media_quantity_sandal(start_date = None, end_date = None, session = Depends(get_session)):
    """
    Calcula a quantidade média de sandálias por venda em um intervalo de tempo.

    Args:
        start_date (str, opcional): Data de início no formato YYYY-MM-DD.
        end_date (str, opcional): Data de término no formato YYYY-MM-DD.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.

    Returns:
        Quantidade média de sandálias por venda.
    """
    return sale.media_quantity_sandal(start_date, end_date, session)

@router.get("/count/total")
def count(start_date = None, end_date = None, session: Session = Depends(get_session)):
    """
    Conta o total de vendas em um intervalo de tempo.

    Args:
        start_date (str, opcional): Data de início no formato YYYY-MM-DD.
        end_date (str, opcional): Data de término no formato YYYY-MM-DD.
        session (Session): Sessão do banco de dados, injetada automaticamente pelo FastAPI.

    Returns:
        int: Total de vendas realizadas no período.
    """
    return sale.count_date(start_date, end_date, session)