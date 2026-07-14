import requests

from config import (
    BOOKING_PAGE,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    WatchItem,
)


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

        remain = (
            int(float(vessel.get("capacity", 0)))
            - int(float(vessel.get("occupiedcnt", 0)))
        )

        if remain < 0:
            remain = 0

departure_time = (
    vessel.get("departuretime", "")
    .split(" ")[-1]
)

message = (
    "🚢 <b>울릉도 예약 가능!</b>\n\n"
    f"노선 : {watch.route}\n"
    f"출발일 : {watch.masterdate}\n"
    f"출발시간 : {departure_time}\n"
    f"선박 : {vessel.get('vessel')}\n"
    f"예약 가능 : {remain}석\n\n"
    f"<a href=\"{BOOKING_PAGE}\">예약페이지 바로가기</a>"
)
        )

        response = requests.post(
            self.url,
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": False,
            },
            timeout=20,
        )

        response.raise_for_status()
