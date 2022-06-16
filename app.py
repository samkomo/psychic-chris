import configparser
import json
import logging
import math
from binance_client import create_binance_order
from binance.exceptions import BinanceAPIException, BinanceOrderException
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from trading_bot import run_bot


config = configparser.ConfigParser()
config.read('config.cfg')

load_dotenv()

# instantiate the app
app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('index.html')


# webhook end point
@app.route('/webhook', methods=['POST'])
def webhook():
    # print(request.data)
    data = json.loads(request.data)
    print(config['GLOBAL']['WEBHOOK_PASSPHRASE'])
    if data['passphrase'] != config['GLOBAL']['WEBHOOK_PASSPHRASE']:
        logging.error("- invalid passphrase")
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }
    print(json.dumps(data, indent=2))

    response = run_bot(data)

    # if data['exchange'] == "BYBIT":
    # 	response = open_position(data)

    if isinstance(response, Exception):
        return {
            "code": response.code,
            "message": response.message
        }

    return json.dumps(response, indent=2)
