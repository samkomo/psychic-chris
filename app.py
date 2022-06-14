import json, config, math, logging
from flask import Flask, request, jsonify, render_template
from pybit import usdt_perpetual
from bybit import open_position, parse_webhook
from binance_client import create_binance_order
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
# instantiate the app
app = Flask(__name__)




@app.route('/')
def welcome():
    return render_template('index.html')


# webhook end point
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
    print(json.dumps(data,indent=2))

    if data['exchange'] == "BINANCE":
    	response = create_binance_order(data)
    	

    if data['exchange'] == "BYBIT":
    	response = open_position(data)

    if isinstance(response, BinanceAPIException):
	    return {
	    	"code": response.code,
	    	"message": response.message
	    }
    return {
	    	"code": "200",
	    	"message": "success"
	    }




