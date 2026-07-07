class EventBus:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_name, callback):
        self.listeners.setdefault(event_name, []).append(callback)

    def unsubscribe(self, event_name, callback):
        if event_name in self.listeners:
            self.listeners[event_name] = [cb for cb in self.listeners[event_name] if cb != callback]

    def emit(self, event_name, data=None):
        for callback in self.listeners.get(event_name, []):
            callback(data)

    def clear(self):
        self.listeners.clear()


event_bus = EventBus()
