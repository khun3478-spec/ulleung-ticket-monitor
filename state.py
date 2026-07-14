import json
from pathlib import Path

from config import STATE_FILE, WatchItem


class StateManager:
    def __init__(self):
        self.path = Path(STATE_FILE)
        self.state = self._load()

    def _load(self) -> dict:
        if not self.path.exists():
            return {}

        try:
            with self.path.open("r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, dict):
                return data

        except Exception:
            pass

        return {}

    def save(self):
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(
                self.state,
                f,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )

    @staticmethod
    def make_key(watch: WatchItem) -> str:
        return "|".join(
            [
                watch.masterdate,
                watch.route,
                watch.departure_time,
                watch.vessel,
            ]
        )

    def is_notified(self, watch: WatchItem) -> bool:
        return self.state.get(self.make_key(watch), False)

    def set_notified(self, watch: WatchItem):
        self.state[self.make_key(watch)] = True
        self.save()

    def clear(self, watch: WatchItem):
        key = self.make_key(watch)

        if key in self.state:
            del self.state[key]
            self.save()

    def clear_all(self):
        self.state.clear()
        self.save()
