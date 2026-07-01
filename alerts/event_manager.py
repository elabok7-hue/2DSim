class EventManager:

    def __init__(self):
        self._observers = {}

    def subscribe(self, event_type, observer):
        if event_type not in self._observers:
            self._observers[event_type] = []
        self._observers[event_type].append(observer)

    def unsubscribe(self, event_type, observer):
        if event_type in self._observers:
            self._observers[event_type].remove(observer)

    def notify(self, event_type, data=None):
        for observer in self._observers.get(event_type, []):
            observer.update(data)
