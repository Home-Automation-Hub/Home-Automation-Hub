import $ from "jquery"

(function() {
    var endpoint = $("meta[name='ws-endpoint']").attr("content");
    var authToken = $("meta[name='ws-auth-token']").attr("content");
    var moduleId = $("meta[name='module-id']").attr("content");
    var moduleEndpoints = {};

    var socket = new WebSocket(endpoint);

    socket.onmessage = function(message) {
        if (message.data == "ok") {
            socket.onmessage = routeSocketMessage;
        } else {
            console.log("Failed to connect to socket, authentication failed")
        }
    };

    socket.onopen = function() {
        socket.send(authToken)
    }


    function routeSocketMessage(msg) {
        var messageData = JSON.parse(msg.data);
        if (typeof moduleEndpoints[messageData["module_id"]] == "undefined") {
            return;
        }

        var callbacks = moduleEndpoints[messageData["module_id"]][""] || []; // Callbacks to run for all keys
        callbacks = callbacks.concat(moduleEndpoints[messageData["module_id"]][messageData["key"]] || []) // Callbacks for key
        for (var i=0; i < callbacks.length; i++) {
            var callback = callbacks[i];
            callback(messageData["key"], messageData["data"])
        }
    }

    function registerModuleWebsocketEndpoint(callback, key) {
        if (typeof key == "undefined") {
            key = "";
        }
        if (typeof moduleEndpoints[moduleId] == "undefined") {
            moduleEndpoints[moduleId] = {};
        }
        if (typeof moduleEndpoints[moduleId][key] == "undefined") {
            moduleEndpoints[moduleId][key] = [];
        }

        moduleEndpoints[moduleId][key].push(callback);
    }

    window.app.registerModuleWebsocketEndpoint = registerModuleWebsocketEndpoint;
})();