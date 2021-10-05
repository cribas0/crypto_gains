from typing import Optional
from pydantic import BaseModel

class UserSignUp(BaseModel):
    firstname: str
    lastname: str
    password: str
    email: str


class AddTransaction(BaseModel):
    userid: int    
    money_currency: str
    coin_currency: str
    traded_money_amount: float 
    traded_coin_amount: float
    IsBuy: bool

class UserMoneyCharge(BaseModel):
    userid: int
    amount: float
    currency: str


# para dar respuesta una vez ejecutado el POST
class StandardResponse(BaseModel):
    code: str 
    message: str

