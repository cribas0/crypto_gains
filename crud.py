import mysql.connector
import json

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

def add_user_db(lastname, firstname, password, email):
    add_user = "INSERT INTO users (lastname, firstname, password, email) VALUES (%s, %s, %s, %s)"
    user_info = (lastname, firstname, password, email)
    my_cursor.execute(add_user, user_info)
    mydb.commit()

def add_buy_tx_db(userid, buy_time, buy_base_currency, buy_coin_currency, initial_balance, final_balance, initial_coin_amount, final_coin_amount, buy_price):
    add_buy_tx = "INSERT INTO buy_tx (userid, buy_time, buy_base_currency, buy_coin_currency, initial_balance, final_balance, initial_coin_amount, final_coin_amount, buy_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    buy_tx_info = (userid, buy_time, buy_base_currency, buy_coin_currency, initial_balance, final_balance, initial_coin_amount, final_coin_amount, buy_price)
    my_cursor.execute(add_buy_tx, buy_tx_info)
    mydb.commit()

def add_sell_tx_db(userid, sell_time, sell_base_currency, sell_coin_currency, initial_balance, final_balance, initial_coin_amount, final_coin_amount, sell_price):
    add_sell_tx = "INSERT INTO sell_tx (userid, sell_time, sell_base_currency, sell_coin_currency, initial_balance, final_balance, initial_coin_amount, final_coin_amount, sell_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    sell_tx_info = (userid, sell_time, sell_base_currency, sell_coin_currency, initial_balance, final_balance, initial_coin_amount, final_coin_amount, sell_price)
    my_cursor.execute(add_sell_tx, sell_tx_info)
    mydb.commit()

def add_user_balance_db(userid, amount, currency):
    add_user_balance = "INSERT INTO user_balance (userid, amount, currency) VALUES (%s, %s, %s)"
    user_balance_info = (userid, amount, currency)
    my_cursor.execute(add_user_balance, user_balance_info)
    mydb.commit()

#add_user_db("Jang","Minho", "jijiji", "minho1693@gmail.com")
#add_buy_tx_db(3, "2021-09-16 03:07:00", "USD", "BTC", 1000, 200, 0, 10, 80)
#add_sell_tx_db(3, "2021-09-16 03:07:00", "BTC", "USD", 200, 1000, 10, 0, 80)
#add_user_balance_db(1,80,"BTC")

## READ USER/TRANSACTION FUNCTION BY ID

def get_user_db(id):
    get_user = "SELECT * FROM users WHERE id = {0}".format(id)
    my_cursor.execute(get_user)
    get_user_info = my_cursor.fetchall()

    print("\nPrinting each column of the id {0}".format(id))
    for column in get_user_info:
        print("ID = ", column[0], ) # AUTO INCREMENT & PRIMARY KEY
        print("LastName = ", column[1])
        print("FirstName  = ", column[2])
        print("Password  = ", column[3])
        print("Email  = ", column[4]) # UNIQUE


get_user_db(1)

def get_buy_tx_db(id):
    get_buy_tx = "SELECT * FROM buy_tx WHERE id = {0}".format(id)
    my_cursor.execute(get_buy_tx)
    get_transaction_info = my_cursor.fetchall()

    print("\nPrinting each column of the id {0}".format(id))
    for column in get_transaction_info:
        print("ID = ", column[0])
        print("UserID = ", column[1])
        print("Buy Time  = ", column[2])
        print("Buy Base Currency  = ", column[3])
        print("Buy Coin Currency  = ", column[4])
        print("Initial Balance (EUR)  = ", column[5])
        print("Final Balance (EUR)  = ", column[6])
        print("Initial Coin amount (EA)  = ", column[7])
        print("Final Coin amount (EA)  = ", column[8])        
        print("Buy Price (EUR/EA)  = ", column[9])


def get_sell_tx_db(id):
    get_sell_tx = "SELECT * FROM sell_tx WHERE id = {0}".format(id)
    my_cursor.execute(get_sell_tx)
    get_transaction_info = my_cursor.fetchall()

    print("\nPrinting each column of the id {0}".format(id))
    for column in get_transaction_info:
        print("ID = ", column[0])
        print("UserID = ", column[1])
        print("Sell Time  = ", column[2])
        print("Sell Base Currency  = ", column[3])
        print("Sell Coin Currency  = ", column[4])
        print("Initial Balance (EUR)  = ", column[5])
        print("Final Balance (EUR)  = ", column[6])
        print("Initial Coin amount (EA)  = ", column[7])
        print("Final Coin amount (EA)  = ", column[8])        
        print("Sell Price (EUR/EA)  = ", column[9])

def get_user_balance_db(id):
    get_user_balance = "SELECT * FROM user_balance WHERE userid = {0}".format(id)
    my_cursor.execute(get_user_balance)
    get_user_info = my_cursor.fetchall()

    print("\nPrinting each column of the userid {0}".format(id))
    for column in get_user_info:
        print("User ID = ", column[0], )
        print("Amount (EUR) = ", column[1])
        print("Currency  = ", column[2])

#get_buy_tx_db(1)
#get_sell_tx_db(1)
#get_user_balance_db(1)

## EDIT USER/TRANSACTION FUNCTION BY ID, COLUMN_NAME AND ITEM

def update_user_db(column_name, item, id):
    update_user ="""UPDATE users SET `{0}` = %s WHERE id = %s""".format(column_name) # <- SQL columns inside ` ` and solve it wz format
    update_user_info = (item, id)    
    my_cursor.execute(update_user,update_user_info)
    mydb.commit()

def update_buy_tx_db(column_name, item, id):
    update_buy_tx ="""UPDATE buy_tx SET `{0}` = %s WHERE id = %s""".format(column_name) # <- SQL columns inside ` ` and solve it wz format
    update_buy_tx_info = (item, id)    
    my_cursor.execute(update_buy_tx,update_buy_tx_info)
    mydb.commit()

def update_sell_tx_db(column_name, item, id):
    update_sell_tx ="""UPDATE sell_tx SET `{0}` = %s WHERE id = %s""".format(column_name) # <- SQL columns inside ` ` and solve it wz format
    update_sell_tx_info = (item, id)    
    my_cursor.execute(update_sell_tx,update_sell_tx_info)
    mydb.commit()

# Here, both id and currency MUST match in order to change the value correctly (currency ==> UNIQUE)
def update_user_balance_db(column_name, item, id, currency):
    update_user ="""UPDATE user_balance SET `{0}` = %s WHERE userid = %s AND currency = %s """.format(column_name) # <- SQL columns inside ` ` and solve it wz format
    update_user_info = (item, id, currency)    
    my_cursor.execute(update_user,update_user_info)
    mydb.commit()    

#update_sell_tx_db('sell_base_currency', 'EUR', 1)
#update_user_balance_db("amount", 100, 1, "BTC")


## DELETE USER/TRANSACTION BY ID 

def delete_user_db(id): 
    delete_user = "DELETE FROM users WHERE id = " + str(id)
    my_cursor.execute(delete_user)
    mydb.commit()

def delete_buy_tx_db(id): 
    delete_buy_tx = "DELETE FROM buy_tx WHERE id = " + str(id)
    my_cursor.execute(delete_buy_tx)
    mydb.commit()

def delete_sell_tx_db(id): 
    delete_sell_tx = "DELETE FROM sell_tx WHERE id = " + str(id)
    my_cursor.execute(delete_sell_tx)
    mydb.commit()


def delete_user_balance_db(id): 
    delete_user_balance = "DELETE FROM user_balance WHERE id = " + str(id)
    my_cursor.execute(delete_user_balance)
    mydb.commit()

#delete_user_db(4)
#delete_buy_tx_db(1)