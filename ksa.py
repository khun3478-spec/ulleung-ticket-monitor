import requests

from config import (
    API_URL,
    BOOKING_URL,
    COMMON_PAYLOAD,
    HEADERS,
    REQUEST_TIMEOUT,
    WatchItem,
)


class KSAClient:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def _create_session(self):
        """
        예약 페이지를 먼저 호출하여
        JSESSIONID를 발급받는다.
        """
        response = self.session.get(
            BOOKING_URL,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

    def _request(self, watch: WatchItem) -> dict:

        payload = {
            **COMMON_PAYLOAD,
            "masterdate": watch.masterdate,
            "t_portsubidlist": watch.t_portsubid,
            "t_portidlist": watch.t_portid,
            "f_portsubidlist": watch.f_portsubid,
            "f_portidlist": watch.f_portid,
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
                f"KSA API Error : {data.get('errCode')} {data.get('message')}"
            )

        return data

    def get_vessels(self, watch: WatchItem) -> list[dict]:
        """
        감시 대상 노선의 모든 선편 반환
        """

        self._create_session()

        data = self._request(watch)

        vessels = []

        #
        # resultAll 사용
        #
        for item in data.get("resultAll", []):

            if item.get("vessel") != watch.vessel:
                continue

            if str(item.get("f_portid")) != watch.f_portid:
                continue

            if str(item.get("t_portid")) != watch.t_portid:
                continue

            vessels.append(item)

        #
        # 층(1층/2층) 중복 제거
        #
        unique = {}

        for vessel in vessels:

            key = (
                vessel["departuretime"],
                vessel["vessel"],
            )

            #
            # 같은 출항시간이면
            # 예약 가능한 정보 우선
            #
            if key not in unique:
                unique[key] = vessel
                continue

            if vessel.get("ispossible") == "1":
                unique[key] = vessel

        return list(unique.values())

    @staticmethod
    def is_possible(vessel: dict) -> bool:
        return vessel.get("
