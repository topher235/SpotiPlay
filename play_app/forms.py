from django import forms
#built in validators
from django.core import validators

class SearchArtistForm(forms.Form):
	artist = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search for an artist'}))
	botcatcher = forms.CharField(required=False,
								widget=forms.HiddenInput,
								validators=[validators.MaxLengthValidator(0)])

class MakePlaylistForm(forms.Form):
	title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Playlist Title'}))

	botcatcher = forms.CharField(required=False,
								widget=forms.HiddenInput,
								validators=[validators.MaxLengthValidator(0)])