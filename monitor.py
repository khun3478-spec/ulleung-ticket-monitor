from ksa import KSAClient
from state import StateManager
from telegram_bot import send_message

BOOKING_URL = "https://island.theksa.co.kr/page/booking"

WATCH_LIST = [
    {
    "name": "가는편",
    "date": "2026-08-14",
    "from_port": "4403",
    "from_sub": "0",
    "to_port": "4311",
    "to_sub": "3",
    "people": 3,
    "ship": "씨스타",
    "departure_time": "12:00"
    },    
    {
        "name": "오는편",
        "date": "2026-08-17",
        "from_port": "4311",
        "from_sub": "3",
        "to_port": "4403",
        "to_sub": "0",
        "people": 5,
        "ship": "씨스타"
    }
]


client = KSAClient()
state = StateManager()


def make_key(item):
    return (
        f"{item['date']}_"
        f"{item['from_port']}_"
        f"{item['to_port']}"
    )


def find_ship(result_list, keyword):

    for ship in result_list:

        vessel = client.vessel(ship)

        if keyword in vessel:
            return ship

    return None
def make_message(item, ship):

    remain = client.remain(ship)

    return f"""
🚢 울릉도 취소표 발견!

구분 : {item['name']}

출발일 : {item['date']}

선박 : {client.vessel(ship)}

출발 : {client.departure(ship)}

도착 : {client.arrival(ship)}

선사 : {client.company(ship)}

총 좌석 : {client.capacity(ship)}

사용 좌석 : {client.occupied(ship)}

남은 좌석(계산) : {remain}

예약상태 : 예약 가능

예매하기
{BOOKING_URL}
"""


def process(item):

    print(f"[CHECK] {item['name']}")

    result = client.search(
        item["date"],
        item["from_port"],
        item["from_sub"],
        item["to_port"],
        item["to_sub"],
    )

    if len(result) == 0:
        print("조회 결과 없음")
        return

    ship = find_ship(
        result,
        item["ship"],
    )

    if ship is None:
        print("선박 없음")
        return

    key = make_key(item)
        if client.available(ship):

        print("예약 가능")

        if state.is_changed(key, "AVAILABLE"):

            message = make_message(item, ship)

            send_message(message)

            print("Telegram 전송 완료")

        else:

            print("이미 알림 보냄")

        return

    print("예약 불가")

    print(client.impossible_reason(ship))

    state.reset(key)
    def is_target_ship(item, ship):
    """
    감시 대상 배인지 확인
    """

    vessel = client.vessel(ship)

    if item["ship"] not in vessel:
        return False

    departure = client.departure(ship)

    # 출발시간 조건이 있으면 검사
    target_time = item.get("departure_time")

    if target_time:

        if target_time not in departure:
            return False

    return True


def main():

    print("=" * 60)
    print("울릉도 티켓 모니터 시작")
    print("=" * 60)

    for item in WATCH_LIST:

        try:

            process(item)

        except Exception as e:

            print(e)

    print("=" * 60)
    print("모니터 종료")
    print("=" * 60)


if __name__ == "__main__":
    main()
