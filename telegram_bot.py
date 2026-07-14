import requests
from config import TELEGRAM_TOKEN, CHAT_ID


def send_message(message: str):
    """
    텔레그램 메시지 전송
    """

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        r = requests.post(url, json=data, timeout=20)

        if r.status_code == 200:
            print("Telegram OK")
            return True

        print(r.text)
        return False

    except Exception as e:
        print(e)
        return False
