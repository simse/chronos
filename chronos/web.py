# Python imports
import time
import json
import os
import datetime

# Third-party dependencies
from flask import Flask, jsonify, send_from_directory, Response, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from loguru import logger

# First-party dependencies
import chronos.script
from chronos.metadata import Session
from chronos.metadata import Script as ScriptModel
from chronos.task import dispatch_task
from chronos.event import event
from chronos.util import for_uid


# Create Flask app
app = Flask(__name__)


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
        return {'uid': for_uid(args["name"])}, 200

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


# Get all scripts
@app.route("/api/scripts")
def scripts():
    scripts = []

    session = Session()

    for s in session.query(ScriptModel).all():
        scripts.append(chronos.script.Script(s.uid).to_dict())

    session.close()

    return jsonify(scripts), 200


@app.route("/api/script/<string:uid>/action/<string:action>")
def action(uid, action):
    script = chronos.script.Script(uid)

    return jsonify({'response': script.action(action)})


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
            logger.debug("Yielded event: {}", e['uid'])
            yield "data: %s\n\n" % json.dumps(e, default=myconverter)
    finally:
        logger.info("Stopping Sever Side Event stream")


@app.route("/api/events/<string:type>")
def stream(type):
    return Response(events(type), mimetype="text/event-stream")


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
        path = os.path.join(path, "index.html")

    return send_from_directory(ui_path, path)


# Register script API resource.
api.add_resource(Script, "/api/script/<string:uid>")
