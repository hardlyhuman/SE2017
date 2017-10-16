# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import datetime
# from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from home.models import *


# Create your views here.


"""

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
"""
def dashboard(request):
    pass

@login_required(login_url="/login/")
class register(FormView):

    def get(self, request, *args, **kwargs):
        userid = request.personnel.Person_ID
        user = Personnel.objects.get(Person_ID=userid)

        if datetime.now().month < 8:
            year_of_study = datetime.now().year - user.Year
        else:
            year_of_study = datetime.now().year - user.Year + 1


        CoursesOffering = Courses.objects.all().filter(Course_Year=year_of_study)

        template_name = "student/CourseRegistration.html"
        context = dict(CourseList=CoursesOffering)

        return render(request, template_name, context)


@login_required(login_url="/login/")
class DropCourse(FormView):

    def get(self, request, *args, **kwargs):
        userid = request.personnel.Person_ID
        user = Personnel.objects.get(Person_ID=userid)

        if datetime.now().month < 8:
            year_of_study = datetime.now().year - user.Year
        else:
            year_of_study = datetime.now().year - user.Year + 1

        MyCourses = [i.Course.course_Name for i in userid.Students_Courses_set.all()]
        RegCourses = [Courses.objects.get(Course_Name=i) for i in MyCourses]

        template_name = 'student/DropCourse.html'
        context = dict(RegisteredCourses=RegCourses)

        return render(request, template_name, context)



def unregister(request):

    courses_selected = Courses.objects.filter(id__in=request.POST.getlist('checks[]'))
    userid = request.personnel.Person_ID
    user = Personnel.objects.get(Person_ID=userid)

    if datetime.now().month < 8:
        year_of_study = datetime.now().year - user.Year
    else:
        year_of_study = datetime.now().year - user.Year + 1

    for course in courses_selected:

        Students_Courses.objects.filter(Student_ID=userid).get(Course_ID__Course_Name= course).delete()

    MyCourses = [i.Course.course_Name for i in userid.Students_Courses_set.all()]
    RegCourses = [Courses.objects.get(Course_Name=i) for i in MyCourses]

    template_name = 'student/MyCourses.html'
    context = dict(RegisteredCourses=RegCourses)

    return render(request, template_name, context)


def register_course(request):

    courses_selected = Courses.objects.filter(id__in=request.POST.getlist('checks[]'))
    userid = request.personnel.Person_ID
    user = Personnel.objects.get(Person_ID=userid)

    if datetime.now().month < 8:
        year_of_study = datetime.now().year - user.Year
    else:
        year_of_study = datetime.now().year - user.Year + 1

    MyCourses = [i.Course.course_Name for i in userid.Students_Courses_set.all()]
    RegCourses = [Courses.objects.get(Course_Name=i) for i in MyCourses]

    for course in courses_selected:
        if course not in RegCourses:
            SC = Students_Courses()
            SC.Student_ID = userid
            SC.Course_ID = course
            SC.save()

    userid = request.personnel.Person_ID
    user = Personnel.objects.get(Person_ID=userid)

    if datetime.now().month < 8:
        year_of_study = datetime.now().year - user.Year
    else:
        year_of_study = datetime.now().year - user.Year + 1

    MyCourses = [i.Course.course_Name for i in userid.Students_Courses_set.all()]
    RegCourses = [Courses.objects.get(Course_Name=i) for i in MyCourses]

    template_name = 'student/MyCourses.html'
    context = dict(RegisteredCourses=RegCourses)

    return render(request, template_name, context)


def AddCourse(request):
    return render(request, 'student/AddCourse.html')





def AssgnSubStatus(request, StuId):

    AssgnId = 0
    Assgn = Submissions.objects.all().filter(Student_ID__submissions=StuId)
    for each in Assgn:
        if each['Assign_ID']==AssgnId:
            status = each['Sub_Status']
            score = each['Score']



    return render(request, 'student/AssgnSubStatus.html', dict(status=status, score=score))


