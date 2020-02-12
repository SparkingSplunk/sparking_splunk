

export default class ShortCuts {

	constructor(key_functions) {
		// Mac command is not considered a modifier key, we must keep track
		document.addEventListener('keydown', function(event) {
			if (event.keyCode == 91 || event.keyCode == 93) // Mac Command key, Chrome/Safari: 91 and 93, Firefox: 224, Opera: 17
				window.commandKey = true;
		});
		document.addEventListener('keyup', function(event) {
			if (event.keyCode == 91 || event.keyCode == 93) // Mac Command key, Chrome/Safari: 91 and 93, Firefox: 224, Opera: 17
				window.commandKey = false;
		});
		for (let i = 0; i < key_functions.length; i++) {
			document.addEventListener('keydown', function(event) {
				if((window.commandKey || event.ctrlKey)) {
					if (event.keyCode == key_functions[i].keyCode) {
						event.preventDefault();
						key_functions[i].callback();
					}
				}
			});
		}
	}
}

new ShortCuts([{
	keyCode : 69, // E
	callback : function() { // Edit HTML
		window.location = window.origin +
		'/manager/ADSP/data/ui/views/' +
		window.location.pathname.split("/").pop() +
		'?action=edit&ns=ADSP&redirect_override=' +
		encodeURIComponent(window.location.pathname)}
	}, {
	keyCode: 82, // R
	callback: function() {doBump()},
}]);

function doBump() {
	try {
		require(["jquery"], function($) {
			$.ajax({
				url: '/en-US/_bump',
				type: 'GET',
				async: false,
				success: function(returneddata) {
					let baseBump = returneddata;
					let postValue = $(baseBump).find("input[type=hidden]").val();
					console.log("Initial Bump Page", returneddata);
					$.ajax({
						url: '/en-US/_bump',
						type: 'POST',
						data: "splunk_form_key=" + postValue,
						async: false,
						success: function(returneddata) {
							console.log("Bumped!", returneddata);
							setTimeout(()=>{location.reload()},100);
						},
						error: function(xhr, textStatus, error) {
							location.reload();
						}
					});
				},
				error: function(xhr, textStatus, error) {
					location.reload();
				}
			});
		});
	} catch (e) {
		location.reload();
	}
}

