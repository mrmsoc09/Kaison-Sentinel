from typing import Dict, Any, Callable, List


class EventBus:
    def __init__(self):
        self._subs: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}

    def subscribe(self, topic: str, fn: Callable[[Dict[str, Any]], None]) -> None:
        self._subs.setdefault(topic, []).append(fn)

    def publish(self, topic: str, event: Dict[str, Any]) -> None:
        for fn in self._subs.get(topic, []):
            fn(event)
