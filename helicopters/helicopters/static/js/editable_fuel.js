
// Reformat buttons when something change on row (del, save, add new row)
// hidden = true mean that row is saved
function format_button(table_id, action_index){

	var rowCount = $('#fuel_tbl tr:visible:gt(0)').length;

    for (var i = 1; i < rowCount; i++){
    	$('#fuel_tbl tr:eq('+ i +')').find('td').eq(4).html(
    			"<img src='../static/media/delete.png' class='btnDelete' onclick='Delete(this)'/> \
				<img src='../static/media/add3.png' class='btnAdd' style='visibility: hidden'/>");
    }
    
    if (rowCount == 1){
    	$('#fuel_tbl tr:visible:eq('+ rowCount +')').find('td').eq(4).html(
        		"<img src='../static/media/add3.png' class='btnAdd' onclick='Add(this)'/>");
    }else{
    	$('#fuel_tbl tr:visible:eq('+ rowCount +')').find('td').eq(4).html(
        		"<img src='../static/media/delete.png' class='btnDelete' onclick='Delete(this)'/> \
        		<img src='../static/media/add3.png' class='btnAdd' onclick='Add(this)'/>");
    }
    
}

// Add new row: append new textbox... with id and name follow django formset
// formCount: count the current number of forms, form_id form 0
function Add(target){
	var par = $(target).parent().parent(); //tr
	tdloc = par.children("td:nth-child(1)");
    	
    val_loc = tdloc.children("span").children("select").val();

	 if (val_loc != ""){
		var formCount = parseInt($('#id_' + 'form' + '-TOTAL_FORMS').val());
		var id_loc = 'id_form-'+ formCount +'-location_id';
		var name_loc = 'form-'+ formCount +'-location_id';
		var id_gallon = 'id_form-'+ formCount +'-gallons';
		var name_gallon = 'form-'+ formCount +'-gallons';
		var id_owner = 'id_form-'+ formCount +'-owner';
		var name_owner = 'form-'+ formCount +'-owner';
		var id_amount = 'id_form-'+ formCount +'-amount';
		var name_amount = 'form-'+ formCount +'-amount';
		
		var id_del = 'id_form-'+ formCount+'-DELETE';
		var name_del = 'form-' + formCount +'-DELETE';
	    $("#fuel_tbl tbody").append(
	        "<tr>"+
	        '<td><select id='+ id_loc +' name='+ name_loc +'></select> <label style="display: none;"> </label></td>' +
	        '<td style="text-align:left; padding: 0.5% 0% 0% 1%; border-right: 0 !important;"><input id='+ id_gallon +' name='+ name_gallon +' type="number" hidden="true"> <label> </label></td>' +
	        '<td><input id='+ id_owner +' name='+ name_owner +' type="text"></td>' +
	        '<td><input id='+ id_amount +' name='+ name_amount +' type="text"></td>' +
	        '<td style="text-align:center; padding: 0.5% 0% 0% 0%;"> \
		        <img src="../static/media/delete.png" class ="btnDelete" onclick="Delete(this)"/> \
		        <img src="../static/media/add3.png" class="btnAdd" onclick="Add(this)"/> \
		        </td>'+
	        '<td style="visibility: hidden; display: none;"><input id='+ id_del +' name='+ name_del+' type="checkbox"></td>' +
	    	"</tr>");
    
		    var combo = document.getElementById("hiddenff");
		
			if (combo != null) {
				$("#"+id_loc).append(new Option("Choose One", ""));
				for (i = 0; i < combo.options.length; i++) {
					$("#"+id_loc).append(new Option(combo.options[i].text, combo.options[i].value));
				}
			}
			
		    var rowCount = $('#fuel_tbl tr:visible:gt(0)').length;
		
		    for (var i = 1; i < rowCount; i++){
		    	$('#fuel_tbl tr:visible:eq('+ i +')').find('td').eq(4).html(
		    			"<img src='../static/media/delete.png' class='btnDelete' onclick='Delete(this)'/> \
						<img src='../static/media/add3.png' class='btnAdd' style='visibility: hidden'/>");
		    }
		    
		    $('#id_' + 'form' + '-TOTAL_FORMS').val(formCount + 1); 
	 }else{
		 alert("Location must be choosen!");
	 }	    
	
    format_button("fuel_tbl", 4);
    load_combo();
};

// Delete a row (just hidden, not remove)
// Decrease formcount by one, add new row if number of visible rows is 0 (except title row)
function Delete(target){
    r = confirm('Are you sure to delete this record?');
    if(r){
    	var par = $(target).parent().parent(); //tr
    	is_hidden = true;

        par.hide();
        var row_visible = $('#fuel_tbl tr:visible:gt(0)').length;
        
        var tdButtons = par.children("td:nth-child(6)");
        id_del = tdButtons.children("input[type=checkbox]").attr('id');
      	$("#"+id_del).prop('checked', true);
        if (row_visible == 0){
        	Add();
        }
        format_button('fuel_tbl', 4);
    }
};

// onchange when choose location
$(document).ready(function() {
	format_button("fuel_tbl", 4);
	load_combo();
	
	var rowCount_fuel1 = $('#fuel_tbl tr:visible:gt(0)').length;
	for ( var j = 1; j <= rowCount_fuel1; j++) { style="visibility: hidden; display: none;"
		$('#fuel_tbl tr:visible:eq('+ j +')').find('td').eq(1).children("input").css('visibility', 'hidden');
		$('#fuel_tbl tr:visible:eq('+ j +')').find('td').eq(1).children("input").css('display', 'none');
	}
});

function load_combo(){
	var rowCount_fuel = $('#fuel_tbl tr:visible:gt(0)').length;
	var combo = document.getElementById("hiddenff");
	
	for ( var j = 1; j <= rowCount_fuel; j++) {
		loc_id1 = $('#fuel_tbl tr:visible:eq('+ j +')').find('td').eq(0).children("span").children("select").attr("id");
		$("#"+loc_id1).find('option').remove();
		if (combo != null) {
			$("#"+loc_id1).append(new Option("Choose One", ""));
			for (i = 0; i < combo.options.length; i++) {
				$("#"+loc_id1).append(new Option(combo.options[i].text, combo.options[i].value));
			}
		}
		$("#"+loc_id1).val();
		if(typeof String.prototype.trim !== 'function') {
		  String.prototype.trim = function() {
		    return this.replace(/^\s+|\s+$/g, ''); 
		  }
		}
		$("#"+loc_id1).val($('#fuel_tbl tr:visible:eq('+ j +')').find('td').eq(0).children("label").text().trim());
	}
	
	$( '#fuel_tbl select' ).change(function() {
		var rowCount_fuel = $('#fuel_tbl tr:gt(0)').length;
		var rowCount = $('#rs_flight_log_form tr:gt(0)').length;
  		var par = $(this).parent().parent().parent().get(0); //tr
		var ind = par.rowIndex;
		var coincide = false;
		
		loc_val_old = $('#fuel_tbl tr:eq('+ ind +')').find('td').eq(0).children("label").text();
		loc_val_old = loc_val_old.trim();
		loc_val_change = $('#fuel_tbl tr:eq('+ ind +')').find('td').eq(0).children("span").children("select").val();
		for ( var int = 1; int <= rowCount_fuel; int++) {
			if (int != ind){
				id_del = $('#fuel_tbl tr:eq('+ int +')').find('td').eq(5).children("input[type=checkbox]").attr('id');
		      	
				loc_val = $('#fuel_tbl tr:eq('+ int +')').find('td').eq(0).children("label").text().trim();
				if(loc_val == loc_val_change.trim() && $("#"+id_del).prop('checked')==false && loc_val_change!= ""){
					alert(" Location is duplicate.");	
					coincide = true;
					$('#fuel_tbl tr:eq('+ ind +')').find('td').eq(0).children("span").children("select").data("kendoDropDownList").value(loc_val_old);
					break;
				}
			}
		}
		
		
		
		if (!coincide){
			var sum_amount = 0;
			loc_id = $('#fuel_tbl tr:eq('+ ind +')').find('td').eq(0).children("span").children("select").attr("id");
			$('#fuel_tbl tr:eq('+ ind +')').find('td').eq(0).children("label").text(loc_val_change);
	    	loc_choosen = $("#" + loc_id + " option:selected").text();
	    	if ($("#" + loc_id).val() != ""){
	    		for (var i=2; i < rowCount; i++) {
					td_final = $('#rs_flight_log_form tr:eq('+ i +')').find('td').eq(13);
					loc = td_final.children("label").text();
					if(loc.trim() == loc_choosen.trim()){
						gallon = td_final.children("input").val();
						if (gallon != ""){
							sum_amount = sum_amount + parseInt(gallon);
						}
					}
				};
	    	}
	  		
			$('#fuel_tbl tr:eq('+ ind +')').find('td').eq(1).children("label").text(sum_amount);
			$('#fuel_tbl tr:eq('+ ind +')').find('td').eq(1).children("input").val(sum_amount);
		}
		
	});
	
	$('#fuel_tbl select').kendoDropDownList({animation:false, template:'<span title=\'#: mytooltip #\'>#: mytooltip #</span>', 
		dataTextField: "mytooltip"});
}

// Call from dajax (ajax.py), change loaction combobox if have new option from flight leg
//Call from dajax (ajax.py), if fuel amount change, gallon also change correspondly
function change_location(){
	var rowCount = $('#fuel_tbl tr:visible:gt(0)').length; 
	before_fuel_location = $("#before_fuel_location").val();
	after_fuel_location = $("#id_flight_data_fuel_station").val(); 
	before_amount = $("#before_amount").val()
	var rowCount_leg = $('#rs_flight_log_form tr:gt(0)').length-1; 
	var sum_amount = 0;
	var sum_before = 0;
	
	for ( var j = 2; j <= rowCount_leg; j++) {
		td_final = $('#rs_flight_log_form tr:eq('+ j +')').find('td').eq(13);
		var loc_label = td_final.children('label').text();
		var p = td_final.children('p').html();
		if (loc_label.trim() == after_fuel_location.trim()){
			var amount = td_final.children("input").val();
			if (amount != ""){
				sum_amount = sum_amount + parseInt(amount);
			}
		}
		
		if (p.trim() == before_fuel_location.trim()){
			var amount = td_final.children("input").val();
			if (amount != ""){
				sum_before = sum_before + parseInt(amount);
			}
		}
	}
	
    for (var i=1; i <= rowCount; i++) { 
        td1 = $('#fuel_tbl tr:visible:eq('+ i +')').find('td').eq(0).children('label').text(); 
    	$('#fuel_tbl tr:visible:eq('+ i +')').find('td').eq(0).children('span').children('select').data("kendoDropDownList").value(td1.trim());
    	
    	loc_id = $('#fuel_tbl tr:eq('+ i +')').find('td').eq(0).children("span").children("select").attr("id");
    	loc_choosen = $("#" + loc_id + " option:selected").text();
    	loc_choosen_val = $('#fuel_tbl tr:eq('+ i +')').find('td').eq(0).children("span").children("select").val();
    	
    	if(loc_choosen == after_fuel_location){
    		$('#fuel_tbl tr:visible:eq('+ i +')').find('td').eq(1).children("label").text(sum_amount);
    		$('#fuel_tbl tr:visible:eq('+ i +')').find('td').eq(1).children("input").val(sum_amount);
    	}

    	if(loc_choosen_val == before_fuel_location){ 
    		$('#fuel_tbl tr:visible:eq('+ i +')').find('td').eq(1).children("label").text(sum_before);
    		$('#fuel_tbl tr:visible:eq('+ i +')').find('td').eq(1).children("input").val(sum_before);
    	}
    };
}

//Validate 
function check_location(){
	var rowCount_fuel = $('#fuel_tbl tr:gt(0)').length;
	var check = true;
	for ( var j = 1; j <= rowCount_fuel; j++) {
		val = $('#fuel_tbl tr:visible:eq('+ j +')').find('td').eq(0).children("span").children("select").val();
		if(val == ""){
			check = false;
			break;
		}
	}
	return check;
}


function change_location_del(){
	var rowCount = $('#fuel_tbl tr:visible:gt(0)').length; 
	before_fuel_location = $('#result').val();
	var rowCount_leg = $('#rs_flight_log_form tr:gt(0)').length-1; 
	var sum_amount = 0;
	
	for ( var j = 2; j <= rowCount_leg; j++) {
		td_final = $('#rs_flight_log_form tr:eq('+ j +')').find('td').eq(13);
		var loc_label = td_final.children('label').text();
		if (loc_label.trim() == before_fuel_location.trim()){
			var amount = td_final.children("input").val();
			if (amount != ""){
				sum_amount = sum_amount + parseInt(amount);
			}
		}
	}
	
    for (var i=1; i <= rowCount; i++) { 
        td1 = $('#fuel_tbl tr:visible:eq('+ i +')').find('td').eq(0).children('label').text(); 
    	$('#fuel_tbl tr:visible:eq('+ i +')').find('td').eq(0).children('span').children('select').data("kendoDropDownList").value(td1.trim());
    	
    	loc_id = $('#fuel_tbl tr:eq('+ i +')').find('td').eq(0).children("span").children("select").attr("id");
    	loc_choosen = $("#" + loc_id + " option:selected").text();
    	
    	if(loc_choosen == before_fuel_location){
    		$('#fuel_tbl tr:visible:eq('+ i +')').find('td').eq(1).children("label").text(sum_amount);
    		$('#fuel_tbl tr:visible:eq('+ i +')').find('td').eq(1).children("input").val(sum_amount);
    	}
    };
}

