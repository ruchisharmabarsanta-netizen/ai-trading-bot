def calculate_risk(account_balance, risk_percent, stop_loss_distance):

    risk_amount = account_balance * (risk_percent / 100)

    lot_size = risk_amount / stop_loss_distance

    return {
        "account_balance": account_balance,
        "risk_percent": risk_percent,
        "risk_amount": round(risk_amount, 2),
        "lot_size": round(lot_size, 2)
    }