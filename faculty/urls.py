from django.conf.urls import url,include
from . import views


from django.views.generic import TemplateView


app_name='faculty'
urlpatterns =[
	
         url(r'^ViewProfs/$',views.ViewProfs,name='ViewProfs'),   
url(r'^ViewRegisteredStudents/$',views.ViewRegisteredStudents,name='ViewRegisteredStudents'), 
url(r'^AddAssignment/$',views.AddAssignment,name='AddAssignment'),   
url(r'^Delass/$',views.Delass,name='Delass'),  
url(r'^delete/$',views.delete,name='delete'), 
url(r'^offercourses/$',views.OfferCourses,name='OfferCourses'), 
url(r'^editdescription/$',views.EditCourseDescription,name='EditCourseDescription'), 
        
        
	
    ]

