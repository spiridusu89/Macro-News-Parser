import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def format_telegram_message(llm_response, headlines):
    summary = llm_response.get("summary", "No summary provided.")
    impact = llm_response.get("impact", {})
    reasons = llm_response.get("reasons", {})
    gpt_prompt = llm_response.get("prompt", "No GPT prompt generated.")

    msg = f"📰 *Daily News Summary*\n\n"
    msg += f"📌 *Global Summary:*\n{summary}\n\n"

    if impact:
        msg += "📊 *Ticker Impact:*\n"
        for ticker, sentiment in impact.items():
            reason_titles = reasons.get(ticker, [])
            title_str = "; ".join(reason_titles) if reason_titles else "No specific title"
            msg += f"- `{ticker}`: *{sentiment}* _(from \"{title_str}\")_\n"
        msg += "\n"

    msg += f"🎯 *GPT Prompt:*\n`{gpt_prompt}`\n\n"

    if headlines:
        msg += "📎 *Headlines:*\n"
        for i, h in enumerate(headlines, start=1):
            msg += f"{i}. {h['title']}\n"

    return msg

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }

    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Telegram send failed: {response.status_code} - {response.text}")
