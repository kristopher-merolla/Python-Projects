from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^ninja$', views.ninja),
	url(r'^ninja/(?P<turtle>\w+)$', views.color),
	url(r'^ninja/(?P<turtle>\d+)$', views.color),
]