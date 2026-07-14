from dataclasses import dataclass
import os

# =========================
# URLs
# =========================

BASE_URL = "https://island.theksa.co.kr"

BOOKING_PAGE = f"{BASE_URL}/page/booking"

API_URL = f"{BASE_URL}/booking/selectDepartureList"

# =========================
# Request
# =========================

REQUEST_HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": BASE_URL,
    "Referer": BOOKING_PAGE,
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

REQUEST_TIMEOUT = 20

# =========================
# Telegram
# =========================

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

TELEGRAM_CHAT_ID = os.environ.get(
    "TELEGRAM_CHAT_ID",
    "8622503258",
)

# =========================
# State
# =========================

STATE_FILE = "state.json"

# =========================
# Watch Route
# =========================


@dataclass(frozen=True)
class WatchItem:
    route: str

    masterdate: str

    departure_time: str

    vessel: str

    t_portidlist: str
    t_portsubidlist: str

    f_portidlist: str
    f_portsubidlist: str


WATCH_LIST = [

    # 2026-08-14
    WatchItem(
        route="묵호 → 울릉도 도동",
        masterdate="2026-08-14",

        # 시간은 더 이상 고정하지 않음
        departure_time="",

        vessel="씨스타 1",

        # 출발 : 묵호
        f_portidlist="4403",
        f_portsubidlist="0",

        # 도착 : 울릉도 도동
        t_portidlist="4311",
        t_portsubidlist="3",
    ),

    # 2026-08-17
    WatchItem(
        route="울릉도 도동 → 묵호",
        masterdate="2026-08-17",

        departure_time="",

        vessel="씨스타 1",

        # 출발 : 울릉도 도동
        f_portidlist="4311",
        f_portsubidlist="3",

        # 도착 : 묵호
        t_portidlist="4403",
        t_portsubidlist="0",
    ),
]
