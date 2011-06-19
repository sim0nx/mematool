$(document).ready(function(){
	
	// datepicker for profiles
	$('input[name="birthDate"], input[name="leavingDate"], input[name="arrivalDate"] ').datepicker({ 
		dateFormat: 'yy-mm-dd',
		changeMonth: true,
		changeYear: true,
		showButtonPanel: true,
		animation:"slideIn" 
	});	
	// end datepicker for profiles
	
	// profiles member delete dialog
	$('input[name="member-delete-confirm"]').dialog({
		resizable: false,
				height:140,
				modal: true,
				buttons: {
					"Remove this member": function() {
						$(location).attr('href','https://hackerspace.lu/mematool/member/delete');
					},
					Cancel: function() {
						$( this ).dialog( "close" );
					}
				}
	});
	// end  profiles member delete dialog
	
	// e-mail validation 
	$('input[name="mail"]').change(function(){
		alert('You changed the field');
	});
	
	// end email validation
});