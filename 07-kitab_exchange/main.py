from fastapi import FastAPI
from database import create_tables
from routes import book, users

import models

app = FastAPI(
    title="api for bookstore",
    description="a simple api bookstore",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    create_tables()

app.include_router(book.router)
app.include_router(users.router)

@app.get("/")
def check():
    return {
        "message": "everything is up and running"
    }