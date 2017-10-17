from __future__ import unicode_literals

import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template import loader

from home.models import *
from home.models import Assignment
from .forms import UploadFileForm


def ViewProfs(request):
    CourseList = []
    CoursedesList = []
    if request.user.personnel.Role.Role_name == 'faculty':
        person_id = request.user.personnel.Person_ID
        IC = Instructors_Courses.objects.all()
        for i in range(0, len(IC)):
            if person_id == IC[i].Inst_ID.Person_ID:
                CourseList.append(IC[i].Course_ID.Course_Name)
                CoursedesList.append(IC[i].Course_ID.Course_description)
    template = loader.get_template('prof1.html')
    context = {'Courses': json.dumps(CourseList), 'Coursedes': json.dumps(CoursedesList),
               'Prof_Name': request.user.username}
    return HttpResponse(template.render(context, request))


def ViewRegisteredStudents(request):
    studentlist = []
    course_name = request.GET.get('name')
    students = Students_Courses.objects.all()
    for student in students:
        if course_name == student.Course_ID.Course_Name:
            studentlist.append(student.Student_ID.LDAP.username)
    template = loader.get_template('student.html')
    context = {'Students': json.dumps(studentlist), 'Course': course_name}
    return HttpResponse(template.render(context, request))


def AddAssignment(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            courses = Courses.objects.all()
            for corse in courses:
                if corse.Course_Name == request.POST.get('dropdown'):
                    course = Courses.objects.get(Course_Name=corse.Course_Name)
                    break
            instance = Assignment(Course_ID=course, Assignment_File=request.FILES['file'])
            instance.save()
            return HttpResponse("Your File has been uploaded successfully!!!")
    else:
        CourseList = []
        form = UploadFileForm()
        if request.user.personnel.Role.Role_name == 'faculty':
            person_id = request.user.personnel.Person_ID
            IC = Instructors_Courses.objects.all()
            for i in range(0, len(IC)):
                if person_id == IC[i].Inst_ID.Person_ID:
                    CourseList.append(IC[i].Course_ID.Course_Name)
    return render(request, 'forms.html',
                  {'Courses': CourseList, 'Prof_Name': request.user.username, 'form': form, 'request': request})


def delete(request):
    if request.method != 'POST':
        raise Http404
    docId = request.POST.getlist('Assignment_File[]')
    for did in docId:
        docToDel = get_object_or_404(Assignment, Assign_ID=did)
        docToDel.Assignment_File.delete()
        docToDel.delete()
    return HttpResponse("Your File has been deleted successfully!!! ")


def Delass(request):
    if request.method == 'POST':
        asslist = []
        Assignments = Assignment.objects.all()
        for ass in Assignments:
            if ass.Course_ID.Course_Name == request.POST.get('dropdown'):
                asslist.append(ass)
        return render(request, 'assignment.html', {'Assignments': asslist})
    else:
        CourseList = []
        if request.user.personnel.Role.Role_name == 'faculty':
            person_id = request.user.personnel.Person_ID
            IC = Instructors_Courses.objects.all()
            for i in range(0, len(IC)):
                if person_id == IC[i].Inst_ID.Person_ID:
                    CourseList.append(IC[i].Course_ID.Course_Name)
    return render(request, 'course_page.html', {'Courses': CourseList})


def EditCourseDescription(request):
    if request.method == 'POST':
        course = request.POST.get('dropdown')
        courseobj = Courses.objects.get(Course_Name=course)
        courseobj.Course_description = request.POST.get('coursedes')
        courseobj.save()

        return HttpResponse("Successfully updated!!!")
    else:
        CourseList = []
        if request.user.personnel.Role.Role_name == 'faculty':
            person_id = request.user.personnel.Person_ID
            IC = Instructors_Courses.objects.all()
            for i in range(0, len(IC)):
                if person_id == IC[i].Inst_ID.Person_ID:
                    CourseList.append(IC[i].Course_ID.Course_Name)
    return render(request, 'editcourse.html', {'Courses': CourseList})


def OfferCourses(request):
    if request.method == 'POST':
        person_id = request.user.personnel.Person_ID
        person = Personnel.objects.get(Person_ID=person_id)
        courseids = request.POST.getlist('courses[]')
        startdate = request.POST.get('startdate')
        enddate = request.POST.get('enddate')
        for cid in courseids:
            corse = Courses.objects.get(Course_ID=cid)
            IC = Instructors_Courses(Course_ID=corse, Inst_ID=person, Start_Date=startdate, End_Date=enddate)
            IC.save()
        return HttpResponse("Successfully Inserted!!!")
    else:
        IC = Instructors_Courses.objects.all()
        IClist = []
        for ic in IC:
            IClist.append(ic.Course_ID)
        person_id = request.user.personnel.Person_ID
        courses = Courses.objects.all()
        courses1 = []
        for corse in courses:
            if corse not in IClist:
                courses1.append(corse)
        template = loader.get_template('reg.html')
        context = {'Courses': courses1, 'IC': IClist, 'Prof_Name': request.user.username}
    return HttpResponse(template.render(context, request))
