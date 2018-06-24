jQuery(document).ready(function() {
    jQuery("#timer-row-container").on("click", ".select-weekdays", function() {
        uncheckAllDays(this);
        checkDays(this, "weekday");
        return false;
    });
    jQuery("#timer-row-container").on("click", ".select-weekend", function() {
        uncheckAllDays(this);
        checkDays(this, "weekend");
        return false;
    });
    jQuery("#timer-row-container").on("click", ".select-all-days", function() {
        checkDays(this, "weekend");
        checkDays(this, "weekday");
        return false;
    });
    jQuery("#timer-row-container").on("click", ".select-no-days", function() {
        uncheckAllDays(this);
        return false;
    });
    jQuery("#timer-row-container").on("click", ".btn-delete-timer", function() {
        jQuery(this).closest("tr").remove();
        return false;
    });

    jQuery("#btn-save-timers").click(function() {
        var formData = serialiseTimerForm();
        jQuery.ajax({
            url: app.vars.moduleBasePath + "/action/save_timers/",
            type: "POST",
            data: JSON.stringify(formData),
            contentType: "application/json",
            dataType: "json",
            success: function(data) {
                // TODO: Replace this with a nicer in-page alert
                alert(data.message);
            }            
        });
    });

    jQuery("#btn-add-timer").click(function() {
        var template = jQuery("#template-timer-row").text();
        jQuery("#timer-row-container").append(template);
    });

    function checkDays(clickedElement, dayType) {
        jQuery(clickedElement).closest(".day-button-group").find("label[data-type='" + dayType + "']").addClass("active");
        jQuery(clickedElement).closest(".day-button-group").find("label[data-type='" + dayType + "'] > input").prop("checked", true);
    }

    function uncheckAllDays(clickedElement) {
        jQuery(clickedElement).closest(".day-button-group").find("label").removeClass("active");
        jQuery(clickedElement).closest(".day-button-group").find("label > input").prop("checked", false);
    }

    function serialiseTimerForm() {
        var timers = [];
        jQuery("#timers-form .timer-row").each(function() {
            var timer = {};
            timer["startTime"] = jQuery(this).find("[name='start-time']").val();
            timer["endTime"] = jQuery(this).find("[name='end-time']").val();
            timer["temperature"] = jQuery(this).find("[name='temperature']").val();
            
            timer["days"] = {}
            jQuery(this).find("[name='day-checkbox']").each(function() {
                timer["days"][jQuery(this).val()] = jQuery(this).is(":checked");
            });

            timers.push(timer);
        });
        return timers;
    }
    window.serialiseTimerForm = serialiseTimerForm;
});