import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

TICKERS = ["SPY", "AAPL", "BTC-USD"]
MODELS = ["Buy & Hold", "SMA 20/50"]
COST = 0.001
Path("figures").mkdir(exist_ok=True)
results = []

for t in TICKERS:
    df = pd.read_csv(f"data/clean/{t}.csv", index_col="Date", parse_dates=True)
    dies_any = 365 if t.endswith("-USD") else 252

    df["Buy & Hold"] = 1.0
    # shift(1): la decisió del dia t només fa servir preus fins al dia t-1
    df["SMA 20/50"] = (df["Close"].rolling(20).mean() > df["Close"].rolling(50).mean()).astype(float).shift(1).fillna(0)

    plt.figure(figsize=(10, 4))
    for split in ["train", "test"]:
        d = df[df["split"] == split]
        for model in MODELS:
            canvis = d[model].diff().abs().fillna(d[model].iloc[0])
            r = d[model] * d["ret"] - COST * canvis
            valor = (1 + r).cumprod()
            results.append({
                "ticker": t,
                "split": split,
                "model": model,
                "rendiment total (%)": (valor.iloc[-1] - 1) * 100,
                "Sharpe": r.mean() / r.std() * dies_any ** 0.5,
                "max drawdown (%)": (valor / valor.cummax() - 1).min() * 100,
                "operacions": int((canvis > 0).sum()),
            })
            if split == "test":
                plt.plot(valor, label=model)

    plt.title(f"{t} (test)")
    plt.ylabel("valor d'1 € invertit")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"figures/baseline_{t}.png")
    plt.close()

print(pd.DataFrame(results).round(2).to_string(index=False))