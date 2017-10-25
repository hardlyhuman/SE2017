#Emergency Edit Protocol : 10/20/2017

from __future__ import unicode_literals

import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from home.models import *
from django.utils import timezone




@login_required(login_url="/login/")
def dashboard(request):
    user = request.user;
    print(user)
    return render(request, "student/index.html", dict(name=user))



@login_required(login_url="/login/")
def viewattendance(request):
    try:
        user = request.user;                                                 
        userPersonnelObj=Personnel.objects.filter(LDAP=user)
        MyCourses = Students_Courses.objects.filter(Student_ID=userPersonnelObj[0].Person_ID); 
        CourseAttendanceContext  = [];

        for course in MyCourses:
            AttendanceSessions = Attendance_Session.objects.filter(Course_Slot = course.Course_ID.Course_ID)
            classesPresent = 0
            totalClasses = 0
            absentDays = []
            for sessions in AttendanceSessions:
                try:
                    attendanceObject = Attendance.objects.filter(Student_ID = userPersonnelObj[0].Person_ID).filter(ASession_ID=sessions.Session_ID)
                    
                    totalClasses += 1
                    if(attendanceObject[0].Marked == 'P'):
                        classesPresent += 1
                    elif(attendanceObject[0].Marked == 'A'):
                        absentDays.append(attendanceObject[0].Date_time)
                except:
                    pass
            retObj = dict(course=course,present = classesPresent,total = totalClasses,absentDays = absentDays)
            CourseAttendanceContext.append(retObj)
        context = dict(CourseAttendanceContext=CourseAttendanceContext)
    except:
        context = dict(ErrorMessage = "No Registered Classes")
    return render(request, "student/ViewAttendance.html", context)




def AssgnSubStatusPending(request):
    user =  request.user;
    pendingAssignments = []
    StudentObject=Personnel.objects.filter(LDAP=user.id)
    CoursesByStudent = Students_Courses.objects.filter(Student_ID=StudentObject[0].Person_ID)
    for course in CoursesByStudent:
        AssignmentsForCourse = Assignment.objects.filter(Course_ID = course.Course_ID.Course_ID)
        for assignment in AssignmentsForCourse:
            submissionsByStudent = Submissions.objects.filter(Assign_ID = assignment).filter(Student_ID = StudentObject[0].Person_ID)
            if(submissionsByStudent.count() == 0):
                now = timezone.now()
                if (assignment.End_Time > now):
                    assignContextObject = dict(Course = course,assignment = assignment)
                    pendingAssignments.append(assignContextObject)
    return render(request, 'student/AssgnSubStatusPending.html', dict(pendingAssignments=pendingAssignments))




def AssgnSubStatusOverdue(request):
    user =  request.user;
    overdueAssignments = []
    StudentObject=Personnel.objects.filter(LDAP=user.id)
    CoursesByStudent = Students_Courses.objects.filter(Student_ID=StudentObject[0].Person_ID)
    for course in CoursesByStudent:
        AssignmentsForCourse = Assignment.objects.filter(Course_ID = course.Course_ID.Course_ID)
        for assignment in AssignmentsForCourse:
            submissionsByStudent = Submissions.objects.filter(Assign_ID = assignment).filter(Student_ID = StudentObject[0].Person_ID)
            if(submissionsByStudent.count() == 0):
                now = timezone.now()
                if (assignment.End_Time < now):
                    assignContextObject = dict(Course = course,assignment = assignment)
                    overdueAssignments.append(assignContextObject)
    return render(request, 'student/AssgnSubStatusOverdue.html', dict(overdueAssignments=overdueAssignments))





def AssgnSubStatusSubmitted(request):
    user =  request.user;
    submittedAssignments = []
    StudentObject=Personnel.objects.filter(LDAP=user.id)
    CoursesByStudent = Students_Courses.objects.filter(Student_ID=StudentObject[0].Person_ID)
    for course in CoursesByStudent:
        AssignmentsForCourse = Assignment.objects.filter(Course_ID = course.Course_ID.Course_ID)
        for assignment in AssignmentsForCourse:
            submissionsByStudent = Submissions.objects.filter(Assign_ID = assignment).filter(Student_ID = StudentObject[0].Person_ID)
            if(submissionsByStudent.count() != 0):
                assignContextObject = dict(Course = course,assignment = assignment,submission = submissionsByStudent)
                submittedAssignments.append(assignContextObject)
    return render(request, 'student/AssgnSubStatusSubmitted.html', dict(submittedAssignments=submittedAssignments))

def addDropCourses(request):
    user = request.user
    StudentObject=Personnel.objects.filter(LDAP=user.id)
    
    courses = Courses.objects.all()
    courseSelectionOption = []
    for course in courses:
        CourseByStudent = Students_Courses.objects.filter(Student_ID=StudentObject[0].Person_ID).filter(Course_ID = course.Course_ID)
        selected = True
        if CourseByStudent.count() == 0:
            selected = False
        FacultyForCourse = Instructors_Courses.objects.filter(Course_ID = course.Course_ID)
        if(FacultyForCourse.count() != 0):
            faculty = FacultyForCourse[0].Inst_ID
        else:
            faculty = "Yet To Be Decided"
        courseSelectionObj = dict(course=course,selected=selected,faculty = faculty)
        courseSelectionOption.append(courseSelectionObj)
    return render(request,'student/CourseRegistration.html',dict(courses = courseSelectionOption))

def registerCourses(request):
    user = request.user
    StudentObject=Personnel.objects.filter(LDAP=user.id)
    courses = Courses.objects.all()
    for course in courses:
        CourseByStudent = Students_Courses.objects.filter(Student_ID=StudentObject[0].Person_ID).filter(Course_ID = course.Course_ID)
        if (request.POST.get(str(course.Course_ID)) and CourseByStudent.count() == 0):       
            registerStudent = CourseByStudent.create(Student_ID = StudentObject[0],Course_ID = course,Reg_Date = datetime.datetime.now())
        elif (CourseByStudent.count() != 0 and not request.POST.get(str(course.Course_ID))):
            CourseByStudent.delete()
    return render(request, "student/index.html", {})


