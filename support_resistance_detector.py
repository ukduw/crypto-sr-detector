# Alpaca-supported crypto:
    # AAVE, AVAX, BAT, BCH, BTC, CRV, DOGE, DOT, ETH, GRT
    # LINK, LTC, MKR, PEPE, SHIB, SOL, SUSHI, TRUMP, UNI, USDC
    # USDG, USDT, XRP, XTZ, YFI
# API call for available crypto in case of update:
    # curl --request GET 'https://api.alpaca.markets/v2/assets?asset_class=crypto' \
    # --header 'Apca-Api-Key-Id: <KEY>' \
    # --header 'Apca-Api-Secret-Key: <SECRET>' \

# look into websocket, available data, etc...


# declare list of coins
# iterate over, api request current day bar data
# detect sr levels
# logic to determine closest ones to strategy parameters
# return to use in parameter_writer