from django.conf.urls import url
from . import views
app_name='faculty'
urlpatterns =[	
         url(r'^ViewProfs/$',views.ViewProfs,name='ViewProfs'),
 url(r'^ViewAttendance/$',views.ViewAttendance,name='ViewAttendance'),    
url(r'^AddAssignment/$',views.AddAssignment,name='AddAssignment'),   
url(r'^ViewAssignment/$',views.ViewAssignment,name='ViewAssignment'),  
url(r'^offercourses/$',views.OfferCourses,name='OfferCourses'),  
url(r'^coursepage/$',views.CoursePage,name='CoursePage'),
url(r'^index/$',views.index,name='index'), 
url(r'^lib/$',views.MyLibrary,name='MyLibrary'),      
]

