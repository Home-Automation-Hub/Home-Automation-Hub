jQuery(document).ready(function() {
    jQuery(".select-weekdays").click(function() {
        toggleDays(this, "weekday");
        return false;
    });
    jQuery(".select-weekend").click(function() {
        toggleDays(this, "weekend");
        return false;
    });

    function toggleDays(clickedElement, dayType) {
        jQuery(clickedElement).closest(".day-button-group").find("label").removeClass("active");
        jQuery(clickedElement).closest(".day-button-group").find("label > input").prop("checked", false);
        jQuery(clickedElement).closest(".day-button-group").find("label[data-type='" + dayType + "']").addClass("active");
        jQuery(clickedElement).closest(".day-button-group").find("label[data-type='" + dayType + "'] > input").prop("checked", true);
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