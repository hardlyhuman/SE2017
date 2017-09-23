from django.conf.urls import url,include
from . import views

#from django.conf.urls import patterns, url
from django.views.generic import TemplateView


app_name='faculty'
urlpatterns =[
	url(r'^file_upload/$',views.upload_file,name='file_upload'),
         url(r'^view/$',views.view,name='view'),     
        
	#url(r'^file_upload/success.html$',views.IndexView,name='upload_file'),
    	#url(r'^index/$',views.IndexView,name='index'),
	#url(r'^profs/$',views.ViewProfs,name='ViewProfs'),
	#url(r'^courses/(?P<id_no>[0-9]+)/$',views.FacultyCourses,name='courses'),
    	#url(r'^courses/$',views.ViewCourses.as_view(),name='courses'),

    ]

