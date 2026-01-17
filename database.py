from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
import os
from dotenv import load_dotenv

#DATABASE_URL="mongodb+srv://galvesa9:hCKeMh2NK12FxpSF@clusterqa.ibgf7.mongodb.net/pratica_3?retryWrites=true&w=majority&appName=ClusterQa"
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

client = AsyncIOMotorClient(DATABASE_URL)
engine = AIOEngine(client=client, database="pratica3")


def get_engine() -> AIOEngine:
    return engine
