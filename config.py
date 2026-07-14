import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

BASE_URL = "https://island.theksa.co.kr"

API_URL = (
    BASE_URL +
    "/booking/selectDepartureList"
)

HEADERS = {

    "User-Agent":
    "Mozilla/5.0",

    "Referer":
    BASE_URL + "/page/booking",

    "Origin":
    BASE_URL,

    "X-Requested-With":
    "XMLHttpRequest"
}
