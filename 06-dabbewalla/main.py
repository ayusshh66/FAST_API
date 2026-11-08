from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes.orders import router as order_router
from routes.stats import router as stats_router
from .database import create_tables


@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    print("table has been created")
    yield 
    print("application shutdown")

app = FastAPI(
    title = "dabbele wala",
    description="API for dabbewala deliviries",
    version = " 1.0.0",
    lifespan=lifespan
)

app.include_router(order_router)
app.include_router(stats_router)

app.get("/health", tags=["health", "checkup"])
def healt_check():
    return {
        "message" : "server is up and running"
    }

