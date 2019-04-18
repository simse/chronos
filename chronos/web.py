from flask import Flask, jsonify, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

import chronos.script
from chronos.runtime import *

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)

class Script(Resource):

    def get(self, uid):
        try:
            script = chronos.script.Script(uid)

            return script.to_dict(), 200
        except chronos.metadata.ScriptDoesNotExist:
            return null, 404


    def post(self, uid):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        args = parser.parse_args()

        return create_script(args['name']), 200

    def put(self, uid):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('interval')
        parser.add_argument('enabled', type=bool)
        parser.add_argument('contents')
        parser.add_argument('requirements')
        args = parser.parse_args()

        try:
            script = chronos.script.Script(uid)
            model = script.db

            # Update each field if it exists
            if args['name'] is not None:
                model.name = args['name']

            if args['interval'] is not None:
                model.interval = args['interval']

            if args['enabled'] is not None:
                model.enabled = args['enabled']

            if args['contents'] is not None:
                script.write_contents(args['contents'])

            if args['requirements'] is not None:
                pass #TODO: FIX

            model.save()

            return 'OK', 200

        except KeyError:
            return None, 404

    def delete(self, uid):
        try:
            chronos.script.Script(uid).delete()
        except Exception:
            pass

        return 'OK', 200

@app.route('/api/scripts')
def scripts():
    scripts = []

    for s in chronos.metadata.Script.select():
        scripts.append(chronos.script.Script(s.uid).to_dict())

    return jsonify(scripts), 200

@app.route('/api/script/<string:uid>/install_requirements')
def install_requirements(uid):
    return jsonify(
        {
            'response': chronos.script.Script(uid).install_requirements()
        }
    ), 200


ui_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'chronos-ui/dist')

@app.route('/', methods=['GET'])
def serve_dir_directory_index():
    return send_from_directory(ui_path, 'index.html')


@app.route('/<path:path>', methods=['GET'])
def serve_file_in_dir(path):

    if not os.path.isfile(os.path.join(ui_path, path)):
        path = os.path.join(path, 'index.html')

    return send_from_directory(ui_path, path)


api.add_resource(Script, '/api/script/<string:uid>')
