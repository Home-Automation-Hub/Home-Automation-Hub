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
        jQuery(clickedElement).closest(".day-button-group").find("label > checkbox").removeAttr("checked");
        jQuery(clickedElement).closest(".day-button-group").find("label[data-type='" + dayType + "']").addClass("active");
        jQuery(clickedElement).closest(".day-button-group").find("label[data-type='" + dayType + "'] > checkbox").attr("checked", "checked");
    }
});