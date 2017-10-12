# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from home import urls


# Create your views here.
@login_required(login_url="/login/")
def dashboard(request):
    return render(request, 'student/dashboard.html')


@login_required(login_url="/login/")
def ViewAttendance(request):
    return render(request, 'student/ViewAttendance.html')


@login_required(login_url="/login/")
def CourseRegistration(request, year):

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
def AssgnSubStatus(request):
    return render(request, 'student/AssgnSubStatus.html')
