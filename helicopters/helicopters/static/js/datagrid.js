var pilots = new Array();

var pilot_list = new Array();

jQuery().ready(function($) {
	
	var combo = document.getElementById("test");
	
	if (combo != null){
		for (i = 0; i < combo.options.length; i++) {
			pilots[i] = {empid:combo.options[i].value, name:combo.options[i].text}
		}
	}
	
    var table = $("#temp");

    table.find('tr').each(function (i) {
        var $tds = $(this).find('td'),
            pilot = $tds.eq(0).text().trim(),
            pic = $tds.eq(1).text().trim(),
            sic = $tds.eq(2).text().trim(),
            day = $tds.eq(3).text().trim(),
            night = $tds.eq(4).text().trim(),
        	ifr = $tds.eq(5).text().trim(),
        	nvg = $tds.eq(6).text().trim(),
        	longin = $tds.eq(7).text().trim(),
        	id = $tds.eq(8).text().trim();
        	
        pilot_list[i] = {a:1, pilot:pilot,pic:pic, sic: sic, day:day, night:night, ifr:ifr, nvg:nvg, longin: longin, id:id};
    });

});
	
$(function() {
	if ($('#id_is_submited').length) {
		var is_sub = document.getElementById('id_is_submited').value
	}
	
	if (is_sub == "True"){
		jQuery('#tt').datagrid(
				{
					data: pilot_list,
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
								hidden: true
							},
							{
								field : 'id',
								title : 'id',
								width : 0,
								align : 'left',
								editor : 'numberbox',
								hidden: true
							},
							{
								field : 'pilot',
								title : 'PILOT',
								width : 300,
								align : 'left',
								formatter : function(value) {
									
									for ( var i = 0; i < pilots.length; i++) {
										if (pilots[i].empid == value)
											return pilots[i].name;
									}
									return value;
								}, 
								editor : {
									type : 'combobox',
									options : {
										valueField : 'empid',
										textField : 'name',
										data : pilots, 
										required : true,
										autocomplete:'on'
									}
								}
							},
							{
								field : 'pic',
								title : 'PIC',
								width : 150,
								align : 'left',
								editor : 'numberbox'
							},
							{
								field : 'sic',
								title : 'SIC',
								width : 125,
								align : 'left',
								editor : 'numberbox'
							},
							{
								field : 'day',
								title : 'DAY',
								width : 120,
								align : 'left',
								editor : 'numberbox'
							},

							{
								field : 'night',
								title : 'NIGHT',
								width : 120,
								align : 'left',
								editor : 'numberbox'
							},

							{
								field : 'ifr',
								title : 'IFR',
								width : 120,
								align : 'left',
								editor : 'numberbox'
							},
							{
								field : 'nvg',
								title : 'NVG',
								width : 120,
								align : 'left',
								editor : 'numberbox'
							},
							{
								field : 'longin',
								title : 'LONG IN',
								width : 130,
								align : 'left',
								editor : 'numberbox'
							} 
							] ],
							 	
					onBeforeEdit : function(index, row) {
						row.editing = true;
						updateActions(index);
					},
					onAfterEdit : function(index, row) {
						row.editing = false;
						updateActions(index);
					},
					onCancelEdit : function(index, row) {
						row.editing = false;
						updateActions(index);
					}
				});
	}else{
		var hcc = pilots.length > 5 ? 110: 28 * pilots.length;
		jQuery('#tt').datagrid(
				
				{
					data: pilot_list,
					iconCls : 'icon-edit',
					width : '100%',
					height : "auto",
					fitColumns : true,
					striped : true,
					nowrap : false,
					singleSelect : true,
					idField : 'item1id',
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
								hidden: true
							},
							{
								field : 'id',
								title : 'id',
								width : 0,
								align : 'left',
								editor : 'numberbox',
								hidden: true
							},
							{
								field : 'pilot',
								title : 'PILOT',
								width : 195,
								align : 'left',
								formatter : function(value) {
									
									for ( var i = 0; i < pilots.length; i++) {
										if (pilots[i].empid == value)
											return "<span title='"+pilots[i].name+"'>" +pilots[i].name+"</span>";
									}
									return value;
								}, 
								editor : {
									type : 'combobox',
									options : {
										valueField : 'empid',
										textField : 'name',
										data : pilots, 
										required : true,
										panelHeight:hcc,
										formatter : function(value) {
											return "<span title='"+value.name+"'>" +value.name+"</span>"
										}
									}
								}
							},
							{
								field : 'pic',
								title : 'PIC',
								width : 100,
								align : 'left',
								editor : {type: 'numberbox', options: {precision: 2}}
							},
							{
								field : 'sic',
								title : 'SIC',
								width : 100,
								align : 'left',
								editor : {type: 'numberbox', options: {precision: 2}}
							},
							{
								field : 'day',
								title : 'DAY',
								width : 100,
								align : 'left',
								editor : {type: 'numberbox', options: {precision: 2}}
							},

							{
								field : 'night',
								title : 'NIGHT',
								width : 100,
								align : 'left',
								editor : {type: 'numberbox', options: {precision: 2}}
							},

							{
								field : 'ifr',
								title : 'IFR',
								width : 100,
								align : 'left',
								editor : {type: 'numberbox', options: {precision: 2}}
							},
							{
								field : 'nvg',
								title : 'NVG',
								width : 100,
								align : 'left',
								editor : {type: 'numberbox', options: {precision: 2}}
							},
							{
								field : 'longin',
								title : 'LONG IN',
								width : 100,
								align : 'left',
								editor : {type: 'numberbox', options: {precision: 2}}
							},
							{
								field : 'action',
								title : 'ACTION',
								width : 180,
								align : 'center',
								formatter : function(value, row, index) {
									var rows = jQuery('#tt').datagrid('getRows').length;
									if (row.editing) {
										var s = '<a href="javascript:void(0)" onclick="saverow(this)" style="margin-right:10px"><img src="../static/media/save.png" /></a> ';
										var c = '<a href="javascript:void(0)" onclick="refresh(this)" style="margin-right:10px"><img src="../static/media/btn_reset.png" /></a>';
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
									} 
									else {
										var e = '<a href="javascript:void(0)" onclick="editrow(this)" style="margin-right:10px"><img src="../static/media/edit.png" /></a> ';
										var d = '<a href="javascript:void(0)" onclick="deleterow(this)" style="margin-right:10px"><img src="../static/media/delete.png" /></a>';
										
										if (rows-1 == index) {
											var f = '<a href="javascript:void(0)" onclick="insert(this)" style="margin-right:6px"> <img src="../static/media/add3.png" /></a>';
											if(rows-2==index){
												var f = '<a href="javascript:void(0)" style="margin-right:10px; visibility: hidden"><img src="../static/media/btn_reset.png" /></a>';
											}
										} else {
											if(rows-2==index){
												var isSave=false;
												if(rows!=0){
													for (var i=0;i<rows;i++) {
														isSave=$('#tt').datagrid('getRows')[i].editing
														if(isSave){
															break;
														}
													}
												}
												if(!isSave){
													var f='<a href="javascript:void(0)" style="margin-right:10px; visibility: hidden"><img src="../static/media/btn_reset.png" /></a>';
												}else{
													var f = '<a href="javascript:void(0)" style="margin-right:6px"> <img src="../static/media/add.png" /></a>';
												}
											}else{
												var f ='<a href="javascript:void(0)" style="margin-right:10px; visibility: hidden"><img src="../static/media/btn_reset.png" /></a>';
											}
										
										}
										
										return e + d + f;
									}
								}
							}, 
							
							] ],
							 	
					onBeforeEdit : function(index, row) {
						row.editing = true;
						updateActions(index);
					},
					onAfterEdit : function(index, row) {
						row.editing = false;
						updateActions(index);
					},
					onCancelEdit : function(index, row) {
						row.editing = false;
						updateActions(index);
					}
				});
	}
	
});
function updateActions(index) {
	jQuery('#tt').datagrid('updateRow', {
		index : index,
		row : {}
	});
}
function getRowIndex(target) {
	var tr = $(target).closest('tr.datagrid-row');
	return parseInt(tr.attr('datagrid-row-index'));
}
function editrow(target) {
	
	var length = $('#tt').datagrid('getRows').length;
	var isSave=false;
	if(length!=0){
		for (var i=0;i<length;i++) {
			isSave=$('#tt').datagrid('getRows')[i].editing
			if(isSave){
				break;
			}
		}
	}
	if(isSave){
		alert('Some row is not saved, you have to save it before!!');
	}else{
		
		$('#tt').datagrid('beginEdit', getRowIndex(target));
		$(".datagrid-editable-input").attr("maxlength","40");
		$(".datagrid-editable-input.numberbox-f.validatebox-text").attr("maxlength","9");
	}
	
	
}
function deleterow(target) {
	var ind = getRowIndex(target);
	var rows = $('#tt').datagrid('getRows').length;
	r = confirm('Are you sure to delete this record?');
	
	if (r) {
		$('#tt').datagrid('deleteRow', getRowIndex(target));
		deleteForm_pilot(ind);
		if(rows == 1){
			insert();
		}
		if(rows!= 0){
			for (var i = 0; i < rows-1; i++){
					$('#tt').datagrid('beginEdit', i);
					$('#tt').datagrid('endEdit', i);
			}
		}
	}
}

function saverow(target) {
	var ind = getRowIndex(target);
	var rows = $('#tt').datagrid('getRows').length;
	
	var pi = $('#tt').datagrid('getEditor', {index:getRowIndex(target),field:'pilot'});
	var pic = $('#tt').datagrid('getEditor', {index:getRowIndex(target),field:'pic'});
	var sic = $('#tt').datagrid('getEditor', {index:getRowIndex(target),field:'sic'});
	var day = $('#tt').datagrid('getEditor', {index:getRowIndex(target),field:'day'});
	var night = $('#tt').datagrid('getEditor', {index:getRowIndex(target),field:'night'});
	var ifr = $('#tt').datagrid('getEditor', {index:getRowIndex(target),field:'ifr'});
	var nvg = $('#tt').datagrid('getEditor', {index:getRowIndex(target),field:'nvg'});
	var longin = $('#tt').datagrid('getEditor', {index:getRowIndex(target),field:'longin'});
	
	var pi_val = $(pi.target).combobox('getValue');
	var combo = document.getElementById("test");
	var test = false;
	
	for (i = 0; i < combo.options.length; i++) {
		
		if (pi_val == combo.options[i].value){
			test = true;
			break;
		} 
	}
	if (test){
		var ed = $('#tt').datagrid('getEditor', {index:getRowIndex(target),field:'a'});
		$(ed.target).numberbox('setValue', 1);
		
		var pic_val = $(pic.target).numberbox('getValue');
		var id_pic = '#id_pilots-' + ind + '-pic';
		$(id_pic).val(pic_val);
		
		var sic_val = $(sic.target).numberbox('getValue');
		var id_sic = '#id_pilots-' + ind + '-sic';
		$(id_sic).val(sic_val);
		
		var day_val = $(day.target).numberbox('getValue');
		var id_day = '#id_pilots-' + ind + '-day';
		$(id_day).val(day_val);
		
		var night_val = $(night.target).numberbox('getValue');
		var id_night = '#id_pilots-' + ind + '-night';
		$(id_night).val(night_val);
		
		var ifr_val = $(ifr.target).numberbox('getValue');
		var id_ifr = '#id_pilots-' + ind + '-ifr';
		$(id_ifr).val(ifr_val);
		
		var nvg_val = $(nvg.target).numberbox('getValue');
		var id_nvg = '#id_pilots-' + ind + '-nvg';
		$(id_nvg).val(nvg_val);
		
		var long_val = $(longin.target).numberbox('getValue');
		var id_long = '#id_pilots-' + ind + '-long_in';
		$(id_long).val(long_val);
		
		var id_employee = '#id_pilots-' + ind + '-employee';
		$(id_employee).val(pi_val);
		
		var id_f = '#id_pilots-' + ind + '-DELETE';
	  	$(id_f).prop('checked', false);
	  	
		$('#tt').datagrid('endEdit', getRowIndex(target));
		
	}else{
		alert('PILOT is required');
	}
	if(rows!= 0){
		for (var i = 0; i < rows; i++){
				$('#tt').datagrid('beginEdit', i);
				$('#tt').datagrid('endEdit', i);
		}
	}
	add_style();
}

function cancelrow(target) {
	$('#tt').datagrid('cancelEdit', getRowIndex(target));
}
//custom
function refresh(target) {
	/*var a = getRowIndex(target);*/
	var ed = $('#tt').datagrid('getEditor', {index:getRowIndex(target),field:'a'});
	var val = $(ed.target).numberbox('getValue');
	
	if (val == 0){
		$('#tt').datagrid('deleteRow', getRowIndex(target));
		insert();
	}else{
		$('#tt').datagrid('cancelEdit', getRowIndex(target));
	}
}

function insert(target) {
	addForm_pilot(this, 'pilots');
	var rows = $('#tt').datagrid('getRows').length;
	if (rows != 0) {
		var index = rows;
	} else {
		index = 0;
	}
	
	$('#tt').datagrid('insertRow', {
		index : index,
		row : {a : 0}
	});
	$('#tt').datagrid('selectRow', index);
	$('#tt').datagrid('beginEdit', index);
	if(rows!= 0){
		for (var i = 0; i < rows; i++){
				$('#tt').datagrid('beginEdit', i);
				$('#tt').datagrid('endEdit', i);
		}
	}
	$(".datagrid-editable-input").attr("maxlength","40");
	$(".datagrid-editable-input.numberbox-f.validatebox-text").attr("maxlength","9");
	add_style();
}	


var formCountTest1 = parseInt($('#id_' + 'pilots' + '-TOTAL_FORMS').val());
function updateElementIndex(el, prefix, ndx) {
  var id_regex = new RegExp('(' + prefix + '-\\d+-)');
  var replacement = prefix + '-' + ndx + '-';
  if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
  if (el.id) el.id = el.id.replace(id_regex, replacement);
  if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function addForm_pilot(btn, prefix) {
  var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());

  // You can only submit a maximum of 10 todo item1s 
  if (formCount < 10) {
    // Clone a form (without event handlers) from the first form
    var row = $(".item1:first").clone(false).get(0);
    // Insert it after the last form
    $(row).removeAttr('id').hide().insertAfter(".item1:last").slideDown(300);
    
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
    
    // Update the total form count
    $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1); 

  } // End if
  else {
  }
  return false;
}

function deleteForm_pilot(ind) 
{
	var formCountTest1 = parseInt($('#id_' + 'form' + '-TOTAL_FORMS').val());
	  for (var i=0;i<formCountTest1;i++)
	  {
		if (i == ind){
			var id_f = '#id_pilots-' + i + '-DELETE';
		  	$(id_f).prop('checked', true);
		  	break;
		}
	  } 
  return true;
}
