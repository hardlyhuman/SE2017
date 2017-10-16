from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$',views.dashboard,name='dashboard'),
        url(r'^viewattendance/', views.ViewAttendance, name='ViewAttendance'),
        #url(r'^CourseRegistration/', views.CourseRegistration, name='CourseRegistration'),
        url(r'^AddCourse/', views.AddCourse, name='AddCourse'),
        #url(r'^DropCourse/', views.DropCourse, name='DropCourse'),
        #url(r'^MarkAttendance/', views.MarkAttendance, name='MarkAttendance'),
        url(r'^assgnsubstatus/', views.AssgnSubStatus, name='AssgnSubmissionStatus'),
        url(r'^register_course/', views.register_course, name='register_course'),
        url(r'^register/', views.register.as_view(), name='register'),
        url(r'^addcourse/', views.register.as_view(), name='register')
        url(r'^DropCourse/', views.DropCourse.as_view(), name='DropCourse'),
        url(r'^unregister/', views.unregister, name='unregister'),

]
