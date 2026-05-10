import yfinance as yf
import matplotlib
matplotlib.use("Agg")  # Render.com uchun muhim — display yo'q
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

YFINANCE_SYMBOLS = {
    "BTCUSDT": "BTC-USD",
    "ETHUSDT": "ETH-USD",
    "XAUUSD": "GC=F",
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "USDJPY": "JPY=X",
}

OUTPUT_DIR = "charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_chart(symbol: str) -> str | None:
    try:
        yf_sym = YFINANCE_SYMBOLS.get(symbol, symbol)
        ticker = yf.Ticker(yf_sym)
        hist = ticker.history(period="3mo", interval="1d")

        if hist.empty:
            return None

        closes = hist["Close"]
        highs = hist["High"]
        lows = hist["Low"]

        resistance = highs.rolling(20).max().iloc[-1]
        support = lows.rolling(20).min().iloc[-1]
        ma20 = closes.rolling(20).mean()
        ma50 = closes.rolling(50).mean()
        current = closes.iloc[-1]

        # Signal rangi
        if current > ma20.iloc[-1] and current > ma50.iloc[-1]:
            signal_color = "#00ff88"
            signal_text = "✅ BUY ZONA"
        elif current < ma20.iloc[-1] and current < ma50.iloc[-1]:
            signal_color = "#ff4444"
            signal_text = "🔻 SELL ZONA"
        else:
            signal_color = "#ffaa00"
            signal_text = "⚠️ KUTISH"

        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor("#0d1117")
        ax.set_facecolor("#0d1117")

        # Narx chizig'i
        ax.plot(closes.index, closes.values, color="#4fc3f7", linewidth=1.5, label="Narx", zorder=3)

        # MA chiziqlar
        ax.plot(ma20.index, ma20.values, color="#ff9800", linewidth=1, linestyle="--", label="MA20", zorder=2)
        ax.plot(ma50.index, ma50.values, color="#ab47bc", linewidth=1, linestyle="--", label="MA50", zorder=2)

        # Resistance zona (qizil)
        ax.axhline(y=resistance, color="#ff4444", linewidth=1.5, linestyle="-", label=f"Resistance: {resistance:,.4f}", zorder=2)
        ax.axhspan(resistance * 0.998, resistance * 1.002, alpha=0.15, color="#ff4444", zorder=1)

        # Support zona (yashil)
        ax.axhline(y=support, color="#00ff88", linewidth=1.5, linestyle="-", label=f"Support: {support:,.4f}", zorder=2)
        ax.axhspan(support * 0.998, support * 1.002, alpha=0.15, color="#00ff88", zorder=1)

        # Joriy narx
        ax.axhline(y=current, color="#ffffff", linewidth=1, linestyle=":", alpha=0.7, zorder=2)

        # Signal matni
        ax.text(
            0.02, 0.95, signal_text,
            transform=ax.transAxes,
            fontsize=13, fontweight="bold",
            color=signal_color,
            verticalalignment="top",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#1a1a2e", edgecolor=signal_color, alpha=0.9)
        )

        # Styling
        ax.set_title(f"{symbol} — Kuchli Zonalar Tahlili", color="white", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Sana", color="#aaaaaa", fontsize=10)
        ax.set_ylabel("Narx", color="#aaaaaa", fontsize=10)
        ax.tick_params(colors="#aaaaaa")
        ax.spines["bottom"].set_color("#333333")
        ax.spines["top"].set_color("#333333")
        ax.spines["left"].set_color("#333333")
        ax.spines["right"].set_color("#333333")
        ax.grid(color="#1e1e2e", linewidth=0.5, linestyle="-", alpha=0.8)
        ax.legend(loc="upper right", facecolor="#1a1a2e", edgecolor="#333333", labelcolor="white", fontsize=9)

        plt.tight_layout()
        path = os.path.join(OUTPUT_DIR, f"{symbol}.png")
        plt.savefig(path, dpi=120, bbox_inches="tight", facecolor=fig.get_facecolor())
        plt.close()
        return path

    except Exception as e:
        print(f"Grafik xatosi: {e}")
        return None