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

    # =========================
    # SYMBOL MAP
    # =========================

    symbol_map = {

        "GOLD": "GC=F",

        "BTCUSD": "BTC-USD",

        "ETHUSD": "ETH-USD",

        "NIFTY": "^NSEI",

        "BANKNIFTY": "^NSEBANK"
    }

    symbol = symbol_map[ticker]

    # =========================
    # DOWNLOAD DATA
    # =========================

    df = yf.download(
        symbol,
        period="5d",
        interval="15m",
        progress=False
    )

    higher_df = yf.download(
        symbol,
        period="10d",
        interval="1h",
        progress=False
    )

    # =========================
    # FIX DATA
    # =========================

    close_prices = (
        df["Close"].squeeze()
    )

    high_prices = (
        df["High"].squeeze()
    )

    low_prices = (
        df["Low"].squeeze()
    )

    volume = (
        df["Volume"].squeeze()
    )

    higher_close = (
        higher_df["Close"].squeeze()
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
    # EMA
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
    # VOLUME
    # =========================

    avg_volume = (
        volume.tail(20).mean()
    )

    latest_volume = (
        volume.iloc[-1]
    )

    high_volume = (
        latest_volume > avg_volume
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
    # CANDLESTICK
    # =========================

    prev_open = float(
        df["Open"].squeeze().iloc[-2]
    )

    prev_close = float(
        close_prices.iloc[-2]
    )

    current_open = float(
        df["Open"].squeeze().iloc[-1]
    )

    current_close = float(
        close_prices.iloc[-1]
    )

    bullish_engulfing = (

        prev_close < prev_open

        and current_close > current_open

        and current_close > prev_open

        and current_open < prev_close
    )

    bearish_engulfing = (

        prev_close > prev_open

        and current_close < current_open

        and current_open > prev_close

        and current_close < prev_open
    )

    # =========================
    # ANALYSIS
    # =========================

    analysis = {

        "approved": False,

        "confidence": 0,

        "rsi": latest_rsi,

        "market_price": current_price,

        "stop_loss": 0,

        "take_profit": 0,

        "reason": "No valid setup"
    }

    # =========================
    # BUY
    # =========================

    if signal == "BUY":

        if (

            latest_rsi > 55

            and current_price > latest_ema

            and latest_macd > latest_macd_signal

            and latest_atr > 5

            and higher_price > higher_ema

            and current_price > (
                recent_high - 5
            )

            and bullish_engulfing

            and high_volume
        ):

            analysis["approved"] = True

            analysis["confidence"] = 0.95

            analysis["stop_loss"] = round(
                current_price
                - (latest_atr * 1.2),
                2
            )

            analysis["take_profit"] = round(
                current_price
                + (latest_atr * 4),
                2
            )

            analysis["reason"] = (
                "Bullish engulfing + "
                "breakout + "
                "volume confirmation + "
                "trend confirmation"
            )

    # =========================
    # SELL
    # =========================

    elif signal == "SELL":

        if (

            latest_rsi < 45

            and current_price < latest_ema

            and latest_macd < latest_macd_signal

            and latest_atr > 5

            and higher_price < higher_ema

            and current_price < (
                recent_low + 5
            )

            and bearish_engulfing

            and high_volume
        ):

            analysis["approved"] = True

            analysis["confidence"] = 0.95

            analysis["stop_loss"] = round(
                current_price
                + (latest_atr * 1.2),
                2
            )

            analysis["take_profit"] = round(
                current_price
                - (latest_atr * 4),
                2
            )

            analysis["reason"] = (
                "Bearish engulfing + "
                "breakdown + "
                "volume confirmation + "
                "trend confirmation"
            )

    return analysis