import json
import os

from config import STATE_FILE


class StateManager:
    def __init__(self):
        self.state = self._load()

    def _load(self) -> dict:
        if not os.path.exists(STATE_FILE):
            return {}

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, dict):
                return data

            return {}

        except Exception:
            return {}

    def save(self) -> None:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(
                self.state,
                f,
                ensure_ascii=False,
                indent=2,
            )

    @staticmethod
    def make_key(watch: dict) -> str:
        return "|".join(
            [
                watch["masterdate"],
                watch["name"],
                watch["departure_time"],
                watch["ship_name"],
            ]
        )

    def already_notified(self, watch: dict) -> bool:
        key = self.make_key(watch)
        return self.state.get(key, False)

    def mark_notified(self, watch: dict) -> None:
        key = self.make_key(watch)
        self.state[key] = True
        self.save()

    def reset(self, watch: dict) -> None:
        key = self.make_key(watch)

        if key in self.state:
            del self.state[key]
            self.save()
