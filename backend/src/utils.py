import asyncio
import json
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import Sequence
from src.TGClient import TGClient
from dotenv import load_dotenv
from src.crud.utils import initialise_db

load_dotenv()
dev = os.getenv("DEV")
client = TGClient(eval(dev))


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(initialise_db())
    client.start()

    yield
    client.stop()
