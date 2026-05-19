import json
from datetime import datetime

def log_trade(data, analysis):

    trade_data = {
        "time": str(datetime.now()),
        "signal": data.signal,
        "ticker": data.ticker,
        "price": data.price,
        "analysis": analysis
    }

    with open("trade_log.json", "a") as file:

        json.dump(trade_data, file)

        file.write("\n")