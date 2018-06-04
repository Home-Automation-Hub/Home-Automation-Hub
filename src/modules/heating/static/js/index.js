window.app.registerModuleWebsocketEndpoint(function(key, data) {
    jQuery("#val-temperature").text(data["latest_reading"]);
}, "temperature");

window.app.registerModuleWebsocketEndpoint(function(key, data) {
    if (data["ch_is_on"]) {
        jQuery("#btn_toggle_heating").text("Turn Off");
        jQuery("#badge_heating_on").removeClass("d-none");
        jQuery("#badge_heating_off").addClass("d-none");
    } else {
        jQuery("#btn_toggle_heating").text("Turn On");
        jQuery("#badge_heating_on").addClass("d-none");
        jQuery("#badge_heating_off").removeClass("d-none");
    }
}, "state");

jQuery("#btn_toggle_heating").click(function() {
    jQuery.post(app.vars.moduleBasePath + "/action/toggle_heating");
});