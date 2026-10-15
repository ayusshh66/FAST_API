from fastapi import FastAPI

app = FastAPI(
    title="Pincode lookup API",
    description="Auto fill city and state pincode of India during checkout"
)

@app.get("/")
def intro():
    return{
         "message":"server is up abd running!"
    }


