import json, config, math
from flask import Flask, request, jsonify, render_template
from binance.client import Client
from binance.enums import *
from decimal import Decimal as D, ROUND_DOWN, ROUND_UP
import decimal
import logging
logging.getLogger().setLevel(logging.DEBUG)

# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
# logging.basicConfig(handlers=[logging.FileHandler(filename="./log_records.txt", encoding='utf-8', mode='a+')],format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%F %A %T", level=logging.INFO)

app = Flask(__name__)

client = Client(config.API_KEY, config.API_SECRET)

def round_step_size(quantity,step_size):
    # step_size_dec = D(str(size))
    if step_size == 1.0:
        return math.floor(quantity)
    elif step_size < 1.0:
        return D(f'{quantity}').quantize(D(f'{step_size}'), rounding=ROUND_DOWN)

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

def order(side, quantity, symbol, price, order_type=ORDER_TYPE_LIMIT):
    try:
        logging.info(f"sending {symbol}-{order_type} order - {side} {quantity} DOGE coins @ {price} USDT ")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity, price=price, timeInForce=TIME_IN_FORCE_GTC)
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
        logging.error("- invalid passphrase")
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }

    side = data['strategy']['order_action'].upper()
    quantity = data['strategy']['order_contracts']
    price = data['strategy']['order_price']
    ticker = data['ticker']


    order_response = order(side, get_round_step_quantity(ticker,quantity), ticker, price)

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