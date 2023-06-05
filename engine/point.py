"""Point module with the Point class to deal with Trading Pairs"""

class Point:  # pylint: disable=R0903
    """Point class is used to represent trading pair price and quantity at some point"""
    trading_pair: str
    price: float
    quantity: float

    def __init__(self, trading_pair: str, price: float, quantity: float):
        self.trading_pair = trading_pair
        self.price = price
        self.quantity = quantity
