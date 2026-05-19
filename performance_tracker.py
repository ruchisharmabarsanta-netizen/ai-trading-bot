performance = {
    "total_trades": 0,
    "wins": 0,
    "losses": 0,
    "win_rate": 0,
    "total_profit": 0
}


def update_performance(
    outcome,
    profit
):

    performance["total_trades"] += 1

    if outcome == "WIN":

        performance["wins"] += 1

    else:

        performance["losses"] += 1

    performance["total_profit"] += profit

    performance["win_rate"] = round(
        (
            performance["wins"]
            /
            performance["total_trades"]
        ) * 100,
        2
    )

    print("\n====================")
    print("SYSTEM PERFORMANCE")
    print("====================")

    print(performance)