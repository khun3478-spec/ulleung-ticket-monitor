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
        "ship": "씨스타"
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
