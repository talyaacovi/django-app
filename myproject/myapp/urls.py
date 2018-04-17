from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^messages/(?P<username>.+)$', views.messages, name='messages'),
	url(r'^login/$', auth_views.login),
	url(r'^logout/$', auth_views.logout),
	url(r'^register/', views.register, name='register'),
]