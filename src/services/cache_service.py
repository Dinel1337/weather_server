import time
from typing import Optional

class SimpleCache:
    def __init__(self, ttl: int = 1800):
        self._store: dict[str, tuple[float, object]] = {}
        self.ttl = ttl

    def get(self, key: str) -> Optional[object]:
        if key in self._store:
            timestamp, value = self._store[key]
            if time.time() - timestamp < self.ttl:
                return value
            del self._store[key]
        return None

    def set(self, key: str, value: object):
        self._store[key] = (time.time(), value)

    def clear(self):
        self._store.clear()
