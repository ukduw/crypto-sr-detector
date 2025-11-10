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


# subscribe as currency pair, e.g. "BTCUSD"

# full list: 22 [AAVE, AVAX, BAT, BCH, BTC, CRV, DOGE, DOT, ETH, GRT, LINK, LTC, MKR, PEPE, SHIB, SOL, SUSHI, TRUMP, UNI, USDC, USDG, USDT, XRP, XTZ, YFI]
# cap >= 200mil, vol/cap 0.02-0.20, vol 50-200mil: 45 coins
# cap >= 200mil, vol/cap 0.02-0.20, vol 200-500mil: 17 coins
# cap >= 200mil, vol/cap 0.02-0.20, vol 500-1,000mil: 6 coins



# determine level parameters (and take-profit conditions for bot script)
# test, tweak parameters, remove prints/plots/comments
# write readme


load_dotenv()
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

coins = [] # update, short list of ~4 is fine for now
dollar_position_size = 1000 # placeholder, depends on length of coin list

universal = pytz.timezone("UTC")

historical_client = CryptoHistoricalDataClient(api_key=API_KEY, secret_key=SECRET_KEY)


def level_detector():
    highs = {}
    lows = {}
    close = {}

    stdevs = {}

    all_levels = {}
    levels = {}

    bar_window = deque(maxlen=6) # 30min

    # NOTE: bar timestamps are the START of the bar, e.g. 10:00 = 10:00-10:04:59

    lookback_bars = 282 # 23.5 hours of 5min bars
    lookback_minutes = lookback_bars * 5 # 1,410 minutes
    now = datetime.datetime.now(universal)
    start_time = now - datetime.timedelta(minutes=lookback_minutes) # schedule for 23:30

    # === API REQUESTS === #
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
        close[coin] = bars[-1].close

    print("HIGHS", highs)
    print("LOWS", lows)
    print("CLOSE", close)

    # === STDEV === #
    for coin in highs:
        highs_stdev = statistics.stdev(highs[coin])
        lows_stdev = statistics.stdev(lows[coin])

        stdevs[coin] = [highs_stdev, lows_stdev]

    print("STDEV", stdevs)

    # === S/R DETECT, MERGE LEVELS === #
    for coin in highs:
        resistance = []
        for high in highs[coin]:
            bar_window.append(high)
            if len(bar_window) == 6:
                no_dupes = [key for key, _ in groupby(bar_window)]
                if len(no_dupes) >= 3:
                    peaks, _ = find_peaks(no_dupes)
                    peaks = [key for key, _ in groupby(peaks)]
                    resistance.append(peaks)
                else:
                    resistance.append(max(no_dupes))
        bar_window.clear()
        resistance = list(chain.from_iterable(resistance))
        for i in range(len(resistance)):
            for j in range(len(resistance)):
                if (resistance[i] - stdevs[coin][0]) <= resistance[j] < resistance[i]:
                    resistance.pop(j)
        all_levels[coin] = resistance
    for coin in lows:
        support = []
        for low in lows[coin]:
            bar_window.append(low * -1)
            if len(bar_window) == 6:
                no_dupes2 = [key for key, _ in groupby(bar_window)]
                if len(no_dupes2) >= 3:
                    peaks2, _ = find_peaks(no_dupes2)
                    peaks2 = [-1 * x for x in peaks2]
                    peaks2 = [key for key, _ in groupby(peaks2)]
                    support.append(peaks2)
                else:
                    no_dupes2 = [-1 * x for x in no_dupes2]
                    support.append(min(no_dupes2))
        bar_window.clear()
        support = list(chain.from_iterable(support))
        for i in range(len(support)):
            for j in range(len(support)):
                if (support[i] + stdevs[coin][1]) >= support[j] > support[i]:
                    support.pop[j]
        all_levels[coin] = all_levels[coin] + support


    # PLOT - REMOVE LATER
    for coin in all_levels:
        plt.plot(highs[coin], lows[coin])
        plt.plot(all_levels[coin], "rx")
        plt.show()


    # === STRATEGY PARAMETERS === #
        # TWEAK THIS - needs more research...
    parameters = {}

    smallest_diff1 = 100
    smallest_diff2 = 100

    closest_highs = [] # in case of multiple; tie-breaker
    closest_lows = []

    for coin in all_levels:
        for level in all_levels[coin]:
            diff1 = abs(level - close[coin] * 1.05) # 5%, TWEAK, needs research
            
            if diff1 < smallest_diff1:
                closest_highs = [level]
                smallest_diff1 = diff1
            elif diff1 == smallest_diff1:
                closest_highs.append(level)
        entry = max(closest_highs)

        for level in all_levels[coin]:
            diff2 = abs(level - entry * 0.95) # 5% from entry, TWEAK

            if diff2 < smallest_diff2:
                closest_lows = [level]
                smallest_diff2 = diff2
            elif diff2 == smallest_diff2:
                closest_lows.append(level)
        stop = min(closest_lows)

        parameters[coin] = [entry, stop]
    
    print("PARAMETERS", parameters)

    levels["parameters"] = parameters
    levels["dollar_value"] = dollar_position_size

    print("LEVELS", levels)

    return levels



# output format:
    #{
        #"parameters": {"COIN1": [100.0, 95.0], "COIN2": [234.0, 223.0], ...},
        #"dollar_value": 2000.0
    #}


if __name__ == "main":
    level_detector()

