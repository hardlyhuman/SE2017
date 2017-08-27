from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'home'
urlpatterns = [
	url(r'^login/',  auth_views.login, {'template_name': 'Login/login.html'}, name='login'),
    url(r'^$', views.index, name='index'),
]
