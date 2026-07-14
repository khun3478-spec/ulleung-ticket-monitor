from dataclasses import dataclass
import os

# ==========================================================
# KSA
# ==========================================================

BASE_URL = "https://island.theksa.co.kr"

BOOKING_URL = f"{BASE_URL}/page/booking"
API_URL = f"{BASE_URL}/booking/selectDepartureList"

REQUEST_TIMEOUT = 20

HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": BASE_URL,
    "Referer": BOOKING_URL,
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/146.0.0.0 "
        "Safari/537.36"
    ),
    "X-Requested-With": "XMLHttpRequest",
}

COMMON_PAYLOAD = {
    "lang": "ko",
    "sourcesiteid": "inew",
}

# ==========================================================
# Telegram
# ==========================================================

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# ==========================================================
# State
# ==========================================================

STATE_FILE = "state.json"

# ==========================================================
# Watch Item
# ==========================================================


@dataclass(frozen=True)
class WatchItem:

    route: str

    masterdate: str

    f_portid: str
    f_portsubid: str

    t_portid: str
    t_portsubid: str

    vessel: str = "씨스타 1"


# ==========================================================
# Watch List
# ==========================================================

WATCH_LIST = [

    #
    # 묵호 → 울릉도 도동
    #
    WatchItem(
        route="묵호 → 울릉도 도동",

        masterdate="2026-08-14",

        f_portid="4403",
        f_portsubid="0",

        t_portid="4311",
        t_portsubid="3",
    ),

    #
    # 울릉도 도동 → 묵호
    #
    WatchItem(
        route="울릉도 도동 → 묵호",

        masterdate="2026-08-17",

        f_portid="4311",
        f_portsubid="3",

        t_portid="4403",
        t_portsubid="0",
    ),

]
