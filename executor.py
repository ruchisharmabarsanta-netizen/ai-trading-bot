from cooldown import (
    can_trade,
    update_trade_time
)

from performance_tracker import (
    update_performance
)

from binance_executor import (
    place_order
)

import random


def execute_trade(
    signal,
    analysis,
    risk
):

    if not analysis["approved"]:

        print("\nTRADE REJECTED")

        return

    if not can_trade():

        print("\nTRADE COOLDOWN ACTIVE")

        return

    print("\n====================")
    print("EXECUTING TRADE")
    print("====================")

    print(f"Signal: {signal}")

    print(
        f"Lot Size: "
        f"{risk['lot_size']}"
    )

    print(
        f"Entry: "
        f"{analysis['market_price']}"
    )

    print(
        f"Stop Loss: "
        f"{analysis['stop_loss']}"
    )

    print(
        f"Take Profit: "
        f"{analysis['take_profit']}"
    )

    # =========================
    # REAL BINANCE EXECUTION
    # =========================

    place_order(
    signal,
    round(
        min(
            risk["lot_size"],
            0.2
        ),
        3
    ),
    analysis["stop_loss"],
    analysis["take_profit"]
    )

    # =========================
    # SIMULATED RESULT
    # =========================

    outcome = random.choice(
        ["WIN", "LOSS"]
    )

    profit = (
        risk["risk_amount"] * 2
        if outcome == "WIN"
        else -risk["risk_amount"]
    )

    print("\n====================")
    print("TRADE RESULT")
    print("====================")

    print(f"Outcome: {outcome}")

    print(f"Profit: {profit}")

    update_performance(
        outcome,
        profit
    )

    update_trade_time()

    print(
        "\nTRADE EXECUTED "
        "SUCCESSFULLY"
    )