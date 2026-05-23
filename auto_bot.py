from paper_trader import (
    open_trade
)

import time

import yfinance as yf

from ai_engine import analyze_trade

from telegram_alerts import (
    send_telegram_alert
)

from cooldown import (
    can_send_signal
)

# =========================
# MARKETS
# =========================

markets = {

    "GOLD": "GC=F",

    "BTCUSD": "BTC-USD",

    "ETHUSD": "ETH-USD",

    "NIFTY": "^NSEI",

    "BANKNIFTY": "^NSEBANK"

}

print("\nAI MULTI-ASSET BOT STARTED...\n")

# =========================
# MAIN LOOP
# =========================

while True:

    try:

        for market_name, symbol in markets.items():

            print("\n====================")
            print(f"SCANNING {market_name}")
            print("====================")

            # =========================
            # GET LIVE PRICE
            # =========================

            df = yf.download(
                symbol,
                period="1d",
                interval="5m",
                progress=False
            )

            close_prices = (
                df["Close"].squeeze()
            )

            current_price = float(
                close_prices.iloc[-1]
            )

            print(
                f"Price: {current_price}"
            )

            # =========================
            # BUY ANALYSIS
            # =========================

            buy_analysis = analyze_trade(
                "BUY",
                market_name,
                current_price
            )

            # =========================
            # SELL ANALYSIS
            # =========================

            sell_analysis = analyze_trade(
                "SELL",
                market_name,
                current_price
            )

            # =========================
            # BUY SIGNAL
            # =========================

            if buy_analysis["approved"]:

                print("\nBUY SIGNAL FOUND")

                message = f"""
🚀 BUY SIGNAL

Market: {market_name}

Price: {buy_analysis['market_price']}

RSI: {buy_analysis['rsi']}

Confidence: {buy_analysis['confidence']}

Stop Loss: {buy_analysis['stop_loss']}

Take Profit: {buy_analysis['take_profit']}

Reason:
{buy_analysis['reason']}
"""

                # =========================
                # COOLDOWN FILTER
                # =========================

                if can_send_signal(
                    market_name,
                    cooldown_minutes=60
                ):

                    # TELEGRAM ALERT

                    send_telegram_alert(
                        message
                    )

                    print(
                        "Telegram Alert Sent"
                    )

                    # =========================
                    # OPEN PAPER TRADE
                    # =========================

                    open_trade(

                        market_name,

                        "BUY",

                        buy_analysis[
                            "market_price"
                        ],

                        buy_analysis[
                            "stop_loss"
                        ],

                        buy_analysis[
                            "take_profit"
                        ]
                    )

                    print(
                        "Paper Trade Opened"
                    )

                else:

                    print(
                        "Cooldown Active"
                    )

            # =========================
            # SELL SIGNAL
            # =========================

            elif sell_analysis["approved"]:

                print("\nSELL SIGNAL FOUND")

                message = f"""
🔻 SELL SIGNAL

Market: {market_name}

Price: {sell_analysis['market_price']}

RSI: {sell_analysis['rsi']}

Confidence: {sell_analysis['confidence']}

Stop Loss: {sell_analysis['stop_loss']}

Take Profit: {sell_analysis['take_profit']}

Reason:
{sell_analysis['reason']}
"""

                # =========================
                # COOLDOWN FILTER
                # =========================

                if can_send_signal(
                    market_name,
                    cooldown_minutes=60
                ):

                    # TELEGRAM ALERT

                    send_telegram_alert(
                        message
                    )

                    print(
                        "Telegram Alert Sent"
                    )

                    # =========================
                    # OPEN PAPER TRADE
                    # =========================

                    open_trade(

                        market_name,

                        "SELL",

                        sell_analysis[
                            "market_price"
                        ],

                        sell_analysis[
                            "stop_loss"
                        ],

                        sell_analysis[
                            "take_profit"
                        ]
                    )

                    print(
                        "Paper Trade Opened"
                    )

                else:

                    print(
                        "Cooldown Active"
                    )

            else:

                print(
                    "NO VALID TRADE"
                )

            # =========================
            # SMALL DELAY
            # =========================

            time.sleep(2)

    except Exception as e:

        print("\nERROR:")
        print(e)

    # =========================
    # WAIT BEFORE NEXT SCAN
    # =========================

    print(
        "\nWAITING 5 MINUTES...\n"
    )

    time.sleep(300)