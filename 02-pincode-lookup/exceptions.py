from fastapi.responses import JSONResponse
from fastapi import Request

class PinCodeNotFoundError(Exception):
    def __init__(self,pincode:str):
        self.pincode = pincode

class InvalidPincodeError(Exception):
    def __init__(self,pincode:str, reason:str = "invalid pincode"):
        self.pincode=pincode
        self.reason = reason

#custom handler

async def pincode_not_found_handler(req:Request, exc:PinCodeNotFoundError):
    return JSONResponse(
        status_code=404,
        content = {
            "error":"pincode_not_found",
            "message":f"no location for pincode {exc.pincode}",
            "pincode":exc.pincode,
        }
    )

async def invalid_pincode_handler(req:Request, exc:InvalidPincodeError):
    return JSONResponse(
        status_code=404,
        content = {
            "error":"invalid pincode",
            "message":f"pincode is not valid {exc.pincode}",
            "pincode":exc.pincode,
            "reason": exc.reason,
        }
    )