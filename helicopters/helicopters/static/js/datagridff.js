var loc = new Array();

var loc_list = new Array();

jQuery().ready(function myfunc() {
	call();
});

function call() {
	var combo = document.getElementById("hiddenff");

	if (combo != null) {
		for (i = 0; i < combo.options.length; i++) {
			loc[i] = {
				locid : combo.options[i].value,
				name : combo.options[i].text
			}
		}
	}

	var table = $("#rs_fuel_expenses_or_usage_form");

	table.find('tr').each(function(i) {
		var $tds = $(this).find('td'), location = $tds.eq(0)
				.text().trim(), gallon = $tds.eq(1).text()
				.trim(), owner = $tds.eq(2).text().trim(), amount = $tds
				.eq(3).text().trim(), pk = $tds.eq(4).text()
				.trim();
		loc_list[i] = {
			a : 1,
			location : location,
			gallon : gallon,
			owner : owner,
			amount : amount,
			id : pk
		};
	});
}

$(function() {
	callgrid();
	if ($('#id_is_submited').length) {
		var is_sub = document.getElementById('id_is_submited').value
		if (is_sub == "True") {
			reset_style();
		}
	}	
});

window.onload = function() {
	var w = $("#div_fuel_cal").width();
	$('#ff').datagrid('resize', {
		width : w,
		height : 'auto'
	});
	$('#tt').datagrid('resize', {
		width : w,
		height : 'auto'
	});
	
	$('.datagrid-header-row td[field=action]').attr('style','border-right: none !important');
	$('.datagrid-row td[field=action]').attr('style','border-right: none !important');
}

$(window).resize(function() {
	var tab_w = $("#div_fuel_cal").width();
	$('#ff').datagrid('resize', {
		width : tab_w,
		height : 'auto'
	});
	$('#tt').datagrid('resize', {
		width : tab_w,
		height : 'auto'
	});

});

function callgrid() {
	if ($('#id_is_submited').length) {
		var is_sub = document.getElementById('id_is_submited').value
	}
	if (is_sub == "True") {
		jQuery('#ff').datagrid(
						{
							data : loc_list,
							iconCls : 'icon-edit',
							width : '100%',
							fitColumns : true,
							striped : true,
							nowrap : false,
							height : "auto",
							singleSelect : true,
							scrollbarSize: -1,
							freezeRow: true,
							scrollTo: true,

							columns : [ [
									{
										field : 'a',
										title : 'a',
										width : 0,
										align : 'left',
										editor : 'numberbox',
										hidden : true
									},
									{
										field : 'id',
										title : 'id',
										width : 0,
										align : 'left',
										editor : 'numberbox',
										hidden : true
									},
									{
										field : 'location',
										title : 'LOCATIONS',
										width : 300,
										align : 'left',
										formatter : function(value) {

											for ( var i = 0; i < loc.length; i++) {
												if (loc[i].locid == value)
													return loc[i].name;
											}
											return value;
										},
										editor : {
											type : 'combobox',
											options : {
												valueField : 'name',
												textField : 'name',
												data : loc,
											}
										}
									},
									{
										field : 'gallon',
										title : 'GALLONS',
										width : 270,
										align : 'left',
										editor : {
											type : 'numberbox'
										}
									},
									{
										field : 'owner',
										title : 'OWNER',
										width : 270,
										align : 'left',
										editor : {
											type : 'text'
										}
									},
									{
										field : 'amount',
										title : 'AMOUNT',
										width : 271,
										align : 'left',
										editor : 'text'
									}
							] ],

							onBeforeEdit : function(index, row) {
								row.editing = true;
								updateActionsff(index);
							},
							onAfterEdit : function(index, row) {
								row.editing = false;
								updateActionsff(index);
							},
							onCancelEdit : function(index, row) {
								row.editing = false;
								updateActionsff(index);
							}
						});
	} else {
		jQuery('#ff').datagrid({
							data : loc_list,
							iconCls : 'icon-edit',
							width : '100%',
							fitColumns : true,
							height : "auto",
							singleSelect : true,
							scrollbarSize: -1,
							freezeRow: true,
							scrollTo: true,

							columns : [ [
									{
										field : 'a',
										title : 'a',
										width : 0,
										align : 'left',
										editor : 'numberbox',
										hidden : true
									},
									{
										field : 'id',
										title : 'id',
										width : 0,
										align : 'left',
										editor : 'numberbox',
										hidden : true
									},
									{
										field : 'location',
										title : 'LOCATIONS',
										resizable: false,
										width : 215,
										align : 'left',
										formatter : function(value) {

											for ( var i = 0; i < loc.length; i++) {
												if (loc[i].locid == value)
													return "<span title='"+loc[i].name+"'>" +loc[i].name+"</span>";
											}
											return value;
										},
										editor : {
											type : 'combobox',
											options : {
												valueField : 'name',
												textField : 'name',
												data : loc,
												editable : false,
												onLoadSuccess: function(data){  
										            orgCount = data.length;  
										        },  
										        onShowPanel: function() {  
										            if (orgCount >=5) {  
										                $(this).combobox('panel').height(20);  
										            }else{
										            	 $(this).combobox('panel').height(orgCount*27);  
										            }
										            if(orgCount==0){
										            	$('.combo-panel:last').attr('style','border: none !important');
										            }else{
										            	$('.combo-panel:last').attr('style','border: 1px solid #898989 !important');
										            }
										        }, 
												formatter : function(value) {
													return "<span title='"+value.name+"'>" +value.name+"</span>"
												},
												resizable: false
											}
										}
									},
									{
										field : 'gallon',
										title : 'GALLONS',
										resizable: false,
										width : 215,
										align : 'left',
										editor : {type: 'numberbox', options: {precision: 2}}
									},
									{
										field : 'owner',
										title : 'OWNER',
										resizable: false,
										width : 215,
										align : 'left',
										editor : {
											type : 'text'
										}
									},
									{
										field : 'amount',
										title : 'AMOUNT',
										resizable: false,
										width : 215,
										align : 'left',
										editor : {
											type : 'text'
										}
									},

									{
										field : 'action',
										title : 'ACTION',
										resizable: false,
										width : 300,
										align : 'center',
										formatter : function(value, row, index) {
											var rows = jQuery('#ff').datagrid('getRows').length;
											if (row.editing) {
												var s = '<a href="javascript:void(0)" onclick="saverowff(this)" style="margin-right:10px"><img src="../static/media/save.png" /></a> ';
												var c = '<a href="javascript:void(0)" onclick="refreshff(this)" style="margin-right:10px"><img src="../static/media/btn_reset.png" /></a>';
												var sc = '<script type="text/javascript">\
													$(document).ready(function(){\
														$(".datagrid-editable-input").attr("maxlength","40");\
														$(".datagrid-editable-input.numberbox-f.validatebox-text").attr("maxlength","9");\
													})\
												;</script>';
												if (rows == 1){
													var an = '<a href="javascript:void(0)" style="margin-right:10px; display: none"><img src="../static/media/btn_reset.png" /></a>';
												}else{
													var an = '<a href="javascript:void(0)" style="margin-right:10px; visibility: hidden"><img src="../static/media/btn_reset.png" /></a>';
												}
												return s + c + sc + an;
											} else {
												var e = '<a href="javascript:void(0)" onclick="editrowff(this)" style="margin-right:10px"><img src="../static/media/edit.png" /></a> ';
												var d = '<a href="javascript:void(0)" onclick="deleterowff(this)" style="margin-right:10px"><img src="../static/media/delete.png" /></a>';
												
												if (rows-1 == index) {
													var f = '<a href="javascript:void(0)" onclick="insertff(this)" style="margin-right:6px"> <img src="../static/media/add3.png" /></a>';
												} else {
													if(rows-2==index){
														var isSave=false;
														if(rows!=0){
															for (var i=0;i<rows;i++) {
																isSave=$('#ff').datagrid('getRows')[i].editing;
																if(isSave){
																	break;
																}
															}
														}
														if(!isSave){
															var f = '<a href="javascript:void(0)" style="margin-right:10px; visibility: hidden"><img src="../static/media/btn_reset.png" /></a>';
														}else{
															var f = '<a href="javascript:void(0)" onclick="" style="margin-right:10px"> <img src="../static/media/add.png" /></a>';
														}
													}else{
														var f = '<a href="javascript:void(0)" style="margin-right:10px; visibility: hidden"><img src="../static/media/btn_reset.png" /></a>';
													}
												
												}
												return e + d + f;
											}
										}
									},

							] ],

							onBeforeEdit : function(index, row) {
								row.editing = true;
								updateActionsff(index);
							},
							onAfterEdit : function(index, row) {
								row.editing = false;
								updateActionsff(index);
							},
							onCancelEdit : function(index, row) {
								row.editing = false;
								updateActionsff(index);
							}
						});
	}
}

function updateActionsff(index) {
	jQuery('#ff').datagrid('updateRow', {
		index : index,
		row : {}
	});
}
function getRowIndexff(target) {
	var tr = $(target).closest('tr.datagrid-row');
	return parseInt(tr.attr('datagrid-row-index'));
}
function editrowff(target) {
	var ind = getRowIndex(target);
	var length = $('#ff').datagrid('getRows').length;
	var isSave = false;
	if (length != 0) {
		for ( var i = 0; i < length; i++) {
			if($('#ff').datagrid('getRows')[i].editing){
				isSave = $('#ff').datagrid('getRows')[i].editing;
			}
			if (isSave) {
				break;
			}
		}
	}
	if (isSave) {
		alert('Some row is not saved, you have to save it before!!');
	} else {
		$('#ff').datagrid('beginEdit', ind);
		fill_data_combo();
		$(".datagrid-editable-input").attr("maxlength", "40");
		$(".datagrid-editable-input.numberbox-f.validatebox-text").attr(
				"maxlength", "9");
		add_style();
	}

}
function deleterowff(target) {
	var ind = getRowIndex(target);
	var rows = $('#ff').datagrid('getRows').length;
	r = confirm('Are you sure to delete this record?');

	if (r) {
		$('#ff').datagrid('deleteRow', getRowIndex(target));
		deleteForm(ind);
		if (rows == 1) {
			insertff();
		}
		if (rows != 0) {
			for ( var i = 0; i < rows - 1; i++) {
				$('#ff').datagrid('beginEdit', i);
				$('#ff').datagrid('endEdit', i);
			}
		}
	}
	add_style();
}

function saverowff(target) {
	
	var ind = getRowIndex(target);
	var rows = $('#ff').datagrid('getRows').length;
	var loc = $('#ff').datagrid('getEditor', {
		index : getRowIndex(target),
		field : 'location'
	});
	var loc_val = $(loc.target).combobox('getValue');

	var ga = $('#ff').datagrid('getEditor', {
		index : getRowIndex(target),
		field : 'gallon'
	});
	var ga_val = $(ga.target).numberbox('getValue');

	var owner = $('#ff').datagrid('getEditor', {
		index : getRowIndex(target),
		field : 'owner'
	});
	var owner_val = $(owner.target).text('getValue').val();

	var amount = $('#ff').datagrid('getEditor', {
		index : getRowIndex(target),
		field : 'amount'
	});
	var amount_val = $(amount.target).text('getValue').val();

	if ((loc_val != "") || (ga_val != "") || (owner_val != "")
			|| (amount_val != "")) {
		var ed = $('#ff').datagrid('getEditor', {
			index : getRowIndex(target),
			field : 'a'
		});
		$(ed.target).numberbox('setValue', 1);
		$('#ff').datagrid('endEdit', getRowIndex(target));
		
		set_val_form(ind, ga_val, owner_val, amount_val, loc_val);
		var id_f = '#id_form-' + ind + '-DELETE';
	  	$(id_f).prop('checked', false);
		if(rows!= 0){
			for (var i = 0; i < rows; i++){
					$('#ff').datagrid('beginEdit', i);
					$('#ff').datagrid('endEdit', i);
			}
		}
	} else {
		alert("There is no information to save. Please enter information.");
	}
	add_style();
}

function cancelrowff(target) {
	$('#ff').datagrid('cancelEdit', getRowIndexff(target));
}
// custom
function refreshff(target) {
	var ed = $('#ff').datagrid('getEditor', {
		index : getRowIndexff(target),
		field : 'a'
	});
	var val = $(ed.target).numberbox('getValue');

	if (val == 0) {
		$('#ff').datagrid('deleteRow', getRowIndexff(target));
		insertff();
	} else {
		$('#ff').datagrid('cancelEdit', getRowIndexff(target));
	}
}

function insertff(target) {
	addForm(this, 'form');
	var rows = $('#ff').datagrid('getRows').length;
	if (rows != 0) {
		var index = rows;
	} else {
		index = 0;
	}
	$('#ff').datagrid('insertRow', {
		index : index,
		row : {
			a : 0
		}
	});
	$('#ff').datagrid('selectRow', index);
	$('#ff').datagrid('beginEdit', index);
	if (rows != 0) {
		for ( var i = 0; i < rows; i++) {
			$('#ff').datagrid('beginEdit', i);
			$('#ff').datagrid('endEdit', i);
		}
	}
	$(".datagrid-editable-input").attr("maxlength", "40");
	$(".datagrid-editable-input.numberbox-f.validatebox-text").attr(
			"maxlength", "9");
	add_style();
	fill_data_combo();
}


function fill_data_combo() {
	var loc = new Array();

	var combo = document.getElementById("hiddenff");

	if (combo != null) {
		for (i = 0; i < combo.options.length; i++) {
			loc[i] = {
				locid : combo.options[i].value,
				name : combo.options[i].text
			}
		}
	}
/*	if(loc.length == 0){
		$('.combo-panel:last').attr('style','border: none !important');
	}*/
	var rows = $('#ff').datagrid('getRows').length;
	for ( var i = 0; i < rows; i++) {
		isSave = $('#ff').datagrid('getRows')[i].editing
		if (isSave) {
			$("#ff").datagrid('beginEdit', i)
			var ed = $("#ff").datagrid('getEditor', {
				index : i,
				field : 'location'
			});
			$(ed.target).combobox('loadData', loc);
		}
		
	}
}

function add_style(){
	$('.datagrid-header-row td[field=action]').attr('style','border-right: none !important');
	$('.datagrid-row td[field=action]').attr('style','border-right: none !important');
}
function reset_style(){
	$('.datagrid-header-row td[field=amount]').attr('style','border-right: none !important');
	$('.datagrid-row td[field=amount]').attr('style','border-right: none !important');
	$('.datagrid-header-row td[field=longin]').attr('style','border-right: none !important');
	$('.datagrid-row td[field=longin]').attr('style','border-right: none !important');
}


function set_val_form(ind, ga_val, owner_val, amount_val, loc_val){
	var id_ga = '#id_form-' + ind + '-gallons';
	$(id_ga).val(ga_val);
	
	var id_owner = '#id_form-' + ind + '-owner';
	$(id_owner).val(owner_val);
	
	var id_amount = '#id_form-' + ind + '-amount';
	$(id_amount).val(amount_val);
	
	var combo = document.getElementById("hiddenff");
	var loc_id = ""
	if (combo != null) {
		for (i = 0; i < combo.options.length; i++) {
			var id_location = '#id_form-' + ind + '-location_id';
			$(id_location).append(new Option(combo.options[i].text, combo.options[i].value));
			
			if(loc_val == combo.options[i].text){
				loc_id = combo.options[i].value;
			}
		}
	}
	
	var id_location = '#id_form-' + ind + '-location_id';
	$(id_location).val(loc_id);
	
}

var formCountTest = parseInt($('#id_' + 'form' + '-TOTAL_FORMS').val());
function updateElementIndex(el, prefix, ndx) {
  var id_regex = new RegExp('(' + prefix + '-\\d+-)');
  var replacement = prefix + '-' + ndx + '-';
  if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
  if (el.id) el.id = el.id.replace(id_regex, replacement);
  if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function addForm(btn, prefix) {
  var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());

  // You can only submit a maximum of 10 todo items 
  if (formCount < 10) {
    // Clone a form (without event handlers) from the first form
    var row = $(".item:first").clone(false).get(0);
    // Insert it after the last form
    $(row).removeAttr('id').hide().insertAfter(".item:last").slideDown(300);
    
    // Remove the bits we don't want in the new row/form
    // e.g. error messages
    $(".errorlist", row).remove();
    $(row).children().removeClass('error');
    
    // Relabel/rename all the relevant bits
    $(row).children().children().each(function() {
      updateElementIndex(this, prefix, formCount);
      if (this.type == 'hidden'){
      	this.removeAttribute("value")
      }
      
      if ( $(this).attr('type') == 'select-one' ){
      	 this.selectedIndex = 0
      }
      
      if ( $(this).attr('type') == 'text' )
        $(this).val('');
    });
    
    // Add an event handler for the delete item/form link 
    $(row).find('.delete').click(function() {
      return deleteForm(this, prefix);
    });

    // Update the total form count
    $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1); 

  } // End if
  else {
    alert("Sorry, you can only enter a maximum of ten items.");
  }
  return false;
}

function deleteForm(ind) 
{
	var formCountTest = parseInt($('#id_' + 'form' + '-TOTAL_FORMS').val());
	  for (var i=0;i<formCountTest;i++)
	  {
		if (i == ind){
			var id_f = '#id_form-' + i + '-DELETE';
		  	$(id_f).prop('checked', true);
		  	break;
		}
	  } 
  return true;
}




