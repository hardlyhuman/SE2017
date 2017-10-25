from celery.decorators import periodic_task
from celery.task.schedules import crontab
from SE2017.celery import app
from django.core.mail import send_mail
from .models import *
import datetime

@app.task
def say_hello():
    print 'hello!'

@app.task
def send_notification():
    now = datetime.datetime.now()
    lastTimeToCheck = now + datetime.timedelta(hours=2)
    courseList = Timetable.objects.filter(T_days = now.weekday(), Start_time__lt= lastTimeToCheck, Start_time__gt=now.time()).values_list('Course_ID','Class_ID','Start_time')
    courseNames = []
    roomNumber =[]
    facultyNames=[]    
    classTime=[]
    for i in range(len(courseList)):
        course_id = courseList[i][0]
        a=Courses.objects.filter(Course_ID = courseList[i][0]).values_list('Course_Name')
        inst_ids = Instructors_Courses.objects.filter(Course_ID = courseList[i][0]).values_list('Inst_ID')
        temp=[]
        for inst in inst_ids:
            ldap = Personnel.objects.filter(Person_ID = inst[0])
            temp.append(ldap[0])
        facultyNames.append(temp)
        courseNames.append(a[0])        
        classTime.append(courseList[i][2].strftime('%H:%M'))
        roomNumber.append(courseList[i][1])
        print inst_ids, ldap[0]
    print '*******************'
    print courseNames
    print roomNumber
    print facultyNames    
    print classTime
    for i in range(len(courseNames)):
        for j in facultyNames[i]:
            send_mail(courseNames[i][0]+" class reminder", "Dear Professor "+str(j)+" you have a class at "+ classTime[i]+"hrs in room number " +str(roomNumber[i]),'ItDept.iiits@gmail.com',['vaishali0001sharma@gmail.com','sriram.t15@iiits.in'],fail_silently=False,)
    
