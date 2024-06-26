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
dev = int(os.getenv("DEV"))
session_path = os.getenv("SESSION_PATH")
client = TGClient(dev, session_path)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(initialise_db())
    client.start()

    yield
    client.stop()
