import json
import configparser
import sys
import time
import ccxt
import logging

# instantiate
logging.getLogger().setLevel(logging.DEBUG)
config = configparser.ConfigParser()
config.read('config.cfg')

# VARIABLES
SYMBOL = config['GRID']['SYMBOL']
GRID_SIZE = float(config['GRID']['GRID_SIZE'])
NUM_SELL_GRID_LINES = int(config['GRID']['NUM_SELL_GRID_LINES'])
NUM_BUY_GRID_LINES = int(config['GRID']['NUM_BUY_GRID_LINES'])
POSITION_SIZE = float(config['GRID']['POSITION_SIZE'])
CLOSED_ORDER_STATUS = config['GRID']['CLOSED_ORDER_STATUS']
CHECK_ORDERS_FREQUENCY = float(config['GRID']['CHECK_ORDERS_FREQUENCY'])

exchange = ccxt.binance(
    {
        'apiKey': config['BINANCE']['API_KEY'],
        'secret': config['BINANCE']['API_SECRET'],
    }
)

ticker = exchange.fetch_ticker(SYMBOL)
logging.debug(json.dumps(ticker, indent=2))

# grid = ["-"] * GRID_LEVELS

buy_orders = []
sell_orders = []

initial_buy_order = exchange.create_market_buy_order(SYMBOL, POSITION_SIZE * NUM_SELL_GRID_LINES)

for i in range(NUM_BUY_GRID_LINES):
    price = ticker['bid'] - (GRID_SIZE * (i+0.01))
    print("submitting market limit buy order at {}".format(price))
    order = exchange.create_limit_buy_order(SYMBOL, POSITION_SIZE, price)
    buy_orders.append(order['info'])

for i in range(NUM_SELL_GRID_LINES):
    price = ticker['bid'] + (GRID_SIZE * (i+1))
    print("submitting market limit sell order at {}".format(price))
    order = exchange.create_limit_sell_order(SYMBOL, POSITION_SIZE, price)
    sell_orders.append(order['info'])

while True:
    closed_order_ids = []

    for buy_order in buy_orders:
        print("checking buy order {}".format(buy_order['orderId']))
        try:
            order = exchange.fetch_order(buy_order['orderId'])
        except Exception as e:
            print("request failed, retrying")
            continue
            
        order_info = order['info']

        if order_info['status'] == CLOSED_ORDER_STATUS:
            closed_order_ids.append(order_info['orderId'])
            print("buy order executed at {}".format(order_info['price']))
            new_sell_price = float(order_info['price']) + GRID_SIZE
            print("creating new limit sell order at {}".format(new_sell_price))
            new_sell_order = exchange.create_limit_sell_order(SYMBOL, POSITION_SIZE, new_sell_price)
            sell_orders.append(new_sell_order)

        time.sleep(CHECK_ORDERS_FREQUENCY)

    for sell_order in sell_orders:
        print("checking sell order {}".format(sell_order['orderId']))
        try:
            order = exchange.fetch_order(sell_order['orderId'])
        except Exception as e:
            print("request failed, retrying")
            continue
            
        order_info = order['info']

        if order_info['status'] == CLOSED_ORDER_STATUS:
            closed_order_ids.append(order_info['orderId'])
            print("sell order executed at {}".format(order_info['price']))
            new_buy_price = float(order_info['price']) - GRID_SIZE
            print("creating new limit buy order at {}".format(new_buy_price))
            new_buy_order = exchange.create_limit_buy_order(SYMBOL, POSITION_SIZE, new_buy_price)
            buy_orders.append(new_buy_order)

        time.sleep(CHECK_ORDERS_FREQUENCY)

    for order_id in closed_order_ids:
        buy_orders = [buy_order for buy_order in buy_orders if buy_order['orderId'] != order_id]
        sell_orders = [sell_order for sell_order in sell_orders if sell_order['orderId'] != order_id]

    if len(sell_orders) == 0:
        sys.exit("stopping bot, nothing left to sell")
