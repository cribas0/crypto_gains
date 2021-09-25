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
    initial_money_amount: float 
    final_money_amount: float
    initial_coin_amount: float
    final_coin_amount: float    
    IsBuy: bool

# para dar respuesta una vez ejecutado el POST
class StandardResponse(BaseModel):
    code: str 
    message: str

