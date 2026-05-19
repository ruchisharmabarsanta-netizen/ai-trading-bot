from datetime import (
    datetime,
    timedelta
)

last_trade_time = None


def can_trade():

    global last_trade_time

    if last_trade_time is None:

        return True

    cooldown = timedelta(
        minutes=15
    )

    return (
        datetime.now()
        - last_trade_time
    ) > cooldown


def update_trade_time():

    global last_trade_time

    last_trade_time = datetime.now()