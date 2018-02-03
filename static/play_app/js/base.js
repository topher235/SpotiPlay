$(document).ready(function() {
	$('.sidenav').sidenav();
	$('.pin-nav').pushpin({
		top: 1
	});

	window.addEventListener('storage', function(event) {
	   	$('#loginBtn-js').html("<i class='material-icons left'>account_box</i>Logout");
	});

	var accessToken = localStorage.getItem('accessToken');
	var accessTokenDate = localStorage.getItem('accessTokenDate');
	var currDate = new Date();

	if(localStorage.getItem('accessToken') != null) {
		//user has logged in before
		$('#loginBtn-js').html("<i class='material-icons left'>account_box</i>Logout");
	} 
	if(Math.abs(currDate - accessTokenDate) >= 3600000) {
		//token has expired, tokens expire after one hour
		$('#loginBtn-js').html("<i class='material-icons left'>account_box</i>Login");
	}
});

function loginSpotify() {
	if($('#loginBtn-js').text() == "account_boxLogout") {
		logoutSpotify();
	} else {
		console.log("logging in");
		var SPOTIPY_CLIENT_ID = "bb7dcf3b9cf841939c48ef54843ef28a"
    	var SPOTIPY_REDIRECT_URI = "http://localhost:8000/play_app/login/"
	    var spotifyScope = "user-library-read playlist-modify-public playlist-modify-private"
	    var spotifyAuthEndpoint = "https://accounts.spotify.com/authorize?"+"client_id="+SPOTIPY_CLIENT_ID+"&redirect_uri="+SPOTIPY_REDIRECT_URI+"&scope="+spotifyScope+"&response_type=token&state=123";
	    window.open(spotifyAuthEndpoint,'callBackWindow','height=500,width=400');
	}
}

function logoutSpotify() {
	localStorage.removeItem('accessToken');
	localStorage.removeItem('accessTokenDate');
	$('#loginBtn-js').html("<i class='material-icons left'>account_box</i>Login");
	window.location = "/play_app/";
}