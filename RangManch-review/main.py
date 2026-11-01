from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_table
from routes.reviews import router as reviews_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    """creates table if its not created"""
    create_table()
    print("database table has been created")
    yield
    print("shutting down the app")

app = FastAPI(
    title="rangmanch db",
    description="api for pune theatre rangmanch",
    lifespan=lifespan
)

app.include_router(reviews_router)


@app.get("/")
def root():
    return {
        "message":"initilizing api"
    }


    