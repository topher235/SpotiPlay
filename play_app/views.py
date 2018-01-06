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
	form = forms.SearchArtistForm()
	context = {'form': form}

	# go to results page
	return render(request, 'play_app/index.html', context)


def searchTracksFromArtist(artist, limit, offset, array):
	client_credentials_manager = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
	results = sp.search(q=artist, limit=limit, offset=offset)

	#print(results['tracks']['items'])
	for i in results['tracks']['items']:
		array[i['name']] = i['id']
	if(results['tracks']['total'] > limit*offset):
		offset += 1
		searchTracksFromArtist(artist, limit, offset, array)

def getAllSongsFromArtist(artist):
	array = {}
	searchTracksFromArtist(artist, 50, 0, array)
	return array

def getQueryFromSetlistFM(headers, context):
	
	artist_search_url   = 'https://api.setlist.fm/rest/1.0/search/artists?artistName={}&p=1&sort=sortName'
	artist_search_query = artist_search_url.format(context['artist'])
	r = requests.get(artist_search_query, headers=headers)
	return r.json()

def getSetlists(headers, context):
	mbid = context['query']['artist'][0]['mbid']
	artist_setlist_url   = 'https://api.setlist.fm/rest/1.0/artist/{}/setlists?p=1'
	artist_setlist_query = artist_setlist_url.format(mbid)
	r = requests.get(artist_setlist_query, headers=headers)
	return r.json()

def getImageURL(context):
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
		for i in range(0, 10):
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

	return render(request, 'play_app/searchResult.html', context)

def about_view(request):
	context = {}
	return render(request, 'play_app/about.html', context)

def feedback_view(request):
	context = {}
	return render(request, 'play_app/feedback.html', context)

def login_view(request):
	return render(request, 'play_app/login.html', {})

def logout_view(request):
	return render(request, 'play_app/logout.html', {})




def page_view(request):
	print(len(array))
	for t in array.items():
		print(t)


	context = {}
	return render(request, 'play_app/page.html', context)

