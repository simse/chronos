# Python dependencies
import threading
import time

# Third-party dependencies
from gevent.pywsgi import WSGIServer

# First-party dependencies
from chronos.runtime import *
from chronos.web import app


# Check that the Docker environment variable is set. This is merely meant as a warning.
if os.getenv('CHRONOS') != 'yes_sir_docker':
    exit('Sorry. This program should only run in a Docker container.')


def main():
    """Start main loop."""
    starttime = time.time()
    i = 1

    while True:
        # Call runtime tick function
        tick(i)

        # Sleep for exactly one second, taking drift and execution time into account
        time.sleep(1 - ((time.time() - starttime) % 1))
        i += 1

main_thread = threading.Thread(target=main)
main_thread.start()


# Start REST API
http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
