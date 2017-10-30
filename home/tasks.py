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
    ttCourseList = Timetable.objects.filter(T_days = now.weekday(), Start_time__gt = now.time())
    courses = []
    faculty = []
    roomNum = []
    classTime = []
    print '%%%%%%%%%%%%', len(ttCourseList), ttCourseList
    for ttcourse in ttCourseList:
        courseId = ttcourse.Course_ID
        facultyCourseIds = Instructors_Courses.objects.filter(Course_ID = courseId)
        addCourse = False
        sameCourseFacultyHolder = []
        for facultyCourseId in facultyCourseIds:
            sameCourseFaculty = []
            facultyName = facultyCourseId.Inst_ID.LDAP
            notificationTimeObj = NotificationTime.objects.get(Personnel_ID = facultyCourseId.Inst_ID )
            notificationTime = notificationTimeObj.Notification_time
            checkTime = now + datetime.timedelta(minutes = notificationTime)
            print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
            print "********"+str(checkTime) + '************',ttcourse.Start_time
            print '***********' +str(now.time()) + '**************' , ttcourse.Start_time
            if checkTime.time() >= ttcourse.Start_time and now.time() < ttcourse.Start_time:
                print '333333'
                sameCourseFaculty.append(facultyName)
            if len(sameCourseFaculty) > 0:
                addCourse = True
                sameCourseFacultyHolder = sameCourseFaculty
        if (1 == 1):
            courses.append(courseId.Course_Name)
            roomNum.append(ttcourse.Class_ID)
            classTime.append(ttcourse.Start_time)            
            faculty.append(sameCourseFacultyHolder)
            sameCourseFacultyHolder = []
    for cIndex in range(len(courses)):
        for fac in faculty[cIndex]:
            send_mail(str(courses[cIndex])+" class reminder", "Dear Professor "+str(fac)+\
                  " you have a class at "+ str(classTime[cIndex])+"hrs in room number "+str(roomNum[cIndex]),'ItDept.iiits@gmail.com',['vaishali0001sharma@gmail.com',],\
                  fail_silently=False,)
