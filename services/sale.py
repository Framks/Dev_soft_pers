from sqlmodel import Session, select, func
from sqlalchemy.sql.functions import count
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from datetime import datetime

from models.sale import Sale, SandalSale
from models.sandal import Sandal

def list(offset, limit, session: Session):
    """
    Lista todas as vendas com suporte à paginação.

    Args:
        offset (int): Número de vendas a pular no início da listagem.
        limit (int): Número máximo de vendas a retornar.
        session (Session): Sessão do banco de dados.

    Returns:
        list[Sale]: Lista de vendas encontradas.
    """
    statement = (select(Sale).offset(offset).limit(limit)).options(joinedload(Sale.client),
                 joinedload(Sale.sandal_sales))
    return session.exec(statement).unique().all()

def create(sale: Sale,session: Session):
    """
    Cria uma nova venda.

    Args:
        sale (Sale): Dados da venda a ser criada.
        session (Session): Sessão do banco de dados.

    Returns:
        Sale: Venda criada.

    Raises:
        HTTPException: Em caso de erro ao criar a venda.
    """
    try:
        session.add(sale)
        sale.sale_date = datetime.fromisoformat(sale.sale_date)
        session.commit()
        session.refresh(sale)
        return sale
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_by_id(sale_id: int,session: Session):
    """
    Busca uma venda pelo ID.

    Args:
        sale_id (int): ID da venda a ser buscada.
        session (Session): Sessão do banco de dados.

    Returns:
        Sale: Venda encontrada.

    Raises:
        HTTPException: Caso a venda não seja encontrada.
    """
    statement = (select(Sale).where(Sale.id == sale_id)
                 .options(
                     joinedload(Sale.client),
                     joinedload(Sale.sandal_sales))
                     )
    sale = session.exec(statement).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale

def update(sale_id, sale: Sale, session: Session):
    """
    Atualiza uma venda existente.

    Args:
        sale_id (int): ID da venda a ser atualizada.
        sale (Sale): Dados atualizados da venda.
        session (Session): Sessão do banco de dados.

    Returns:
        Sale: Venda atualizada.

    Raises:
        HTTPException: Caso a venda não seja encontrada ou haja erro na atualização.
    """
    db_sale = session.get(Sale, sale_id)
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    for key, value in sale.model_dump(exclude_unset=True).items():
        setattr(db_sale, key, value)
    session.add(db_sale)
    session.commit()
    session.refresh(db_sale)
    return db_sale

def delete(sale_id: int, session: Session):
    """
    Remove uma venda pelo ID.

    Args:
        sale_id (int): ID da venda a ser removida.
        session (Session): Sessão do banco de dados.

    Returns:
        dict: Indica se a operação foi bem-sucedida.

    Raises:
        HTTPException: Caso a venda não seja encontrada.
    """
    sale = session.get(Sale, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(sale)
    session.commit()
    return {"ok": True}

def add_sandal(sale_id:int, sandal_id:int, quantity:int, session: Session, sandal_sale: SandalSale):
    """
    Adiciona uma sandália a uma venda.

    Args:
        sale_id (int): ID da venda.
        sandal_id (int): ID da sandália.
        quantity (int): Quantidade da sandália.
        session (Session): Sessão do banco de dados.

    Returns:
        Sale: Venda atualizada.

    Raises:
        ValueError: Caso a venda ou sandália não seja encontrada.
    """
    sale = session.get(Sale, sale_id)
    sandal = session.get(Sandal, sandal_id)

    if not sale or not sandal:
        raise ValueError("Venda ou sandália não encontrada")
    
    sandal_sale = SandalSale(sale_id=sale_id, sandal_id=sandal_id, quantity=quantity)
    session.add(sandal_sale)
    sale.valor_total += sandal.valor * quantity

    session.commit()
    session.refresh(sale)

    return sale

def delete_sandalSale(session: Session, sale_id, sandal_id):
    """
    Remove uma relação de sandália de uma venda.

    Args:
        session (Session): Sessão do banco de dados.
        sale_id (int): ID da venda.
        sandal_id (int): ID da sandália.

    Returns:
        bool: Indica se a operação foi bem-sucedida.

    Raises:
        HTTPException: Em caso de erro na remoção.
    """
    try:
        sandal_sale = session.exec(select(SandalSale).where(SandalSale.sale_id == sale_id and SandalSale.sandal_id == sandal_id))
        session.delete(sandal_sale)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise HTTPException(detail=str(e), status_code=400)

def count_date(init_date, fin_date, session: Session):
    """
    Conta as vendas realizadas entre duas datas.

    Args:
        init_date (str): Data inicial no formato YYYY-MM-DD.
        fin_date (str): Data final no formato YYYY-MM-DD.
        session (Session): Sessão do banco de dados.

    Returns:
        int: Número de vendas no período.

    Raises:
        HTTPException: Em caso de erro.
    """
    try:
        if init_date and fin_date:
            start = datetime.strptime(init_date, "%Y-%m-%d")
            end = datetime.strptime(fin_date, "%Y-%m-%d")
            return session.exec(select(count(Sale.id)).where((Sale.sale_date >= start) & (Sale.sale_date <= end))).one()
        else:
            return session.exec(select(count(Sale.id))).one()
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=400)

def media_quantity_sandal( start_date: datetime, end_date: datetime, session: Session):
    """
    Calcula a média de quantidade de sandálias vendidas em um período.

    Args:
        start_date (str): Data inicial no formato YYYY-MM-DD.
        end_date (str): Data final no formato YYYY-MM-DD.
        session (Session): Sessão do banco de dados.

    Returns:
        float: Média de quantidade de sandálias por venda.
    """
    if start_date and end_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        sub_search= (
            select(SandalSale.sale_id, func.sum(SandalSale.quantity).label("quantity_sale"))
            .join(Sale, Sale.id == SandalSale.sale_id)
            .where(Sale.sale_date.between(start, end))
            .group_by(SandalSale.sale_id)
            .subquery()
        )
    else:
        sub_search= (
            select(SandalSale.sale_id, func.sum(SandalSale.quantity).label("quantity_sale"))
            .join(Sale)
            .group_by(SandalSale.sale_id)
            .subquery()
        )
    print("\n\n CONSULTA \n")
    result = session.exec(select(func.avg(sub_search.c.quantity_sale).label("media_quantity_sale"))).first()
    return result

def finished_sale(sale_id, session: Session):
    """
    Finaliza uma venda, marcando-a como concluída.

    Args:
        sale_id (int): ID da venda a ser finalizada.
        session (Session): Sessão do banco de dados.

    Returns:
        Sale: Venda finalizada.

    Raises:
        HTTPException: Caso a venda não seja encontrada ou já esteja finalizada.
    """
    sale = session.get(Sale, sale_id)
    if not sale:
        raise HTTPException(detail=f"Sale not found id={sale_id}",status_code=404)
    if sale.finished:
        raise HTTPException(detail="sale id === Sale already finished", status_code=400)
    sale.finished = True
    update(sale_id, sale, session)
    return sale 