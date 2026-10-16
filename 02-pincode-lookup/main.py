
from fastapi import FastAPI
from fastapi.requests import Request

from exceptions import (
    invalid_pincode_handler,
    InvalidPincodeError,
    pincode_not_found_handler,
    PinCodeNotFoundError,
)
from models import (locationResponse, PincodeRequest, BulkRequest, BulkResponse)
from data import pincode_db

app = FastAPI(
    title="Pincode Lookup API",
    description="Auto fill city and state pincode of India during checkout"
)

app.add_exception_handler(
    InvalidPincodeError,
    invalid_pincode_handler
)

app.add_exception_handler(
    PinCodeNotFoundError,
    pincode_not_found_handler
)


@app.get("/")
def intro():
    return {
        "message": "Server is up and running!"
    }

@app.get("/pincode/{code}",response_model=locationResponse)
def lookup_pincode(code:str):
    if len(code) != 6 or not code.isdigit():
        raise InvalidPincodeError(code, "code must be 6 digit")

    if code not in pincode_db:
        raise PinCodeNotFoundError(code)
    return pincode_db[code]

@app.get("/pincode/bulk", response_model=BulkResponse)
def bulk_lookup(request:BulkRequest):
    results = []
    missing=[]

    for code in request.pincodes:
        if code in pincode_db:
            results.append(pincode_db[code])
        else :
            missing.append(code)
            
    return BulkResponse(
        found=len(results),
        not_found = len(missing),
        results = results,
        missing = missing,
    )