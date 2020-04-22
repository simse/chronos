import time
import datetime


class Event():
    def __init__(self):
        self.callbacks = {}
        self.events = {}

    def _add_event(self, id):
        if id not in self.callbacks.keys():
            self.callbacks[id] = []

        if id not in self.events.keys():
            self.events[id] = []

    def trigger(self, id, payload={}):
        self._add_event(id)

        for callback in self.callbacks[id]:
            callback()

        self.events[id].append({
            'timestamp': datetime.datetime.now(),
            'id': id,
            'payload': payload
        })

    def callback(self, id, callback):
        self._add_event(id)
        self.callbacks[id].append(callback)

    def listen(self, id):
        self._add_event(id)

        seen_events = []

        while True:
            for event in self.events[id]:
                event_uid = str(event['timestamp']) + event['id']

                if event_uid not in seen_events:
                    seen_events.append(event_uid)
                    yield event

            time.sleep(0.05)

event = Event()