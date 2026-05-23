last_signal_time = {}

def can_send_signal(
    market,
    cooldown_minutes=60
):

    import time

    current_time = time.time()

    if market not in last_signal_time:

        last_signal_time[market] = current_time

        return True

    elapsed = (
        current_time
        - last_signal_time[market]
    )

    if elapsed > (
        cooldown_minutes * 60
    ):

        last_signal_time[market] = current_time

        return True

    return False