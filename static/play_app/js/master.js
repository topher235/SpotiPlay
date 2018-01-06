var spotifyApi = new SpotifyWebApi();
spotifyApi.setAccessToken(String(localStorage.getItem("accessToken")));
var songArray = [];

function searchTracks(artist, offset) {
	options = 'artist:'+artist+', limit:50, offset:'+offset+'';
	spotifyApi.searchTracks('artist:'+artist)
		.then(function(data) {
			console.log(data);
			var i = data.tracks.limit;
			for(j = 0; j < i; j++) {
				songArray.push(data.tracks.items[j].name);
			}
			if(data.tracks.total > 50*offset) {
				offset += 1;
				searchTracks(artist, offset);
			}
		}, function(err) {
			console.log(err);
		});
}

$('#result-js').on('click', function() {
	var artist = $('#artistName-js').text();
	var offset = 0;
	setTimeout(function() {
		searchTracks(artist, offset);
	}, 0);
	console.log(songArray);

	$('.songName-js').each(function() {
		if(!$(this).hasClass("searchDone")) {
			var song = $(this);
			var songName = song.text();
			if(!songArray.includes(songName)) {
				song.addClass("red-text");
			}
			song.addClass("searchDone");
		}
	});

	/*
	$('.songName-js').each(function() {
		//highlight red if not found in spotify
		if(!$(this).hasClass("searchDone")) {
			var song = $(this);
			var songName = song.text();
			var options = 'artist:' + artist;
			setTimeout(function() {
				spotifyApi.searchTracks(songName, options)
					.then(function(data) {
						if(data.tracks.items[0].artists[0].name != artist) {
							song.addClass("red-text");
						}
						song.addClass("searchDone");
						console.log(data.tracks.items[0].artists[0].name + " ----- " + data.tracks.items[0].name);
					}, function(err) {
						console.log(err);
					});
			}, 0);
		}
	});
	*/
});