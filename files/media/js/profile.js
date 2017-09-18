function showNewSecondName(id) {
    if ($(id).val() == 'f') {
        $('#element_new_last_name').show();
    } else {
        $('#element_new_last_name').hide();
    }
}

function showCityLive(id) {
    if ($(id).is(':checked')) {
        $('#element_city_live').show();
    } else {
        $('#element_city_live').hide();
    }
}

$(document).ready(function() {
    showNewSecondName("input[name='sex']:checked");
    showCityLive("input[name='is_emigrated']");
    $("input[name='sex']").change(function(){
        showNewSecondName(this);
    });
    $("input[name='is_emigrated']").change(function(){
        showCityLive(this);
    });

});
