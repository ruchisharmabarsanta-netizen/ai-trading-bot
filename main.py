from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from ai_engine import analyze_trade
from risk_manager import calculate_risk
from executor import execute_trade
from trade_logger import log_trade

app = FastAPI()


class TradingSignal(BaseModel):
    signal: str
    ticker: str
    price: str


@app.get("/")
async def home():

    return {
        "status": "AI Trading Bot Running"
    }


@app.post("/webhook")
async def webhook(data: TradingSignal):

    print("\n====================")
    print("SIGNAL RECEIVED")
    print("====================")

    print(f"Time: {datetime.now()}")

    print(f"Signal: {data.signal}")

    print(f"Ticker: {data.ticker}")

    print(f"Price: {data.price}")

    # =========================
    # AI ANALYSIS
    # =========================

    analysis = analyze_trade(
        data.signal,
        data.ticker,
        data.price
    )

    print("\n====================")
    print("AI ANALYSIS")
    print("====================")

    print(analysis)

    # =========================
    # RISK MANAGEMENT
    # =========================

    risk = calculate_risk(
        account_balance=10000,
        risk_percent=1,
        stop_loss_distance=abs(
            analysis["market_price"]
            - analysis["stop_loss"]
        ) if analysis["approved"] else 1
    )

    print("\n====================")
    print("RISK MANAGEMENT")
    print("====================")

    print(risk)

    # =========================
    # EXECUTE TRADE
    # =========================

    execute_trade(
        data.signal,
        analysis,
        risk
    )

    # =========================
    # SAVE LOGS
    # =========================

    log_trade(data, analysis)

    return {
        "status": "success",
        "analysis": analysis,
        "risk": risk
    }