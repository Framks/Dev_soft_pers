from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy import event, Engine
import sqlite3
#import logging
import os
from dotenv import load_dotenv

#logging.basicConfig()
#logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

load_dotenv()

db_url = os.getenv("DATABASE_URL")

if not db_url:
    db_url = "sqlite:///database.db"
    print("\n\nO ACESSO AO BANCO DE DADOS NÃO FOI POSSÍVEL. \n\nUtilizaremos o padrão.\n\n")

engine = create_engine(db_url,connect_args={"detect_types":1},echo=True)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if type(dbapi_connection) is sqlite3.Connection:  # somente para o SQLite
       cursor = dbapi_connection.cursor()
       cursor.execute("PRAGMA foreign_keys=ON")
       cursor.close()