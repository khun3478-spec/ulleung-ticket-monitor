import requests
from config import API_URL, HEADERS


class KSAClient:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def search(
        self,
        date,
        from_port,
        from_sub,
        to_port,
        to_sub,
    ):

        payload = {
            "masterdate": date,
            "f_portidlist": from_port,
            "f_portsubidlist": from_sub,
            "t_portidlist": to_port,
            "t_portsubidlist": to_sub,
            "lang": "ko",
            "sourcesiteid": "inew",
        }

        response = self.session.post(
            API_URL,
            data=payload,
            timeout=20,
        )

        response.raise_for_status()

        data = response.json()

        if not data.get("result"):
            return []

        return data["result"]
            @staticmethod
    def is_available(ship):

        return ship.get("ispossible") == "1"

    @staticmethod
    def vessel(ship):

        return ship.get("vessel", "")

    @staticmethod
    def departure(ship):

        return ship.get("departuretime", "")

    @staticmethod
    def arrival(ship):

        return ship.get("arrivaltime", "")

    @staticmethod
    def company(ship):

        return ship.get("company", "")

    @staticmethod
    def reason(ship):

        return ship.get("impossiblereason", "")

    @staticmethod
    def notice(ship):

        return ship.get("onlinecntnotice", "")
