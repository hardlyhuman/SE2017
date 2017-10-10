from django.conf.urls import url,include
from . import views

urlpatterns = [
        url(r'^$',views.dashboard,name='dashboard'),
        url(r'^viewattendance/', views.ViewAttendance, name='ViewAttendance'),
        url(r'^CourseRegistration/', views.CourseRegistration, name='CourseRegistration'),
        url(r'^AddCourse/', views.AddCourse, name='AddCourse'),
        url(r'^DropCourse/', views.DropCourse, name='DropCourse'),
        url(r'^MarkAttendance/', views.MarkAttendance, name='MarkAttendance'),
        url(r'^assgnsubstatus/', views.AssgnSubStatus, name='AssgnSubmissionStatus'),
]
