import requests

from config import (
    COMMON_PAYLOAD,
    KSA_API_URL,
    REQUEST_HEADERS,
    REQUEST_TIMEOUT,
)


class KSAClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(REQUEST_HEADERS)

    def get_departure_list(self, watch: dict) -> dict:
        payload = {
            **COMMON_PAYLOAD,
            "masterdate": watch["masterdate"],
            "t_portsubidlist": watch["t_portsubidlist"],
            "t_portidlist": watch["t_portidlist"],
            "f_portsubidlist": watch["f_portsubidlist"],
            "f_portidlist": watch["f_portidlist"],
        }

        response = self.session.post(
            KSA_API_URL,
            data=payload,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.json()

    def find_target_sailing(self, response_json: dict, watch: dict) -> dict | None:
        """
        응답 JSON에서 감시 대상 선편을 찾는다.
        """

        if isinstance(response_json, list):
            items = response_json
        elif isinstance(response_json, dict):
            for key in (
                "list",
                "departureList",
                "resultList",
                "data",
                "rows",
            ):
                if isinstance(response_json.get(key), list):
                    items = response_json[key]
                    break
            else:
                items = []
        else:
            items = []

        for item in items:
            ship_name = str(
                item.get("shipname")
                or item.get("shipName")
                or item.get("vslnm")
                or ""
            ).strip()

            departure_time = str(
                item.get("departuretime")
                or item.get("departureTime")
                or item.get("deptime")
                or ""
            ).strip()

            if watch["ship_name"] and ship_name != watch["ship_name"]:
                continue

            if watch["departure_time"]:
                if departure_time != watch["departure_time"]:
                    continue

            return item

        return None

    @staticmethod
    def is_available(item: dict) -> bool:
        return str(item.get("ispossible", "0")) == "1"

    @staticmethod
    def impossible_reason(item: dict) -> str:
        return str(item.get("impossiblereason", "")).strip()
