# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def dashboard(request):
	return render(request, 'student/dashboard.html')
	
	
	
def ViewAttendance(request):
	return render(request, 'student/ViewAttendance.html')
	
	
def CourseRegistration(request):
	return render(request, 'student/CourseRegistration.html')
	
	
def MarkAttendance(request):
	return render(request, 'student/MarkAttendance.html')
	
	
	
def AddCourse(request):
	return render(request, 'student/AddCourse.html')
	
	
def DropCourse(request):
	return render(request, 'student/DropCourse.html')
	
	
def AssgnSubStatus(request):
	return render(request, 'student/AssgnSubStatus.html')
