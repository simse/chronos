# Python dependencies
import threading
import logging
import time
import sys
import os

# Third-party dependencies
from loguru import logger

# First-party dependencies
from chronos.web import app
from chronos.task import execute_next_task
from chronos.bus import interval_trigger, on_startup_trigger
from chronos.event import event

IS_RUNNING = True

interval_trigger.listen(100, execute_next_task)


def main():
    """Start main loop."""
    logger.info("Starting main loop")
    starttime = time.time()
    i = 1

    on_startup_trigger.tick

    while IS_RUNNING:
        # execute_next_task()
        interval_trigger.tick()

        # Sleep for exactly one second, taking drift and execution time into account
        time.sleep(0.1 - ((time.time() - starttime) % 0.1))
        i += 1

    logger.info("Exiting main loop")


main_thread = threading.Thread(target=main)
main_thread.start()


def test():
    event.trigger("test")


# interval_trigger.listen(1000, test)
interval_trigger.listen(100, event.garbage_collect)


logger.info("Starting API server")

# Surpress Werkzeug output

log = logging.getLogger("werkzeug")
log.disabled = True
log.setLevel(logging.ERROR)
os.environ["WERKZEUG_RUN_MAIN"] = "true"


# Start REST API
try:
    logger.info("API server started")
    app.run()
except (KeyboardInterrupt):
    IS_RUNNING = False
