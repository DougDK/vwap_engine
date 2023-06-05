import time
import os
from pytest import CaptureFixture
from typing import Callable
from threading import Thread

import engine.coinbase_data


class ThreadWithExc(Thread):
    """Class to run a function in a thread and capture exception"""
    target: Callable
    exc: BaseException

    def __init__(self, target: Callable):
        self.target = target
        super().__init__(target=self.target) 

    def run(self):
        # Variable that stores the exception, if raised by someFunction
        self.exc = None           
        try:
            self.target()
        except BaseException as e:
            self.exc = e

# capfd is a pytest fixture that allows working with stdout
# The VWAP values will be printed by the engine
def test_conn_should_success(capfd: CaptureFixture):
    websocket = engine.coinbase_data.create_websocket_app()

    # We execute in a thread in order to make it halt anyways
    t1 = Thread(target=websocket.run_forever)
    t1.start()
    time.sleep(1)
    websocket.keep_running = False
    t1.join()
    
    out,err = capfd.readouterr()
    print(out)
    print(type(err))
    assert err == ''

def test_conn_should_fail():
    # Configure fake WSS URL
    os.environ["URL_PROD"] = 'wss://fake.coinbase.com'
    websocket = engine.coinbase_data.create_websocket_app()

    # We expect this to fail but, to be sure it won't loop forever
    # We execute in a thread in order to make it halt anyways
    # The reason to use ThreadWithExc instead of Thread is to capture exception
    t1 = ThreadWithExc(target=websocket.run_forever)
    t1.start()
    time.sleep(0.1)
    websocket.keep_running = False # This commands halts run_forever
    t1.join()
    assert str(t1.exc) == '[Errno -5] No address associated with hostname'
