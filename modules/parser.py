import requests
from bs4 import BeautifulSoup
from datetime import datetime
from email.utils import parsedate_to_datetime

RSS_FEEDS = [
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://feeds.marketwatch.com/marketwatch/topstories/",
    "https://seekingalpha.com/market_currents.xml"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_rss_feed(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.find_all("item")

        today_str = datetime.utcnow().strftime("%Y-%m-%d")
        headlines = []

        for item in items:
            title = item.title.text.strip() if item.title else ""
            summary = item.description.text.strip() if item.description else ""
            pub_date = item.pubDate.text.strip() if item.pubDate else ""

            try:
                pub_datetime = parsedate_to_datetime(pub_date)
                pub_str = pub_datetime.strftime("%Y-%m-%d")
            except Exception:
                continue

            if pub_str != today_str or not title:
                continue

            headlines.append({
                "title": title,
                "summary": summary
            })

        return headlines

    except Exception as e:
        print(f"❌ Error fetching RSS from {url}: {e}")
        return []

def get_headlines():
    all_headlines = []
    seen_titles = set()

    for feed_url in RSS_FEEDS:
        headlines = fetch_rss_feed(feed_url)
        for h in headlines:
            if h["title"] in seen_titles:
                continue
            all_headlines.append(h)
            seen_titles.add(h["title"])

    print(f"✅ Total headlines collected from RSS: {len(all_headlines)}")
    return all_headlines
