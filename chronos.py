import threading
import time

from gevent.pywsgi import WSGIServer

import chronos.metadata
from chronos.util import *
from chronos.execute import *
from chronos.venv import *
from chronos.runtime import *
from chronos.script import Script
from chronos.web import app


def main():
    starttime = time.time()
    i = 1

    while True:
        tick(i)

        # Sleep for exactly one second, taking drift and execution time into account
        time.sleep(1 - ((time.time() - starttime) % 1))
        i += 1

main_thread = threading.Thread(target=main)
main_thread.start()


# Start REST api
http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
