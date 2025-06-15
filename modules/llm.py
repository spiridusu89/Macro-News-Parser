import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GPT_MODEL = os.getenv("GPT_MODEL", "openai/gpt-4.1")

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "https://yourproject.com",
    "Content-Type": "application/json"
}

TICKERS_OF_INTEREST = [
    # AI & Tech
    "NVDA", "TSM", "ARM", "SMCI", "MU", "PLTR", "CRWV", "OKLO", "CEG", "VST",
    "BWXT", "GEV", "GOOGL", "ORCL", "NOW", "SNOW", "DDOG", "ANET", "CIEN", "VRT",
    "HPE", "NICE", "Cerebras",  # companie nelistată încă

    # Commodities (tickere oficiale)
    "CL",     # Crude Oil WTI
    "XAU/USD",  # Gold
    "XAG/USD",  # Silver
    "PL",     # Platinum

    # Indici bursieri (tickere oficiale)
    "RUT",      # Russell 2000
    "SPX",      # S&P 500
    "NDX",      # Nasdaq 100
    "DJI",      # Dow Jones
    "STOXX50E", # Euro Stoxx 50
    "FTSE",     # FTSE 100
    "DAX",    # DAX
    "N225",     # Nikkei 225

    # Crypto
    "BTC-USD",  # Bitcoin
    "DOGE-USD"  # Dogecoin
]

def build_prompt(headlines, tickers):
    headline_block = "\n".join(
        f'- "{h["title"]}"\n  Summary: "{h["summary"]}"'
        for h in headlines
    )
    tickers_block = ", ".join(tickers)

    prompt = f"""
You are a financial reasoning assistant specialized in macroeconomic news, geopolitics, and stock market impact.

Your task is to analyze the following news headlines and summaries. You will be given:
- A list of news items (each with a title and a short summary)
- A list of stock tickers of interest

Instructions:

1. For each ticker:
   - Decide if it is affected by any of the news.
   - If yes, identify which headline(s) are relevant.
   - Determine the direction of impact: positive / negative / neutral.

2. Write a brief overall summary of the current market sentiment and context based on all headlines (2–3 sentences).

3. Create a structured response with:
   - A global summary.
   - A section called "impact" listing each ticker and the impact.
   - A section "reasons" explaining which headlines affect which tickers.
   - A final section "prompt": generate a ChatGPT-style question that can be used for deeper analysis of the affected tickers and their context.

Important:
- Only include tickers that are actually affected in the "reasons" and "prompt".
- Be concise, factual, and avoid speculation.
- The final output must be in valid JSON format with 4 top-level fields: summary, impact, reasons, and prompt.

Below are the inputs:
---
HEADLINES:
{headline_block}

TICKERS OF INTEREST:
{tickers_block}
"""
    return prompt.strip()

def query_llm(headlines):
    prompt = build_prompt(headlines, TICKERS_OF_INTEREST)

    payload = {
        "model": GPT_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=HEADERS,
        json=payload
    )

    if response.status_code != 200:
        raise Exception(f"LLM API failed: {response.status_code} - {response.text}")

    reply = response.json()["choices"][0]["message"]["content"]

    try:
        result = eval(reply) if reply.strip().startswith("{") else {}
    except Exception:
        result = {}

    return result
