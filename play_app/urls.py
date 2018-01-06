from django.conf.urls import url
from play_app import views

app_name = "play_app"

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^searchResult/', views.search_result_view, name='search_result'),
	url(r'^about/', views.about_view, name='about'),
	url(r'^feedback/', views.feedback_view, name='feedback'),
	url(r'^page/', views.page_view, name='page'),
	url(r'^login/', views.login_view, name='login'),
	url(r'^logout/', views.logout_view, name='logout'),
]