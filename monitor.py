from datetime import datetime

from config import (WATCH_LIST, TEST_MODE)
from ksa import KSAClient
from state import StateManager
from telegram_bot import TelegramBot


def log(message: str):
    print(
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}",
        flush=True,
    )


def print_route_header(route, date):

    log("")
    log("=" * 60)
    log(route)
    log(date)
    log("=" * 60)


def main():

    log("")
    log("울릉도 티켓 모니터 시작")

    ksa = KSAClient()

    telegram = TelegramBot()

    state = StateManager()

    for watch in WATCH_LIST:

        try:

            print_route_header(
                watch.route,
                watch.masterdate,
            )

            vessels = ksa.get_vessels(watch)

            if not vessels:

                log("조회 결과 없음")

                continue

            available_exists = False

            for vessel in vessels:

                departure = ksa.departure(vessel)

                arrival = ksa.arrival(vessel)

                classes = ksa.classes(vessel)

                remain = ksa.remain(vessel)

                possible = ksa.is_possible(vessel)

                reason = ksa.impossible_reason(vessel)

                log(
                    f"{departure}"
                    f" | {classes}"
                    f" | 예약가능={possible}"
                    f" | online={remain}"
                )

                if reason:

                    log(f"사유 : {reason}")

                #
                # 예약 가능
                #
                if TEST_MODE or possible:

                    available_exists = True

                    if (not TEST_MODE) and state.is_notified(
                        watch,
                        vessel,
                    ):

                        log(
                            f"{departure} "
                            f"{classes} "
                            f"이미 발송됨"
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
                        f"{departure} "
                        f"{classes} "
                        f"Telegram 발송"
                    )

            #
            # 모두 예약불가
            #
            if not available_exists:

                state.clear_route(
                    watch,
                    vessels,
                )

                log("예약 가능한 객실 없음")

        except Exception as e:

            log("ERROR")

            log(type(e).__name__)

            log(str(e))

    log("")
    log("모니터 종료")


if __name__ == "__main__":
    main()
