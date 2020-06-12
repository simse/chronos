# Python imports
import time
import json
import os
import uuid
import sys
import datetime

# Third-party dependencies
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    Response,
    request,
    stream_with_context,
)
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from loguru import logger
from twisted.python import log
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource, WSGIRootResource


# First-party dependencies
import chronos.script
from chronos.script import get_all_scripts
from chronos.metadata import Session
from chronos.metadata import Script as ScriptModel
from chronos.task import dispatch_task
from chronos.event import event
from chronos.util import for_uid
from chronos.settings import get_setting, set_setting, get_all_settings


# Create Flask app
app = Flask(__name__)
app.secret_key = str(uuid.uuid4())


# Allow CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)

# Register Flask API
api = Api(app)



class Script(Resource):
    """Main Script resource to create, update, delete and get script metadata."""

    def get(self, uid):
        """Get script metadate."""
        try:
            script = chronos.script.Script(uid)

            return script.to_dict(), 200
        except chronos.metadata.ScriptDoesNotExist:
            return null, 404

    def post(self, uid):
        """Create new script. This is a slow function."""
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        args = parser.parse_args()

        dispatch_task("create_script", {"name": args["name"]}, "NOW")
        return {"uid": for_uid(args["name"])}, 200

    def put(self, uid):
        """Update script."""
        args = request.get_json(force=True)

        session = Session()

        try:
            script = chronos.script.Script(uid)
            model = session.query(ScriptModel).get(uid)

            # Update each field if it exists
            try:
                model.name = args["name"]
            except KeyError:
                pass

            try:
                model.triggers = args["triggers"]
            except KeyError:
                pass

            try:
                model.enabled = args["enabled"]
            except KeyError:
                pass

            try:
                script.write_contents(args["contents"])
            except KeyError:
                pass

            try:
                script.write_requirements(args["requirements"])
            except KeyError:
                pass

            session.commit()

            return "OK", 200

        except KeyError:
            return None, 404

    def delete(self, uid):
        """Delete script."""
        chronos.script.Script(uid).delete()

        return "OK", 200


class Setting(Resource):
    def get(self, key):
        return get_setting(key)

    def post(self, key):
        args = request.get_json(force=True)

        return set_setting(key, args["value"])


@app.route("/api/settings")
def settings():
    return jsonify(get_all_settings()), 200


# Get all scripts
@app.route("/api/scripts")
def scripts():
    return jsonify(get_all_scripts()), 200


@app.route("/api/script/<string:uid>/action/<string:action>")
def action(uid, action):
    script = chronos.script.Script(uid)

    return jsonify({"response": script.action(action)})


# Install Pip requirements for specific script. This is a slow function.
@app.route("/api/script/<string:uid>/install_requirements")
def install_requirements(uid):
    return jsonify({"response": chronos.script.Script(uid).install_requirements()}), 200


# Execute specific script and return result.
@app.route("/api/script/<string:uid>/execute")
def execute(uid):
    chronos.script.Script(uid).execute()
    return jsonify({"response": "OK"}), 200


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def events(type):
    try:
        for e in event.listen(type):
            logger.debug("Yielded event: {}", e["uid"])
            yield "data: %s\n\n" % json.dumps(e, default=myconverter)

    except GeneratorExit:
        logger.debug("Bye bye")

    finally:
        logger.info("Stopping Sever Side Event stream")


@app.route("/api/events/<string:type>")
def stream(type):
    #return Response(stream_with_context(events(type)), mimetype="text/event-stream")
    return ""


# This part serves the UI from chronos-ui/dist, i.e. it must be built.
ui_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "chronos-ui/dist"
)


@app.route("/", methods=["GET"])
def serve_dir_directory_index():
    return send_from_directory(ui_path, "index.html")


@app.route("/<path:path>", methods=["GET"])
def serve_file_in_dir(path):

    if not os.path.isfile(os.path.join(ui_path, path)):
        path = os.path.join("index.html")

    return send_from_directory(ui_path, path)


# Register script API resource.
api.add_resource(Script, "/api/script/<string:uid>")
api.add_resource(Setting, "/api/setting/<string:key>")


# Websocket stuff
class ChronosWebSocketProtocol(WebSocketServerProtocol):
    connections = list()

    def onConnect(self, request):
        self.connections.append(self)
        logger.debug("New WebSocket client")

    def onClose(self, wasClean, code, reason):
        self.connections.remove(self)
        logger.debug("WebSocket client disconnected: {}", reason)


    @classmethod
    def broadcast_message(cls, data):
        payload = json.dumps(data, ensure_ascii = False).encode('utf8')
        for c in set(cls.connections):
            reactor.callFromThread(cls.sendMessage, c, payload)


# Websocket methods
def emit_message(key, data):
    ChronosWebSocketProtocol.broadcast_message({
        "event": key,
        "payload": data
    })




def start_server():
    log.startLogging(sys.stdout)

    # create a Twisted Web resource for our WebSocket server
    wsFactory = WebSocketServerFactory("ws://127.0.0.1:5000")
    wsFactory.protocol = ChronosWebSocketProtocol
    wsResource = WebSocketResource(wsFactory)

    # create a Twisted Web WSGI resource for our Flask server
    wsgiResource = WSGIResource(reactor, reactor.getThreadPool(), app)

    # create a root resource serving everything via WSGI/Flask, but
    # the path "/ws" served by our WebSocket stuff
    rootResource = WSGIRootResource(wsgiResource, {b'ws': wsResource})

    # create a Twisted Web Site and run everything
    site = Site(rootResource)

    reactor.listenTCP(5000, site)
    reactor.run()