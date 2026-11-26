import yfinance as yf
from pathlib import Path

TICKERS = ["SPY", "AAPL", "BTC-USD"]
Path("data/raw").mkdir(parents=True, exist_ok=True)

for t in TICKERS:
    df = yf.Ticker(t).history(start="2015-01-01", end="2026-01-01")
    df.to_csv(f"data/raw/{t}.csv")
    print(t, len(df), "dies |", df.index[0].date(), "->", df.index[-1].date())