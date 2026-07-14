import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

API_URL = "https://island.theksa.co.kr/booking/selectDepartureList"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://island.theksa.co.kr/page/booking"
}
