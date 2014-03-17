$(function() {
  $( "#id_log_date, #id_log_date_search" ).datepicker();
  $('#id_log_date, #id_log_date_search').datepicker({dateFormat: 'yy-mm-dd'});
  $( "#id_log_date" ).datepicker( "option", "maxDate", new Date());
  
 $('#id_log_date, #id_log_date_search').datepicker({
	}).click(function() {
	    var test = $(".ui-datepicker-today").children().attr("class").indexOf("ui-state-active");
	    if(test != -1){
	    	$(".ui-datepicker-today").children().removeClass("ui-state-highlight");
	    }
	    
	});
  
  
});
$(document).ready(function() {
	if ($('#id_is_submited').length) {
		var is_sub = document.getElementById('id_is_submited').value
		if (pilot_list == 0 && is_sub !== "True" ){
			insert();	
		}
		if (loc_list == 0 && is_sub !== "True" ){
			insertff();	
		}
	}
	$("#id_pilot_weight, #id_a1c_empty_weight, #id_allowable_takeoff_weight, \
			#id_opterational_weight, #id_payload_available, #id_co_pilot_weight, \
			#id_fuel, #id_manifest_number, #id_flight_data_cargo_weight, \
			#id_flight_data_amount, #id_flight_data_fuel_amount, \
			#id_flight_data_block_time, #id_flight_data_patient").attr('maxlength','9');
});