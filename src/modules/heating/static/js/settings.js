jQuery(document).ready(function() {
    jQuery("#form-settings").submit(function() {
        jQuery.ajax({
            url: app.vars.moduleBasePath + "/action/save_settings/",
            type: "POST",
            data: JSON.stringify({
                "numReadingsAverage": jQuery("#num-readings-average").val(),
                "thermostatDeltaBelow": jQuery("#thermostat-delta-below").val(),
                "thermostatDeltaAbove": jQuery("#thermostat-delta-above").val()
            }),
            contentType: "application/json",
            dataType: "json",
            success: function(data) {
                // TODO: Replace this with a nicer in-page alert
                alert(data.message);
            }            
        });

        return false;
    });
});