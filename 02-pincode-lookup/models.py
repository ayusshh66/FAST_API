from pydantic import BaseModel, field_validator

class PincodeRequest(BaseModel):
    pincode:str

    #pincode must be 6 only
    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls,value):
        if len(value) != 6 or not value.isdigit():
            raise ValueError("pincode must be exactly 6 digit")
        return value

class locationResponse(BaseModel):
    pincode:str
    city:str
    state:str
    district:str

class BulkRequest(BaseModel):
    pincodes : list[str]

    @field_validator("pincodes")
    @classmethod
    def validate_pincodes(cls, values):
        if len(values) == 0:
            raise ValueError("atleast 1 pincode should be there")
        if len(values)>20:
            raise ValueError("maximum limit is 20")

        for code in values:
            if len(code) != 6 or not code.isdigit():
                raise ValueError("pincode must be exactly 6!")
        return values;
        
class BulkResponse(BaseModel):
    status : str = "success"
    found : int
    not_found : int
    results : list[locationResponse] 
    missing : list[str]