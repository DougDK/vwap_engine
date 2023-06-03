"""VWAP MODULE"""
from threading import Lock
from .point import Point

class Vwap:
    """VWAP CLASS"""
    sliding_window: int
    points: dict[str, list[Point]]
    sum_price_qty: dict[str, float]
    sum_qty: dict[str, float]
    vwap: dict[str, float]
    __mutex: Lock

    def __init__(self, sliding_window: int):
        self.sliding_window = sliding_window
        self.points = {}
        self.sum_price_qty = {}
        self.sum_qty = {}
        self.vwap = {}
        self.__mutex = Lock()

    def get_vwap(self, trading_pair: str):
        """VWAP FUNC"""
        last_vwap = self.vwap.get(trading_pair)
        if last_vwap is None :
            raise TypeError(f"VWAP value is undefined for the traiding pair: {trading_pair}")

        return last_vwap

    def process(self, point: Point):
        """VWAP FUNC"""
        with self.__mutex:
            trading_pair = point.trading_pair

            if self.points.get(trading_pair) is None :
                self.points[trading_pair] = []
                self.sum_price_qty[trading_pair] = 0.0
                self.sum_qty[trading_pair] = 0.0
                self.vwap[trading_pair] = 0.0
            else:
                if len(self.points[trading_pair]) == self.sliding_window :
                    self.__remove(trading_pair)

            self.__add(trading_pair, point)

        return self.vwap[trading_pair]

    def __remove(self, trading_pair: str):
        """VWAP FUNC"""
        first_point = self.points[trading_pair][0]

        price = first_point.price
        qty = first_point.quantity
        mul_price_qty = price * qty

        self.sum_price_qty[trading_pair] -= mul_price_qty
        self.sum_qty[trading_pair] -= qty

        if self.sum_qty[trading_pair] != 0 :
            self.vwap[trading_pair] = self.sum_price_qty[trading_pair] / self.sum_qty[trading_pair]

        self.points[trading_pair].pop(0)

    def __add(self, trading_pair: str, point: Point):
        """VWAP FUNC"""
        price = point.price
        qty = point.quantity
        mul_price_qty = price * qty

        self.sum_price_qty[trading_pair] += mul_price_qty
        self.sum_qty[trading_pair] += qty

        if self.sum_qty[trading_pair] != 0 :
            self.vwap[trading_pair] = self.sum_price_qty[trading_pair] / self.sum_qty[trading_pair]

        self.points[trading_pair].append(point)
