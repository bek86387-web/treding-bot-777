import yfinance as yf
import requests

COINGECKO_IDS = {
    "BTCUSDT": "bitcoin",
    "ETHUSDT": "ethereum",
    "XAUUSD": None,  # yfinance orqali
    "EURUSD": None,
    "GBPUSD": None,
}

YFINANCE_SYMBOLS = {
    "XAUUSD": "GC=F",
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "USDJPY": "JPY=X",
    "BTCUSDT": "BTC-USD",
    "ETHUSDT": "ETH-USD",
}


def get_price(symbol: str) -> str:
    try:
        # Crypto narxlari — CoinGecko
        if symbol in ["BTCUSDT", "ETHUSDT"]:
            coin_id = COINGECKO_IDS.get(symbol)
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true"
            r = requests.get(url, timeout=10)
            data = r.json()
            price = data[coin_id]["usd"]
            change = data[coin_id].get("usd_24h_change", 0)
            emoji = "🟢" if change > 0 else "🔴"
            return (
                f"💰 *{symbol}*\n"
                f"Narx: `${price:,.2f}`\n"
                f"{emoji} 24s o'zgarish: `{change:.2f}%`"
            )

        # Forex va Oltin — yfinance
        yf_sym = YFINANCE_SYMBOLS.get(symbol, symbol)
        ticker = yf.Ticker(yf_sym)
        hist = ticker.history(period="2d")
        if hist.empty:
            return f"❌ {symbol} uchun ma'lumot topilmadi."
        last = hist["Close"].iloc[-1]
        prev = hist["Close"].iloc[-2] if len(hist) > 1 else last
        change = ((last - prev) / prev) * 100
        emoji = "🟢" if change > 0 else "🔴"
        return (
            f"💰 *{symbol}*\n"
            f"Narx: `{last:,.4f}`\n"
            f"{emoji} O'zgarish: `{change:.2f}%`"
        )
    except Exception as e:
        return f"❌ Narx olishda xato: {str(e)}"


def get_analysis(symbol: str) -> str:
    try:
        yf_sym = YFINANCE_SYMBOLS.get(symbol, symbol)
        ticker = yf.Ticker(yf_sym)
        hist = ticker.history(period="3mo", interval="1d")

        if hist.empty:
            return f"❌ {symbol} uchun ma'lumot topilmadi."

        closes = hist["Close"]
        highs = hist["High"]
        lows = hist["Low"]

        current = closes.iloc[-1]
        resistance = highs.rolling(20).max().iloc[-1]
        support = lows.rolling(20).min().iloc[-1]
        ma20 = closes.rolling(20).mean().iloc[-1]
        ma50 = closes.rolling(50).mean().iloc[-1]

        # Signal
        if current > ma20 and current > ma50:
            signal = "🟢 BUY — Narx MA20 va MA50 dan yuqorida"
        elif current < ma20 and current < ma50:
            signal = "🔴 SELL — Narx MA20 va MA50 dan pastda"
        else:
            signal = "🟡 KUTISH — Narx noaniq holatda"

        dist_resistance = ((resistance - current) / current) * 100
        dist_support = ((current - support) / current) * 100

        return (
            f"📊 *{symbol} Tahlil*\n\n"
            f"💵 Joriy narx: `{current:,.4f}`\n\n"
            f"🔴 Resistance (Qarshilik): `{resistance:,.4f}` ({dist_resistance:.1f}% yuqorida)\n"
            f"🟢 Support (Tayanch): `{support:,.4f}` ({dist_support:.1f}% pastda)\n\n"
            f"📈 MA20: `{ma20:,.4f}`\n"
            f"📉 MA50: `{ma50:,.4f}`\n\n"
            f"📌 Signal: {signal}"
        )
    except Exception as e:
        return f"❌ Tahlil xatosi: {str(e)}"