import os
import requests

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": "✅ 울릉도 티켓 모니터 테스트 성공!"
}

r = requests.post(url, json=data)

print(r.status_code)
print(r.text)
