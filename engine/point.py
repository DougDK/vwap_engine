"""POINT MODULE"""

class Point:  # pylint: disable=R0903
    """POINT CLASS"""
    trading_pair: str
    price: float
    quantity: float

    def __init__(self, trading_pair: str, price: float, quantity: float):
        self.trading_pair = trading_pair
        self.price = price
        self.quantity = quantity
