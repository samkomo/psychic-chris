import json
import configparser
import string
import ccxt
import logging

# instantiate 
logging.getLogger().setLevel(logging.DEBUG)
config = configparser.ConfigParser()
config.read('config.cfg')

def run_bot(data):
    exchange_id = data['exchange']
    exchange_class = getattr(ccxt, exchange_id.lower())

    exchange = exchange_class({
        'apiKey': config[exchange_id]['API_KEY'],
        'secret': config[exchange_id]['API_SECRET'],
        #   'password': config[exchange_id]['PASSWORD']
    })

    try:
        symbol = data['ticker']
        side = data['strategy']['order_action']
        type = 'market'
        amount = data['strategy']['order_contracts']
        price = data['strategy']['order_price']
        stop_loss = data['strategy']['alert_message']['stop_loss']
        take_profit = data['strategy']['alert_message']['take_profit']
        leverage = data['strategy']['alert_message']['leverage']
    except Exception as e:
            print("=========Error============")
            print(e)
            # return e

    params = {'stop_loss': stop_loss, 'take_profit':take_profit}

    if exchange.has['setLeverage']:
        try:
            exchange.setLeverage(leverage, symbol, params = {"marginMode": "isolated"})
        except Exception as e:
            print("=========Info============")
            print(e)

    if exchange.has['createOrder']:
        try:
            logging.info(f"sending {side}-{type} order - {amount} {symbol}  coins @ {price} USDT")
            order = exchange.createOrder(symbol, type, side, amount, price, params)
            return order
        except Exception as e:
            print("=========Error============")
            print(e)
 
# bot = run_bot(data)
# print(json.dumps(bot, indent=2))

    # exchange = ccxt.bitget()
   #  print(exchange.requiredCredentials)  # prints required credentials
   #  exchange.checkRequiredCredentials()  # raises AuthenticationError
   
# data = {
#         "passphrase":"abcdefgh",
#         "time":"2022-07-08T05:13:50Z",
#         "exchange":"BYBIT",
#         "ticker":"GMTUSDT",
#         "bar":{
#             "time":"2022-07-08T05:00:00Z",
#             "open":1.01021,
#             "high":1.01229,
#             "low":1.00734,
#             "close":1.00766,
#             "volume":331500.1
#         },
#         "strategy":{
#             "order_id":"Long Entry",
#             "order_action":"sell",
#             "order_contracts":10,
#             "order_price":1.01021,
#             "alert_message":{
#                 "stop_loss":0.9112452619,
#                 "take_profit":1.0444795809,
#                 "leverage":1
#             },
#             "market_position":"long",
#             "position_size":98.969,
#             "market_position_size":98.969,
#             "prev_market_position":"flat",
#             "prev_market_position_size":0
#         }
#     }



    # params={'triggerPrice':23240.00,'reduceOnly': True}

    # params={'stopLossPrice': stop_loss,'takeProfitPrice': take_profit}

    # params={'reduce_only': True}

    # params={
    #     # 'leverage': 3,
    #     'stopLossPrice': 23161,
    #     'takeProfitPrice': 23240,
    # }

      # exchange.setMarginMode('isolated', symbol, params = {"leverage": 5})

   #  markets = exchange.load_markets()
   #  for market in markets:
   #      if 'GMT' in market:
   #          print(market)
   #          print(json.dumps(exchange.fetch_ticker('GMT/USDT:USDT'), indent=2))

              # return e
        
    # if exchange.has['cancelOrder']:
    #     try:
    #         # logging.info(f"sending {side}-{type} order - {amount} {symbol}  coins @ {price} USDT")
    #         order = exchange.cancelOrder(1129777491,symbol)
    #     except Exception as e:
    #         print(e)
    #         return e

    # # print(json.dumps(exchange.has, indent=2))
    
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