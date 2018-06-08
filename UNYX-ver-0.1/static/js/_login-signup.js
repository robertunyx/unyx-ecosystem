$(document).ready(function() {

	// LOGIN

	$('#login').on('submit', function(event) {
		$.ajax({
			data : {
				username : $('#username').val(),
				password : $('#password').val()
			},
			type : 'POST',
			url : '/login'
		}).done(function(data) {
			console.log(data.error);
			if (data.error) {
				x = data.error;
				$('#testbox2').append('<p>' + x + '</p>');
			};

		});

		$('#username').val('');
		$('#password').val('');
		event.preventDefault();
	});

	// REGISTER

	$('#register').on('submit', function(event) {
		$.ajax({
			data : {
				first_name : $('#first_name').val(),
				last_name : $('#last_name').val(),
				r_username : $('#r_username').val(),
				r_password : $('#r_password').val()
			},
			type : 'POST',
			url : '/register'
		}).done(function(data) {
			console.log(data);
			console.log(data.error);
			if (data.error) {
				console.log(data.error);
				x = data.error;
				$('#testbox').append('<p>' + x + '</p>');
			};
		});

		$('#r_username').val('');
		$('#r_password').val('');
		event.preventDefault();
	});


	// LOG OUT

	$('#logout').on('click', function(event) {
		$.ajax({
			type : 'GET',
			url : '/logout',
			success: function(data) {
				console.log("Checking logout process complete.");
				if (data.success) {
					console.log(data.success);
					console.log("User successfully logged out.");
					y = data.success;
					$('#testbox2').append('<p>' + y + '</p>');
					$('#menu_login').show();
					$('#signup_area').show();
					$('#logout').remove();
					$('#logged_message').remove();
				} else {
					console.log(data.error);
					console.log("Logout failed.");
					x = data.error;
					$('#testbox2').append('<p>' + x + '</p>');
				};
			}
		});
		event.preventDefault();
	});


});