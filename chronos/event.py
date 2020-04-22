import time
import datetime

from loguru import logger


class Event:
    def __init__(self):
        self.callbacks = {}
        self.events = {}
        self.listeners = {"any": []}

    def _add_event(self, id):
        if id not in self.callbacks.keys():
            self.callbacks[id] = []

        if id not in self.events.keys():
            self.events[id] = []

        if id not in self.listeners.keys():
            self.listeners[id] = []

    def trigger(self, id, payload={}):
        self._add_event(id)

        for callback in self.callbacks[id]:
            callback()

        self.events[id].append(
            {
                "timestamp": datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"),
                "id": id,
                "payload": payload,
                "listeners": self.listeners[id] + self.listeners["any"],
                "uid": id + datetime.datetime.now().strftime("%H%M%S%f"),
            }
        )

        logger.debug("Triggered event: {}", id)

    def callback(self, id, callback):
        self._add_event(id)
        self.callbacks[id].append(callback)

    def listen(self, id):
        self._add_event(id)

        listener_id = id + datetime.datetime.now().strftime("%H%M%S%f")
        self.listeners[id].append(listener_id)

        print(self.listeners[id])

        seen_events = []

        if id == "any":
            while True:
                event_ids = list(self.events.keys())
                for event_id in event_ids:
                    for event in self.events[event_id]:
                        event_uid = event["timestamp"] + event["id"]

                        if event_uid not in seen_events:
                            seen_events.append(event_uid)

                            try:
                                event["listeners"].remove(listener_id)
                            except ValueError:
                                pass

                            yield event

                    time.sleep(0.05)
        else:
            while True:
                for event in self.events[id]:
                    event_uid = event["timestamp"] + event["id"]

                    if event_uid not in seen_events:
                        seen_events.append(event_uid)

                        try:
                            event["listeners"].remove(listener_id)
                        except ValueError:
                            pass

                        yield event

                time.sleep(0.05)

    def garbage_collect(self):
        for event_id in self.events.keys():
            for index, event in enumerate(self.events[event_id]):

                timestamp = datetime.datetime.strptime(event["timestamp"], "%d-%b-%Y (%H:%M:%S.%f)")

                if event["listeners"] == [] or timestamp < datetime.datetime.now() - datetime.timedelta(seconds=60):
                    logger.debug("Removed event with ID: {} from memory", event["uid"])
                    del self.events[event_id][index]


event = Event()
