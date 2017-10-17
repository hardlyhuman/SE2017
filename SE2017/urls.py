###################################################
# SE2017/urls.py: Consists of all the valid urls of SAMS-IIITS
#__authors__ = "Sri Harsha Gajavalli", "SriRamKumar", "Savitha"
#__copyright__ = "Copyright 2017, SE2017 Course"
#__Team__ = ["Sri Harsha Gajavalli", "", "David Christie", "Likhith Lanka", "Sajas P", "Rajeev Reddy"]
#__license__ = "MIT"
#__version__ = "1.2"
#__maintainer__ = "SriRamKumr"
#__email__ = "sriramkumar.t15@iiits.in"
#__status__ = "Development"
####################################################


"""SE2017 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets



urlpatterns = [
	url(r'^$', include('home.urls'), name='home'),
    url(r'^login/',  auth_views.login, {'template_name': 'Login/login.html'}, name='login'),
	url(r'^logout/$', auth_views.logout, {'template_name': 'Login/login.html'}, name='logout'),
	url(r'^student/', include('students.urls'), name='student'),
	url(r'^faculty/', include('faculty.urls'), name='faculty'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/',include('home.urls')),

]
