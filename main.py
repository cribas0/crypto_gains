from fastapi import FastAPI, Path, HTTPException, status
from requests.sessions import Request
from crud import *
#from crud import (add_user_db,add_transaction_db, delete_transaction_db, delete_user_balance_db, get_transaction_db,get_user_db,get_user_balance_db,delete_user_db,add_user_balance_db, delete_user_balance_db, delete_transaction_db)
from coin_base import (get_buy_price, get_sell_price)
from pydantic_models import (UserSignUp, AddTransaction, StandardResponse, UserMoneyCharge)

app = FastAPI()

@app.post("/sign_up")
def SignUpUser(RequestBody: UserSignUp): 
    try:
        add_user_db(RequestBody)
    except:
        raise HTTPException (
            status_code = status.HTTP_409_CONFLICT,
            detail = (
                ("The email address already exists")
            )
        ) 
    return StandardResponse(code = "Success", message = "User created successfully")
 

@app.post("/add_transaction")
def addTransaction(RequestBody: AddTransaction): 
    try:
        add_transaction_db(RequestBody)
    except:
        raise HTTPException (
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = (
                ("Please check again the operation")
            )
        )
    return StandardResponse(code = "Success", message = "Transaction done successfully")

@app.post("/credit_charge")
def addUserBalanceDB(RequestBody: UserMoneyCharge):
    try:
        add_user_balance_db(RequestBody)
    except:
            raise HTTPException (
                status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail = (
                    ("Please check again the input data")
                )
            )
    return StandardResponse(code = "Success", message = "Credit charge done successfully")


@app.get("/get_buy_price/{coin_currency}/{base_currency}")
def GetBuyPrice(coin_currency: str, base_currency: str):
    return (get_buy_price(coin_currency,base_currency))

@app.get("/get_sell_price/{coin_currency}/{base_currency}")
def GetSellPrice(coin_currency: str, base_currency: str):
    return (get_sell_price(coin_currency,base_currency))


@app.get("/get_user_by_id/{user_id}")
def GetUserInfo(user_id: int):
    return(get_user_db(user_id))

@app.get("/get_user_transaction_by_id/{user_id}")
def GetUserTransactionByID(user_id: int):
    return(get_transaction_db(user_id))


@app.get("/get_user_balance_by_id/{user_id}")
def GetUserBalanceInfo(user_id: int):
    return(get_user_balance_db(user_id))

@app.delete("/delete_user_by_id/{user_id}")
def DeleteUserInfo(user_id: int):
    try:
        delete_user_db(user_id)
        delete_transaction_db(user_id)
        delete_user_balance_db(user_id)
    except:
        raise HTTPException (
            status_code = status.HTTP_409_CONFLICT,
            detail = ("This User ID does not exist")
        )
    return StandardResponse(code = "Success", message = "User deleted successfully")
