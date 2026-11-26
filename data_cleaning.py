import pandas as pd
from pathlib import Path

TICKERS = ["SPY", "AAPL", "BTC-USD"]
PREUS = ["Open", "High", "Low", "Close"]
Path("data/clean").mkdir(parents=True, exist_ok=True)

for t in TICKERS:
    df = pd.read_csv(f"data/raw/{t}.csv")
    df["Date"] = pd.to_datetime(df["Date"].str[:10])
    df = df.set_index("Date")[PREUS + ["Volume"]].sort_index()

    print(f"\n===== {t}: {len(df)} dies =====")
    print("Dates duplicades:", df.index.duplicated().sum())
    print("Valors nuls:", df.isna().sum().sum())
    print("Preus <= 0:", (df[PREUS] <= 0).sum().sum())
    print("Files amb High < Low:", (df["High"] < df["Low"]).sum())
    print("Salt més gran entre dues dates:", df.index.to_series().diff().max())

    df = df[~df.index.duplicated()]
    df = df[~((df[PREUS] <= 0).any(axis=1) | (df["High"] < df["Low"]))]
    df = df.ffill()

    df["ret"] = df["Close"].pct_change()
    df = df.dropna()
    print("Rendiments diaris de més del 15% (no s'esborren, cal mirar-los):")
    print(df.loc[df["ret"].abs() > 0.15, "ret"].round(3).to_string())

    df["split"] = "train"
    df.loc["2023-01-01":, "split"] = "test"
    print(df["split"].value_counts().to_string())
    df.to_csv(f"data/clean/{t}.csv")