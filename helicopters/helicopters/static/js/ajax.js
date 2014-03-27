$(document).ready(function(){

	$(document).on('change', '#id_model', function(e){
		$("#div_error_passenger").html("");
		Dajaxice.flight_log.ajax_model_request(
				 change_model, 
				 {'mode': $(this).val()}); 
		
		//$("select").data("kendoDropDownList").each(function(){dropdownlist.text("Apples");});
		
	});
	
	vali_decimal();
	
	$(document).on('change', '#id_customer', function(e){
		Dajaxice.flight_log.ajax_contract_request(
				change_contract, 
				 {'cus_id': $(this).val()}); 
	});
	
	$("select.req").on("change", function(e) {
		var com = $(this).val();
		var id_com = "#err_" + jQuery(this).attr("id");

		if (com == 0){
			jQuery('.error-line').css('display','block');
			jQuery('.err').css('display','block');
			var tex1 = jQuery(this).parent().parent().parent().find('span').html();
			tex1 = tex1.replace("<span class=\"star\">*</span>","");
			tex1 = tex1.replace("<SPAN class=star>*</SPAN>","");
			tex1 = tex1.replace("<span class=\"star\" style=\"display: inline;\">*</span>","");
			if (id_com == "#err_id_co_pilot_employee_number"){
				$(id_com).text('Co-Pilot Employee Number is required');
			}else{
				$(id_com).text(tex1 + ' is required');
			}
			jQuery(this).parent().find('span:first').addClass('input_error');
		}else{
			$(id_com).text('');
			jQuery(this).parent().find('span:first').removeClass('input_error');
		}
	});
	
});


function change_contract(data) {	
	document.getElementById('id_contract1charter').options.length = 1; //Clean list district
	var textb = data.list_contract
	var combo = document.getElementById("id_contract1charter");
	for ( var i = 0; i < textb.length; i++) {
		var option = document.createElement("option");
		option.text = textb[i].name;
		option.value = textb[i].id;
		try {
			combo.add(option, null); // Standard browser
		} catch (error) {
			combo.add(option); //IE browser
		}
	}	
	console.log("change_contract:\n" + data.list_contract);
	$('#id_contract1charter').kendoDropDownList({animation:false, template:'<span title=\'#: mytooltip #\'>#: mytooltip #</span>', 
		dataTextField: "mytooltip"});
}

function change_model(data) {
	document.getElementById('id_a1c').options.length = 1; //Clean list district
	var textb = data.list_ac
	var combo = document.getElementById("id_a1c");
	for ( var i = 0; i < textb.length; i++) {
		var option = document.createElement("option");
		option.text = textb[i].name;
		option.value = textb[i].id;
		try {
			combo.add(option, null); // Standard browser
		} catch (error) {
			combo.add(option); //IE browser
		}
	}
	$('#div_error_passenger').text(data.pass_message);
	$('#mass_gross').text(data.mass_gross);
	$('#from').text(data.from);
	$('#to').text(data.to);
	document.getElementsByName('max_pax')[0].value = data.max_pax;
	
	$('#id_a1c').kendoDropDownList({animation:false, template:'<span title=\'#: mytooltip #\'>#: mytooltip #</span>', 
		dataTextField: "mytooltip"});
	
	$("#mass_gross").change(); //.trigger("change");

}

function pad(number, length) {
	   
    var str = '' + number;
    while (str.length < length) {
        str = '0' + str;
    }
    return str;

}

function search(data){
	var lst = data.list;
	var p = data.page;
	$('#history').find("tr:gt(0)").remove();
	$("input:not(:hidden)[name^='all_check']").attr('checked', false); 
	if(lst.length != 0){
		jQuery('.err').css('display','none');
		$('#er_search').text('');
		for (var i = 0; i < lst.length; i++){
			var d = lst[i].date.split("-");
			date = d[1]+ "/" + d[2] + "/" + d[0];
			lst[i].log_number = pad(lst[i].log_number, 6)
			if (i % 2 == 0){
				$('#history').append('<tr class="row_odd"><td class="center_nopadding"><input  style="width: 30%" type="checkbox" name = "row_check_'+ lst[i].id + '"/><input class = "log_number" type="hidden" value=' + lst[i].log_number + '> </td><input class = "log_id" type="hidden" name="id" value=' + lst[i].id + '> <td>' + lst[i].log_number + '</td><td>'+ date + 
						'</td><td>' + lst[i].cus +
						'</td><td>'+ lst[i].contract+ '</td><td>'+ lst[i].mo_name +
						'</td><td>' +  lst[i].a1c_name+'</	td></tr>');	
			}else{
				$('#history').append('<tr class="row_even"><td class="center_nopadding"><input  style="width: 30%" type="checkbox" name = "row_check_'+ lst[i].id + '"/><input class = "log_number" type="hidden" value=' + lst[i].log_number + '> </td><input class = "log_id" type="hidden" name="id" value=' + lst[i].id + '> <td>' + lst[i].log_number + '</td><td>'+ date + 
						'</td><td>' + lst[i].cus +
						'</td><td>'+ lst[i].contract+ '</td><td>'+ lst[i].mo_name +
						'</td><td>' +  lst[i].a1c_name+'</	td></tr>');		
			}
		}
		
		var page_current = data.page_current;
		var pre = page_current -1;
		var next = page_current +1;
		pagerHtml = '<span id="pa_of">Page '+ page_current +' / '+ p.length +'</span>';
		if(p.length > 1){
			if (pre > 0){
				pagerHtml = pagerHtml + '<input class="page margin-left-none first" type="submit" value="Previous" onclick="pagging_function('+ pre +', '+ data.is_sub+')">';
			}else {
				pagerHtml = pagerHtml + '<input class="page margin-left-none first dis first-black" type="submit" value="Previous" onclick="">';
			}
		}
		
		
		for (var j =0; j < p.length; j++){
			
			if (p[j] == page_current){
				var pagerHtml = pagerHtml + 
				'<input class="page margin-left-none active" class="page" type="submit" value="'+ p[j]+'" onclick="pagging_function('+ p[j] +', '+ data.is_sub+')">';			
			}else{
				var pagerHtml = pagerHtml +
				'<input class="page margin-left-none" type="submit" value="'+ p[j]+'" onclick="pagging_function('+ p[j] +', '+ data.is_sub+')">';	
			}
		}
		
		if(p.length > 1){
			if (next <= p[p.length -1]){
				pagerHtml = pagerHtml + '<input class="page margin-left-none last" type="submit" value="Next" onclick="pagging_function('+ next +', '+ data.is_sub+')">';
			}else {
				pagerHtml = pagerHtml + '<input class="page margin-left-none last dis last-black" type="submit" value="Next">';
			}
		}
		
		$('.pagination').html(pagerHtml);
		$("#pagging_bnt :input:submit, #pagging_bnt :input:button").each(function(){
			$(this).prop('disabled', false);
		});
		
	}else{
		$( ".pagination" ).empty();
		jQuery('.err').css('display','block');
		$('#er_search').text('No Flight Log is found');
		$("#pagging_bnt :input:submit, #pagging_bnt :input:button").each(function(){
			$(this).prop('disabled', true);
		});
	}
	
}

function search_function(pg, is_sub){

	if (valid_search() && valid_num() == true && valid_date_search())
		Dajaxice.flight_log.ajax_search(search, 
		{'log_num': $('#id_log_number').val(), 
		'customer': $('#cus').val(), 
		'model': $('#mod').val(), 
		'date': $('#id_log_date_search').val(),
		'ac': $('#id_a1c').val(), 'pg': pg, 'is_sub': is_sub});
	return false;
}

function pagging_function(pg,is_sub){

		Dajaxice.flight_log.ajax_search(search, 
		{'log_num': $('#id_log_number').val(), 
		'customer': $('#cus').val(), 
		'model': $('#mod').val(), 
		'date': $('#id_log_date_search').val(),
		'ac': $('#id_a1c').val(), 'pg': pg, 'is_sub': is_sub});
}

