from django.conf.urls import url
from play_app import views

app_name = "play_app"

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^searchResult/', views.search_result_view, name='search_result'),
	url(r'^login/', views.login_view, name='login'),
	url(r'^create_playlist_ajax/$', views.create_playlist_ajax, name='create_playlist_ajax'),
]