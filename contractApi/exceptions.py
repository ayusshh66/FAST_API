from fastapi.responses import JSONResponse
from fastapi import Request

class orderId_error(Exception):
    def __init__(self, orderId:str):
        self.orderId=orderId

class invalid_orderId(Exception):
    def __init__(self, orderId:str, reason : str):
        self.orderId = orderId
        self.reason = reason

async def orderId_error_handler(req:Request, exc: orderId_error):
    return JSONResponse(
        status_code=404,
        content = {
            "message":"order not found",
            "error": f"no order found with this order Id : {exc.orderId}",
            "orderId" : f"{exc.orderId}"    
        }
    )

async def invalid_orderId_handler(req:Request, exc : invalid_orderId):
    return JSONResponse(
        status_code=400,
        content = {
            "error" : f"invalid orderId {exc.orderId}",
            "reason" : f"{exc.reason}"
        }
    )