import json
from pathlib import Path

from config import STATE_FILE, WatchItem
from ksa import KSAClient


class StateManager:

    def __init__(self):
        self.path = Path(STATE_FILE)
        self.state = self._load()

    def _load(self) -> dict:

        if not self.path.exists():
            return {}

        try:
            with self.path.open(
                "r",
                encoding="utf-8",
            ) as f:

                data = json.load(f)

            if isinstance(data, dict):
                return data

        except Exception:
            pass

        return {}

    def save(self):

        with self.path.open(
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                self.state,
                f,
                ensure_ascii=False,
                indent=4,
                sort_keys=True,
            )

    @staticmethod
    def make_key(
        watch: WatchItem,
        vessel: dict,
    ) -> str:

        return "|".join(
            [
                watch.masterdate,
                watch.name,
                KSAClient.departure(vessel),
                vessel["vessel"],
            ]
        )

    def is_notified(
        self,
        watch: WatchItem,
        vessel: dict,
    ) -> bool:

        key = self.make_key(
            watch,
            vessel,
        )

        return self.state.get(key, False)

    def set_notified(
        self,
        watch: WatchItem,
        vessel: dict,
    ):

        key = self.make_key(
            watch,
            vessel,
        )

        self.state[key] = True

        self.save()

    def clear(
        self,
        watch: WatchItem,
        vessel: dict,
    ):

        key = self.make_key(
            watch,
            vessel,
        )

        if key in self.state:

            del self.state[key]

            self.save()

    def clear_route(
        self,
        watch: WatchItem,
        vessels: list[dict],
    ):
        """
        해당 노선이 모두 예약불가가 되었을 때
        상태를 초기화한다.
        """

        for vessel in vessels:

            if KSAClient.is_possible(vessel):
                return

        for vessel in vessels:

            key = self.make_key(
                watch,
                vessel,
            )

            self.state.pop(
                key,
                None,
            )

        self.save()
