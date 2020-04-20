# Python dependencies
import threading
import time
import sys

# Third-party dependencies
from gevent.pywsgi import WSGIServer
from loguru import logger

# First-party dependencies
from chronos.runtime import *
from chronos.web import app
from chronos.task import execute_next_task

IS_RUNNING = True


def main():
    """Start main loop."""
    logger.info("Starting main loop")
    starttime = time.time()
    i = 1

    while IS_RUNNING:
        # Call runtime tick function
        tick(i)

        execute_next_task()

        # Sleep for exactly one second, taking drift and execution time into account
        time.sleep(1 - ((time.time() - starttime) % 1))
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
