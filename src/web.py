from flask import Flask, request, render_template

import config
import websocket
import os
from gevent.wsgi import WSGIServer

_app = Flask(__name__)
endpoint_register_path_prefix = ""  # TODO: Use module_id passed to add_endpoint to avoid this?
path_module_ids = {}


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


def add_endpoint(module_id, path, view_func, methods=None):
    if not methods:
        methods = ["GET"]

    endpoint_path = "/" + "/".join([x.strip("/") for x in ["modules", endpoint_register_path_prefix, path]])
    path_module_ids[endpoint_path] = module_id
    endpoint = endpoint_path.replace("/", "_").replace(" ", "_")
    _app.add_url_rule(endpoint_path, endpoint, view_func, methods=methods)


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
