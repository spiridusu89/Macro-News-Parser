import requests
from bs4 import BeautifulSoup

def fetch_yahoo_finance_headlines():
    url = "https://finance.yahoo.com/"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.select("li.js-stream-content")

    headlines = []
    for article in articles:
        title_tag = article.select_one("h3 a")
        summary_tag = article.select_one("p")  # lead text

        if not title_tag or not title_tag.text:
            continue

        title = title_tag.text.strip()
        summary = summary_tag.text.strip() if summary_tag else ""

        # curățăm titlurile irelevante (ex: "Live", "Video", etc.)
        if any(bad in title.lower() for bad in ["live", "video", "podcast", "watch"]):
            continue

        headlines.append({
            "title": title,
            "summary": summary
        })

        if len(headlines) >= 5:  # limităm la cele mai recente 5
            break

    return headlines

# funcția principală de parser pe care o va apela main.py
def get_headlines():
    return fetch_yahoo_finance_headlines()
