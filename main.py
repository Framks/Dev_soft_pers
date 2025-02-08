from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import create_db_and_tables
from routes import home, client, sale, sandal

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(home.router)
app.include_router(client.router)
app.include_router(sandal.router)
app.include_router(sale.router)
