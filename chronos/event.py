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
                "event": id,
                "payload": payload,
                "listeners": self.listeners[id] + self.listeners["any"],
                "uid": id + datetime.datetime.now().strftime("%H%M%S%f"),
            }
        )

        logger.debug("Triggered event: {}", id)

    def callback(self, id, callback):
        self._add_event(id)
        self.callbacks[id].append(callback)

    def listen(self, id, timeout=60):
        # Ensure event ID exists, you can start listening before the event exists
        self._add_event(id)

        # Construct listener ID from taks ID and current time
        listener_id = id + datetime.datetime.now().strftime("%H%M%S%f")
        self.listeners[id].append(listener_id)

        # List of events seen by this listener
        seen_events = []

        # Time listened by this listener (in seconds)
        listen_time = 0

        # Infinite loop to be broken when done
        while True:
            # List of event IDs to listen for
            event_ids = [id]

            # If event ID is "any" or "all" gather all current event IDs
            if id in ["any", "all"]:
                event_ids = list(self.events.keys())

            # Break loop if timeout is reached
            if listen_time > timeout:
                logger.debug(
                    "Listener: {} timed out after {} seconds", listener_id, timeout
                )
                self.listeners[id].remove(listener_id)
                return

            # Gather all events to be yielded
            events = []

            # Loop over each event ID
            for event_id in event_ids:
                # Gather all events with ID
                events_with_id = self.events[event_id]

                # Loop through each event
                for event in events_with_id:
                    events.append(event)

            # Sort events by oldest first
            events.sort(key=lambda event: event["timestamp"])

            for event in events:
                # Generate unique event ID from timestamp and event name
                event_uid = event["timestamp"] + event["id"]

                # Yield event if listener has not yet heard it
                if event_uid not in seen_events:
                    seen_events.append(event_uid)

                    try:
                        event["listeners"].remove(listener_id)
                    except ValueError:
                        pass

                    yield event

            listen_time += 0.01
            time.sleep(0.01)

    def garbage_collect(self):
        for event_id in self.events.keys():
            for index, event in enumerate(self.events[event_id]):

                timestamp = datetime.datetime.strptime(
                    event["timestamp"], "%d-%b-%Y (%H:%M:%S.%f)"
                )

                if event[
                    "listeners"
                ] == [] or timestamp < datetime.datetime.now() - datetime.timedelta(
                    seconds=60
                ):
                    logger.debug("Removed event with ID: {} from memory", event["uid"])
                    del self.events[event_id][index]


event = Event()
