from django.conf.urls import url
from . import views
app_name='students'
urlpatterns = [
        url(r'^$',views.dashboard,name='index'),
        url(r'^viewattendance/', views.viewattendance , name='ViewAttendance'),
        url(r'^assgnsubstatuspending/', views.AssgnSubStatusPending, name='AssgnSubmissionStatusPending'),
        url(r'^assgnsubstatusoverdue/', views.AssgnSubStatusOverdue, name='AssgnSubStatusOverdue'),
        url(r'^assgnsubstatussubmitted/', views.AssgnSubStatusSubmitted, name='AssgnSubStatusSubmitted'),
        url(r'^adddropcourses/', views.addDropCourses, name='addDropCourses'),
        url(r'^register/', views.registerCourses, name='register'),
]
