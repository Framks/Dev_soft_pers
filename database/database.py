from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")

if not db_url:
    db_url = "sqlite:///database.db"
    print("O ACESSO AO BANCO DE DADOS NÃO FOI POSSÍVEL.")

engine = create_engine(db_url)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_Session() -> Session:
    with Session(engine) as session:
        yield session