# 📰 Macro News Bot – Telegram Alert for Market Open

This bot automatically:
- Scrapes financial headlines (from Yahoo Finance)
- Uses GPT-4.1 via OpenRouter to analyze news
- Detects impact on a watchlist of tickers (stocks, indices, commodities, crypto)
- Sends a Telegram message 1 hour before NYSE opens (08:30 AM New York time)

## ✅ Features
- Stateless: no files saved, runs in memory
- Hosted on Render (free tier)
- Daily ping via `render.yaml` cron
- Output delivered via Telegram

## 🛠️ Stack
- Python 3.x
- OpenRouter (GPT-4.1)
- Telegram Bot API
- BeautifulSoup + Requests

## 🔧 .env Configuration

Set the following secrets in your Render dashboard or `.env` file:
- OPENROUTER_API_KEY=your_openrouter_key
- TELEGRAM_BOT_TOKEN=your_telegram_bot_token
- TELEGRAM_CHAT_ID=your_chat_id
- GPT_MODEL=openai/gpt-4.1

## 🧠 Custom Watchlist

Tickers analyzed daily:
- AI/Tech: NVDA, PLTR, ARM, SMCI, MU, TSM, ORCL, etc.
- Nuclear: BWXT, CEG, VST
- Commodities: XAU/USD, CL=F, XAG/USD
- Indices: SPX, NDX, RUT, STOXX50E, FTSE, etc.
- Crypto: BTC-USD, DOGE-USD
- Special: Cerebras (IPO watch)

## 🕒 Run Schedule

Set in `render.yaml` to run once per day:
- **12:30 UTC** = 08:30 New York = 15:30 Romania (GMT+3)

## 🚀 Deployment (Render)
1. Push code to GitHub
2. Import repo in [render.com](https://render.com/)
3. Add `.env` variables in dashboard
4. Confirm `render.yaml` is detected
5. Done – bot will run daily and send alerts via Telegram
