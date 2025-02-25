from fastapi import FastAPI
import logging

from src.routes import home, sale, sandal, client

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()

app.include_router(home.router)
app.include_router(client.router)
app.include_router(sandal.router)
app.include_router(sale.router)