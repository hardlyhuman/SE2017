from __future__ import unicode_literals
from django.template.context import RequestContext
import json as simplejson
from django.http import HttpResponse
import json
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template import loader
from django.shortcuts import render_to_response
from home.models import *
from home.models import Assignment
from .forms import UploadFileForm
from home.serializers import *

import json



OPTIONS = """{  timeFormat: "H:mm",
                header: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'month,agendaWeek,agendaDay',
                },
                allDaySlot: false,
                firstDay: 0,
                weekMode: 'liquid',
                slotMinutes: 15,
                defaultEventMinutes: 30,
                minTime: 8,
                maxTime: 20,
                editable: false,
                dayClick: function(date, allDay, jsEvent, view) {
                    if (allDay) {       
                        $('#calendar').fullCalendar('gotoDate', date)      
                        $('#calendar').fullCalendar('changeView', 'agendaDay')
                    }
                },
                eventClick: function(event, jsEvent, view) {
                    if (view.name == 'month') {     
                        $('#calendar').fullCalendar('gotoDate', event.start)      
                        $('#calendar').fullCalendar('changeView', 'agendaDay')
                    }
                },
            }"""

def index(request):
	# data=CalendarEvent.objects.all()
	# #return HttpResponse(data)
	# context={'data':json.dumps(data)}
	all_events = Events.objects.all()
	serializer = EventsSerializer(all_events, many=True)
	a=[]
	for i in serializer.data:

		a.append({"title":i["Event_Name"],"start":i["Event_Date"],"allDay":True})
	print serializer.data
	return render(request, 'fullcalendar/calendar.html',{"Events":json.dumps(a)})
	
	
	
def ViewProfs(request):
    CourseList = []
    if request.user.personnel.Role.Role_name == 'Faculty':
	request.session['Prof_Name']=request.user.username
        person_id = request.user.personnel.Person_ID
        IC = Instructors_Courses.objects.all()
        for i in range(0, len(IC)):
            if person_id == IC[i].Inst_ID.Person_ID:
                CourseList.append(IC[i].Course_ID.Course_Name)
	if CourseList==[]:
            flag=0
	    
	else:
            flag=1
    template = loader.get_template('prof.html')
    context = {'flag':flag,'Courses':CourseList,'Prof_Name':request.session['Prof_Name']}
    return HttpResponse(template.render(context, request))
def CoursePage(request):		
	if request.POST.get('action')=='Save':
		course=Courses.objects.get(Course_Name=request.session['course'])
		course.Course_description = request.POST.get('coursedes')
        	course.save()		
	elif request.POST.get('action')=="submit":
		request.session['course'] =request.POST.get('dropdown')
	course=Courses.objects.get(Course_Name=request.session['course']) 				
    	template = loader.get_template('prof1.html')
    	context = {'Course':course,'CourseName':request.session['course']}
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
    s=0;
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            courses = Courses.objects.all()
            for corse in courses:
                if corse.Course_Name == request.session['course']:
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
        context = {'Courses': courses1,'CourseName':request.session['course'], 'IC': IClist, 'Prof_Name': request.user.username}
    return HttpResponse(template.render(context, request))

def ViewAttendance(request):	
    	studentcount={}
	sessioncount=0
	students=Attendance.objects.all()
    	classes=Attendance_Session.objects.all()
	for Class in classes:
		if Class.Course_Slot.Course_ID.Course_Name==request.session['course']:
			sessioncount=sessioncount+1
		
	for student in students:
		value=[0,1]
		value[0]=student.Student_ID.LDAP.username
		value[1]=0
		studentcount[student.Student_ID.Person_ID]=value	
	for student in students:
		if student.ASession_ID.Course_Slot.Course_ID.Course_Name==request.session['course'] and student.Marked=='A':
			studentcount[student.Student_ID.Person_ID][1]=studentcount[student.Student_ID.Person_ID][1]+1
	if request.method=="POST":
		return HttpResponse(request.POST.get('abc'))			    
    	template = loader.get_template('attendance.html')
    	context = {'classes':studentcount,'CourseName':request.session['course'],'workingdays':sessioncount}
    	return HttpResponse(template.render(context, request))	

def EnterMarks(request):
	assignidlist=[]
	idlist=[]
	studentlist=[]
	studentdict={}
	assignid=Assignment.objects.all()
	students=Students_Courses.objects.all()
	
	for assign in assignid:
		if assign.Course_ID.Course_Name==request.session['course']:
			assignidlist.append(assign.Assign_ID)
	for student in students:
		if student.Course_ID.Course_Name==request.session['course']:
			studentlist.append(student)
			studentdict[student.Student_ID.Person_ID]=[]
	for i in range(1,len(assignid)+1):
		idlist.append(i)
	if request.method=="POST":
		return HttpResponse(request.POST.get('assign'))
	template = loader.get_template('marks.html')
    	context = {'assignid':idlist,'CourseName':request.session['course'],'students':studentlist,'studentdict':studentdict}
    	return HttpResponse(template.render(context, request))

