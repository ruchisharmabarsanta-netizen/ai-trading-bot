import yfinance as yf

from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from ta.trend import MACD


print("\nSTARTING BACKTEST...\n")

# =========================
# DOWNLOAD DATA ONCE
# =========================

df = yf.download(
    "GC=F",
    period="5d",
    interval="15m",
    progress=False
)

# =========================
# FIX DATA
# =========================

close_prices = (
    df["Close"].squeeze()
)

# =========================
# INDICATORS
# =========================

rsi = RSIIndicator(
    close=close_prices,
    window=14
)

df["RSI"] = rsi.rsi()

ema = EMAIndicator(
    close=close_prices,
    window=200
)

df["EMA200"] = ema.ema_indicator()

macd = MACD(
    close=close_prices
)

df["MACD"] = macd.macd()

df["MACD_SIGNAL"] = (
    macd.macd_signal()
)

# =========================
# RESULTS
# =========================

wins = 0
losses = 0
profit = 0

# =========================
# LOOP
# =========================

for i in range(200, len(df) - 5):

    current_price = float(
        close_prices.iloc[i]
    )

    current_rsi = float(
        df["RSI"].iloc[i]
    )

    current_ema = float(
        df["EMA200"].iloc[i]
    )

    current_macd = float(
        df["MACD"].iloc[i]
    )

    current_macd_signal = float(
        df["MACD_SIGNAL"].iloc[i]
    )

    # =========================
    # BUY CONDITIONS
    # =========================

    if (

        current_rsi > 35

        and current_price > current_ema

        and current_macd > current_macd_signal

    ):

        entry = current_price

        sl = entry - 10

        tp = entry + 20

        future_price = float(
            close_prices.iloc[i + 5]
        )

        # WIN

        if future_price >= tp:

            wins += 1

            profit += 20

        # LOSS

        elif future_price <= sl:

            losses += 1

            profit -= 10

# =========================
# FINAL RESULTS
# =========================

print("\n====================")
print("BACKTEST RESULTS")
print("====================")

total = wins + losses

win_rate = (
    (wins / total) * 100
    if total > 0 else 0
)

print(f"Trades: {total}")

print(f"Wins: {wins}")

print(f"Losses: {losses}")

print(
    f"Win Rate: {round(win_rate, 2)}%"
)

print(
    f"Profit: {round(profit, 2)}"
)