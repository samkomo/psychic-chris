import json, config, math, logging
from pybit import usdt_perpetual

# instantiate logger
logging.getLogger().setLevel(logging.DEBUG)

# instantiate pybit session client
session_auth = usdt_perpetual.HTTP(
                endpoint=config.ENDPOINT,
                api_key=config.BYBIT_API_KEY,
                api_secret=config.BYBIT_API_SECRET
            )

# JSON data object
def parse_webhook(webhook_data):
    
    data = ast.literal_eval(webhook_data)
    print('Data as Literal', json.dumps(data, indent=4))
    
    
    # with open('data.json', 'r+') as json_file:
    #     datasa = json.load(json_file)
    #     print('Data Read From File', datasa)
    #     datasa.update(data)
    #     print('Updated Data', datasa)
    #     #json_file.seek(0)
    #     #json.dump(datasa,data)
    return data

# function to create orders
def open_position(data, order_type="Limit"):
    
    print(json.dumps(data, indent=4))
    # local variables
    side = data['strategy']['order_action'].capitalize()
    ticker = data['ticker']
    quantity = data['strategy']['order_contracts'] 
    price = data['strategy']['order_price']
    profit = data['strategy']['alert_message']['take_profit']
    loss = data['strategy']['alert_message']['stop_loss']

    try:
        logging.info(f"sending {ticker}-{order_type} order - {side} {quantity} coins @ {price} ")
        order = session_auth.place_active_order(
            symbol=ticker,
            side=side,
            order_type="Limit",
            qty=quantity,
            price=0.59,
            time_in_force="GoodTillCancel",
            reduce_only=False,
            close_on_trigger=False
        )
        # order = session_auth.place_active_order(
        #             symbol=ticker,
        #             side=side,
        #             order_type="Limit",
        #             qty=quantity,
        #             price=price,
        #             # take_profit=profit,
        #             # stop_loss=loss,
        #             time_in_force="GoodTillCancel",
        #             reduce_only=False,
        #             close_on_trigger=False
        #         )
        print(json.dumps(order, indent=4))
    except Exception as e:
        logging.error("ORDER: Error occurred while placing order > {}".format(e))
        return e

    return order