import requests

from config import (
    BOOKING_PAGE,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
)


class TelegramBot:
    def __init__(self):
        self.api_url = (
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        )

    def send_available(self, watch: dict) -> None:
        message = (
            "🚢 <b>울릉도 예약 가능!</b>\n\n"
            f"노선 : {watch['name']}\n"
            f"출발일 : {watch['masterdate']}\n"
            f"출발시간 : {watch['departure_time'] or '전체'}\n"
            f"선박 : {watch['ship_name']}\n"
            "상태 : 예약 가능\n\n"
            f"예약페이지\n{BOOKING_PAGE}"
        )

        response = requests.post(
            self.api_url,
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
            timeout=20,
        )

        response.raise_for_status()
