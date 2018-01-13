from django.contrib.auth import logout
from django.shortcuts import render
from django.core.cache import cache
from django.http import JsonResponse
from . import forms
from . import objects
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import json

SETLIST_FM_API_KEY = 'b0bf96c4-6af5-4ac0-ae87-1b3d8e6cd9cb'
SPOTIFY_CLIENT_ID = 'bb7dcf3b9cf841939c48ef54843ef28a'
SPOTIFY_CLIENT_SECRET = 'a38bc6643c2847429cde433ea6770e24'


def index(request):
	'''
		Inserts a form into the index page
	'''
	form = forms.SearchArtistForm()
	context = {'form': form}
	return render(request, 'play_app/index.html', context)


def searchTracksFromArtist(artist, limit, offset, array):
	'''
		Requests all songs from an artist and adds them to a dictionary
		Calls itself if not all songs have been visited
	'''
	client_credentials_manager = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
	results = sp.search(q=artist, limit=limit, offset=offset)

	for i in results['tracks']['items']:
		array[i['name'].lower()] = i['id']
	if(results['tracks']['total'] > limit*offset):
		offset += 50
		searchTracksFromArtist(artist, limit, offset, array)

def getAllSongsFromArtist(artist):
	'''
		Gets all songs from an artist using Spotiy's API
		returns a dictionary of those songs (key) with an ID (value)
		Works because Python is pass-by-object-reference
	'''
	array = {}
	searchTracksFromArtist(artist, 50, 0, array)
	for t in array.items():
		print(t)
	return array

def getQueryFromSetlistFM(headers, context):
	'''
		Requests artist information from Setlist.FM
		Returns a json object for the artist
	'''
	artist_search_url   = 'https://api.setlist.fm/rest/1.0/search/artists?artistName={}&p=1&sort=sortName'
	artist_search_query = artist_search_url.format(context['artist'])
	r = requests.get(artist_search_query, headers=headers)
	return r.json()

def getSetlists(headers, context):
	'''
		Requests setlists for an artist from Setlist.FM
		Returns a json object for the setlists
	'''
	mbid = context['query']['artist'][0]['mbid']
	artist_setlist_url   = 'https://api.setlist.fm/rest/1.0/artist/{}/setlists?p=1'
	artist_setlist_query = artist_setlist_url.format(mbid)
	r = requests.get(artist_setlist_query, headers=headers)
	return r.json()

def getImageURL(context):
	'''
		Requests the image url from the Spotify API
		Returns that url
	'''
	client_credentials_manager = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
	results = sp.search(q='artist:' + context['artist'], limit=5, type='artist')
	#This is the structure of the Spotify API object to get an image url
	image_url = results['artists']['items'][0]['images'][0]['url']
	return image_url

### Searches for an artist with Setlist.fm's api
### Grabs that artist's 'mbid'
### Searches for an artist's recent setlists with Setlist.fm's api
### Store ~20 (1 page in the api) results in context
def search_result_view(request):
	'''
		Searches for an artist with Setlist.fm's api
		Creates artist & setlist objects that will later
		be displayed on the screen.
		Gets the image of the artist/band.
		Gets all of the songs from an artist/band available
		on Spotify so that the ones not available can be
		specified on the screen.

	'''
	context = {}
	if request.method == 'POST':
		form = forms.SearchArtistForm(request.POST)

		if form.is_valid():
			context['artist'] = form.cleaned_data['artist']
	
	#SETLIST.FM -- search for artist
	headers = {
		'Accept': 'application/json',
		'x-api-key': SETLIST_FM_API_KEY
	}
	context['query'] = getQueryFromSetlistFM(headers, context)

	#SETLIST.FM -- get artist's setlists
	artist_list = []
	#possible that the user enters in an artist that can't be found
	#either due to typo or not existing
	try:
		for i in range(0, 20):
			artist_list.append(objects.Artist(context['query']['artist'][0], i))
	except KeyError:
		return render(request, 'play_app/searchError.html', context)

	context['setlists'] = getSetlists(headers, context)

	i = 0
	for artist in artist_list:
		artist.setlist = objects.Setlist(context['setlists']['setlist'][i])
		i += 1
	context['artist_list'] = artist_list

	#SPOTIFY -- get image url for artist
	context['image_url'] = getImageURL(context)

	#Playlist form, maybe remove if JS/Ajax is used?
	playlist_form = forms.MakePlaylistForm()
	context['playlist_form'] = playlist_form

	#Get all songs from the artist
	context['all_songs'] = getAllSongsFromArtist(context['artist'])
	context['all_songs_json'] = json.dumps(context['all_songs'])

	return render(request, 'play_app/searchResult.html', context)

def about_view(request):
	'''
		Displays the about page for SpotiPlay.
	'''
	context = {}
	return render(request, 'play_app/about.html', context)

def feedback_view(request):
	'''
		Displays the feedback page for SpotiPlay.
	'''
	context = {}
	return render(request, 'play_app/feedback.html', context)

def login_view(request):
	'''
		Page for logging into Spotify.
	'''
	return render(request, 'play_app/login.html', {})

def logout_view(request):
	'''
		Page for logging out of Spotify.
	'''
	return render(request, 'play_app/logout.html', {})

def create_playlist_ajax(request):
	data = {}
	if request.method == 'GET':
		print(request.GET)
		data['title'] = request.GET['title']
		data['songs'] = request.GET['songs[]']
		data['visibility'] = request.GET['visibility']
		data['access_token'] = request.GET['access_token']
		data['user_id'] = request.GET['user_id']
		#get all_songs

	sp = spotipy.Spotify(auth=data['access_token'])
	sp.trace = False
	#retrieve all of the id's for the songs in this new playlist
	playlists = sp.user_playlist_create(data['user_id'], data['title'], "Description");
	print(playlists);
	return JsonResponse(data)



def page_view(request):
	'''
		Page for testing functions...
		Remove later.
	'''
	array = getAllSongsFromArtist('touche amore')
	print(len(array))
	for t in array.items():
		print(t)


	context = {}
	return render(request, 'play_app/page.html', context)

