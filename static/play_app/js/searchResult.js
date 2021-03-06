var access_token = String(localStorage.getItem("accessToken"));
var playlist_array = [];
var playlist_title = "";
var playlist_visibility;
var user_id;

$(document).ready(function() {
	$.ajax({
		type: 'GET',
		beforeSend: function(xhr) {
			xhr.setRequestHeader("Authorization", "Bearer " + access_token);
		},
		url: 'https://api.spotify.com/v1/me',
		success: function(data) {
			console.log(data.id);
			user_id = data.id;
		},
		fail: function() {
			console.log("An error occurred while trying to get user id.");
		}
	});
});

$('body').on('click', '#playlistBtn-js', function() {
	//check if has a title
	//get private or public value
	//send array of id's to django with ajax
	//receive a success or fail
	if(access_token == "" || access_token == null) {
		M.toast({html: 'Please login with your Spotify account.'});
		return;
	}

	if(validatePlaylistTitle()) {
		if(validateChosenPlaylist()) {
			playlist_visibility = $('#visibility-js').is(':checked');
			if(playlist_visibility) {
				makePublicPlaylist();
			} else {
				makePrivatePlaylist();
			}
		}
	}
});


function makePublicPlaylist() {
	console.log("Making a public playlist");
	$.ajax({
		type: 'GET',
		url: '/play_app/create_playlist_ajax/',
		dataType: 'json',
		data: {
			'title': playlist_title,
			'songs': JSON.stringify(playlist_array),
			'all_songs': JSON.stringify(all_songs),
			'visibility': playlist_visibility,
			'access_token': access_token,
			'user_id': user_id
		},
		success: function(data) {
			M.toast({html: 'Your public playlist: ' + data.title + ' has been created'});
			playlist_array = [];
		},
		fail: function(data) {
			M.toast({html: 'An error occurred while making your playlist.'});
		}
	});
}

function makePrivatePlaylist() {
	console.log("Making a private playlist");
	$.ajax({
		type: 'GET',
		url: '/play_app/create_playlist_ajax/',
		dataType: 'json',
		data: {
			'title': playlist_title,
			'songs': JSON.stringify(playlist_array),
			'all_songs': JSON.stringify(all_songs),
			'visibility': playlist_visibility,
			'access_token': access_token,
			'user_id': user_id
		},
		success: function(data) {
			M.toast({html: 'Your private playlist: ' + data.title + ' has been created.'});
			playlist_array = [];
		},
		fail: function(data) {
			M.toast({html: 'An error occurred while making your playlist.'});
		}
	})
}

/*** WORKS ***/

//A user clicks on a setlist and this function adds those songs
//to the global variable playlist_array.
//The contents of that array will be sent to the back-end.
$('body').on('click', '.setlists-card-js', function() {
	playlist_array = [];
	songs = $(this).siblings().find('#songsList-js')[0].children;
	$.each(songs, function() {
		console.log($(this).text());
		if($(this).css("color") != "rgb(244, 67, 54)") {
			playlist_array.push($(this).text().toLowerCase());
		}
	})
	console.log(playlist_array);
});

//Displays a Toast element if there is no title.
function validatePlaylistTitle() {
	playlist_title = $('#playlistTitle-js').val();
	if(playlist_title == "") {
		M.toast({html: 'Please enter a title for your playlist.'});
		return false;
	} else {
		return true;
	}
}

//Displays a Toast element if there is no setlist.
function validateChosenPlaylist() {
	if(playlist_array.length == 0) {
		M.toast({html: 'Please select a setlist.'});
		return false;
	} else {
		return true;
	}
}

