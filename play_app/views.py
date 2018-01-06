from django.contrib.auth import logout
from django.shortcuts import render
from django.core.cache import cache
from . import forms
from . import objects
import sys
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyClientCredentials
import requests

SETLIST_FM_API_KEY = 'b0bf96c4-6af5-4ac0-ae87-1b3d8e6cd9cb'
SPOTIFY_CLIENT_ID = 'bb7dcf3b9cf841939c48ef54843ef28a'
SPOTIFY_CLIENT_SECRET = 'a38bc6643c2847429cde433ea6770e24'

# Create your views here.

def index(request):
	if 'user_token' in request.session:
		print()
		print("GOT TO THE USER TOKEN IN INDEX")
		sp = spotipy.Spotify(auth=request.session['user_token'])
		results = sp.current_user_saved_tracks()
		for item in results['items']:
			track = item['track']
			print(track['name'] + ' - ' + track['artists'][0]['name'])

	form = forms.SearchArtistForm()
	context = {'form': form}

	# go to results page
	return render(request, 'play_app/index.html', context)

### Searches for an artist with Setlist.fm's api
### Grabs that artist's 'mbid'
### Searches for an artist's recent setlists with Setlist.fm's api
### Store ~20 (1 page in the api) results in context
def search_result_view(request):
	context = {}
	if request.method == 'POST':
		form = forms.SearchArtistForm(request.POST)

		if form.is_valid():
			context['artist'] = form.cleaned_data['artist']


#	SETLIST.FM -- search for artist
	headers = {
		'Accept': 'application/json',
		'x-api-key': SETLIST_FM_API_KEY
	}

	artist_search_url   = 'https://api.setlist.fm/rest/1.0/search/artists?artistName={}&p=1&sort=sortName'
	artist_search_query = artist_search_url.format(context['artist'])
	r = requests.get(artist_search_query, headers=headers)
	context['query'] = r.json()

	artistList = []

	#possible that the user enters in an artist that can't be found
	#either due to typo or not existing
	try:
		for i in range(0, 20):
			artistList.append(objects.Artist(context['query']['artist'][0], i))
	except KeyError:
		return render(request, 'play_app/searchError.html', context)

#	SETLIST.FM -- get artist's setlists
	mbid = context['query']['artist'][0]['mbid']
	artist_setlist_url   = 'https://api.setlist.fm/rest/1.0/artist/{}/setlists?p=1'
	artist_setlist_query = artist_setlist_url.format(mbid)
	r = requests.get(artist_setlist_query, headers=headers)
	context['setlists'] = r.json()
	print(context['query'])

	i = 0
	for artist in artistList:
		artist.setlist = objects.Setlist(context['setlists']['setlist'][i])
		i += 1

	context['artistList'] = artistList

#	scope = 'user-library-read'
#	token = util.prompt_for_user_token

	
	client_credentials_manager = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	results = sp.search(q='artist:' + context['artist'], limit=5, type='artist')
#	This is the structure of the Spotify API object to get an image url
	image_url = results['artists']['items'][0]['images'][0]['url']
	context['image_url'] = image_url

	playlist_form = forms.MakePlaylistForm()
	context['playlist_form'] = playlist_form

	return render(request, 'play_app/searchResult.html', context)

def about_view(request):
	context = {}
	return render(request, 'play_app/about.html', context)

def feedback_view(request):
	context = {}
	return render(request, 'play_app/feedback.html', context)

def page_view(request):
	context = {}
	return render(request, 'play_app/page.html', context)

def login_view(request):
#	scope = 'user-library-read playlist-modify-public playlist-modify-private'
#	if len(sys.argv) > 1:
#	    username = sys.argv[1]
#	else:
#		print("Usage: %s username" % (sys.argv[0],))
#		sys.exit()
#
#	token =	util.prompt_for_user_token(username, scope, client_id=SPOTIFY_CLIENT_ID,
#		client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri='http://localhost:8000/play_app/')
#	
#
#
#
#	cache_path = ".cache-" + username
#	sp_oauth = oauth2.SpotifyOAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET,
#		'http://localhost:8000/play_app/', scope=scope)
#	access_token = ""
#	token_info = sp_oauth.get_cached_token()
#
#	if token_info:
#		print("Found cached token")
#		print(cache_path)
#		access_token = token_info['access_token']
#	else:
#		url = request.url
#		code = sp_oauth.parse_response_code(url)
#		if code:
#			print("Found auth code...")
#			token_info = sp_oauth.get_access_token(code)
#			access_token = token_info['access_token']
#
#	if access_token:
#		print("Access token available...")
#		request.session['user_token'] = access_token
#		print("SUCCESS")
#		print("---------------------------------------------------------------------")
#		return index(request)
#	else:
#		print("----------------------------------------------------------------------")
#		print("FAIL")
#		return index(request)




#	if token:
#		request.session['user_token'] = token
#		print("SUCCESS")
#		print("---------------------------------------------------------------------")		
#		return index(request)
#	else:
#		print("----------------------------------------------------------------------")
#		print("FAIL")

	return render(request, 'play_app/login.html', {})



def logout_view(request):
	try:
		#del request.session['user_token']
		logout(request)
		#cache.delete('.cache-runserver')
		print(cache.get('access_token'))
		return render(request, 'play_app/logout.html', {})
	except KeyError:
		return render(request, 'play_app/logout.html', {})