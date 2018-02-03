$(document).ready(function() {
	$('.home-li-js').addClass("active");
})

function validateSearch() {
	var accessTokenDate = localStorage.getItem('accessTokenDate');
	var currDate = new Date();

	if(Math.abs(currDate - accessTokenDate) >= 3600000) {
		//token has expired, tokens expire after one hour
		M.toast({html: 'Please login with your Spotify account.'});
		return false;
	} else if($('#artist-js') == "") {
		M.toast({html: 'Please enter an artist in the search field.'});
		return false;
	} else {
		return true;
	}
}