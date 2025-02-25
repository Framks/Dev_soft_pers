from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")

client = AsyncIOMotorClient(DATABASE_URL)
engine = AIOEngine(client=client, database="pratica3")


def get_engine() -> AIOEngine:
    return engine
