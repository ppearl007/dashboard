from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Union
from uuid import uuid4

class ItemSchema(BaseModel):
    uid: Union[int, str, uuid4]
    # uid: str = Field(default_factory=uuid4)
    PN: str 
    Desc: str
    QtyStock: int
    MOQ: int
    Price: float
    LT: float
    
try:
    ItemSchema()
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))

class UpdateItemModel(BaseModel):
    uid: Optional[Union[int, str, uuid4]]
    # uid: str = Field(default_factory=uuid4)
    PN: Optional[str]
    Desc: Optional[str]
    QtyStock: Optional[int]
    MOQ: Optional[int]
    Price: Optional[float]
    LT: Optional[float]
    

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}