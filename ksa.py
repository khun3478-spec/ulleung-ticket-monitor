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

    def create_session(self) -> None:
        """
        예약 페이지 접속
        JSESSIONID 자동 생성
        """

        response = self.session.get(
            BOOKING_URL,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

    def search(self, watch: WatchItem) -> list[dict]:

        self.create_session()

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

        print(data)

        print("result :", len(data.get("result", [])))

        print("resultAll :", len(data.get("resultAll", [])))

        if data.get("errCode") != 0:
            raise RuntimeError(
                f"KSA Error : {data.get('errCode')} "
                f"{data.get('message')}"
            )

        return data.get("resultAll", [])

    def get_vessels(
        self,
        watch: WatchItem,
    ) -> list[dict]:

        vessels = []
    
        
        for item in self.search(watch):

            print(item)
            #
            # 노선 확인
            #
            if str(item.get("f_portid")) != watch.f_portid:
                continue

            if str(item.get("t_portid")) != watch.t_portid:
                continue

            #
            # 선박 확인
            #
            if item.get("vessel") != watch.vessel:
                continue

            vessels.append(item)

        #
        # 출항시간 + 객실 기준 정렬
        #
        vessels.sort(
            key=lambda x: (
                x.get("departuretime"),
                int(x.get("classesid", 0)),
            )
        )

        return vessels

    @staticmethod
    def departure(vessel: dict) -> str:
        return vessel["departuretime"].split(" ")[1]

    @staticmethod
    def arrival(vessel: dict) -> str:
        return vessel["arrivaltime"].split(" ")[1]

    @staticmethod
    def classes(vessel: dict) -> str:
        return vessel.get("classes", "")

    @staticmethod
    def classes_id(vessel: dict) -> str:
        return str(vessel.get("classesid"))

    @staticmethod
    def remain(vessel: dict) -> int:
        """
        실제 온라인 예약 가능 좌석
        """
        return int(float(vessel.get("onlinecnt", 0)))

    @staticmethod
    def is_possible(vessel: dict) -> bool:
        return vessel.get("ispossible") == "1"

    @staticmethod
    def impossible_reason(vessel: dict) -> str:
        return vessel.get(
            "impossiblereason",
            "",
        )

    @staticmethod
    def vessel_name(vessel: dict) -> str:
        return vessel.get("vessel", "")
