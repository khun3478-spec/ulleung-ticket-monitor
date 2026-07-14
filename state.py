import json
import os


STATE_FILE = "state.json"


class StateManager:

    def __init__(self):
        self.state = {}
        self.load()

    def load(self):

        if not os.path.exists(STATE_FILE):
            self.state = {}
            return

        with open(STATE_FILE, "r", encoding="utf-8") as f:
            try:
                self.state = json.load(f)
            except Exception:
                self.state = {}

    def save(self):

        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(
                self.state,
                f,
                ensure_ascii=False,
                indent=4,
            )

    def is_changed(self, key, value):

        old = self.state.get(key)

        if old == value:
            return False

        self.state[key] = value
        self.save()

        return True

    def reset(self, key):

        if key in self.state:
            del self.state[key]
            self.save()
