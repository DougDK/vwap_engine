"""COINBASE MODULE"""

import json
import sys
import os
from websocket import WebSocketApp
from websocket import WebSocketAddressException
from .point import Point
from .vwap import Vwap

SLIDING_WINDOW = 200
URL_SANDBOX = 'wss://ws-feed-public.sandbox.exchange.coinbase.com'
URL_PROD = 'wss://fake.coinbase.com'
PRODUCT_IDS = [
    'BTC-USD',
    'ETH-USD',
    'ETH-BTC'
]

def run():
    """XXXX"""
    try:
        vwap = Vwap(SLIDING_WINDOW)

        def on_open(websocket: WebSocketApp):
            """XXXX"""
            subscribe_msg = {
                'type': 'subscribe',
                'channels':[{
                    'name':'ticker',
                    'product_ids': PRODUCT_IDS
                }]
            }
            websocket.send(json.dumps(subscribe_msg))

        def on_message(websocket: WebSocketApp, message: str): # pylint: disable=W0613
            """XXXX"""
            decoded_message = json.loads(message)
            if decoded_message['type'] == 'ticker' :
                trading_pair = decoded_message['product_id']
                price = float(decoded_message['price'])
                qty = float(decoded_message['volume_24h'])

                new_point = Point(trading_pair, price, qty)
                vwap.process(new_point)

                print(vwap.get_vwap(trading_pair))

        def on_error(websocket: WebSocketApp, error: WebSocketAddressException):
            raise error

        websocket = WebSocketApp(
            url=URL_PROD,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error
        )
        websocket.run_forever()
    except KeyboardInterrupt:
        print('Interrupted')
        if websocket:
            websocket.close()
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
