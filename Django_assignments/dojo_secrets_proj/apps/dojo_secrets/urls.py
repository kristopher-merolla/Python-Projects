from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^register$', views.register, name="register"),
	url(r'^login$', views.login, name="login"),
	url(r'^register_user$', views.new_login, name="register_user"),
	url(r'^main$', views.main, name="main"),
	url(r'^post$', views.post, name="post"),
	url(r'^popular$', views.popular, name="popular"),
	url(r'^like/(?P<id>\d+)/(?P<sentby>\w+)$', views.newlike, name="like"),
	url(r'^delete/(?P<id>\d+)/(?P<sentby>\w+)$', views.delete, name="delete"),
]
