import requests

from config import (
    API_URL,
    BOOKING_PAGE,
    COMMON_PAYLOAD,
    REQUEST_HEADERS,
    REQUEST_TIMEOUT,
    WatchItem,
)


class KSAClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(REQUEST_HEADERS)

    def _initialize_session(self) -> None:
        """
        예약 페이지를 먼저 호출하여
        JSESSIONID를 발급받는다.
        """

        response = self.session.get(
            BOOKING_PAGE,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

    def search(self, watch: WatchItem) -> list[dict]:
        self._initialize_session()

        payload = {
            **COMMON_PAYLOAD,
            "masterdate": watch.masterdate,
            "t_portsubidlist": watch.t_portsubidlist,
            "t_portidlist": watch.t_portidlist,
            "f_portsubidlist": watch.f_portsubidlist,
            "f_portidlist": watch.f_portidlist,
        }

        response = self.session.post(
            API_URL,
            data=payload,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("errCode") != 0:
            raise RuntimeError(
                f"KSA API Error : {data.get('errCode')} "
                f"{data.get('message')}"
            )

        return data.get("result", [])

    def find_target(self, watch: WatchItem) -> dict | None:
        vessels = self.search(watch)

        for vessel in vessels:

            if vessel.get("vessel") != watch.vessel:
                continue

            departure = (
                vessel.get("departuretime", "")
                .split(" ")[-1]
                .strip()
            )

            if departure != watch.departure_time:
                continue

            return vessel

        return None

    @staticmethod
    def is_possible(vessel: dict) -> bool:
        return vessel.get("ispossible") == "1"

    @staticmethod
    def impossible_reason(vessel: dict) -> str:
        return vessel.get("impossiblereason", "")

    @staticmethod
    def available_count(vessel: dict) -> int:
        capacity = int(float(vessel.get("capacity", 0)))
        occupied = int(float(vessel.get("occupiedcnt", 0)))
        remain = capacity - occupied

        if remain < 0:
            remain = 0

        return remain
