import json, config, math
from flask import Flask, request, jsonify, render_template
from binance.client import Client
from binance.enums import *
from decimal import Decimal as D, ROUND_DOWN, ROUND_UP
import decimal
import logging

app = Flask(__name__)

client = Client(config.API_KEY, config.API_SECRET)

def round_step_size(quantity,step_size):
    # step_size_dec = D(str(size))
    if step_size == 1.0:
        return math.floor(quantity)
    elif step_size < 1.0:
        return Decimal(f'{quantity}').quantize(Decimal(f'{step_size}'), rounding=ROUND_DOWN)

def get_round_step_quantity(symbol, qty):
    info = client.get_symbol_info(symbol)
    for x in info["filters"]:
        if x["filterType"] == "LOT_SIZE":
            minQty = float(x["minQty"])
            maxQty = float(x["maxQty"])
            stepSize= float(x["stepSize"])
    if qty < minQty:
        qty = minQty
    return round_step_size(qty, minQty)

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        logging.error("Error occurred while placing order > {}".format(e.message))
        return e

    return order

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    #print(request.data)
    data = json.loads(request.data)
    
    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }

    side = data['strategy']['order_action'].upper()
    quantity = data['strategy']['order_contracts']
    ticker = data['ticker']


    order_response = order(side, get_round_step_quantity(ticker,quantity), ticker)

    if isinstance(order_response, Exception) :
        return {
            "code": order_response.code,
            "message": order_response.message
        }
    else:
        return {
            "status": order_response['status'],
            "fills": order_response['fills']
        }