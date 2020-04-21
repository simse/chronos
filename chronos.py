# Python dependencies
import threading
import time
import sys

# Third-party dependencies
from gevent.pywsgi import WSGIServer
from loguru import logger

# First-party dependencies
from chronos.web import app
from chronos.task import execute_next_task
from chronos.bus import interval_trigger, on_startup_trigger

IS_RUNNING = True

interval_trigger.listen(100, execute_next_task)

def main():
    """Start main loop."""
    logger.info("Starting main loop")
    starttime = time.time()
    i = 1

    on_startup_trigger.tick()

    while IS_RUNNING:
        # execute_next_task()
        interval_trigger.tick()

        # Sleep for exactly one second, taking drift and execution time into account
        time.sleep(0.1 - ((time.time() - starttime) % 0.1))
        i += 1

    logger.info("Exiting main loop")


main_thread = threading.Thread(target=main)
main_thread.start()


logger.info("Starting API server")


class devnull:
    write = lambda _: None


# Start REST API
http_server = WSGIServer(("", 5000), app, log=devnull)
try:
    logger.info("API server started")
    http_server.serve_forever()
except (KeyboardInterrupt):
    IS_RUNNING = False
