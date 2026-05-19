import yfinance as yf

from ta.momentum import RSIIndicator

from ta.trend import EMAIndicator
from ta.trend import MACD

from ta.volatility import AverageTrueRange


def analyze_trade(
    signal,
    ticker,
    price
):

    symbol = "GC=F"

    # =========================
    # LOWER TIMEFRAME DATA
    # =========================

    df = yf.download(
        symbol,
        period="5d",
        interval="15m",
        progress=False
    )

    # =========================
    # HIGHER TIMEFRAME DATA
    # =========================

    higher_df = yf.download(
        symbol,
        period="10d",
        interval="1h",
        progress=False
    )

    # =========================
    # FIX DATAFRAMES
    # =========================

    close_prices = (
        df["Close"].squeeze()
    )

    higher_close = (
        higher_df["Close"].squeeze()
    )

    high_prices = (
        df["High"].squeeze()
    )

    low_prices = (
        df["Low"].squeeze()
    )

    open_prices = (
        df["Open"].squeeze()
    )

    # =========================
    # RSI
    # =========================

    rsi_indicator = RSIIndicator(
        close=close_prices,
        window=14
    )

    df["RSI"] = (
        rsi_indicator.rsi()
    )

    # =========================
    # EMA 200
    # =========================

    ema_indicator = EMAIndicator(
        close=close_prices,
        window=200
    )

    df["EMA200"] = (
        ema_indicator.ema_indicator()
    )

    # =========================
    # HIGHER EMA
    # =========================

    higher_ema_indicator = EMAIndicator(
        close=higher_close,
        window=200
    )

    higher_df["EMA200"] = (
        higher_ema_indicator.ema_indicator()
    )

    # =========================
    # MACD
    # =========================

    macd_indicator = MACD(
        close=close_prices
    )

    df["MACD"] = (
        macd_indicator.macd()
    )

    df["MACD_SIGNAL"] = (
        macd_indicator.macd_signal()
    )

    # =========================
    # ATR
    # =========================

    atr_indicator = AverageTrueRange(
        high=high_prices,
        low=low_prices,
        close=close_prices,
        window=14
    )

    df["ATR"] = (
        atr_indicator.average_true_range()
    )

    # =========================
    # LATEST VALUES
    # =========================

    latest_rsi = float(
        round(
            df["RSI"].iloc[-1],
            2
        )
    )

    latest_ema = float(
        round(
            df["EMA200"].iloc[-1],
            2
        )
    )

    latest_macd = float(
        round(
            df["MACD"].iloc[-1],
            2
        )
    )

    latest_macd_signal = float(
        round(
            df["MACD_SIGNAL"].iloc[-1],
            2
        )
    )

    latest_atr = float(
        round(
            df["ATR"].iloc[-1],
            2
        )
    )

    current_price = float(
        close_prices.iloc[-1]
    )

    higher_ema = float(
        round(
            higher_df["EMA200"].iloc[-1],
            2
        )
    )

    higher_price = float(
        higher_close.iloc[-1]
    )

    # =========================
    # SUPPORT & RESISTANCE
    # =========================

    recent_high = float(
        high_prices.tail(20).max()
    )

    recent_low = float(
        low_prices.tail(20).min()
    )

    # =========================
    # CANDLESTICK PATTERNS
    # =========================

    prev_open = float(
        open_prices.iloc[-2]
    )

    prev_close = float(
        close_prices.iloc[-2]
    )

    current_open = float(
        open_prices.iloc[-1]
    )

    current_close = float(
        close_prices.iloc[-1]
    )

    # =========================
    # BULLISH ENGULFING
    # =========================

    bullish_engulfing = (

        prev_close < prev_open

        and current_close > current_open

        and current_close > prev_open

        and current_open < prev_close
    )

    # =========================
    # BEARISH ENGULFING
    # =========================

    bearish_engulfing = (

        prev_close > prev_open

        and current_close < current_open

        and current_open > prev_close

        and current_close < prev_open
    )

    # =========================
    # ANALYSIS OBJECT
    # =========================

    analysis = {

        "approved": False,

        "confidence": 0,

        "rsi": latest_rsi,

        "ema200": latest_ema,

        "macd": latest_macd,

        "macd_signal": latest_macd_signal,

        "atr": latest_atr,

        "market_price": current_price,

        "support": round(
            recent_low,
            2
        ),

        "resistance": round(
            recent_high,
            2
        ),

        "bullish_engulfing": bullish_engulfing,

        "bearish_engulfing": bearish_engulfing,

        "stop_loss": 0,

        "take_profit": 0,

        "reason": "No valid setup"
    }

    # =========================
    # BUY LOGIC
    # =========================

    if signal == "BUY":

        if (

            latest_rsi > 45

            and current_price > latest_ema

            and latest_macd > latest_macd_signal

            and latest_atr > 5

            and higher_price > higher_ema

            and current_price > (
                recent_high - 15
            )

            and bullish_engulfing

        ):

            analysis["approved"] = True

            analysis["confidence"] = 0.93

            analysis["stop_loss"] = round(
                current_price
                - (latest_atr * 1.5),
                2
            )

            analysis["take_profit"] = round(
                current_price
                + (latest_atr * 3),
                2
            )

            analysis["reason"] = (
                "Bullish engulfing + "
                "breakout + "
                "trend confirmation + "
                "RSI strength + "
                "MACD bullish"
            )

    # =========================
    # SELL LOGIC
    # =========================

    elif signal == "SELL":

        if (

            latest_rsi < 55

            and current_price < latest_ema

            and latest_macd < latest_macd_signal

            and latest_atr > 5

            and higher_price < higher_ema

            and current_price < (
                recent_low + 15
            )

            and bearish_engulfing

        ):

            analysis["approved"] = True

            analysis["confidence"] = 0.93

            analysis["stop_loss"] = round(
                current_price
                + (latest_atr * 1.5),
                2
            )

            analysis["take_profit"] = round(
                current_price
                - (latest_atr * 3),
                2
            )

            analysis["reason"] = (
                "Bearish engulfing + "
                "breakdown + "
                "trend confirmation + "
                "RSI weakness + "
                "MACD bearish"
            )

    return analysis