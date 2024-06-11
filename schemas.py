from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id:Optional[int]
    username:str
    email:str
    password:str
    address:str
    is_staff:Optional[bool]

    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                "username":"johndoe",
                "email":"johndoe@gmail.com",
                "password":"password",
                "address":"address",
                "is_staff":False,
            }
        }


class Settings(BaseModel):
    authjwt_secret_key:str='6938d4cdd34230829edd94c521565c0af91f2d173d0f792e5d4c20d19360b98b'

class LoginModel(BaseModel):
    username:str
    password:str

class OrderModel(BaseModel):
    id:Optional[int]
    quantity:int
    order_status:Optional[str]="ON-TRANSIT"
    dimensions:Optional[str]="2 * 2"
    user_id:Optional[int]


    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "quantity":2,
                "dimensions":"2 * 2"
            }
        }

class OrderStatusModel(BaseModel):
    order_status:Optional[str]="IN-TRANSIT"

    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "order_status":"In Tansition"
            }
        }