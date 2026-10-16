
from fastapi import Request
from fastapi.responses import JSONResponse


class PinCodeNotFoundError(Exception):
    def __init__(self, pincode: str):
        self.pincode = pincode


class InvalidPincodeError(Exception):
    def __init__(self, pincode: str, reason: str = "invalid pincode"):
        self.pincode = pincode
        self.reason = reason


# Custom exception handlers

async def pincode_not_found_handler(
    req: Request,
    exc: PinCodeNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={
            "error": "pincode_not_found",
            "message": f"No location found for pincode {exc.pincode}",
            "pincode": exc.pincode
        }
    )


async def invalid_pincode_handler(
    req: Request,
    exc: InvalidPincodeError
):
    return JSONResponse(
        status_code=400,
        content={
            "error": "invalid_pincode",
            "message": f"Pincode is not valid: {exc.pincode}",
            "pincode": exc.pincode,
            "reason": exc.reason
        }
    )
