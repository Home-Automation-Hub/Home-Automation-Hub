from flask import Flask, request, render_template, Blueprint

import config
import websocket
import os
from gevent.wsgi import WSGIServer

_app = Flask(__name__)
path_module_ids = {}
endpoints_to_register = []

@_app.context_processor
def inject_websocket_auth():
    token = websocket.generate_auth_token()
    return dict(ws_auth=token)

@_app.context_processor
def inject_module_id():
    module_id = path_module_ids.get(request.path)
    if not module_id:
        module_id = "application"
    return dict(module_id=module_id)


@_app.route("/")
def index():
    return render_template("dashboard.html")


# TODO: Store the endpoints that should be registered somewhere then create
# blueprints and register them in all in one go once all modules have had their
# register() function called.
def add_endpoint(module_id, path, view_func, methods=None):
    if not methods:
        methods = ["GET"]

    endpoints_to_register.append({
        "module_id": module_id,
        "path": path,
        "view_func": view_func,
        "methods": methods
    })


def register_all_endpoints():
    for endpoint in endpoints_to_register:
        blueprint = _app.blueprints.get(endpoint["module_id"])
        module_attributes = config.config.enabled_modules[endpoint[
                "module_id"]]

        if not blueprint:
            blueprint = Blueprint(endpoint["module_id"],
                    module_attributes["module"].__name__)
        
        # The path to an endpoint is the word modules followed by the
        # endpoint's path prefix folloed by the path specified in the
        # call to add_endpoint()
        endpoint_path = "/" + "/".join([x.strip("/") for x in ["modules",
                module_attributes["url_prefix"], endpoint["path"]]])

        path_module_ids[endpoint_path] = endpoint["module_id"]

        # This is a string that is required by flask to identify the
        # endpoint, we will just use the path with slashes and spaces
        # replaced by underscores
        endpoint_identifier = endpoint_path.replace("/", "_").replace(" ", "_")

        blueprint.add_url_rule(endpoint_path, endpoint_identifier,
                endpoint["view_func"], methods=endpoint["methods"])

        _app.register_blueprint(blueprint)


def register_blueprint(blueprint):
    _app.register_blueprint(blueprint)
    print(_app.blueprints)


def get_request_args():
    return dict(request.args)


def get_request_form():
    return dict(request.form)


def get_request_method():
    return request.method


# def render_template(module_id, filename, data):
#     template_dir = os.path.join(os.path.dirname(config.config.enabled_modules[module_id]["module"].__file__))


def run():
    server = WSGIServer(('', 5000), _app)
    server.serve_forever()
