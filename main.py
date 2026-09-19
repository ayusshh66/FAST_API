from typing import Optional
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello(arg: Optional[str] = None):
    return {
        "message": "HI",
        "arg_passed": arg
    }

if __name__ == "__main__":
    uvicorn.run("main:app", port=8001, reload=True)
