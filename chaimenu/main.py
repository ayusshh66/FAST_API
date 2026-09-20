from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="chai point menu api",
    description="read only menu api"
)

@app.get("/")
def root():
    return {
        "message": "the server is up and running"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)