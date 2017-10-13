from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'home'
urlpatterns = [
	url(r'^login/',  auth_views.login, {'template_name': 'Login/login.html'}, name='login'),
    url(r'^$', views.index, name='index'),
    url(r'^personnel/$',views.people),
    url(r'^personnel/(?P<pk>[0-9]+)/$',views.person),
    url(r'^departments/$',views.departments),
    url(r'^department/(?P<pk>[0-9]+)/$',views.department),
    url(r'^add_view_roles/',views.add_view_roles),
    url(r'^role/(?P<pk>[0-9]+)/$',views.role),
    url(r'^add_view_courses/',views.add_view_courses),
    url(r'^course/(?P<pk>[0-9]+)/$',views.course),
    url(r'^add_view_documents/',views.add_view_documents),
    url(r'^document/(?P<pk>[0-9]+)/$',views.document),
    url(r'^add_view_assignments/',views.add_view_assignments),
    url(r'^assignment/(?P<pk>[0-9]+)/$',views.assignment),
    url(r'^add_view_submissions/',views.add_view_submissions),
    url(r'^submission/(?P<pk>[0-9]+)/$',views.submission),
    url(r'^add_view_IC/',views.add_view_IC),
    url(r'^IC/(?P<pk>[0-9]+)/$',views.IC),
    url(r'^add_view_SC/',views.add_view_SC),
    url(r'^SC/(?P<pk>[0-9]+)/$',views.SC),
    url(r'^add_view_events/',views.add_view_events),
    url(r'^event/(?P<pk>[0-9]+)/$',views.event),
    url(r'^add_view_SP/',views.add_view_SP),
    url(r'^SP/(?P<pk>[0-9]+)/$',views.SP),
	url(r'^add_view_attendance/',views.add_view_attendance),
    url(r'^attendance/(?P<pk>[0-9]+)/$',views.attendance),
	url(r'^add_view_attendance_sessions/',views.add_view_attendance_sessions),
	url(r'^add_view_timetable/',views.add_view_timetable),
	url(r'^validate_user/',views.validate_user),
	url(r'^facultyusers/',views.faculty_users),
	url(r'^studentusers/',views.student_users),
]
