import json
import configparser
import string
import ccxt

config = configparser.ConfigParser()
config.read('config.cfg')
# data = {
#     "passphrase": "abcdefgh",
#     "time": "2022-06-14T08:35:00Z",
#     "exchange": "BYBIT",
#     "ticker": "GMTUSDT",
#     "bar": {
#         "time": "2022-06-14T08:35:00Z",
#         "open": 0.6595,
#         "high": 0.6595,
#         "low": 0.6595,
#         "close": 0.6595,
#         "volume": 27.3
#     },
#     "strategy": {
#         "position_size": 20.714,
#         "order_action": "buy",
#         "order_contracts": 20.714,
#         "order_price": 0.50000,
#         "order_id": "Long",
#         "market_position": "long",
#         "market_position_size": 1518.714,
#         "prev_market_position": "flat",
#         "prev_market_position_size": 0
#     }
# }


def run_bot(data):
    exchange_id = data['exchange']
    exchange_class = getattr(ccxt, exchange_id.lower())
    exchange = ccxt.bitget()
   #  print(exchange.requiredCredentials)  # prints required credentials
   #  exchange.checkRequiredCredentials()  # raises AuthenticationError
    exchange = exchange_class({
        'apiKey': config[exchange_id]['API_KEY'],
        'secret': config[exchange_id]['API_SECRET'],
      #   'password': config[exchange_id]['PASSWORD']
    })

    symbol = data['ticker']
    side = data['strategy']['order_action']
    type = 'Limit'
    amount = data['strategy']['order_contracts']
    price = data['strategy']['order_price']

   #  markets = exchange.load_markets()
   #  for market in markets:
   #      if 'GMT' in market:
   #          print(market)
   #          print(json.dumps(exchange.fetch_ticker('GMT/USDT:USDT'), indent=2))

    if exchange.has['createOrder']:
      try:
         order = exchange.createOrder(symbol, type, side, amount, price)
      except Exception as e:
         print(e)
         return e

   #  print(json.dumps(exchange.has, indent=2))
    return order
    # order = exchange.createOrder(symbol, type, side, )


# print(exchange.fetch_balance())

# print(json.dumps(exchange.has, indent=2))
# for exchanges in ccxt.exchanges:
#     print(exchanges)
# exchange = ccxt.bybit()
# print(exchange.requiredCredentials)  # prints required credentials
# exchange.checkRequiredCredentials()  # raises AuthenticationError
# markets = exchange.load_markets()
# for market in markets:
#     if 'GMT' in market:
#         print(market)
# print(json.dumps(exchange.fetch_ticker('GMT/USDT:USDT'), indent=2))
# print(json.dumps(exchange.fetch_order_book('GMT/USDT:USDT'), indent=2))
# bot = run_bot(data)
# print(json.dumps(bot, indent=2))
