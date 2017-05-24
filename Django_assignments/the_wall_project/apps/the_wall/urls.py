from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^thewall$', views.active_user),
	url(r'^login$', views.login),
	url(r'^register_user$', views.new_login),
	url(r'^post$', views.new_post),
]