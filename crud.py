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

def add_transaction_db(userid, trade_time, money_currency, coin_currency, initial_money_amount, final_money_amount, initial_coin_amount, final_coin_amount, money_coin_rate, buy_boolean):
    add_transaction = "INSERT INTO transaction (userid, trade_time, money_currency, coin_currency, initial_money_amount, final_money_amount, initial_coin_amount, final_coin_amount, money_coin_rate, buy_boolean) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    transaction_info = (userid, trade_time, money_currency, coin_currency, initial_money_amount, final_money_amount, initial_coin_amount, final_coin_amount, money_coin_rate, buy_boolean)
    my_cursor.execute(add_transaction, transaction_info)
    mydb.commit()


def add_user_balance_db(userid, amount, currency):
    add_user_balance = "INSERT INTO user_balance (userid, amount, currency) VALUES (%s, %s, %s)"
    user_balance_info = (userid, amount, currency)
    my_cursor.execute(add_user_balance, user_balance_info)
    mydb.commit()

#add_transaction_db(2, "2021-09-16 03:07:00", "USD", "BTC", 1000, 200, 0, 10, 80,True)
#add_user_db("Jang","Minho", "jijiji", "minho1693@gmail.com")
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

#get_user_db(1)

def get_transaction_db(id):
    get_transaction = "SELECT * FROM transaction WHERE id = {0}".format(id)
    my_cursor.execute(get_transaction)
    get_transaction_info = my_cursor.fetchall()

    print("\nPrinting each column of the id {0}".format(id))
    for column in get_transaction_info:
        print("ID = ", column[0])
        print("UserID = ", column[1])
        print("Trade Time  = ", column[2])
        print("Money Currency  = ", column[3])
        print("Coin Currency  = ", column[4])
        print("Initial Balance (EUR)  = ", column[5])
        print("Final Balance (EUR)  = ", column[6])
        print("Initial Coin amount (EA)  = ", column[7])
        print("Final Coin amount (EA)  = ", column[8])        
        print("Money Coin Rate (EUR/EA)  = ", column[9])
        print("Purchasing action TRUE or NOT  = ", column[10])

def get_user_balance_db(id):
    get_user_balance = "SELECT * FROM user_balance WHERE userid = {0}".format(id)
    my_cursor.execute(get_user_balance)
    get_user_info = my_cursor.fetchall()

    print("\nPrinting each column of the userid {0}".format(id))
    for column in get_user_info:
        print("User ID = ", column[0], )
        print("Amount (EUR) = ", column[1])
        print("Currency  = ", column[2])

#get_transaction_db(1)
#get_user_balance_db(1)

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

#update_user_balance_db("amount", 100, 1, "BTC")


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
