
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
import json
from django.http import *
from django.shortcuts import *
from django.template import *
from home.models import *
from home.serializers import *
import easygui
from django.utils import *
from datetime import datetime
from dateutil.parser import parse
@login_required
def index(request):
	all_events = Events.objects.all()
	serializer = EventsSerializer(all_events, many=True)
	a=[]
	for i in serializer.data:

		a.append({"title":i["Event_Name"],"start":i["Event_Date"],"allDay":True})
	print serializer.data
	return render(request, 'fullcalendar/calendar.html',{"Events":json.dumps(a)})


@login_required
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

@login_required
def CoursePage(request):
	if request.POST.get('action')=='Save':

		course=Courses.objects.get(Course_Name=request.session['course'])
		course.Course_description = request.POST.get('coursedes')
		try:
        		course.save()
		except:
			easygui.msgbox("Oops!Data Too Long.",title="ERROR")

	else:
		request.session['course'] =request.POST.get('dropdown')
	course=get_object_or_404(Courses,Course_Name=request.session['course'])
    	template = loader.get_template('prof1.html')
    	context = {'Course':course,'CourseName':request.session['course']}
    	return HttpResponse(template.render(context, request))



@login_required
def AddAssignment(request):
    s=0

    if request.method == 'POST':

  	date_joined =datetime.now()
	if parse(request.POST.get('enddate'))>=date_joined:
		courses = Courses.objects.all()
		for corse in courses:
			if corse.Course_Name == request.session['course']:
		            course = Courses.objects.get(Course_Name=corse.Course_Name)
		            break
		instance = Assignment(Course_ID=course, Assignment_File=request.FILES['file'],End_Time=request.POST.get('enddate'))
		instance.save()
	    	s=1
	else:
		s=2
	return render(request, 'forms.html',{'CourseName':request.session['course'],'s':s})

    else:

		if 'course' in request.session:

			s=0
    			return render(request, 'forms.html',{'CourseName':request.session['course'],'s':s})
		else:
			easygui.msgbox("please select a course",title="ERROR")
			return redirect('http:../ViewProfs/')
@login_required
def ViewAssignment(request):
     asslist = []
     Assignments = Assignment.objects.all()
     for ass in Assignments:
	if 'course' in request.session:
     		if ass.Course_ID.Course_Name ==request.session['course'] and ass.End_Time.date()!=datetime.strptime('1900-01-01',"%Y-%m-%d").date():
			print ass.Assignment_File
			asslist.append(ass)
	else:
		easygui.msgbox("please select a course",title="ERROR")
		return redirect('http:../ViewProfs/')
     return render(request, 'assignment.html', {'Assignments': asslist,'CourseName':request.session['course']})


@login_required
def OfferCourses(request):
    if request.method == 'POST':
        person_id = request.user.personnel.Person_ID
        person = Personnel.objects.get(Person_ID=person_id)
        courseids = request.POST.getlist('courses[]')
        for cid in courseids:
            corse = Courses.objects.get(Course_ID=cid)
            IC = Instructors_Courses(Course_ID=corse, Inst_ID=person, Start_Date='2017-1-1',End_Date='2017-1-1')
            IC.save()
	return redirect('http:../offercourses/')


    else:
        IC = Instructors_Courses.objects.all()
        IClist = []
	courselist=[]
        for ic in IC:
            IClist.append(ic.Course_ID)
        person_id = request.user.personnel.Person_ID
        courses = Courses.objects.all()
        courses1 = []
        for corse in courses:
            if corse not in IClist:
                courses1.append(corse)
	for course in courses:
		courselist.append(course.Course_ID)
		courselist.append(course.Course_Name)

        template = loader.get_template('reg.html')
        context = {'Courses': courses1,'Courses1':json.dumps(courselist), 'IC': IC, 'Prof_Name': request.user.username}
    	return HttpResponse(template.render(context, request))
@login_required
def ViewAttendance(request):
	sessionlist={}
	sessions=Attendance_Session.objects.all()
	students=Attendance.objects.all()
	for session in sessions:
		if session.Course_Slot.Course_ID.Course_Name==request.session['course']:
			sessionlist[session.Session_ID]=[session.Date_time.date,0]
	for session in sessionlist:
		for student in students:
			if session==student.ASession_ID.Session_ID and student.Marked=='P':
				sessionlist[session][1]=sessionlist[session][1]+1
    	template = loader.get_template('attendance.html')
    	context = {'sessions':sessionlist,'CourseName':request.session['course']}
    	return HttpResponse(template.render(context, request))
@login_required
def ViewAttendanceDetails(request):
	slotid=request.GET.get('id')
	session=Attendance_Session.objects.get(Session_ID=slotid)
	students=Attendance.objects.all()
	studentlist=[]
	for student in students:
		if str(student.ASession_ID.Session_ID)==str(slotid):
			studentlist.append(student)
	template = loader.get_template('details.html')
    	context = {'students':studentlist,'CourseName':request.session['course'],'date':session.Date_time.date}
    	return HttpResponse(template.render(context, request))




@login_required
def MyLibrary(request):
    s=0
    libfiles=[]
    if request.method == 'POST':
	courses = Courses.objects.all()
	libfiles=request.FILES.getlist("files")
	for corse in courses:
		if corse.Course_Name == request.session['course']:
			course = Courses.objects.get(Course_Name=corse.Course_Name)
		        break
	for libfile in libfiles:
		instance = Assignment(Course_ID=course, Assignment_File=libfile,End_Time='1900-01-01')
		instance.save()
	s=1
	asslist = []
     	Assignments = Assignment.objects.all()
     	for ass in Assignments:
		if ass.Course_ID.Course_Name ==request.session['course'] and ass.End_Time.date()==datetime.strptime('1900-01-01',"%Y-%m-%d").date():
			asslist.append(ass)
    	return render(request, 'lib.html',{'MyLibList':asslist,'CourseName':request.session['course'],'s':s})


    else:
	asslist = []
	s=0
     	Assignments = Assignment.objects.all()
     	for ass in Assignments:
		if ass.Course_ID.Course_Name ==request.session['course'] and ass.End_Time.date()==datetime.strptime('1900-01-01',"%Y-%m-%d").date():
			asslist.append(ass)
	return render(request, 'lib.html',{'MyLibList':asslist,'CourseName':request.session['course'],'s':s})
