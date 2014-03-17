$(document).ready(function() {
	/*$('select').addClass('easyui-combobox');*/
	$(document).on('click', '.cc_line, .bcc_line', function(){
		var show = 'show_' + jQuery(this).attr('class');
		jQuery(this).css('display', 'none');
		jQuery('.' + show).css('display', 'block');
	});
	$(document).on('click', '.cc, .bcc', function(){
		var hide = 'show_' + jQuery(this).attr('class') + '_line';
		var show =  jQuery(this).attr('class') + '_line';
		jQuery('.' + hide).css('display', 'none');
		jQuery('.' + hide + ' .m_email').val('');
		jQuery('.' + show).css('display', 'block');
	});
	
	$(document).on('click', '.close-attack', function(){
		var parent = jQuery(this).parent().remove();
		var valu = '';
		jQuery('input.attack_file').each( function(){
			v = jQuery(this).val().replace('flight_log_','');
			valu = valu + ',' + v.replace('.pdf','');
		});		
		valu = valu.substring(1);
		jQuery('.hiden_attack').val(valu);
	});
	
  jQuery("form#register input, form#login input").each(function(){
		var input = jQuery(this);
		input.on('focus', function(){
			if(input.val() == '' || input.val() == 'This is requied field' || input.val() == 'Not a valid e-mail address'
				 || input.val() == 'Employee Number is incorrrect.' || input.val() == 'Password is incorrect.' 
				 || input.val().indexOf('is required.') > 0	) {
				input.val('');
				input.css('color','#000');
			}
			var e_id = 'over_' + input.attr('id');
			jQuery('#' + e_id).css('display','none');
			jQuery('.error_id_mess').html('');
		})
		.on('blur', function(){
			if(input.val() == '' || input.val() == 'This is requied field' || input.val() == 'Not a valid e-mail address'|| input.val().indexOf('is required.') > 0	) {
				input.val('');
				input.css('color','#000');
				var e_id = 'over_' + input.attr('id');
				if(jQuery('#' + e_id).html() == 'Password is required.') {
					jQuery('#' + e_id).html('Password');
					jQuery('#' + e_id).css('color','#666');
					jQuery('#' + e_id).css('font-weight','normal');
				}
				if(jQuery('#' + e_id).html() == 'Confirm Password is required.') {
					jQuery('#' + e_id).html('Confirm Password');
					jQuery('#' + e_id).css('color','#666');
					jQuery('#' + e_id).css('font-weight','normal');
				}
				jQuery('#' + e_id).css('display','block');
			}						
		});
		if(input.val() != '' && input.val() != 'This is requied field'	) {
			var e_id = 'over_' + input.attr('id');
			jQuery('#' + e_id).css('display','none');
			ret =false;
		}
		jQuery('.error_id_mess').click(function() {
			jQuery('.error_id_mess').html('');
		});		
	});
  	
	jQuery('.error_id_mess').each(function(){
		var err = jQuery(this);
		if (err.children().length > 0) {
			var id = '#id_'+ err.attr('id');
			jQuery(id).val('');
		}
	});
	$(document).on('click', '.jqte_editor', function(){
		var jqte_editor = jQuery('.jqte_editor');
		if(jqte_editor.html() == '' || jqte_editor.html() == 'This is required field' || jqte_editor.html() == 'Not a valid e-mail address') {
			jqte_editor.html('');
			jqte_editor.css('color','#000');
		}
		jqte_editor.on('focus', function(){
			if(jqte_editor.html() == '' || jqte_editor.html() == 'This is required field' || jqte_editor.html() == 'Not a valid e-mail address') {
				jqte_editor.html('');
				jqte_editor.css('color','#000');
			}
		})
		.on('blur', function(){
			if(jqte_editor.html() == '' || jqte_editor.html() == 'This is required field' || jqte_editor.html() == 'Not a valid e-mail address') {
				jqte_editor.html('');
				jqte_editor.css('color','#000');
			}						
		});
	});
	$(document).on('click mousedown','form#login #over_id_employee_number,form#login .icon_hiden_en', function() {
		//jQuery(this).css('display', 'none');
		jQuery('#id_employee_number').focus();
		//jQuery('#over_id_password).css('display','block');
	});
	$(document).on('click mousedown','form#login #over_id_password,form#login .icon_hiden_pass', function() {
		//jQuery(this).css('display', 'none');
		jQuery('#id_password').focus();
		//jQuery('#over_id_employee_number).css('display','block');
	});
	
	
	jQuery("form#login input").each(function(){
		var input = jQuery(this);
		if(input.val() != '') {
			var id = 'over_' + input.attr('id');
			jQuery('#' + id).css('display', 'none');
		}
		input.on('focus', function(){
				if (input.attr('id') == "id_password" && input.is(':text'))
					input.attr('type', 'password');
				if(input.val() == '' || input.val() == 'This is requied field' 
						|| input.val() == 'Employee Number is incorrrect.' || input.val() == 'Password is incorrect.') {
					input.val('');
					input.css('color','#000');
				}
				var e_id = 'over_' + input.attr('id');
				jQuery('#' + e_id).css('display','none');
			})
			.on('blur', function(){
				// remove error span
				$(".login-err").remove();
				if(input.val() == '' || input.val() == 'This is requied field' ) {
					input.val('');
					input.css('color','#000');
					var e_id = 'over_' + input.attr('id');
					jQuery('#' + e_id).css('display','block');
				}						
			});
	});
});
