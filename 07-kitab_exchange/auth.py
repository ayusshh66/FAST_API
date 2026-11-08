from fastapi import Header, HTTPException

API_KEY="my_xyz_api_key"

def verify_api(x_api_key:str=Header()):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=404, detail="invalid api key")
    return x_api_key