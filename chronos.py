import threading
import time

from gevent.pywsgi import WSGIServer

from chronos.runtime import *
from chronos.web import app

# Make sure we're running Docker
if os.getenv('CHRONOS') != 'yes_sir_docker':
    exit('Sorry. This program should only run in a Docker container.')

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
