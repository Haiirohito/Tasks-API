import os

from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from colorama import Fore, Style

from app.api.task_routes import router as task_router

env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)


@asynccontextmanager
async def lifespan(app: FastAPI):
    uri = os.getenv("MONGO_URI")
    client = AsyncIOMotorClient(uri, server_api=ServerApi("1"))

    try:
        await client.admin.command("ping")
        print(f"{Fore.MAGENTA}DATABASE:{Style.RESET_ALL} Database connected ...")
    except Exception as e:
        print(f"{Fore.MAGENTA}DATABASE:{Style.RESET_ALL} Database connection error ...")
        raise e

    app.state.mongo_client = client
    yield
    client.close()
    print(f"{Fore.MAGENTA}DATABASE:{Style.RESET_ALL} Database connection terminated ...")


app = FastAPI(lifespan=lifespan)


app.include_router(task_router, prefix="/tasks", tags=["Tasks"])
