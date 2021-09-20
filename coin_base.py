from coinbase.wallet.client import Client


# BASIC configuration of COINBASE with API_KEY & SECRET
api_key = ''
api_secret = ''
client = Client(api_key, api_secret)


## The results are returned in JSON format

'''
{
  "data": {
    "amount": "1010.25",
    "currency": "USD"
  }
}
'''
def get_buy_price(Coin_currency, Base_currency):  
  buy_price = client.get_buy_price(currency_pair = str(Coin_currency) + "-" + str(Base_currency))
  buy_price_amount = buy_price.get("amount")
  print("The buy price is: " + buy_price_amount + " {0}/{1} .".format(Base_currency,Coin_currency))

def get_sell_price(Coin_currency, Base_currency):  
  sell_price = client.get_sell_price(currency_pair = str(Coin_currency) + "-" + str(Base_currency))
  sell_price_amount = sell_price.get("amount")
  print("The sell price is: " + sell_price_amount + " {0}/{1} .".format(Base_currency,Coin_currency))


get_buy_price("BTC","USD")
get_sell_price("BTC","USD")

# Get SELL PRICE API
#price = client.get_sell_price(currency_pair = 'BTC-USD')

# Get SPOT (CURRENT) PRICE API
#price = client.get_spot_price(currency_pair = 'BTC-USD')



