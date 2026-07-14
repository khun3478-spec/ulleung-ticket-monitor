from datetime import datetime

from config import WATCH_LIST
from ksa import KSAClient
from state import StateManager
from telegram_bot import TelegramBot


def log(message: str) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {message}", flush=True)


def main() -> None:
    ksa = KSAClient()
    telegram = TelegramBot()
    state = StateManager()

    log("===== 울릉도 티켓 모니터 시작 =====")

    for watch in WATCH_LIST:
        log(
            f"조회 : {watch['name']} / "
            f"{watch['masterdate']} / "
            f"{watch['departure_time'] or '전체'} / "
            f"{watch['ship_name']}"
        )

        try:
            response = ksa.get_departure_list(watch)
            sailing = ksa.find_target_sailing(response, watch)

            if sailing is None:
                log("대상 선편을 찾지 못했습니다.")
                continue

            possible = ksa.is_available(sailing)
            reason = ksa.impossible_reason(sailing)

            log(
                f"ispossible={sailing.get('ispossible')} "
                f"impossiblereason={reason}"
            )

            if possible:
                if not state.already_notified(watch):
                    telegram.send_available(watch)
                    state.mark_notified(watch)
                    log("Telegram 발송 완료")
                else:
                    log("이미 알림 발송된 상태")
            else:
                state.reset(watch)
                log("예약 불가")

        except Exception as e:
            log(f"오류 : {e}")

    log("===== 모니터 종료 =====")


if __name__ == "__main__":
    main()
