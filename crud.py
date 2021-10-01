import mysql.connector
import json
from pydantic_models import (UserSignUp, AddTransaction)
from datetime import datetime
from coin_base import get_buy_price, get_sell_price

now = datetime.now()
date_time = now.strftime("%Y-%m-%d %H:%M:%S")
#print(date_time)

with open('secret/credentials.json') as json_file:
    data = json.load(json_file)

# Connect to MySQL
mydb = mysql.connector.connect(
    host = "localhost",
    user = data["MySQL_credentials"]['user'],
    password = data["MySQL_credentials"]['password'],
    database = 'testdb'
)

my_cursor = mydb.cursor()

# How to create a database in MySQL
#my_cursor.execute("CREATE DATABASE testdb") <- no need to repeat once it is already created -> once created, put the database name inside "mydb"


## ADD USER/TRANSACTION FUNCTION

def add_user_db(UserSignUp: UserSignUp) -> None:
    add_user = "INSERT INTO users (lastname, firstname, password, email) VALUES (%s, %s, %s, %s)"
    user_info = (UserSignUp.lastname, UserSignUp.firstname, UserSignUp.password, UserSignUp.email)
    my_cursor.execute(add_user, user_info)
    mydb.commit()


# add_transaction_with pydantic
def add_transaction_db(AddTransaction: AddTransaction) -> None:
    add_transaction = "INSERT INTO transaction (userid, trade_time, money_currency, coin_currency, initial_money_amount, final_money_amount, initial_coin_amount, final_coin_amount, money_coin_rate, IsBuy) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    initial_money_amount = float(get_user_balance_byCurrency_db(AddTransaction.userid, AddTransaction.money_currency)) 
    initial_coin_amount = float(get_user_balance_byCurrency_db(AddTransaction.userid, AddTransaction.coin_currency))
            
    if AddTransaction.IsBuy == True:
        money_coin_rate = float(get_buy_price(AddTransaction.coin_currency,AddTransaction.money_currency))
        final_money_amount = initial_money_amount - AddTransaction.traded_money_amount
        final_coin_amount = initial_coin_amount + AddTransaction.traded_money_amount/money_coin_rate
        update_user_balance_db("amount",final_money_amount,AddTransaction.userid,AddTransaction.money_currency)
        update_user_balance_db("amount",final_coin_amount,AddTransaction.userid,AddTransaction.coin_currency)
    else: 
        money_coin_rate = float(get_sell_price(AddTransaction.coin_currency,AddTransaction.money_currency))
        final_coin_amount = initial_coin_amount - AddTransaction.traded_coin_amount
        final_money_amount = initial_money_amount + AddTransaction.traded_coin_amount*money_coin_rate
        update_user_balance_db("amount",final_money_amount,AddTransaction.userid,AddTransaction.money_currency)
        update_user_balance_db("amount",final_coin_amount,AddTransaction.userid,AddTransaction.coin_currency)

    transaction_info = (AddTransaction.userid, date_time, AddTransaction.money_currency, AddTransaction.coin_currency, initial_money_amount, final_money_amount, initial_coin_amount, final_coin_amount, money_coin_rate, AddTransaction.IsBuy)
    my_cursor.execute(add_transaction, transaction_info)
    mydb.commit()

def add_user_balance_db(userid, amount, currency):
    add_user_balance = "INSERT INTO user_balance (userid, amount, currency) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE userid = %s, amount = amount + %s, currency = %s"
    user_balance_info = (userid, amount, currency,userid, amount, currency)
    my_cursor.execute(add_user_balance, user_balance_info)
    mydb.commit()


#add_user_balance_db(1,5000,"KRW")

#add_transaction_db(3, "2021-09-16 03:07:00", "USD", "BTC", 1000, 200, 0, 10, 80,True)
#add_user_db("Jang","Minho", "jijiji", "minho1693@gmail.com")
#add_user_balance_db(1,80,"BTC")

## READ USER/TRANSACTION FUNCTION BY ID

def get_user_db(id):
    get_user = "SELECT * FROM users WHERE id = {0}".format(id)
    my_cursor.execute(get_user)
    get_user_info = my_cursor.fetchall()
    return get_user_info
 

#get_user_db(1)

def get_transaction_db(id):
    get_transaction = "SELECT * FROM transaction WHERE id = {0}".format(id)
    my_cursor.execute(get_transaction)
    get_transaction_info = my_cursor.fetchall()
    return get_transaction_info

    print("\nPrinting each column of the id {0}".format(id))
    for column in get_transaction_info:
        print("ID = ", column[0])
        print("UserID = ", column[1])
        print("Trade Time  = ", column[2])
        print("Initial Currency  = ", column[3])
        print("Final Currency  = ", column[4])
        print("Initial Balance (EUR)  = ", column[5])
        print("Final Balance (EUR)  = ", column[6])
        print("Initial Coin amount (EA)  = ", column[7])
        print("Final Coin amount (EA)  = ", column[8])        
        print("Money Coin Rate (EUR/EA)  = ", column[9])
        print("Purchasing action TRUE(1) or NOT(0)  = ", column[10])

#get_transaction_db(1)

def get_user_balance_db(id):
    get_user_balance = "SELECT * FROM user_balance WHERE userid = {0}".format(id)
    my_cursor.execute(get_user_balance)
    get_user_balance_info = my_cursor.fetchall()
    return get_user_balance_info

#get_user_balance_db(1)


def get_user_balance_byCurrency_db(id,currency):
    get_user_balance_byCurrency = 'SELECT * FROM user_balance WHERE userid = {0} AND currency = "{1}"'.format(id,currency)
    my_cursor.execute(get_user_balance_byCurrency)
    get_user_balance_info = my_cursor.fetchall()    

    #if the requested currency does not exist, create those ones in the user_balance_DB 
    if not get_user_balance_info: 
        add_user_balance_db(id,0,currency)
    for x in get_user_balance_info:
        return x[1]

#get_user_balance_byCurrency_db(1,"ETH")

## EDIT USER/TRANSACTION FUNCTION BY ID, COLUMN_NAME AND ITEM

def update_user_db(column_name, item, id):
    update_user ="""UPDATE users SET `{0}` = %s WHERE id = %s""".format(column_name) # <- SQL columns inside ` ` and solve it wz format
    update_user_info = (item, id)    
    my_cursor.execute(update_user,update_user_info)
    mydb.commit()

def update_transaction_db(column_name, item, id):
    update_transaction ="""UPDATE transaction SET `{0}` = %s WHERE id = %s""".format(column_name) # <- SQL columns inside ` ` and solve it wz format
    update_transaction_info = (item, id)    
    my_cursor.execute(update_transaction,update_transaction_info)
    mydb.commit()

#update_transaction_db('money_currency', 'EUR', 1)

# Here, both id and currency MUST match in order to change the value correctly (currency ==> UNIQUE)
def update_user_balance_db(column_name, item, id, currency):
    update_user ="""UPDATE user_balance SET `{0}` = %s WHERE userid = %s AND currency = %s """.format(column_name) # <- SQL columns inside ` ` and solve it wz format
    update_user_info = (item, id, currency)    
    my_cursor.execute(update_user,update_user_info)
    mydb.commit()    



#update_user_balance_db("amount", 10000, 1, "EUR")


## DELETE USER/TRANSACTION BY ID 

def delete_user_db(id): 
    delete_user = "DELETE FROM users WHERE id = " + str(id)
    my_cursor.execute(delete_user)
    mydb.commit()

def delete_transaction_db(id):
    delete_transaction = "DELETE FROM transaction WHERE id = " + str(id)
    my_cursor.execute(delete_transaction)
    mydb.commit()

def delete_user_balance_db(id): 
    delete_user_balance = "DELETE FROM user_balance WHERE id = " + str(id)
    my_cursor.execute(delete_user_balance)
    mydb.commit()

#delete_transaction_db(2)
#delete_user_db(4)
