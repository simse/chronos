# Python dependencies
import threading
import time

# Third-party dependencies
from gevent.pywsgi import WSGIServer
from loguru import logger

# First-party dependencies
from chronos.runtime import *
from chronos.web import app


def main():
    """Start main loop."""
    logger.info("Starting main loop")
    starttime = time.time()
    i = 1

    while True:
        # Call runtime tick function
        tick(i)

        # Sleep for exactly one second, taking drift and execution time into account
        time.sleep(1 - ((time.time() - starttime) % 1))
        i += 1


main_thread = threading.Thread(target=main)
try:
    main_thread.start()
except(KeyboardInterrupt):
    exit()


logger.info("Starting API server")
class devnull:
    write = lambda _: None

# Start REST API
http_server = WSGIServer(("", 5000), app, log=devnull)
try:
    http_server.serve_forever()
except(KeyboardInterrupt):
    exit()
