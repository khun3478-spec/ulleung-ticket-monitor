from datetime import datetime

from config import WATCH_LIST
from ksa import KSAClient
from state import StateManager
from telegram_bot import TelegramBot


def log(message: str) -> None:
    print(
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}",
        flush=True,
    )


def main():
    log("===== 울릉도 티켓 모니터 시작 =====")

    ksa = KSAClient()
    telegram = TelegramBot()
    state = StateManager()

    for watch in WATCH_LIST:

        log(
            f"조회 : {watch.route} "
            f"({watch.masterdate} {watch.departure_time})"
        )

        try:
            vessel = ksa.find_target(watch)

            if vessel is None:
                log("대상 선편을 찾지 못했습니다.")
                continue

            possible = ksa.is_possible(vessel)
            reason = ksa.impossible_reason(vessel)
            remain = ksa.available_count(vessel)

            log(
                f"선박={vessel.get('vessel')} "
                f"출항={vessel.get('departuretime')} "
                f"ispossible={vessel.get('ispossible')} "
                f"잔여={remain} "
                f"사유={reason}"
            )

            if possible:

                if state.is_notified(watch):
                    log("이미 알림 발송됨")
                    continue

                telegram.send_available(
                    watch,
                    vessel,
                )

                state.set_notified(watch)

                log("Telegram 발송 완료")

            else:

                state.clear(watch)

                log("예약 불가")

        except Exception as e:

            log(f"ERROR : {type(e).__name__}")

            log(str(e))

    log("===== 종료 =====")


if __name__ == "__main__":
    main()
