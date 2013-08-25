$(document).ready(function(){
	
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
	
	// system message fade out
	// profile_save
	// login_success
	// logout
	// login_fail
	$('div#profile_save, div#login_success, div#logout, div#login_fail, div#flash,').fadeOut(4000);
});
