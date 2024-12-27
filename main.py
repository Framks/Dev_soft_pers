from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.exceptions import ValidationException

from controllers import router_client, sale_router, sandal_router
from database.database import create_db_and_tables
from exceptions import not_found_exception, invalid_argument_exception, InvalidArgumentException, OperationalException, \
    NotFoundException, operational_exception, validation_exception_handle, exception_handle


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
app = FastAPI(lifespan=lifespan, description="API para gerenciar vendas de sandalias com SQLite e SQLModel")

## APP INCLUDE ROUTERS
app.include_router(router_client)
app.include_router(sale_router)
app.include_router(sandal_router)


## EXCEPTION HANDLES ADD
app.add_exception_handler(NotFoundException, not_found_exception)
app.add_exception_handler(InvalidArgumentException, invalid_argument_exception)
app.add_exception_handler(OperationalException, operational_exception)
app.add_exception_handler(ValidationException, validation_exception_handle)
app.add_exception_handler(Exception, exception_handle)
