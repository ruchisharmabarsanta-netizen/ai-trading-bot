import json

PORTFOLIO_FILE = "paper_portfolio.json"


def load_portfolio():

    with open(
        PORTFOLIO_FILE,
        "r"
    ) as f:

        return json.load(f)


def save_portfolio(data):

    with open(
        PORTFOLIO_FILE,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


def open_trade(

    market,
    signal,
    entry,
    sl,
    tp

):

    portfolio = load_portfolio()

    trade = {

        "market": market,

        "signal": signal,

        "entry": entry,

        "sl": sl,

        "tp": tp
    }

    portfolio["open_trades"].append(
        trade
    )

    portfolio["total_trades"] += 1

    save_portfolio(portfolio)


def get_stats():

    portfolio = load_portfolio()

    balance = portfolio["balance"]

    wins = portfolio["wins"]

    losses = portfolio["losses"]

    total = portfolio["total_trades"]

    profit = portfolio["profit"]

    open_count = len(
        portfolio["open_trades"]
    )

    win_rate = 0

    if total > 0:

        win_rate = round(
            (wins / total) * 100,
            2
        )

    return f"""
📊 PAPER TRADING STATS

Balance: ₹{balance}

Total Trades: {total}

Wins: {wins}

Losses: {losses}

Win Rate: {win_rate}%

Net Profit: ₹{profit}

Open Trades: {open_count}
"""