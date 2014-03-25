//Confirm before submit form add flight log
//If - OK: Continue submit
//	 - Cancel: Add flight into pending
var idButton = "";
function submit_form_add() {
	if(idButton=="add_flight_log_submit"){
		if (verify_inp_sel() & valid_grid_fuel() & valid_grid_fuel()){
			if(!confirm('Are you sure to submit this flight log?')){
				return false;
			} else{
				return true;
			}
		}
	}else{
		return true;
	}
}

function validate_operational_weight() {
	if (jQuery("#id_opterational_weight").val() == "") {
		$("#err_id_opterational_weight").text('Operational Weight is required');
	} else {
		$("#err_id_opterational_weight").text('');
	}
}
function verify_inp_sel() {
	var valid = true;
	var i = 0;
	var allInputs = $("input.req");
	allInputs.each(function() {
		var id = "#err_" + jQuery(this).attr("id");
		if (jQuery(this).val() == "") {
			i = i + 1;
			var tex = jQuery(this).parent().find('span').html();
			tex = tex.replace("<span class=\"star\">*</span>","");
			tex = String(tex).replace("<SPAN class=star>*</SPAN>","");
			$(id).text(tex + ' is required');
			jQuery(this).addClass('input_error');

		} else if (jQuery(this).attr("id") == 'id_log_date') {
			if (valid_date() == false) {
				jQuery(this).addClass('input_error');
				i = i + 1;
			}
		}
	});

	var allselects = $("select.req");
	allselects.each(function() {
		if (jQuery(this).val() == 0) {
			i = i + 1;
			var id_com = "#err_" + jQuery(this).attr("id");
			var tex1 = jQuery(this).parent().parent().parent().find('span').html();
			tex1 = tex1.replace("<SPAN class=star>*</SPAN>","");
			tex1 = tex1.replace("<span class=\"star\">*</span>","");
			tex1 = tex1.replace("<span class = \"star\" style=\"display: inline;\">*</span>","");
			tex1 = tex1.replace("<SPAN class = \"star\" style=\"display: inline;\">*</SPAN>","");
			if (id_com == "#err_id_co_pilot_employee_number") {
				$(id_com).text('Co-Pilot Employee Number is required');
			} else {
				$(id_com).text(tex1 + ' is required');
			}

			jQuery(this).parent().find('span:first').addClass('input_error');
		}
	});
	if (i > 0) {
		valid = false;
	}
	if (valid == false) {
		jQuery('.err').css('display', 'block');
		window.location.hash = "#number";
	}

	return valid;
}

function verify_blur(e) {
	var val = jQuery(e).val();
	var id = "#err_" + jQuery(e).attr("id");
	if (val == "") {
		jQuery('.err').css('display', 'block');
		var tex = jQuery(e).parent().find('span').html();
		tex = tex.replace("<span class=\"star\">*</span>","");
		tex = tex.replace("<SPAN class=star>*</SPAN>","");
		$(id).text(tex + ' is required');
		jQuery(e).addClass('input_error');
	} else {
		$(id).text('');
		jQuery(e).removeClass('input_error');
	}
}

function valid_grid() {
	var length = $('#tt').datagrid('getRows').length;
	var isSave = false;
	var valid = true;
	if (length != 0) {
		for ( var i = 0; i < length; i++) {
			isSave = $('#tt').datagrid('getRows')[i].editing
			if (isSave) {
				break;
			}
		}
	}
	if (isSave) {
		valid = false;
	}

	return valid;
}

function valid_grid_fuel() {
	var length = $('#ff').datagrid('getRows').length;
	var isSave = false;
	var notSave = false;
	var valid = true;
	if (length != 0) {
		for ( var i = 0; i < length; i++) {
			isSave = $('#ff').datagrid('getRows')[i].editing
			if (isSave) {
				var loc = $('#ff').datagrid('getEditor', {
					index : i,
					field : 'location'
				});
				var loc_val = $(loc.target).combobox('getValue');

				var ga = $('#ff').datagrid('getEditor', {
					index : i,
					field : 'gallon'
				});
				var ga_val = $(ga.target).numberbox('getValue');

				var owner = $('#ff').datagrid('getEditor', {
					index : i,
					field : 'owner'
				});
				var owner_val = $(owner.target).text('getValue').val();

				var amount = $('#ff').datagrid('getEditor', {
					index : i,
					field : 'amount'
				});
				var amount_val = $(amount.target).text('getValue').val();

				if ((loc_val != "") || (ga_val != "") || (owner_val != "")
						|| (amount_val != "")) {
					notSave = true;
				}

				break;
			}
		}
	}
	if (notSave) {
		valid = false;
	}

	return valid;
}

function validateRegisterForm() {
	// return true;
	jQuery('.error_id_mess').html('');
	var ret = true;
	jQuery('.err').css('display', 'none');
	jQuery('.err').html('');
	jQuery('#over_id_password').css('color', '#666');
	jQuery('#id_confirm_password').css('color', '#666');
	jQuery('#over_id_confirm_password').css('font-weight', 'normal');
	jQuery('#over_id_password').css('font-weight', 'normal');
	if (ret == true) {
		jQuery("form#register input").each(
				function() {
					var input = jQuery(this);
					input.css('color', '#000');
					if ((input.val() == ''
							|| input.val() == 'This is request field' || input
							.val().indexOf('is required.') > 0)
							&& input.attr('type') != 'password') {
						var e_id = 'over_' + input.attr('id');
						var text = jQuery('#' + e_id).html();
						input.val(text + ' is required.');
						input.css('color', '#c2192a');
						jQuery('#' + e_id).css('display', 'none');
						ret = false;
					}
				});
		if (jQuery('#id_password').val() == '') {
			jQuery('#over_id_password').html('Password is required.');
			jQuery('#over_id_password').css('color', '#c2192a');
			jQuery('#over_id_password').css('font-weight', 'bold');
			ret = false;
		}
		if (jQuery('#id_confirm_password').val() == '') {
			jQuery('#over_id_confirm_password').html(
					'Confirm Password is required.');
			jQuery('#over_id_confirm_password').css('color', '#c2192a');
			jQuery('#over_id_confirm_password').css('font-weight', 'bold');
			ret = false;
		}
	}
	if (ret == true) {
		jQuery('#id_email').css('color', '#000');
		var x = document.forms["register"]["email"].value;
		var atpos = x.indexOf("@");
		var dotpos = x.lastIndexOf(".");
		if (atpos < 1 || dotpos < atpos + 2 || dotpos + 2 >= x.length) {
			jQuery('#id_email').css('color', '#c2192a');
			jQuery('#id_email').val('Not a valid e-mail address');
			ret = false;
		}
	}
	if (ret == true
			&& jQuery('#id_password').val() != jQuery('#id_confirm_password')
					.val()) {
		jQuery('#id_confirm_password').val('');
		jQuery('.err').css('display', 'block');
		jQuery('.err').html('The password doesn\’t match confirmation.');
		ret = false;
	}
	if (jQuery('.err').html() == 'The password doesn\’t match confirmation.'
			|| jQuery('#confirm_password').html() != '') {
		jQuery('#over_id_confirm_password').css('display', 'none');
		ret = false;
	}
	if (ret == false) {
		return false;
	}
}

function validateLoginForm() {
	var ret = true;
	var err;
	if (ret == true) {
		jQuery("form#login input").each(
				function() {
					var input = jQuery(this);
					input.css('color', '#000');
					if (input.val() == ''
							|| input.val() == 'This is request field'
							|| input.val() == 'Employee Number is incorrrect.'
							|| input.val() == 'Password is incorrect.'
							|| input.val().indexOf('is required.') > 0) {

						var e_id = 'over_' + input.attr('id');
						var text = jQuery('#' + e_id).html();
						input.val(text + ' is required.');
						if (input.attr('id') == "id_password"
								&& input.is(':password'))
							input.attr('type', 'text');
						input.css('color', '#c2192a');
						jQuery('#' + e_id).css('display', 'none');
						// input.focus();
						ret = false;
					}
				});
	}
	if (ret == false) {
		// $('#id_employee_number').focus();
		return false;
	}
}
function validate_email_form() {
	var valu = '';
	jQuery('input.attack_file').each(function() {
		v = jQuery(this).val().replace('flight_log_', '');
		valu = valu + ',' + v.replace('.pdf', '');
	});
	valu = valu.substring(1);
	jQuery('.hiden_attack').val(valu);
	var ret = true;
	jQuery('.jqte_editor').css("color", "#000");
	/*if (ret == true) {
		jQuery("form#form_email_popup input.request")
				.each(
						function() {
							var input = jQuery(this);
							input.css("color", "#000");
							if (input.val() == "") {
								input.val("This is required field");
								input.css("color","#c2192a");
								ret = false;
								return;
							}
							input
									.on(
											"focus",
											function() {
												if (input.val() == "This is required field"
														|| input.val() == "Not a valid e-mail address") {
													input.val("");
													input.css("color", "#000");
												}
											})
									.on(
											"blur",
											function() {
												if (input.val() == "This is required field"
														|| input.val() == "Not a valid e-mail address") {
													input.val("");
													input.css("color", "#000");
												}
											});
						});
	}*/
	if (jQuery('.jqte_editor').html() == ''
			|| jQuery('.jqte_editor').html() == 'This is required field') {
		/*
		 * jQuery('.jqte_editor').html("This is required field");
		 * jQuery('.jqte_editor').css("color","#c2192a"); ret = false;
		 */}
	jQuery(".field_email").css("color", "#000");
	jQuery("form#form_email_popup .field_email").each(function() {
		var em = jQuery(this);
		var x = em.val();
		if (x == "" || x == "This is required field") {
			em.val("This is required field");
			em.css("color","#c2192a");
			ret = false;
		}else if (x && em.css('display') == 'block') {
			x.replace(";", ",");
			x.replace(" ", "");
			var array = x.split(',');
			for (i = 0; i < array.length; i++) {
				if(array[i] != "" && array[i].indexOf(" ") == -1){
					var atpos = array[i].indexOf("@");
					var dotpos = array[i].lastIndexOf(".");
					if (atpos < 1 || dotpos < atpos + 2
							|| dotpos + 2 >= array[i].length) {
						em.css("color", "#c2192a");
						em.val("Not a valid e-mail address");
						ret = false;
					}
				} 
			}
		}
	});
	
	jQuery("form#form_email_popup .m_email")
			.each(
					function() {
						var em = jQuery(this);
						var x = em.val();
						if (x && em.css('display') == 'block') {
							x.replace(";", ",");
							x.replace(" ", "");
							var array = x.split(',');
							for (i = 0; i < array.length; i++) {
								if(array[i] != "" && array[i].indexOf(" ") == -1){
									var atpos = array[i].indexOf("@");
									var dotpos = array[i].lastIndexOf(".");
									if (atpos < 1 || dotpos < atpos + 2
											|| dotpos + 2 >= array[i].length) {
										em.css("color", "#c2192a");
										em.val("Not a valid e-mail address");
										ret = false;
									}
								} 
							}
							em
									.on(
											"focus",
											function() {
												if (em.val() == "This is required field"
														|| em.val() == "Not a valid e-mail address") {
													em.val("");
													em.css("color", "#000");
												}
											})
									.on(
											"blur",
											function() {
												if (em.val() == "This is required field"
														|| em.val() == "Not a valid e-mail address") {
													em.val("");
													em.css("color", "#000");
												}
											});
						}
					});
	if (ret == false) {
		return false;
	}else{
		 if ($("#btn_send_email").attr("type") = "submit"){
			 return true;
		 }else{
			 return false;
		 }
	}
	$(this).attr("type","button");
}

$(document).on('click', '#btn_send_email', function(){
	if($("#email").val() != "Not a valid e-mail address"){
		$(this).attr("type","submit");
	}
});

function valid_num() {
	valid = true;
	if ($('#id_log_number').val() != "") {
		var value = $('#id_log_number').val().replace(/^\s\s*/, '').replace(
				/\s\s*$/, '');
		var intRegex = /^\d+$/;
		if (!intRegex.test(value)) {
			jQuery('.min-32-error').css('display', 'block');
			$('#search_num_er').text('This must be a number');
			valid = false;
		} else {
			$('#search_num_er').text('');
		}
	} else {
		$('#search_num_er').text('');
	}
	if (valid == false) {
		jQuery('.err').css('display', 'block');
	}
	return valid;

}

function valid_date() {
	valid = true;
	var d = $("#id_log_date").val();
	if (d != "") {
		var comp = d.split('/');
		var m = parseInt(comp[0], 10);
		var d = parseInt(comp[1], 10);
		var y = parseInt(comp[2], 10);
		var date = new Date(y, m - 1, d);
		if (date.getFullYear() == y && date.getMonth() + 1 == m
				&& date.getDate() == d) {
			var tday = new Date();
			if (date.getTime() > tday.getTime()) {
				jQuery('.min-32-error').css('display', 'block');
				$("#id_log_date").addClass('input_error');
				$("#err_id_log_date").text(
						"Date can't be greater than current date");
				valid = false;
			} else {
				$("#id_log_date").removeClass('input_error');
				$("#err_id_log_date").text("");
			}

		} else {
			$("#err_id_log_date").text("Invalid date");
			$("#id_log_date").addClass('input_error');
			jQuery('.min-32-error').css('display', 'block');
			valid = false;
		}
	} else {
		$("#id_log_date").addClass('input_error');
		$("#err_id_log_date").text("Date is require");
		valid = false;
	}

	if (valid == false) {
		jQuery('.err').css('display', 'block');
	}

	return valid;
}

function valid_date_search() {
	valid = true;
	var d = document.getElementsByName("log_date")[0].value;
	date_er = document.getElementById("search_date_er");
	if (d != "") {
		var comp = d.split('/');
		var m = parseInt(comp[0], 10);
		var d = parseInt(comp[1], 10);
		var y = parseInt(comp[2], 10);
		var date = new Date(y, m - 1, d);
		if (date.getFullYear() == y && date.getMonth() + 1 == m
				&& date.getDate() == d) {
			date_er.innerHTML = "";
		} else {
			date_er.innerHTML = "Invalid date";
			valid = false;
		}
	}
	if (valid == false) {
		jQuery('.err').css('display', 'block');
	}
	return valid;
}

$(document).ready(function() {
	$("#id_log_number").change(function (e){
		if(isNaN($("#id_log_number").val())){
			$("#er_search").text("");
			$("#id_log_number").val("");
			$("#err_log_number").text("Please enter a number");
			$("#search_flight_log").attr("disabled", "disabled");
			setTimeout('$("#search_flight_log").removeAttr("disabled")', 500);
		}else{
			$("#err_log_number").text("");
		}
	});
});

function valid_search() {
	$("#log_num_hidden").val($("#id_log_number").val());
	if ($("#id_log_number").val() != "" 
		&& isNaN($("#id_log_number").val())){
		$('#er_search').text('');
		$("#id_log_number").val("");
		$("#err_log_number").text("Please enter a number");
		return false;
	}else{
		$("#err_log_number").text("");
		jQuery('.messages').remove();
		var valid = true;
		var log_num = jQuery('#id_log_number').val();
		var mod = jQuery('#mod').val();
		var a1c = jQuery('#id_a1c').val();
		var cus = jQuery('#cus').val();
		var log_date = jQuery('#id_log_date_search').val();
		if (log_num == "" && mod == "" && a1c == "" && cus == "" && log_date == "") {
			valid = false;
			jQuery('.err').css('display', 'block');
			$('#er_search').text('Please enter Search criteria');
		} else {
			jQuery('.err').css('display', 'none');
			$('#er_search').text('');
		}
		return valid;
	}
	
}

function vali_decimal() {
			$(
			"#id_pilot_weight, #id_a1c_empty_weight, #id_allowable_takeoff_weight, \
			#id_opterational_weight, #id_payload_available, #id_co_pilot_weight, \
			#id_fuel, #id_log_number")
			.keypress(function(evt) {
				var theEvent = evt || window.event;
				var key = theEvent.keyCode || theEvent.which;
				 if (evt.ctrlKey && (key == 118 || key==120 || key==122 || key==99) || key==9) {
				}else{
						key = String.fromCharCode(key);
						var regex = /[0-9]|\./;
						if (regex.test(key) || theEvent.keyCode == 8) {
							var str = $(this).val();
							var check = str.match(/\./);
							if (check && key == ".") {
								return false;
							}
						} else {
							theEvent.returnValue = false;
							if (theEvent.preventDefault)
								theEvent.preventDefault();
						}
					}
			});
}

jQuery(document).ready(function($) {

	if (window.history && window.history.pushState) {
		$(window).on('popstate', function() {
			if ($('#form_email_popup .popup_content').html()) {
				$('#mask , .login-popup').fadeOut(0, function() {
					$('#mask').remove();
					$(".popup_main").remove();
				});
			}
		});

	}

});
