from flask import Flask, request, render_template
import storage

_app = Flask(__name__)
endpoint_register_path_prefix = ""


@_app.route("/")
def index():
    return render_template("dashboard.html")


def add_endpoint(path, view_func, methods=None):
    if not methods:
        methods = ["GET"]

    endpoint_path = "/" + "/".join([x.strip("/") for x in ["modules", endpoint_register_path_prefix, path]])
    endpoint = endpoint_path.replace("/", "_").replace(" ", "_")
    _app.add_url_rule(endpoint_path, endpoint, view_func, methods=methods)


def get_request_args():
    return dict(request.args)


def get_request_form():
    return dict(request.form)


def get_request_method():
    return request.method


def run():
    _app.run()
