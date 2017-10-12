# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from home import urls
from home.models import Courses, Submissions, Attendance, Attendance_Session


# Create your views here.
@login_required(login_url="/login/")
def dashboard(request):
    return render(request, 'student/dashboard.html')


@login_required(login_url="/login/")
def ViewAttendance(request, StuId):
    CourseId = 0
    Total = 25
    present = 0
    Atnd = Attendance.objects.select_related("ASession_ID")
    for each in Atnd:
        if each['Student_ID'] == StuId:
            if each['Marked'] == 'P':
                present += 1
    return render(request, 'student/ViewAttendance.html', {'Total': Total, 'present': present, 'Absent': Total - present, 'percent': (present/Total)*100})


@login_required(login_url="/login/")
def CourseRegistration(request, year):
    assert isinstance(year, object)
    courses = Courses.objects.all().filter(batch=year)
    return render(request, 'student/CourseRegistration.html')


@login_required(login_url="/login/")
def MarkAttendance(request):
    return render(request, 'student/MarkAttendance.html')


@login_required(login_url="/login/")
def AddCourse(request):
    return render(request, 'student/AddCourse.html')


@login_required(login_url="/login/")
def DropCourse(request):
    return render(request, 'student/DropCourse.html')


@login_required(login_url="/login/")
def AssgnSubStatus(request, StuId):

    AssgnId = 0
    Assgn = Submissions.objects.all().filter(Student_ID__submissions=StuId)
    for each in Assgn:
        if each['Assign_ID']==AssgnId:
            status = each['Sub_Status']
            score = each['Score']

    return render(request, 'student/AssgnSubStatus.html', dict(status=status, score=score))
