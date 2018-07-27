# SpotiPlay

SpotiPlay is a web application for users with an interest in music. A user can visit the website and search for their favorite artist. The search will yield results containing recent setlists from their favorite band. The user can then select a setlist and save it to their Spotify account as a playlist.

https://spotiplay-235.herokuapp.com

This application is powered by https://www.setlist.fm/ and Spotify. The back-end is being developed with Python and the Django framework. The front-end is being developed with the help of the Materialize framework and JQuery. Currently, I am not using a wrapper to access the API for Setlist.FM, but I am using Spotipy (https://github.com/plamere/spotipy) and a JS wrapper (https://github.com/JMPerez/spotify-web-api-js) to access the Spotify API. I may drop Spotipy altogether and move all API calls to the front-end for consistency.

Things learned:

1. Django - I am used to doing web development in Java. I watched a course hosted on Udemy that focused on Django and then dived right in. So far, my experience has been pleasant.
2. Materialize - Again, I am used to a different and more popular framework: Bootstrap. However, I wanted to try something new. I think that Materialize is cleaner, but that may be because it is smaller than Bootstrap and just not as much to do.
3. API calls - During the development of SpotiPlay, I have been introduced to making API calls. For the most part, it is just tedious work figuring out syntax to access the information I need in the response.
