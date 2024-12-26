from fastapi import FastAPI

from controllers import ClientRoutes
from controllers import DataRoutes
from controllers import SandalRoutes
from controllers import SalesRoutes
from repositories import ClientRepository, SandalRepository, SaleRepository
from services import ClientService, SandalService, SaleService, DataService
from utils.paths import CLIENT_CSV, SANDAL_CSV, SALE_CSV, CSV_FILES_PATH, ZIP_FILES_PATH


app = FastAPI()

# Repositories
client_repository = ClientRepository(CLIENT_CSV)
sandal_repository = SandalRepository(SANDAL_CSV)
sale_repository = SaleRepository(SALE_CSV, sandal_repository, client_repository)

# Services
data_service = DataService(CSV_FILES_PATH, ZIP_FILES_PATH)

# Controllers
client_controller = ClientRoutes(ClientService(client_repository))
sandal_controller = SandalRoutes(SandalService(sandal_repository))
sale_controller = SalesRoutes(SaleService(sale_repository))
data_controller = DataRoutes(data_service)


app.include_router(client_controller.router)
app.include_router(sandal_controller.router)
app.include_router(sale_controller.router)
app.include_router(data_controller.router)
