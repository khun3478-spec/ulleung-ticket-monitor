import os

# ==========================================
# KSA API
# ==========================================

KSA_API_URL = "https://island.theksa.co.kr/booking/selectDepartureList"
BOOKING_PAGE = "https://island.theksa.co.kr/page/booking"

REQUEST_HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://island.theksa.co.kr",
    "Referer": BOOKING_PAGE,
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
}

# ==========================================
# Telegram
# ==========================================

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "8622503258")

# ==========================================
# State
# ==========================================

STATE_FILE = "state.json"

# ==========================================
# Watch List
# ==========================================

WATCH_LIST = [
    {
        "name": "묵호 → 울릉도 도동",
        "masterdate": "2026-08-14",
        "t_portsubidlist": "",
        "t_portidlist": "1001",
        "f_portsubidlist": "",
        "f_portidlist": "2101",
        "departure_time": "12:00",
        "ship_name": "씨스타",
    },
    {
        "name": "울릉도 도동 → 묵호",
        "masterdate": "2026-08-17",
        "t_portsubidlist": "",
        "t_portidlist": "2101",
        "f_portsubidlist": "",
        "f_portidlist": "1001",
        "departure_time": "",
        "ship_name": "씨스타",
    },
]

# ==========================================
# Common Payload
# ==========================================

COMMON_PAYLOAD = {
    "lang": "ko",
    "sourcesiteid": "inew",
}

# ==========================================
# Timeout
# ==========================================

REQUEST_TIMEOUT = 20
