import json

CONFIG_FILE = "configs.json" # placeholder - change to the config json in crypto bot after testing
    # ../crypto-hybrid-tradebot/configs.json
    # test, tweak support_resistance_detector parameters, write readme

# dict:
    #{
        #"parameters": {"COIN1": [100.0, 95.0], "COIN2": [234.0, 223.0], ...},
        #"dollar_value": 2000.0
    #}

def parameter_writer(dict):
    configs = []

    for symbol in dict[0]:
        configs.append({"symbol": symbol, "entry_price": dict[symbol][0], "stop_loss": dict[symbol][1], "dollar_value": dict['dollar_value']})

    with open(CONFIG_FILE, "w") as file:
        json.dump(configs, file, indent=2)

    print("New configs saved to configs.json")
    for c in configs:
        print(f" - {c['symbol']}: Entry {c['entry_price']}, Stop {c['stop_loss']}, Qty ${c['dollar_value']}")
    print(f"Total symbols saved: {len(configs)}")


# output format:
    #[
        #{
            #"symbol": "COIN1",
            #"entry_price": 100.0,
            #"stop_loss": 95.0,
            #"dollar_value": 2000.0
        #},
        #{
            #"symbol": "COIN2",
            #"entry_price": 234.0,
            #"stop_loss": 223.0,
            #"dollar_value": 2000.0
        #},
    #]


