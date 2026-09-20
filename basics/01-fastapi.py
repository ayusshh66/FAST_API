from fastapi import FastAPI
from fastapi import Request
import uvicorn

app = FastAPI(
    title = "dashboard service",
    description= ("gives cool 3d dashboard"
                    "and much more UI/UX stuff"
    ),
    version = "1.2.1",
    docs_url="/docs",
    redoc_url="/redocs",
    openapi_url="/openapi.json",
)

@app.get("/")
def hello():
    """hi all """
    return {
        "message" : "what is up guys!"
    }

@app.get("/info")
async def request_info(req:Request):
    """just extracting info from url"""
    return {
        "method" : req.method,
        "header" : dict(req.headers),
        "query" : req.query_params,
        "params" :dict( req.path_params),
    }

@app.get(
    "/activity/info",
    summary="get activity in detail",
    description=(
        "idk waht to write"
        "im just exploring it "
    ), 
    tags=["ollalal"],
    deprecated=False,
    response_description="this is response description"
)
def get_activity():
    """this is activity """
    return {
        "message": "hi g"
    }

if __name__ == "__main__":
    uvicorn.run("01-fastapi:app", reload=True)
