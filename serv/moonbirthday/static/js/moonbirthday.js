function clear_select_vals(select) {
    select.empty()
        .append($("<option></option>")
        .attr("value",'0')
        .text('----------'));
    return select
}

function gt_slctd(select_val, choosen_val) {
    return (select_val == choosen_val) ? 'selected' : ''
}

function show_detail_sity() {
    $('#detail_form').show();
    $('#element_city').hide();
    $('#detail_city').hide();
    $('#id_is_russian').val(0);
    $('#element_country').show()
    $('#element_region').show()
    $('#element_detail_city').show()

    clear_select_vals($('#id_region'))
    clear_select_vals($('#id_detail_city'))

    $.get(url_ajax_get_countries).done(function(data){
        clear_select_vals($('#id_country'))
        $.each($.parseJSON(data), function(key, value) {
            $('#id_country')
                .append($("<option "
                    + gt_slctd(key, value_form_country_value)
                    + " ></option>")
                .attr("value", key)
                .text(value));
        });
        if (value_form_country_value != '0') {
            fill_regions(value_form_country_value);
        }
        if (value_form_region_value !== 'None' ) {

            fill_cities(value_form_region_value);
        }
    });
}

$('#detail_city').click(function(){
    show_detail_sity();
    return false;
})

function fill_regions(country_id) {
    $.get( url_ajax_get_regions + '?country_id=' + country_id).done(
        function(data) {
            clear_select_vals($('#id_region'))
            clear_select_vals($('#id_detail_city'))
            $.each( $.parseJSON(data), function(key, value) {
                selected = gt_slctd(key, value_form_region_value)
                $('#id_region')
                    .append($("<option "+ selected +" ></option>")
                    .attr("value",key)
                    .text(value));
            });
        });
    }

$('#id_country').change(function() {
    var country_id = $( this ).val();
    fill_regions(country_id);
})

function fill_cities(region_id)
{
    $.get( url_ajax_get_city + '?region_id='+region_id).done(function(data){
        clear_select_vals($('#id_detail_city'))
        $.each( $.parseJSON(data), function(key, value) {
            selected = gt_slctd(key, value_form_detail_city_value)
            $('#id_detail_city')
                .append($("<option  "+ selected +" ></option>")
                .attr("value",key)
                .text(value));
        });
    });
}

$('#id_region').change(function(){
    var region_id = $( this ).val();
    fill_cities(region_id);
})


$('#simple_search').click(function(){
    jQuery('#element_region').hide()
    jQuery('#element_country').hide()
    jQuery('#element_detail_city').hide()
    $('#element_city').show();
    $('#detail_form').hide();
    $('#detail_city').show();
    $('#id_is_russian').val(1);
    return false;
})

jQuery(function(){
    if ($('#id_is_russian').val() == 0) {
        show_detail_sity();
    } else {
        $('#detail_form').hide();
        jQuery('#element_region').hide()
        jQuery('#element_country').hide()
        jQuery('#element_detail_city').hide()
    }

    jQuery('input[placeholder], textarea[placeholder]').placeholder('');
    if ($(window).width() >= 900) {
        jQuery("#id_date").mask("99.99.9999");
        jQuery("#id_time").mask("99:99");
    }
        jQuery("#id_city").autocomplete({
            serviceUrl: url_ajax_city_autocomplete,
            onSelect: function (data) {
               jQuery("#id_city_id").val(data['data'])
            }
        })

});