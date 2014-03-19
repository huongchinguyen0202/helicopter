function set_tabindex_submited() {
	$("#id_log_number,#mod,#id_a1c,#cus, #id_log_date_search,input:reset, input:submit[value='Search'],"+
		"input[type='button']").each(function (i) { 
		$(this).attr('tabindex', i + 1); 
	});
}
function set_tabindex_add_flight_log() {
	if ($("#total")[0].rowIndex % 2 == 0){
		$("#total").attr("class", "row_even");
	}else{
		$("#total").attr("class", "row_odd");
	}
	$('#id_contract1charter, #id_a1c,#id_base, #id_co_pilot_employee_number').kendoDropDownList({ 
		animation: false,
		template:'<span title=\'#: mytooltip #\'>#: mytooltip #</span>', 
		dataTextField: "mytooltip"
	});
	$('#id_customer').kendoDropDownList({ 
		animation: false,
		template:'<span title=\'#: mytooltip #\'>#: mytooltip #</span>', 
		dataTextField: "mytooltip", 
		change: function(e) { 
			var select_none = e.sender.selectedIndex < 1 && !e.sender._selectedValue;
			$('#id_contract1charter').data('kendoDropDownList').enable(!select_none);
		},
		dataBound: function(e) { 
			$('#id_contract1charter').data('kendoDropDownList').enable(e.sender.selectedIndex > 0); 
		}
	});
	$('#id_model').kendoDropDownList({ 
		animation: false,
		template:'<span title=\'#: mytooltip #\'>#: mytooltip #</span>', 
		dataTextField: "mytooltip", 
		change: function(e) {
			var select_none = e.sender.selectedIndex < 1 && !e.sender._selectedValue;
			$('#id_a1c').data('kendoDropDownList').enable(!select_none);
		},
		dataBound: function(e) { 
			$('#id_a1c').data('kendoDropDownList').enable(e.sender.selectedIndex > 0); 
		}
	});

	$('#number,#id_log_date,span[aria-owns="id_customer_listbox"],'+
		'span[aria-owns="id_contract1charter_listbox"],'+
		'span[aria-owns="id_model_listbox"],'+
		'span[aria-owns="id_a1c_listbox"],'+
		'span[aria-owns="id_base_listbox"],'+
		'#id_fuel, #id_a1c_empty_weight, #id_pilot_weight,'+
		'span[aria-owns="id_co_pilot_employee_number_listbox"],'+
		'#id_co_pilot_weight, #id_opterational_weight, #id_allowable_takeoff_weight, '+
		'#id_payload_available, .btn_default_flight_log.last_margin.add_flight_log'
		).each(function (i) { 
		$(this).attr('tabindex', i + 1);
	}); 
	
}
function load_ajax_popop(list_loc_name) {
	$("#id_off").timeEntry({
		spinnerImage: "../static/img/spinnerUpDown.png",
		spinnerSize: [15, 16, 0], 
		spinnerBigSize: [30, 32, 0], 
		show24Hours: true,
		spinnerIncDecOnly: true}
	);
	$("#id_on").timeEntry({
	    spinnerImage: "../static/img/spinnerUpDown.png",
	    spinnerSize: [15, 16, 0], 
	    spinnerBigSize: [30, 32, 0], 
	    show24Hours: true,
	    spinnerIncDecOnly: true}
	);
	$(".popup_main select").kendoDropDownList({ animation: false,
		template:'<span title=\'#: mytooltip #\'>#: mytooltip #</span>', dataTextField: "mytooltip"
	});
//	$("#id_flight_data_fuel_station").kendoComboBox({animation: false,dataSource:list_loc_name, filter: "contains"});
	$("#id_flight_data_fuel_station").kendoComboBox({
		animation: false,
		filter: "contains",
	    dataSource:list_loc_name,
	    dataBound: function() {
	        $(this.items()).each(function(index, item) {
	            var model = $("#id_flight_data_fuel_station").data("kendoComboBox").dataItem(index);
	            $(item).attr("title", model);
	        });
	    }
	});
	$('#id_flight_data_fuel, #id_flight_time, #id_all_nfr, #id_all_ifr').each(function(){
		$(this).attr('tabIndex', -1);
	});
	$('span[aria-owns="id_slot_purpose_id_listbox"]').focus();
}

function set_fuel_station(location_name) {
	var combobox = $("#id_flight_data_fuel_station").data("kendoComboBox");
	//combobox.select(2);
	combobox.value(location_name);
//	combobox.select(function(dataItem) {
//	    return dataItem.text === location_name;
//	});
}
function save_confirm(page){
	if($("#id_is_submited").val() == "False" || $("#id_is_submited").val() == ""){
		if (confirm("Unsaved data will be lost. Do you want to save the changes before continuing?")){
			$("#add_flight_log_save").trigger('click');
		}else{
			if (page == 'search'){
				window.location='/search/';
			}else if (page == 'pending'){
				window.location='/';
			}else{
				window.location='/log/';
			}
		}
	}else{
		if (page == 'search'){
			window.location='/search/';
		}else if (page == 'pending'){
			window.location='/';
		}else{
			window.location='/log/';
		}
	}
	return true;
}


function save_add_flight_leg(e){
	check = true;
	if(!$('#id_load_schedule').is(":checked")){
		if ($('#id_flight_data_cg').val() == ""){
			$("#id_flight_data_cg").addClass("input_error");
    		$("#error_id_flight_data_cg").css("display","inline");
    		check = false;
		}
		if ($("#id_flight_data_range_from").val() == ""&&
			$("#id_flight_data_range_to").val() == ""){
			$("#range_to_error_id").css("display","inline");
    		$("#id_flight_data_range_from").addClass("input_error");
    		$("#id_flight_data_range_to").addClass("input_error");
    		check = false;
		}
		
		if($("#id_flight_data_range_range").val() == ""){
			$("#range_to_error_id").css("display","inline");
    		$("#id_flight_data_range_from").addClass("input_error");
    		check = false;
		}
		
		if($("#id_flight_data_range_to").val() == ""){
			$("#range_to_error_id").css("display","inline");
    		$("#id_flight_data_range_to").addClass("input_error");
    		check = false;
		}
    		
	}
	if (check == false){
		e.preventDefault();
	}
	return check;
}


function review_popup(id,e) {
		var index = e.sectionRowIndex;
		var max_pax = $("#max_pax").val();
	    Dajaxice.flight_log.edit_flight_log(Dajax.process, {'index':index,
	    													'max_pax':max_pax,
	    													'is_submitted':true});
	    
	 // Getting the variable's value from a link 
	    open_popup(id);
}

function open_popup(loginBox){
	$(loginBox).fadeIn(300);
	$('body').append('<div id="mask"></div>');
	$('#mask').fadeIn(300);
	jQuery(loginBox).center();
}

function val_send_email(is_checked, id){
	var j = [];
	i = 0;
	if(id != '') {
		j[0] = id;
	}
	$("input:not(:hidden)[name^='row_check_']").each(function(){
		if($(this).is(':checked')) {// if exist one  untick
			is_checked = true;
			//j[i] = $(this).attr("name").replace('row_check_','');
			j[i] = $(this).parent().find('input.log_number').val();
			i++;
			// break from each loop
			//return false;
		}
	});
	if (!is_checked){
		alert("Please select at least one log to send email.");
	}else{
		// Send email
		//$(document).on('click', '.send_email',function(e) {
			Dajaxice.flight_log.send_email(Dajax.process,{'arr':j});
			open_popup('#send_email');
		//});
	}
	window.location = "#Email"
}


function val_print_pdf(is_checked,id){
	//var j = [];
	//i = 0;
	var j = id;
	$("input:not(:hidden)[name^='row_check_']").each(function(){
		if($(this).is(':checked')) {// if exist one  untick
			is_checked = true;
			j = j + ',' + $(this).parent().find('input.log_number').val();
			//j[i] = $(this).attr("name").replace('row_check_','');
			// break from each loop
			//return false;
			//i++;
		}
	});
	if (!is_checked){
		alert("Please select at least one log to print pdf.");
		return false;
	}else{
		if(j.length > 1) {
			j = j.substring(1);
		}
		window.location='print?i='+j;
		/*for (var i=0;i<j.length;i++) {
			window.location= 'print?i='+j[i];
		}*/
	}
}

$(document).ready(function() {
	// check all checkbox
	$("input[name='all_check']").on('change',function() {
	        var check_status =  $(this).is(':checked');
	        $("input:not(:hidden)[name^='row_check_']").each(function(){
				$(this).prop('checked', check_status); // attr problem ???
			});
	});
	
	// Input change event
	$(document).on('change', 'input', function(){
		error_id = "#error_" + $(this).attr("id");
		element_value = $(this).val();
		class_select = $(this).attr("class")
		name = $(this).attr("name")
		if (name == "flight_data_tlo_w"){
			name = "T/O W";
		}
		if (name == "fuel_wheels_down"){
			name = "Fuel at Wheels Down";
		}
		// Check load schedule not check
		if(!$("#id_load_schedule").is(":checked")){
			// Appear star at CG
			jQuery("#id_flight_data_cg").parent().find('span span').css("display", "inline");
			jQuery("#id_flight_data_range_from").parent().find('span span').css("display", "inline");
			jQuery("#id_flight_data_range_from").parent().find('span span').css("display", "inline");
			
			if($(this).attr("id") == "id_flight_data_cg" ||
					$(this).attr("id") == "id_flight_data_range_from" ||
					$(this).attr("id") == "id_flight_data_range_to" ||
					$(this).attr("id") == "id_load_schedule"){
					if($(this).attr("id") == "id_load_schedule"){
						if($('#id_flight_data_cg').val() == ""){
							$("#error_id_flight_data_cg").css("display","inline");
							$("#id_flight_data_cg").addClass("input_error");
						}else{
							$("#error_id_flight_data_cg").css("display","none");
							$("#id_flight_data_cg").removeClass("input_error");
						}
						if ($("#id_flight_data_range_from").val() == ""&&
							$("#id_flight_data_range_to").val() == ""){
							$("#range_to_error_id").css("display","inline");
				    		$("#id_flight_data_range_from").addClass("input_error");
				    		$("#id_flight_data_range_to").addClass("input_error");
						}
						
						if($("#id_flight_data_range_from").val() == ""){
							$("#range_to_error_id").css("display","inline");
				    		$("#id_flight_data_range_from").addClass("input_error");
						}
						
						if($("#id_flight_data_range_to").val() == ""){
							$("#range_to_error_id").css("display","inline");
				    		$("#id_flight_data_range_to").addClass("input_error");
						}
						
						if ($("#id_flight_data_range_from").val() != ""&&
								$("#id_flight_data_range_to").val() != ""){
							$("#range_to_error_id").css("display","none");
				    		$("#id_flight_data_range_from").removeClass("input_error");
				    		$("#id_flight_data_range_to").removeClass("input_error");
						}
					}else{
						if($(this).attr("id") == 'id_flight_data_cg'){
							if($('#id_flight_data_cg').val() == ""){
								$("#error_id_flight_data_cg").css("display","inline");
								$("#id_flight_data_cg").addClass("input_error");
							}else{
								$("#error_id_flight_data_cg").css("display","none");
								$("#id_flight_data_cg").removeClass("input_error");
							}
						}else{
							if ($("#id_flight_data_range_from").val() != "" &&
									$("#id_flight_data_range_to").val() != ""){
								$("#range_to_error_id").css("display","none");
					    		$("#id_flight_data_range_from").removeClass("input_error");
					    		$("#id_flight_data_range_to").removeClass("input_error");
							}
							
							if($("#id_flight_data_range_from").val() == ""){
								$("#range_to_error_id").css("display","inline");
					    		$("#id_flight_data_range_from").addClass("input_error");
							}
							
							if($("#id_flight_data_range_to").val() == ""){
								$("#range_to_error_id").css("display","inline");
					    		$("#id_flight_data_range_to").addClass("input_error");
							}
							
							if ($(this).val() != ""){
					    		$(this).removeClass("input_error");
							}
							
							if ($("#id_flight_data_range_from").val() != ""&&
									$("#id_flight_data_range_to").val() != ""){
								$("#range_to_error_id").css("display","none");
					    		$("#id_flight_data_range_from").removeClass("input_error");
					    		$("#id_flight_data_range_to").removeClass("input_error");
							}
						}
					}
			}else{
				var element = jQuery(this).parent().parent().parent().find('span').html();
				// Check input is null
				if ((element_value == "" || element_value == " " || element_value == null) 
						&& class_select.indexOf("req") > -1){
					$("#"+$(this).attr("id")).addClass("input_error");
					$(error_id).append("<ul class = 'errorlist' ><li>"+name+" is required.</li></ul>");
				}else{// Input has data
					$("#"+$(this).attr("id")).removeClass("input_error");
					$(error_id + " ul").remove();
				}
			}
		} else{// Check
			// Disappear star
			jQuery("#id_flight_data_cg").parent().find('span span').css("display", "none");
			jQuery("#id_flight_data_range_from").parent().find('span span').css("display", "none");
			jQuery("#id_flight_data_range_to").parent().find('span span').css("display", "none");
				if($(this).attr("id") == "id_flight_data_cg" ||
						$(this).attr("id") == "id_flight_data_range_from" ||
						$(this).attr("id") == "id_flight_data_range_to" ||
						$(this).attr("id") == "id_load_schedule"){
					if ($(this).attr("id") == "id_load_schedule"){
						$("#error_id_flight_data_cg").css("display","none");
						$("#id_flight_data_cg").removeClass("input_error");
						$("#range_to_error_id").css("display","none");
						$("#id_flight_data_range_from").removeClass("input_error");
						$("#id_flight_data_range_to").removeClass("input_error");
					}
					if ($(this).attr("id") == "id_flight_data_cg"){
						$("#error_id_flight_data_cg").css("display","none");
						$("#id_flight_data_cg").removeClass("input_error");
					}
				}else{
					// Check input is null
					if ((element_value == "" || element_value == " " || element_value == null) 
							&& class_select.indexOf("req") > -1){
						$("#"+$(this).attr("id")).addClass("input_error");
						$(error_id).append("<ul class = 'errorlist' ><li>"+name+" is required.</li></ul>");
					}else{// Input has data
						$("#"+$(this).attr("id")).removeClass("input_error");
						$(error_id + " ul").remove();
					}
				}// End else
			}// End else
	});// End input change
	
	$(document).on('change', '#id_flight_data_range_from', function(e){
		if($('#id_flight_data_range_to').val() != "" 
				& !isNaN($('#id_flight_data_range_from').val())
				& (parseFloat($('#id_flight_data_range_to').val()) <= parseFloat($('#id_flight_data_range_from').val()))){
			$(this).val("");
			if(!$("#id_load_schedule").is(":checked")){
				$(this).addClass("input_error");
				$("#range_to_error_id").css("display","inline");
			}
			$(this).focus();
			alert("Range to must be greater than Range from.")
		}
	});
	
	$(document).on('change', '#id_flight_data_range_to', function(e){
		if((parseFloat($('#id_flight_data_range_to').val()) <= parseFloat($('#id_flight_data_range_from').val())) 
				& !isNaN($('#id_flight_data_range_to').val())
				& !isNaN($('#id_flight_data_range_from').val())){
			$(this).val("");
			if(!$("#id_load_schedule").is(":checked")){
				$(this).addClass("input_error");
				$("#range_to_error_id").css("display","inline");
			}
			$(this).focus();
			alert("Range to must be greater than Range from.")
		}
	});
	
	// checkbox event on each row
	$(document).on("change", "input:not(:hidden)[name^='row_check_']", function() {
		//console.log("check_change");
		if($(this).is(':checked')) {// tick
	    	var is_check_all = true;
	    	var count = 0;
	    	$("input:not(:hidden)[name^='row_check_']").each(function(){
	    		if(!$(this).is(':checked')) {// if exist one  untick
	    			is_check_all = false;
	    			// break from each loop
	    			return false;
	    		}
	    	});
	    	if (is_check_all)
	    		$("input[name='all_check']").prop('checked', true);
	    	
	    } else {// untick
	    	$("input[name='all_check']").prop('checked', false);
	    }
	});
	
	// untick checkbox- all when click on page link
	$(document).on("click", "div.pagging input.page", function(e) {
		$("input[name='all_check']").prop('checked', false);
	});

	
//	Total column
	function colSum(subclass, totalclass) {
	    var sum=0;
	    $(subclass).each(function() { 
	    	if($(this).html())
				sum = sum + parseFloat($(this).html());
	    });
	    if(totalclass == "#total_pas" 
	    	|| totalclass == "#flight_time" 
	    		|| totalclass == "#patient"){
	    	if(sum){
	    		$(totalclass).html(sum);
	    	}
	    	
	    }else{
	    	if(sum){
	    		$(totalclass).html(sum.toFixed(2));
	    	}
	    }
	}
	colSum(".cls_pas","#total_pas");
	colSum(".cls_flight_time","#flight_time");
	colSum(".cls_cargo","#cargo");
	colSum(".cls_block_time","#block_time");
	colSum(".patient","#patient");
	
	
//	Check time field
	on = false
	off = false
	$(document).on('change', '#id_off', function(e){
		if($("#id_off").val() != "" && $("#id_on").val() != ""){
			$("#on_off_error_mess_div").css("display","none");
		}
		$("#id_off").css("border","1px solid #c6c6c6");
		if (check_off_on_valid('#id_off')){
			off = true;
		}
		if ($('#id_on').val() != ""){
			if(check_off_on_valid('#id_on')){
				on = true;
			}
			
		}
		
		diff_time();
	});
	
	$(document).on('change', '#id_on', function(e){
		if($("#id_off").val() != "" && $("#id_on").val() != ""){
			$("#on_off_error_mess_div").css("display","none");
		}
		$("#id_on").css("border","1px solid #c6c6c6");
		if (check_off_on_valid('#id_on')){
			on = true
		}
		if ($('#id_off').val() != ""){
			if(check_off_on_valid('#id_off')){
				on = true	
			}
		}
		
		diff_time();
	});
	
	function check_off_on_valid(id){
		if (check_time($(id).val()) == false){
			$("#id_flight_time").val(""); 
			$(id).val("");	

			if($("#id_off").val() == ""){
				$("#id_off").css("border","1px solid red");
			}
			if($("#id_on").val() == ""){
				$("#id_on").css("border","1px solid red");
			}
			$(id).focus();
			return false
		}
		if ($(id).val().indexOf(" ") != -1){
			$(id).val($(id).val().trim())
		}
		return true
	}
	
	function check_time(value){
		var regexp = /([01][0-9]|[02][0-3]):[0-5][0-9]/;
		var correct = regexp.test(value);
		if (correct == false || value.trim().length != 5){
			alert("Please input correct time format (HH:MM)")
			$("#on_off_error_mess_div").css("display","block");
			correct = false;
		}
		return correct
	}
	
	function diff_time(){
		var start = $("#id_off").val();
		var end = $("#id_on").val();
	    if (start && end){
		    s = start.split(':');
		    e = end.split(':');
		    min = e[1]-s[1];
		    hour_carry = 0;
		    if(min < 0){
		        min += 60;
		        hour_carry += 1;
		    }
		    hour = e[0]-s[0]-hour_carry;
		    value = hour*60 + min;
		    if (value > 0){
		    	$("#id_flight_time").val(value);
	    		load_partial_nfr();
		    }else{
		    	$("#id_flight_time").val("");
		    }
		}
	}
	
	function load_partial_nfr(){
		value = $("#id_flight_time").val();
		var select = document.getElementById("id_partial_nfr");
    	var length = select.options.length;
    	for (i = 1; i < length; i++) {
    	  select.options[i] = null;
    	  i --;
    	  length --;
    	}
    	for (index = 0; index <= value; index ++){
    		var option = document.createElement("option");
    		option.text = index;
    		option.value = index;
    		select.add(option);
    	}
//    	$("#id_partial_nfr").prop('selectedIndex', select_value);
    	$('#id_partial_nfr').kendoDropDownList({ animation: false});
	}
	
	$(document).on('click', '.edit_flight_log', function(e){
		var index = $(this).closest('td').parent()[0].sectionRowIndex;
		var max_pax = $("#max_pax").val();
		var loc_id = $("#id_flight_data_fuel_station").val();
	    Dajaxice.flight_log.edit_flight_log(Dajax.process, {'index':index,									
	    													'max_pax':max_pax,
	    													'is_submitted':false
	    													});
	    open_popup('#log-box');
	});
	
	$(document).on('click', '.delete_flight_log', function(e){
		if (confirm("Are you sure to delete this record?")){
			var list_fuel_location = []
			var length = $('#ff').datagrid('getRows').length;
			if(length!=0){
				for (var i=0;i<length;i++) {
					list_fuel_location.push($('#ff').datagrid('getRows')[i].location);
				}
			}
//			var index = $(this).closest('td').parent()[0].sectionRowIndex;
			var index = $(this).parent().parent().find("td:first").html()
			var max_pax = $("#max_pax").val();
		    Dajaxice.flight_log.delete_flight_log(call_back_delete, {'index':index,
		    														'max_pax':max_pax,
		    														'list_fuel_location':list_fuel_location});
		}
	});
	
	
// 	SAVE FLIGHT LOG INTO SESSION
	$(document).on('click', '#save_flight_log', function(e){
		if(verify_inp_req()){			
			var list_fuel_location = []
			var length = $('#ff').datagrid('getRows').length;
			if(length!=0){
				for (var i=0;i<length;i++) {
					list_fuel_location.push($('#ff').datagrid('getRows')[i].location);
				}
			}
			before_fuel_location = $("#before_fuel_location").val()
			
			var max_pax = $("#max_pax").val();
			var partial_range = $("#id_flight_time").val();
			var is_edit = $("#is_edit").val();
			Dajaxice.flight_log.save_flight_log(js_callback, 
					{'forms':$('#popup_add_flight_log').serialize(),
					 'max_pax':max_pax,
					 'partial_range':partial_range,
					 "is_edit":is_edit,
					 'before_fuel_location':before_fuel_location,
					 'list_fuel_location':list_fuel_location});
		}
		
	});
	
// Close popup
	$(document).on('click', '.close_popup', function(e){
		close_popup();
	});
	
	$('.add_flight_log').click(function() {
		if (verify_inp_sel()){
			var rowCount = $('#rs_flight_log_form tr').length;
			var fuel = $('#id_fuel').val();
		    var next_order = rowCount - 2
		    var max_pax = $("#max_pax").val();
		    
			Dajaxice.flight_log.add_flight_log(Dajax.process, 
					{'next_order_id':next_order,
					'max_pax':max_pax,
					'fuel':fuel});
		    open_popup('#log-box');
		}else{
			alert("All required fields must be entered before adding flight leg.");
			return false;
		}
		
	});
	
	function open_popup(loginBox){
		//Fade in the Popup and add close button
		$(loginBox).fadeIn(300);
		
		// Add the mask to body
		$('body').append('<div id="mask"></div>');
		$('#mask').fadeIn(300);
		jQuery(loginBox).center();
	}
	
	/* Monitor Center */
	jQuery.fn.center = function () {
	    this.css("position","absolute");
	    this.css("top",  $(window).scrollTop() + 100 + "px");
	    //this.css("top", Math.max(200, ($(window).innerHeight()/2 - $(this).outerHeight()) + $(window).scrollTop()) + "px")
	    this.css("height", "auto");
	    this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) + 
                $(window).scrollLeft()) + "px");
	    return this;
	}
	
	// When clicking on the button close or the mask layer the popup closed
	function close_popup(){
		$('#mask , .login-popup').fadeOut(0 , function() {
			$('#mask').remove();
			$(".popup_main").remove();
		}); 
	}
	
	$("#history").delegate("tr", "dblclick", function(event){
        var log_id = $(this).find(".log_id").val()
        $("active_link")
        if (log_id){
        	window.location.href = '/log/?log_id=' + log_id;
        }
        event.preventDefault();
        return false;
    });
	
	function js_callback(data){
		Dajax.process(data);
		if(save_add_flight_leg()){
			close_popup();
		}
		fill_data_combo();
		return true
	}
	
	function call_back_delete(data){
		Dajax.process(data);
		fill_data_combo();
		return true
	}
	
	$(document).on('change', '#log-box select', function(){
		error_id = "#error_" + $(this).attr("id");
		element_value = $(this).val();
		name = $(this).parent().parent().find('span').html();
		name = name.replace("*","");
		class_select = $(this).attr("class");
		if ((element_value == "" || element_value == " " || element_value == null) 
				&& class_select.indexOf("req") > -1){
			if ($(error_id + " ul li").html() == null){
				$("#"+$(this).attr("id")).parent().find('span:first').addClass("input_error");
				$(error_id).append("<ul class = 'errorlist' ><li>"+name+" is required.</li></ul>");
			}
		}else{
			$("#"+$(this).attr("id")).parent().find('span:first').removeClass("input_error");
			$(error_id + " ul").remove();
		}
	});
	
	$(document).on('click', '.id_cancel_popup',function(e) {
		close_popup();
	});
	
	$(document).on('click', '#add_flight_log_cancel',function(e) {
		if(!confirm('Do you want to save edited information?')){
			window.location='/';
			return false;
		} else{
			return true;
		}
			
	});
	
	$(document).on('click', '#id_submit',function(e) {
		var is_checked = false;
		$("input:not(:hidden)[name^='row_check_']").each(function(){
    		if($(this).is(':checked')) {// if exist one  untick
    			is_checked = true;
    			// break from each loop
    			return false;
    		}
    	});
		if (!is_checked){
			alert("Please select at least one log to submit.");
			return false;
		}else{
			if(!confirm('Are you sure to submit these flight logs?'))
				return false;
		}
	});
	
	$(document).on('click', '#id_delete',function(e) {
		var is_checked = false;
		$("input:not(:hidden)[name^='row_check_']").each(function(){
    		if($(this).is(':checked')) {// if exist one  untick
    			is_checked = true;
    			// break from each loop
    			return false;
    		}
    	});
		if (!is_checked){
			alert("Please select at least one log to delete.");
			return false;
		}else{
			if(!confirm('Are you sure to delete these flight logs?'))
				return false;
		}
	});
	
	$(document).on('click', '#popup_reset', function(e){
		//$("#id_flight_data_fuel_station").val("");
		$("#id_manifest_number, #id_flight_data_tlo_w, #id_flight_data_cargo_weight,\
				#id_flight_data_amount, #id_fuel_wheels_down, #id_flight_data_cg,\
				#id_off, #id_on, #id_flight_data_block_time, #id_flight_data_range_from,\
				#id_flight_data_range_to, #id_flight_data_fuel_amount, #id_flight_time,\
				#id_flight_data_patient, #id_day, #id_night, #id_pilot_nvg, #id_co_pilot_nvg").val("");
		 document.getElementById('id_partial_nfr').selectedIndex = 0;
		 //document.getElementById('id_flight_data_fuel_station').selectedIndex = 0;
		 $("#id_flight_data_fuel_station").val("");
		 document.getElementById('id_to').selectedIndex = 0;
		 document.getElementById('id_passenger').selectedIndex = 0;
		 document.getElementById('id_from_field').selectedIndex = 0;
		 document.getElementById('id_slot_purpose_id').selectedIndex = 0;
		 document.getElementById('id_emp_by').selectedIndex = 0;
		$('input').attr('checked', false);
		
		$(".errorlist li").remove();
		$("#on_off_error_mess_div").css("display","none");
		$("input").removeClass("input_error");
		$("select").parent().find("span:first").removeClass("input_error");
		
		value = $("#id_flight_time").val();
		var select = document.getElementById("id_partial_nfr");
    	var length = select.options.length;
    	for (i = 1; i < length; i++) {
    	  select.options[i] = null;
    	  i --;
    	  length --;
    	}
    	$(".popup_main select").kendoDropDownList({ animation: false });
    	$("#id_flight_data_fuel_station").data("kendoComboBox").text("");
	    return false
	});
	
	function verify_inp_req(){
		var pass = true;
		var length = $(".popup_main input.req").length;
		var allInputs = $( "input.req" );
    	allInputs.each(function(){
    		var id = "#error_" + jQuery(this).attr("id");
    		if(jQuery(this).val() == ""){
    			i= i + 1;
    			tex = jQuery(this).parent().find('span').html();
    			tex = tex.replace("<span class=\"star\">*</span>","");
    			tex = tex.replace("<span class=\"star\" style=\"display: inline;\">*</span>","");
    			$(id).html("<ul class = 'errorlist' ><li>"+ tex +" is required.</li></ul>");
    			jQuery(this).addClass('input_error');
    		}
    	});
		for (index = 0; index < length; index++){
            if($(".popup_main input.req")[index].value == ""){
            	pass = false;
            	id = $(".popup_main input.req")[index].id;
            	if(!$('#id_load_schedule').is(":checked")){
            		if(id == "id_flight_data_cg"){
                		$("#error_id_flight_data_cg").css("display","inline");
                	}
            		if(id == "id_flight_data_range_from"){
                		$("#range_to_error_id").css("display","inline");
                	}
            		if(id == "id_flight_data_range_to"){
                		$("#range_to_error_id").css("display","inline");
                	}
            	}else{
            		if(id == "id_flight_data_cg"){
            			pass = true;
            			$("#id_flight_data_cg").removeClass("input_error");
                		$("#error_id_flight_data_cg").css("display","none");
            		}
            		if(id == "id_flight_data_range_from"){
            			pass = true;
                		$("#range_to_error_id").css("display","none");
                		$("#id_flight_data_range_from").removeClass("input_error");
                	}
            		if(id == "id_flight_data_range_to"){
            			pass = true;
                		$("#range_to_error_id").css("display","none");
                		$("#id_flight_data_range_to").removeClass("input_error");
                	}
            	}
            	if(id == "id_off" || id == "id_on"){
            		$("#on_off_error_mess_div").css("display","block");
            	}
            }
        }
		var length = $(".popup_main select.req").length;
		for (index = 0; index < length; index++){
            if($(".popup_main select.req")[index].value == ""){
            	pass = false;
            	id = $(".popup_main select.req")[index].id;
        		//$("#"+id).addClass('input_error');
            	jQuery("#"+id).parent().find('span:first').addClass('input_error');
            	name = $("#"+id).parent().parent().find('span:first').html();
            	name = name.replace("<span class=\"star\">*</span>","");
            	$("#error_"+id).html("<ul class = 'errorlist' ><li>"+name+" is required.</li></ul>");
            }
        }
		var start = $("#id_off").val();
		var end = $("#id_on").val();
	    if (start && end){
		    s = start.split(':');
		    e = end.split(':');
		    min = e[1]-s[1];
		    hour_carry = 0;
		    if(min < 0){
		        min += 60;
		        hour_carry += 1;
		    }
		    hour = e[0]-s[0]-hour_carry;
		    value = hour*60 + min;
		    partial_temp = $("#id_partial_nfr").val();
		    if (value > 0){
		    	$("#id_flight_time").val(value);
	    		load_partial_nfr();
		    }else{
		    	$("#id_flight_time").val("");
		    	alert("Land time must be greater than take off time.");
		    	$("#id_on").css("border","1px solid red");
		    	$("#id_on").focus();
		    	$("#id_flight_time").val("");
		    	$("#on_off_error_mess_div").css("display","block");
		    	pass = false;
		    }
	    }	 
	    $("#id_partial_nfr").prop('selectedIndex', parseInt(partial_temp)+1);
		return pass;
	}
	
	$("#id_log_number, #mod, #id_a1c, #cus, #id_log_date_search").keyup(function(event){
	    if(event.keyCode == 13){
	        $("#search_flight_log").click();
	    }
	});
	
	// Event click on smart auto complete
	$(document).on('click', '#id_flight_data_fuel_station', function(e){
		$( "#id_flight_data_fuel_station" ).keyup();
		$( "#id_flight_data_fuel_station").keyup(function( e ) {
			if (!e.keyCode){
				e.keyCode = 40;
			}
			
			var options = $(this).data("smart-autocomplete");
			if(e.keyCode === 40){
	          if(options.resultsContainer && options.resultsContainer.is(':visible')){
	            var current_selection = options.currentSelection - 1;
	            var result_suggestions = $(options.resultsContainer).children();
	            if(current_selection >= 0)
	              $(options.context).trigger("itemUnfocus", result_suggestions[current_selection] );

	            if(isNaN(current_selection) || null == current_selection || (++current_selection >= result_suggestions.length) )
	              current_selection = 0;

	            options["currentSelection"] = current_selection;

	            $(options.context).trigger("itemFocus", [result_suggestions[current_selection]] );
	            e.keyCode = 1; 
	          }
	          else {
	            $(options.context).trigger("keyIn", [$(this).val()]);
	          }
	        }
		});
	});
	
	$("#id_co_pilot_employee_number").change(function() {
		co_pilot = $(this).val(); 
		Dajaxice.flight_log.load_copilot(Dajax.process, 
				{'co_pilot':co_pilot});
	});
});