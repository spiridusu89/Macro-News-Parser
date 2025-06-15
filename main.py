from modules.parser import get_headlines
from modules.llm import query_llm
from modules.telegram import format_telegram_message, send_telegram_message

def run_bot():
    try:
        headlines = get_headlines()
        if not headlines:
            send_telegram_message("⚠️ No headlines could be retrieved today.")
            return

        llm_result = query_llm(headlines)
        if not llm_result:
            send_telegram_message("⚠️ LLM failed to analyze the headlines.")
            return

        message = format_telegram_message(llm_result, headlines)
        send_telegram_message(message)

    except Exception as e:
        send_telegram_message(f"❌ Bot crashed:\n{str(e)}")

if __name__ == "__main__":
    run_bot()
