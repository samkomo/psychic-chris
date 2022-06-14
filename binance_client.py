import json, config, math
from binance.client import Client
from binance.enums import *
from decimal import Decimal as D, ROUND_DOWN, ROUND_UP
import logging

binance = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)
logging.getLogger().setLevel(logging.DEBUG)


def round_step_size(quantity,step_size):
    # step_size_dec = D(str(size))
    if step_size == 1.0:
        return math.floor(quantity)
    elif step_size < 1.0:
        return D(f'{quantity}').quantize(D(f'{step_size}'), rounding=ROUND_DOWN)

def round_tick_size(price,tick_size):
    # step_size_dec = D(str(size))
    return D(f'{price}').quantize(D(f'{tick_size}'), rounding=ROUND_DOWN)
    

def get_price_precision(info, price):    
    for x in info["filters"]:
        if x["filterType"] == "PRICE_FILTER":
            minPrice = float(x["minPrice"])
            maxPrice = float(x["maxPrice"])
            tickSize= float(x["tickSize"])
    if price < minPrice:
        price = minPrice
    return round_tick_size(price, tickSize)

def get_round_step_quantity(info, qty):
    for x in info["filters"]:
        if x["filterType"] == "LOT_SIZE":
            minQty = float(x["minQty"])
            maxQty = float(x["maxQty"])
            stepSize= float(x["stepSize"])
    if qty < minQty:
        qty = minQty
    return round_step_size(qty, stepSize)
# ORDER_TYPE_LIMIT, ORDER_TYPE_MARKET
def create_binance_order(data, order_type=ORDER_TYPE_LIMIT):
    try:
        side = data['strategy']['order_action'].upper()
        ticker = data['ticker']
        info = binance.get_symbol_info(ticker)
        # print(info)
        quantity = get_round_step_quantity(info,data['strategy']['order_contracts']) 
        # precision = get_quantity_precision()
        price = get_price_precision(info, data['strategy']['order_price'])

        logging.info(f"sending {ticker}-{order_type} order - {side} {quantity} {info['baseAsset']} coins @ {price} {info['quoteAsset']} ")
        order = binance.create_order(symbol=ticker, side=side, type=order_type, quantity=quantity, price=price, timeInForce=TIME_IN_FORCE_GTC)

        # order = binance.create_order(symbol=ticker, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        logging.error("ORDER: Error occurred while placing order > {}".format(e.message))
        return e
    print(json.dumps(order,indent=2))
    return order        