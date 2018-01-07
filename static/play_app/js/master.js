var access_token = String(localStorage.getItem("accessToken"));
var playlist_array = [];

$('#playlistBtn-js').on('click', function() {
	//check if has a title
	//get private or public value
	//get song titles
	//send array of id's to django with ajax
	//receive a success or fail
	validatePlaylistTitle();
	
	var visibility = $('#visibility-js').is(':checked');
	if(visibility) {
		//makePublicPlaylist($(this));
		$('#songsList-js').children().each(function() {
			console.log($(this).text().toLowerCase());
			var songName = $(this).text().toLowerCase();
			if(all_songs[songName]) {
				playlist_array.push(songName);
			}
			console.log();
			console.log(playlist_array);
		});
	} else {
		makePrivatePlaylist($(this));
	}
	playlist_array = [];
});

//WORKS
function validatePlaylistTitle() {
	var playlist_title = $('#playlistTitle-js').val().trim();
	if(playlist_title == "") {
		alert("Please enter a title for your playlist.");
	}
}

function makePrivatePlaylist(div) {
	console.log('making private playlist');
	$('li', div).each(function() {
		console.log(this.text());
	});
}

function makePublicPlaylist(div) {
	console.log('making public playlist')
}