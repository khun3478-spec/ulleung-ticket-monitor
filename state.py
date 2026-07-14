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

        """
        배편별 상태 관리

        날짜
        노선
        출발시간
        선박
        객실ID
        """

        return "|".join(
            [
                watch.masterdate,
                watch.route,
                KSAClient.departure(vessel),
                KSAClient.vessel_name(vessel),
                KSAClient.classes_id(vessel),
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

        return self.state.get(
            key,
            False,
        )

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
        해당 노선에 예약 가능한 객실이 하나도 없으면
        상태를 초기화한다.
        """

        #
        # 하나라도 예약가능이면 유지
        #
        for vessel in vessels:

            if KSAClient.is_possible(vessel):
                return

        #
        # 전부 예약불가이면 초기화
        #
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
