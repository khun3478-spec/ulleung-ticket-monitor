import requests
from config import API_URL, HEADERS


class KSAClient:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def search(
        self,
        date: str,
        from_port: str,
        from_sub: str,
        to_port: str,
        to_sub: str,
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

        r = self.session.post(
            API_URL,
            data=payload,
            timeout=20,
        )

        r.raise_for_status()

        data = r.json()

        if not data.get("result"):
            return []

        return data["result"]

    def available(self, ship):

        return ship.get("ispossible") == "1"

    def reason(self, ship):

        return ship.get("impossiblereason", "")

    def vessel(self, ship):

        return ship.get("vessel", "")

    def departure(self, ship):

        return ship.get("departuretime", "")

    def arrival(self, ship):

        return ship.get("arrivaltime", "")

    def company(self, ship):

        return ship.get("company", "")

    def capacity(self, ship):

        return int(ship.get("capacity", 0))

    def occupied(self, ship):

        return int(ship.get("occupiedcnt", 0))

    def remain(self, ship):

        return self.capacity(ship) - self.occupied(ship)

    def notice(self, ship):

        return ship.get("onlinecntnotice", "")

    def impossible_reason(self, ship):

        return ship.get("impossiblereason", "")
