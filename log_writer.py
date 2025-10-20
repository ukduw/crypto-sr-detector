import datetime, pytz

universal = pytz.timezone("UTC")
now = datetime.datetime.now(universal)


# dict:
    #{
        #"parameters": {"COIN1": [100.0, 95.0], "COIN2": [234.0, 223.0], ...},
        #"dollar_value": 2000.0
    #}

def log_writer(dict):
    with open("param-log/param_log.txt", "a") as file:
        file.write(f" === {now} UTC === " + "\n")
        for key in dict.parameters:
            file.write(f"{key}: Entry {dict.parameters[key][0]}, Stop {dict.parameters[key][1]}" + "\n")



