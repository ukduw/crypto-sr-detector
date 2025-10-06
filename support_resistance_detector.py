from alpaca.data.historical.crypto import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame

from dotenv import load_dotenv
import os

import datetime, pytz

# Alpaca-supported crypto:
    # AAVE, AVAX, BAT, BCH, BTC, CRV, DOGE, DOT, ETH, GRT
    # LINK, LTC, MKR, PEPE, SHIB, SOL, SUSHI, TRUMP, UNI, USDC
    # USDG, USDT, XRP, XTZ, YFI
# API call for available crypto in case of update:
    # curl --request GET 'https://api.alpaca.markets/v2/assets?asset_class=crypto' \
    # --header 'Apca-Api-Key-Id: <KEY>' \
    # --header 'Apca-Api-Secret-Key: <SECRET>' \

# subscribe as currency pair, e.g. "BTCUSD"

# get up to date list later...
# transition to binance business account(?) in future?
    # direct access to exchange(s)
    # long and short (alpaca no shorts...)
        # future 24/7 version can have long and short logic; for now, long only
    # complete coverage vs ~20+...

# check above list of coins for ~50 - 200/300/500/1,000mil average volume?

# don't forget pip freeze > requirements.txt

load_dotenv()
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

coins = [] # fill later
dollar_position_size = 2000 # placeholder

bar_data = {}
all_levels = {}
levels = {}

universal = pytz.timezone("UTC")

historical_client = CryptoHistoricalDataClient(api_key=API_KEY, secret_key=SECRET_KEY)

def level_detector(): # ASYNC?
    # iterate over coins, api request current day bar data
        # needs sleep to avoid api limit?
        # NOTE: bar timestamps are the START of the bar, e.g. 10:00 = 10:00-10:04:59

    lookback_bars = 282 # 23.5 hours of 5min bars
    lookback_minutes = lookback_bars * 5 # 1,410 minutes
    now = datetime.datetime.now(universal)
    start_time = now - datetime.timedelta(minutes=lookback_minutes) # schedule for 23:30

    for coin in coins:
        request_params = CryptoBarsRequest(
            symbol_or_symbols=coin,
            timeframe=TimeFrame(5, TimeFrame.Minute),
            start=start_time,
            end=now,
            feed="us"
        )

        # no need for df? consider just storing relevant data, e.g. highs/lows
        bars = historical_client.get_crypto_bars(request_params).df
        if isinstance(bars.index, pd.MultiIndex):
            df = bars.xs(coin, level=0).sort_index()
        else:
            df = bars.sort_index()


    # store in bar_data
    # detect sr levels, append all_levels
    # calculate stdev of highs/lows
    # logic to determine ones closest to strategy parameters
    # logic to determine which levels to merge (e.g. within stdev of each other)
    # append those to levels, per coin
    # add dollar_value key with dollar_position_size as value
    # return levels for use in parameter_writer
    return



# output format:
    #{
        #{"COIN1": [100.0, 95.0], "COIN2": [234.0, 223.0], ...},
        #"dollar_value": 2000.0
    #}