from binance.client import Client
from dotenv import load_dotenv

import os

load_dotenv()

API_KEY = os.getenv(
    "BINANCE_API_KEY"
)

SECRET_KEY = os.getenv(
    "BINANCE_SECRET_KEY"
)

client = Client(
    API_KEY,
    SECRET_KEY
)

# Futures testnet
client.FUTURES_URL = (
    "https://testnet.binancefuture.com/fapi"
)


def place_order(
    signal,
    quantity,
    stop_loss,
    take_profit
):

    try:

        # =========================
        # SET LEVERAGE
        # =========================

        client.futures_change_leverage(
            symbol="BTCUSDT",
            leverage=5
        )

        # =========================
        # MARKET ORDER
        # =========================

        order = client.futures_create_order(
            symbol="BTCUSDT",
            side=signal,
            type="MARKET",
            quantity=quantity
        )

        print("\n====================")
        print("BINANCE MARKET ORDER")
        print("====================")

        print(order)

        # =========================
        # OPPOSITE SIDE
        # =========================

        exit_side = (
            "SELL"
            if signal == "BUY"
            else "BUY"
        )

        # =========================
        # STOP LOSS
        # =========================

        sl_order = client.futures_create_order(
            symbol="BTCUSDT",
            side=exit_side,
            type="STOP_MARKET",
            stopPrice=round(stop_loss, 2),
            closePosition=True
        )

        print("\nSTOP LOSS SET")

        print(sl_order)

        # =========================
        # TAKE PROFIT
        # =========================

        tp_order = client.futures_create_order(
            symbol="BTCUSDT",
            side=exit_side,
            type="TAKE_PROFIT_MARKET",
            stopPrice=round(take_profit, 2),
            closePosition=True
        )

        print("\nTAKE PROFIT SET")

        print(tp_order)

    except Exception as e:

        print("\nBINANCE ERROR")

        print(e)