###################################################
# students/urls.py: Consists of list of urls of students app of SAMS-IIITS
#__author__ = "Sri Harsha Gajavalli"
#__copyright__ = "Copyright 2017, SE2017 Course"
#__Team__ = ["Sri Harsha Gajavalli", "Koushik Bharadwaj", "David Christie", "Likhith Lanka", "Sajas P", "Rajeev Reddy"]
#__license__ = "MIT"
#__version__ = "1.2"
#__maintainer__ = "Likhith Lanka"
#__email__ = "likhith.l15@iiits.in"
#__status__ = "Development"
####################################################


# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$',views.dashboard,name='dashboard'),
        url(r'^viewattendance/', views.ViewAttendance, name='ViewAttendance'),
        url(r'^assgnsubstatus/', views.AssgnSubStatus, name='AssgnSubmissionStatus'),
        url(r'^register_course/', views.register_course, name='register_course'),
        url(r'^register/', views.register, name='register'),
        url(r'^addcourse/', views.register, name='register'),
        url(r'^DropCourse/', views.DropCourse, name='DropCourse'),
        url(r'^unregister/', views.unregister, name='unregister'),

]
