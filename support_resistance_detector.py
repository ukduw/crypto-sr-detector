from alpaca.data.historical.crypto import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame

from dotenv import load_dotenv
import os

import datetime, pytz, statistics

from collections import deque
from itertools import groupby, chain
from scipy.signal import find_peaks

import matplotlib.pyplot as plt

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

highs = {}
lows = {}

stdevs = {}

all_levels = {}
levels = {}

universal = pytz.timezone("UTC")

historical_client = CryptoHistoricalDataClient(api_key=API_KEY, secret_key=SECRET_KEY)


def level_detector():
    bar_window = deque(maxlen=6) # 30min

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

        bars = historical_client.get_crypto_bars(request_params)
        for bar in bars:
            highs[bar.symbol] = [bar.high] if bar.symbol not in highs else highs[bar.symbol].append(bar.high)
            lows[bar.symbol] = [bar.low] if bar.symbol not in lows else lows[bar.symbol].append(bar.low)


    for coin in highs:
        highs_stdev = statistics.stdev(highs[coin])
        lows_stdev = statistics.stdev(lows[coin])

        stdevs[coin] = [highs_stdev, lows_stdev]


    for coin in highs:
        for high in coin:
            bar_window.append(high)
            if len(bar_window) == 6:
                no_dupes = [key for key, _ in groupby(bar_window)]
                if len(no_dupes) >= 3:
                    peaks, _ = find_peaks(no_dupes)
                    all_levels[coin] = peaks if coin not in all_levels else all_levels[coin].append(peaks)
                else:
                    all_levels[coin] = max(no_dupes) if coin not in all_levels else all_levels[coin].append(max(no_dupes))
        bar_window.clear()
    for coin in lows:
        for low in coin:
            bar_window.append(low * -1)
            if len(bar_window) == 6:
                no_dupes2 = [key for key, _ in groupby(bar_window)]
                if len(no_dupes2) >= 3:
                    peaks2, _ = find_peaks(no_dupes2)
                    peaks2 = [-1 * x for x in peaks2]
                    all_levels[coin].append(peaks2)
                else:
                    no_dupes2 = [-1 * x for x in no_dupes2]
                    all_levels[coin].append(min(no_dupes2))
        bar_window.clear()

    for coin in all_levels:
        all_levels[coin] = list(chain.from_iterable(all_levels[coin]))


    # REMOVE LATER
    for coin in all_levels:
        plt.plot(highs[coin], lows[coin])
        plt.plot(all_levels[coin], "rx")
        plt.show()


    # logic to determine which levels to merge (e.g. within stdev of each other)
    # logic to determine ones closest to strategy parameters
    # append those to levels, per coin


    levels.update({"dollar_value": dollar_position_size})

    return levels



# output format:
    #{
        #{"COIN1": [100.0, 95.0], "COIN2": [234.0, 223.0], ...},
        #"dollar_value": 2000.0
    #}