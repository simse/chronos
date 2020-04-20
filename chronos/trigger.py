def parse_triggers():
    pass


class IntervalTrigger:
    def __init__(self, interval):
        self._tick = 0
        self.interval = interval # Set interval in milliseconds
        self.listeners = []

    def tick(self):
        self._tick += 1

        for listener in self.listeners:
            if self._tick * self.interval % listener[0] == 0:
                if not listener[2]:
                    listener[1]()
                else:
                    listener[1](self._tick, self.interval)

    def listen(self, interval, callback, clock=False):
        self.listeners.append([interval, callback, clock])



class CronTrigger:
    pass


class OnStartupTrigger:
    pass
