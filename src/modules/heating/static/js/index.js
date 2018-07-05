window.app.registerModuleWebsocketEndpoint(function(key, data) {
    jQuery("#val-temperature").text(data["latest_reading"]);
}, "temperature");

window.app.registerModuleWebsocketEndpoint(function(key, data) {
    // if (data["ch_is_on"]) {
    //     jQuery("#btn_toggle_heating").text("Turn Off");
    //     jQuery("#badge_heating_on").removeClass("d-none");
    //     jQuery("#badge_heating_off").addClass("d-none");
    // } else {
    //     jQuery("#btn_toggle_heating").text("Turn On");
    //     jQuery("#badge_heating_on").addClass("d-none");
    //     jQuery("#badge_heating_off").removeClass("d-none");
    // }
    console.log(data);
}, "state");

window.app.registerModuleWebsocketEndpoint(function(key, data) {
    if (data["control_mode"] == "manual") {
        jQuery("#manual-controls").removeClass("d-none");
        jQuery("#toggle-control-mode label").removeClass("active");
        jQuery("#toggle-control-mode input").prop("checked", false);
        jQuery("#control-mode-manual").addClass("active");
        jQuery("#control-mode-manual input").prop("checked", true);
    } else {
        jQuery("#manual-controls").addClass("d-none");
        jQuery("#toggle-control-mode label").removeClass("active");
        jQuery("#toggle-control-mode input").prop("checked", false);
        jQuery("#control-mode-timer").addClass("active");
        jQuery("#control-mode-timer input").prop("checked", true);
    }
}, "controlModeModified");

jQuery("#btn_toggle_heating").click(function() {
    jQuery.post(app.vars.moduleBasePath + "/action/toggle_heating/");
});

jQuery("#toggle-control-mode input").change(function() {
    var controlMode = jQuery(this).attr("data-mode");
    jQuery.ajax({
        url: app.vars.moduleBasePath + "/action/save_control_mode/",
        type: "POST",
        data: JSON.stringify({mode: controlMode}),
        contentType: "application/json",
        dataType: "json",
        success: function(data) {
            if (!data.success) {
                alert(data.message);
            }
        }            
    });
});

jQuery("#select-manual-start-time").change(function() {
    if(jQuery(this).val() == "now") {
        jQuery("#manual-start-time").addClass("d-none");
    } else {
        jQuery("#manual-start-time").removeClass("d-none");
    }
});

jQuery("#select-manual-end-time").change(function() {
    if(jQuery(this).val() == "indefinitely") {
        jQuery("#manual-end-time").addClass("d-none");
    } else {
        jQuery("#manual-end-time").removeClass("d-none");
    }
});

jQuery("#submit-manual-control").click(function() {
    jQuery.ajax({
        url: app.vars.moduleBasePath + "/action/store_manual_control/",
        type: "POST",
        data: JSON.stringify({
            startTimeType: jQuery("#select-manual-start-time").val(),
            startTime: jQuery("#manual-start-time").val(),
            endTimeType: jQuery("#select-manual-end-time").val(),
            endTime: jQuery("#manual-end-time").val()
        }),
        contentType: "application/json",
        dataType: "json",
        success: function(data) {
            if (!data.success) {
                alert(data.message);
            }
        }            
    });
});