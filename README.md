# VWAP calculation engine developed in Python

This app ingests live data from  [Coinbase's websockets feed](https://docs.cloud.coinbase.com/exchange/docs/websocket-overview) using the callback based [websocket-client](https://pypi.org/project/websocket-client/) and streamlines [VWAP (Volume-Weighted Average Price)](https://en.wikipedia.org/wiki/Volume-weighted_average_price) values to the stdout.
The sliding window used in the calculation is defined by the SLIDING_WINDOW env var

## How does it work?  

The websocket-client takes care to receive live price and quantity from Coinbase. Every time Coinbase sends a new message to the websocket-client the VWAP value is updated using the formula:

> VWAP equation = sum(price*quantity) / sum(quantity)

In order to improve performance we always keep the current sums of ```price*quantity```and ```quantity``` for each trading pair, so that when a new Point(p,q) arrives, we remove the oldest ```p0*q0``` value from the numerator and ```q0``` value from the denominator, and add the new related values ```p*q``` and ```q``` ```price*quantity```and ```quantity```. Idea taken from [https://github.com/cgmello/marketdata](https://github.com/cgmello/marketdata)

The function used to calculate VWAP needs to be Thread Safe, since a second message from Coinbase could be received before first message calculates VWAP. For that we implemented a mutex

## How to run it?  


Follow the steps below in order to prepare your environment to run it and also for local development:  

1. Install and configure [Pyenv](https://github.com/pyenv/pyenv)  
1. Run the commands
```bash
pyenv virtualenv 3.10.11 vwapengine
pyenv local vwapengine
pip install -r requirements.txt
python main.py
```

To run the tests you can use the following:  

```bash
pytest
pylint engine/
```

### Containerized  


Follow the steps below in order to Build and Run the container solution:  

1. Install docker  
1. Run the commands  
```bash
docker build -t coinbasevwap .
docker run -d \
    --name=coinbasevwap -d \
    coinbasevwap python main.py
docker logs coinbasevwap
docker rm -f coinbasevwap
```

## The ENV vars

The env vars are defined in the `.env` file and loaded using [python-dotenv](https://pypi.org/project/python-dotenv/), that means,
you don't need to change `.env` which can cause an unecessary commit, preferably, you set it in the terminal and python-dotenv will not overwrite it
```bash
export SLIDING_WINDOW=100

```

1. SLIDING_WINDOW - The number of points used during VWAP calculation of some determined traiding pair
1. URL_SANDBOX - The sandbox URL provided by Coinbase
1. URL_PROD - The prod URL provided by Coinbase
1. PRODUCT_IDS - The list of traiding pairs that you have interest on calculating the VWAP
