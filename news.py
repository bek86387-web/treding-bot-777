import feedparser
import html
import re


RSS_FEEDS = [
    ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("Reuters Biznes", "https://feeds.reuters.com/reuters/businessNews"),
    ("Investing.com", "https://www.investing.com/rss/news_25.rss"),
]


def clean_text(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def get_news(count: int = 5) -> str:
    all_news = []

    for source, url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:2]:
                title = clean_text(entry.get("title", ""))
                link = entry.get("link", "")
                if title:
                    all_news.append((source, title, link))
        except Exception:
            continue

    if not all_news:
        return "❌ Yangiliklar olinmadi. Keyinroq urinib ko'ring."

    result = "📰 *So'nggi Moliyaviy Yangiliklar*\n\n"
    for i, (source, title, link) in enumerate(all_news[:count], 1):
        result += f"{i}. [{title}]({link})\n   📌 _{source}_\n\n"

    return result