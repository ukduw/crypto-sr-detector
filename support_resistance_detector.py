# Alpaca-supported crypto:
    # AAVE, AVAX, BAT, BCH, BTC, CRV, DOGE, DOT, ETH, GRT
    # LINK, LTC, MKR, PEPE, SHIB, SOL, SUSHI, TRUMP, UNI, USDC
    # USDG, USDT, XRP, XTZ, YFI
# API call for available crypto in case of update:
    # curl --request GET 'https://api.alpaca.markets/v2/assets?asset_class=crypto' \
    # --header 'Apca-Api-Key-Id: <KEY>' \
    # --header 'Apca-Api-Secret-Key: <SECRET>' \

# get up to date list later...
# transition to binance business account(?) in future?

# check above list of coins for ~50 - 200/300/500/1,000mil average volume?
# alpaca - look into websocket, available data, etc...

# don't forget pip freeze > requirements.txt


coins = [] # fill later
dollar_position_size = 2000

bar_data = {}
all_levels = {}
levels = {}

def level_detector():
    # iterate over coins, api request current day bar data
    # store in bar_data
    # detect sr levels, append all_levels
    # logic to determine ones closest to strategy parameters
    # append those to levels, per coin
    # add dollar_value key with dollar_position_size as value
    # return levels for use in parameter_writer
    return



# output format:
    #{
        #{"COIN1": [100.0, 95.0], "COIN2": [234.0, 223.0], ...},
        #"dollar_value": 2000.0
    #}