from fastapi import FastAPI
from contextlib import asynccontextmanager

from controllers import SandalRoutes
from controllers import router_client
from controllers import SalesRoutes
from database.database import create_db_and_tables
from repositories import SandalRepository, SaleRepository
from services import ClientService, SandalService, SaleService

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
app = FastAPI(lifespan=lifespan, description="API para gerenciar vendas de sandalias com SQLite e SQLModel")

app.include_router(router_client)
#app.include_router(sandal_controller.router)
#app.include_router(sale_controller.router)
