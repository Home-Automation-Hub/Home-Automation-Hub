from flask import Flask

_app = Flask(__name__)
endpoint_register_path_prefix = ""


@_app.route("/")
def index():
    return "Hello world!"


def add_endpoint(path, view_func):
    endpoint_path = "/" + "/".join([x.strip("/") for x in ["modules", endpoint_register_path_prefix, path]])
    endpoint = endpoint_path.replace("/", "_").replace(" ", "_")
    _app.add_url_rule(endpoint_path, endpoint, view_func)


def run():
    _app.run()
