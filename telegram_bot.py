import requests

from config import (
    BOOKING_URL,
    REQUEST_TIMEOUT,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    WatchItem,
)
from ksa import KSAClient


class TelegramBot:

    def __init__(self):

        self.url = (
            f"https://api.telegram.org/bot"
            f"{TELEGRAM_BOT_TOKEN}/sendMessage"
        )

    def send_available(
        self,
        watch: WatchItem,
        vessel: dict,
    ) -> None:

        departure = KSAClient.departure(vessel)
        arrival = KSAClient.arrival(vessel)
        remain = KSAClient.remain(vessel)
        classes = KSAClient.classes(vessel)

        message = (
            "🚢 <b>울릉도 예약 가능!</b>\n\n"

            f"🛳 노선 : {watch.route}\n"
            f"📅 출발일 : {watch.masterdate}\n"
            f"🕒 출발 : {departure}\n"
            f"🕓 도착 : {arrival}\n"
            f"⛴ 선박 : {KSAClient.vessel_name(vessel)}\n"
            f"💺 객실 : {classes}\n"
            f"✅ 온라인 예약 가능 : {remain}석\n\n"

            f"<a href=\"{BOOKING_URL}\">예약 페이지 바로가기</a>"
        )

        response = requests.post(
            self.url,
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": False,
            },
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()
