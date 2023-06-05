"""Main file with the run function"""

import json
import sys
import os
import ast
import datetime
from dotenv import load_dotenv
from websocket import WebSocketApp
from websocket import WebSocketAddressException
from .point import Point
from .vwap import Vwap

def create_websocket_app():
    """Create websocket and define callback functions"""
    load_dotenv()
    sliding_window = int(os.getenv("SLIDING_WINDOW"))
    # URL_SANDBOX = os.getenv("URL_SANDBOX")
    url_prod = os.getenv("URL_PROD")
    product_ids = ast.literal_eval(os.getenv("PRODUCT_IDS"))
    vwap = Vwap(sliding_window)

    def on_open(websocket: WebSocketApp):
        """Callback function to subscribe to the Coinbase Channels"""
        subscribe_msg = {
            'type': 'subscribe',
            'channels':[{
                'name':'ticker',
                'product_ids': product_ids
            }]
        }
        websocket.send(json.dumps(subscribe_msg))

    def on_message(websocket: WebSocketApp, message: str): # pylint: disable=W0613
        """Callback function to process new points"""
        decoded_message = json.loads(message)
        if decoded_message['type'] == 'ticker' :
            trading_pair = decoded_message['product_id']
            price = float(decoded_message['price'])
            qty = float(decoded_message['volume_24h'])

            new_point = Point(trading_pair, price, qty)
            vwap.process(new_point)
            vwap_value = vwap.get_vwap(trading_pair)
            now = datetime.datetime.now()
            print(f"{now} - {trading_pair}: {vwap_value}")

    def on_error(websocket: WebSocketApp, error: WebSocketAddressException):
        """Callback function to deal with any error"""
        raise error

    websocket = WebSocketApp(
        url=url_prod,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error
    )

    return websocket

def run():
    """
    The run function. It process and streamline VWAP value of Coinbase Trading Pairs.
    The SLIDING_WINDOW defines the amount of points used to calculate the VWAP.
    When it reached the SLIDING_WINDOW lengh, it removes the first point of the
    calculation in a FIFO schema.
    """
    try:
        websocket = create_websocket_app()
        websocket.run_forever()
    except KeyboardInterrupt:
        # CTRL+C or CTRL+Z stopps the execution, websocket is closed and gracefully exits
        print('Interrupted')
        if websocket:
            websocket.close()
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
