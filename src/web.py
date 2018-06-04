from flask import Flask, request, render_template, Blueprint, \
        send_from_directory

import config
import websocket
import os
from gevent.wsgi import WSGIServer

_app = Flask(__name__)
path_module_ids = {}
module_base_paths = {}
endpoints_to_register = []
enabled_modules = []

@_app.context_processor
def inject_websocket_auth():
    token = websocket.generate_auth_token()
    return dict(ws_auth=token)

@_app.context_processor
def inject_module_info():
    module_id = path_module_ids.get(request.path.strip("/"))
    module_base_path = module_base_paths.get(module_id)
    if not module_id:
        module_id = "application"
        module_base_path = "/"
    return dict(module_id=module_id, module_base_path=module_base_path)

@_app.context_processor
def inject_enabled_modules():
    return dict(enabled_modules=enabled_modules)


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
    registered_module_ids = []
    module_ids_with_default_endpoint = []
    module_title_lookup = {}
    for endpoint in endpoints_to_register:
        registered_module_ids.append(endpoint["module_id"])
        if endpoint["path"].replace("/", "") == "":
            module_ids_with_default_endpoint.append(endpoint["module_id"])

        blueprint = _app.blueprints.get(endpoint["module_id"])
        module_attributes = config.config.enabled_modules[endpoint[
                "module_id"]]

        module_title_lookup[endpoint["module_id"]] = module_attributes["title"]
        path_prefix = "/" + "/".join([x.strip("/") for x in ["modules",
                module_attributes["url_prefix"]]])

        if not blueprint:
            blueprint = Blueprint(endpoint["module_id"],
                    module_attributes["module"].__name__,
                    template_folder="templates")
            
            # Register an endpoint for serving static files from the
            # module's static directory
            @blueprint.route(f"{path_prefix}/static/<path:path>")
            def static_endpoint(path):
                static_dir = os.path.join(
                        os.path.dirname(module_attributes["module"].__file__),
                        "static"
                )
                return send_from_directory(static_dir, path)
        
        # The path to an endpoint is the word modules followed by the
        # endpoint's path prefix folloed by the path specified in the
        # call to add_endpoint()
        module_base_paths[endpoint["module_id"]] = path_prefix

        endpoint_path = path_prefix + "/" + endpoint["path"].strip("/")
        path_module_ids[endpoint_path.strip("/")] = endpoint["module_id"]

        blueprint.add_url_rule(endpoint_path,
                generate_endpoint_identifier(endpoint_path),
                endpoint["view_func"], methods=endpoint["methods"])

        _app.register_blueprint(blueprint)
    
    module_ids_without_default = set(registered_module_ids).difference(
        set(module_ids_with_default_endpoint))
    if len(module_ids_without_default) > 0:
        print("Error registering modules, the following modules do not have"
              " a default endpoint set: ", end="")
        print(",".join([module_title_lookup[x] for x in \
                module_ids_without_default]), end="")
        print(". A default endpoint should have an empty \"path\" value in the"
              " call to add_endpoint.")
        os._exit(1)



def register_blueprint(blueprint):
    _app.register_blueprint(blueprint)
    print(_app.blueprints)


def get_request_args():
    return dict(request.args)


def get_request_form():
    return dict(request.form)


def get_request_method():
    return request.method

# This is a string that is required by flask to identify the endpoint,
# we will just use the path with slashes and spaces replaced by
# underscores
def generate_endpoint_identifier(path):
    return path.replace("/", "_").replace(" ", "_")

def run():
    server = WSGIServer(('', 5000), _app)
    server.serve_forever()
