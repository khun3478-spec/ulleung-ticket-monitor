from datetime import datetime

from config import WATCH_LIST
from ksa import KSAClient
from state import StateManager
from telegram_bot import TelegramBot


def log(message: str):

    print(
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}",
        flush=True,
    )


def main():

    log("========================================")
    log("울릉도 티켓 모니터 시작")
    log("========================================")

    ksa = KSAClient()
    telegram = TelegramBot()
    state = StateManager()

    for watch in WATCH_LIST:

        log("")
        log(f"노선 : {watch.name}")
        log(f"날짜 : {watch.masterdate}")

        try:

            vessels = ksa.get_vessels(watch)

            if not vessels:

                log("조회 결과 없음")
                continue

            available_found = False

            for vessel in vessels:

                departure = ksa.departure(vessel)

                remain = ksa.remain(vessel)

                possible = ksa.is_possible(vessel)

                reason = ksa.impossible_reason(vessel)

                log(
                    f"[{departure}] "
                    f"ispossible={vessel['ispossible']} "
                    f"remain={remain} "
                    f"reason={reason}"
                )

                #
                # 예약 가능
                #
                if possible:

                    available_found = True

                    if state.is_notified(
                        watch,
                        vessel,
                    ):

                        log(
                            f"[{departure}] 이미 알림 발송"
                        )

                        continue

                    telegram.send_available(
                        watch,
                        vessel,
                    )

                    state.set_notified(
                        watch,
                        vessel,
                    )

                    log(
                        f"[{departure}] Telegram 발송 완료"
                    )

            #
            # 모든 배편이 예약불가
            #
            if not available_found:

                state.clear_route(
                    watch,
                    vessels,
                )

                log("예약 가능한 배편 없음")

        except Exception as e:

            log(
                f"ERROR : {type(e).__name__}"
            )

            log(str(e))

    log("")
    log("========================================")
    log("모니터 종료")
    log("========================================")


if __name__ == "__main__":
    main()
