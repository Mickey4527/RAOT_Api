from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting")
    await init_db()
    yield
    print("server is shutting down")


app = FastAPI(
    title="Test",
    version="0.1.0",
    description="This is a test project",
    lifespan=lifespan,
)
