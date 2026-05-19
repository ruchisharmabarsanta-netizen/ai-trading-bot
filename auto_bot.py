import time

import yfinance as yf

from ai_engine import analyze_trade

from telegram_alerts import (
    send_telegram_alert
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
                interval="1m",
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
                symbol,
                current_price
            )

            # =========================
            # SELL ANALYSIS
            # =========================

            sell_analysis = analyze_trade(
                "SELL",
                symbol,
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

                send_telegram_alert(
                    message
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

                send_telegram_alert(
                    message
                )

            else:

                print("NO VALID TRADE")

            # =========================
            # SMALL DELAY
            # =========================

            time.sleep(5)

    except Exception as e:

        print("\nERROR:")
        print(e)

    # =========================
    # WAIT BEFORE NEXT SCAN
    # =========================

    print("\nWAITING 60 SECONDS...\n")

    time.sleep(60)