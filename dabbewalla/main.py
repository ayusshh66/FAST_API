from contextlib import asynccontextmanager
from fastapi import FastAPI

from dabbewalla.database import create_tables


@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    print("table has been created")
    yield 
    print("application shutdown")

