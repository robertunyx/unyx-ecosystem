$(document).ready(function() {

	console.log("Inside authenticate.js file...");
// IF LOGGED IN
	$.ajax({
		type: "GET",
		url: "/checklogin",
		success: function(data) {
			console.log("Checking login process complete.")
			if (data.success) {
				console.log(data.success);
				$('#menu_login').hide();
				$('#signup_area').hide();
				$('.menu').append("<p id='logged_message'>Logged in as username.</p>");
				$('.menu').append("<form><button id='logout' type='submit'>log out</button></form>");
			} else {
				console.log(data.error);
				console.log("Not logged in.");
			};
		}
	});


});