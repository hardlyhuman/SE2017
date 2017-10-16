# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

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


def ViewRegCourse(request):
    CourseList = []
    if request.user.personnel.Role.Role_name == "student":
        person_id = request.user.personnel.Person_ID
        SC = Students_Courses.objects.all()
        for i in range(0, len(SC)):
            if person_id == SC[i].Student_ID.Person_ID:
                CourseList.append(SC[i].Course_ID.Course_Name)

    template = loader.get_template('student/dashboard.html')
    context = dict(Course=json.dumps(CourseList), Stud_Name=request.user.username)
    return HttpResponse(template.render(context, request))
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

""""@login_required(login_url="/login/")
def CourseRegistration(request, ):

    
    course = None
    form_class = CourseEnrollForm
    
    return render(request, 'student/CourseRegistration.html', {'courses': c})"""
"""
class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm


    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView,
                     self).form_valid(form)

    @property
    def get_success_url(self):
        return reverse_lazy('student_course_detail',
                            args=[self.course.id])
"""
@login_required(login_url="/login/")
class register(FormView):

    def get(self, request, *args, **kwargs):
        userid = request.personnel.Person_ID
        user = Personnel.objects.get(Person_ID=userid)

        year_of_study = user.Year

        CoursesOffering = Courses.objects.all().filter(Course_Year=year_of_study)

        template_name = "student/CourseRegistration.html"
        context = dict(CourseList=CoursesOffering)

        return render(request, template_name, context)


@login_required(login_url="/login/")
class DropCourse(FormView):

    def get(self, request, *args, **kwargs):
        userid = request.personnel.Person_ID
        user = Personnel.objects.get(Person_ID=userid)

        year_of_study = user.Year
        MyCourses = [i.Course.course_Name for i in userid.Students_Courses_set.all()]

        RegCourses = [Courses.objects.get(Course_Name=i) for i in MyCourses]

        template_name = 'student/DropCourse.html'

        context = dict(RegisteredCourses=RegCourses)

        return render(request, template_name, context)



def unregister(request):

    courses_selected = Courses.objects.filter(id__in=request.POST.getlist('checks[]'))
    userid = request.personnel.Person_ID
    user = Personnel.objects.get(Person_ID=userid)

    year_of_study = user.Year

    for course in courses_selected:

        Students_Courses.objects.filter(Student_ID=userid).get(Course_ID__Course_Name= course).delete()

    MyCourses = [i.Course.course_Name for i in userid.Students_Courses_set.all()]
    RegCourses = [Courses.objects.get(Course_Name=i) for i in MyCourses]

    template_name = 'student/MyCourses.html'

    context = dict(RegisteredCourses=RegCourses)

    return render(request, template_name, context)




def MarkAttendance(request):
    return render(request, 'student/MarkAttendance.html')


def AddCourse(request):
    return render(request, 'student/AddCourse.html')


def DropCourse(request):
    return render(request, 'student/DropCourse.html')

class ViewAttendance(TemplateView):
    template_name = 'student/ViewAttendance.html'

    def get(self, request, *args, **kwargs):
        try:
            if request.user.personnel.Role.Role_name == "student":
                person_id = request.user.personnel.Person_ID
            my_courses_list = [i.Course.course_title for i in person_id.Students_Courses_set.all()]
            courses_registered = [model_to_dict(Students_Courses.objects.get(course_title=i)) for i in my_courses_list]

            dic = {}
            absent_on = [[i.course_title, i.date] for i in
                         Attendance.objects.filter(student_id=person_id.Stu).filter(status="A")]

            # Making a dictionary { Course: [date1, date2, ....], .... }
            for c in absent_on:
                if c[0] not in dic:
                    dic[c[0]] = [c[1]]
                else:
                    dic[c[0]] += [c[1]]

            # Converting date to a dic as follows - { Month1: [day1, day2, .. ], ..... }
            month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                           "October", "November", "December"]
            for course in dic:

                month_dic = {}
                for date in dic[course]:

                    t_month = month_names[date.month - 1]
                    if t_month not in month_dic:
                        month_dic[t_month] = [date]
                    else:
                        month_dic[t_month] += [date]
                dic[course] = month_dic

            context = {'courses_registered': courses_registered,  'absent_on': dic}

            return render(request, self.template_name, context)
        except:
            return render(request, self.template_name, {'error_message': 'No data found'})


def AssgnSubStatus(request, StuId):

    AssgnId = 0
    Assgn = Submissions.objects.all().filter(Student_ID__submissions=StuId)
    for each in Assgn:
        if each['Assign_ID']==AssgnId:
            status = each['Sub_Status']
            score = each['Score']



    return render(request, 'student/AssgnSubStatus.html', dict(status=status, score=score))


