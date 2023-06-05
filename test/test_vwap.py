from engine import Vwap
from engine import Point
from threading import Thread

points = [
	Point("XXX-YYY", 100, 10),
	Point("XXX-YYY", 150, 15),
	Point("XXX-YYY", 200, 10),
    Point("XXX-YYY", 200, 15),
]

def test_vwap():
    SLIDING_WINDOW = 3

    vwap = Vwap(SLIDING_WINDOW)

    # Add first point
    current_vwap = vwap.process(points[0])
    assert len(vwap.points["XXX-YYY"]) == 1
    assert vwap.points["XXX-YYY"][0] == points[0]
    assert current_vwap == 100

    # Add second point
    current_vwap = vwap.process(points[1])
    assert len(vwap.points["XXX-YYY"]) == 2
    assert vwap.points["XXX-YYY"][1] == points[1]
    assert current_vwap == 130

    # Add third point
    current_vwap = vwap.process(points[2])
    assert len(vwap.points["XXX-YYY"]) == 3
    assert vwap.points["XXX-YYY"][2] == points[2]
    assert current_vwap == 150

    # Test if sliding_window is working for sliding window of maximum 3
    current_vwap = vwap.process(points[3])
    assert len(vwap.points["XXX-YYY"]) == 3
    assert vwap.points["XXX-YYY"][2] == points[3]
    assert vwap.points["XXX-YYY"][1] == points[2]
    assert vwap.points["XXX-YYY"][0] == points[1]
    assert current_vwap == 181.25


def test_concurrency():
    SLIDING_WINDOW = 200

    vwap = Vwap(SLIDING_WINDOW)
    t1 = Thread(target=vwap.process, args=(points[0],))
    t2 = Thread(target=vwap.process, args=(points[1],))
    t3 = Thread(target=vwap.process, args=(points[2],))

    # Run all the threads concurrently
    t1.start()
    t2.start()
    t3.start()

    # Wait for all the threads to finish
    t1.join()
    t2.join()
    t3.join()

    assert len(vwap.points["XXX-YYY"]) == 3
    current_vwap = vwap.get_vwap("XXX-YYY")
    assert current_vwap == 150
