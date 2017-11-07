from django import template
from django.contrib.auth import authenticate
import sys
import jwt
import datetime
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django import template
from django.http import HttpResponse,JsonResponse
from .forms import PersonnelForm
from django.views.decorators.csrf import csrf_exempt
from ldif3 import LDIFParser
from rest_framework import exceptions,status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework_jwt.settings import api_settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.models import User
from .forms import *
from .models import *
from math import radians, cos, sin, asin, sqrt
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])


    #harvesine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371000.0 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

#custom decorators for JWT verification
def jwt_accept(function):#request function
	def wrap(request, *args, **kwargs):
		try:
			token = request.META['HTTP_AUTHORIZATION'].split()[1]
		except KeyError:
			return Response({"message","No Token Found"}, status=status.HTTP_400_BAD_REQUEST)
		try:
			payload = jwt_decode_handler(token)
		except jwt.ExpiredSignature:
			return Response({"message","Signature has expired."}, status=status.HTTP_406_NOT_ACCEPTABLE)
		except jwt.DecodeError:
			return Response({"message","Error decoding signature."}, status=status.HTTP_400_BAD_REQUEST)
		except jwt.InvalidTokenError:
			return Response({"message","Invalid Token"}, status=status.HTTP_401_UNAUTHORIZED)
		return function(request, *args, **kwargs)
	wrap.__doc__=function.__doc__
	wrap.__name__=function.__name__
	return wrap

# importing all models

from .models import *
from math import radians, cos, sin, asin, sqrt
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
# importing all models
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])


    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371000.0 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

#custom decorators for JWT verification
def jwt_accept(function):
	def wrap(request, *args, **kwargs):
		try:
			token = request.META['HTTP_AUTHORIZATION'].split()[1]
		except KeyError:
			return Response({"message","No Token Found"}, status=status.HTTP_400_BAD_REQUEST)
		try:
			payload = jwt_decode_handler(token)
		except jwt.ExpiredSignature:
			return Response({"message","Signature has expired."}, status=status.HTTP_406_NOT_ACCEPTABLE)
		except jwt.DecodeError:
			return Response({"message","Error decoding signature."}, status=status.HTTP_400_BAD_REQUEST)
		except jwt.InvalidTokenError:
			return Response({"message","Invalid Token"}, status=status.HTTP_401_UNAUTHORIZED)
		return function(request, *args, **kwargs)
	wrap.__doc__=function.__doc__
	wrap.__name__=function.__name__
	return wrap
#..............................................................
#..............................................................
#..............................................................
#..............................................................

# Create your views here.
PRIVATE_IPS_PREFIX = ('10.', '172.', '192.',)
register = template.Library()
@login_required(login_url="login/")#login credentials
def index(request):
    if request.user.personnel.Role.Role_name == "Faculty":
        return HttpResponseRedirect('../faculty/ViewProfs')
    if request.user.personnel.Role.Role_name == "Student":
        return HttpResponseRedirect('../student')
    now = datetime.datetime.now()
    remote_address = request.META.get('REMOTE_ADDR')
    # set the default value of the ip to be the REMOTE_ADDR if available
    # else None
    ip = remote_address
    # try to get the first non-proxy ip (not a private ip) from the
    # HTTP_X_FORWARDED_FOR
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        # remove the private ips from the beginning
        while (len(proxies) > 0 and proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
            # take the first ip which is not a private one (of a proxy)
        if len(proxies) > 0:
            ip = proxies[0]
    html = "IP: %s" % ip

    return render(request, "home/index.html", {'html': html, 'now': now})
#..............................................................
#..............................................................
#..............................................................
#..............................................................
#..............................................................
#..............................................................
@csrf_exempt
@api_view(['GET', 'POST'])
@jwt_accept
def people(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        all_people = Personnel.objects.all()
        serializer = PersonnelSerializer(all_people, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PersonnelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'PUT','DELETE'])#requests for get, pull or delete
@jwt_accept
#..............................................................
#..............................................................
#..............................................................
#..............................................................
#..............................................................


# importing all models


def person(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        person = Personnel.objects.get(pk=pk)
    except Personnel.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PersonnelSerializer(person)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PersonnelSerializer(person, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        person.delete()
        return HttpResponse(status=204)
#..............................................................
#..............................................................
#..............................................................
#..............................................................
#..............................................................
#..............................................................
#..............................................................
#..............................................................
@csrf_exempt
@api_view(['GET', 'POST'])
@jwt_accept
def departments(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        all_departments = Department.objects.all()
        serializer = DepartmentSerializer(all_departments, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DepartmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
#..............................................................
#..............................................................
#..............................................................
#..............................................................

@csrf_exempt
@api_view(['GET', 'POST','DELETE'])
@jwt_accept
def department(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        one_department = Department.objects.get(pk=pk)
    except Department.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DepartmentSerializer(one_department)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DepartmentSerializer(one_department, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        one_department.delete()
        return HttpResponse(status=204)
#..............................................................
#..............................................................
#..............................................................
#..............................................................

@csrf_exempt
@api_view(['GET', 'POST'])
@jwt_accept
def add_view_roles(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        all_roles = Roles.objects.all()
        serializer = RolesSerializer(all_roles, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RolesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
#..............................................................
#..............................................................
#..............................................................
#..............................................................

@csrf_exempt
@api_view(['GET', 'POST','DELETE'])
@jwt_accept
def role(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        one_role = Roles.objects.get(pk=pk)
    except Roles.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = RolesSerializer(one_role)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = RolesSerializer(one_role, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        one_role.delete()
        return HttpResponse(status=204)
#..............................................................
#..............................................................
#..............................................................
#..............................................................

@csrf_exempt
@api_view(['GET', 'POST'])
@jwt_accept
def add_view_courses(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        all_courses = Courses.objects.all()
        serializer = CoursesSerializer(all_courses, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CoursesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

#..............................................................
#..............................................................
#..............................................................

@csrf_exempt
@api_view(['GET', 'DELETE'])
@jwt_accept
def course(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        one_course = Courses.objects.get(pk=pk)
    except Courses.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CoursesSerializer(one_course)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CoursesSerializer(one_course, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        one_course.delete()
        return HttpResponse(status=204)


@csrf_exempt
@api_view(['GET', 'POST'])
@jwt_accept
def add_view_documents(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        all_documents = Documents.objects.all()
        serializer = DocumentsSerializer(all_documents, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DocumentsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'PUT','DELETE'])
@jwt_accept
def document(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        one_document = Documents.objects.get(pk=pk)
    except Documents.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DocumentsSerializer(one_document)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DocumentsSerializer(one_document, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        one_document.delete()
        return HttpResponse(status=204)


@csrf_exempt
@api_view(['GET','POST'])
@jwt_accept
def add_view_assignments(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        all_assignments = Assignment.objects.all()
        serializer = AssignmentSerializer(all_assignments, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AssignmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'PUT','DELETE'])
@jwt_accept
def assignment(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        one_assignment = Assignment.objects.get(pk=pk)
    except Assignment.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AssignmentSerializer(one_assignment)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AssignmentSerializer(one_document, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        one_assignment.delete()
        return HttpResponse(status=204)


@csrf_exempt
@api_view(['GET', 'POST'])
@jwt_accept
def add_view_submissions(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        all_submissions = Submissions.objects.all()
        serializer = SubmissionsSerializer(all_submissions, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SubmissionsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'PUT','DELETE'])
@jwt_accept
def submission(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        one_submission = Submissions.objects.get(pk=pk)
    except Submissions.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SubmissionsSerializer(one_submission)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SubmissionsSerializer(one_submission, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        one_submission.delete()
        return HttpResponse(status=204)


@csrf_exempt
@api_view(['GET', 'POST'])
@jwt_accept
def add_view_IC(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        all_IC = Instructors_Courses.objects.all()
        serializer = ICSerializer(all_IC, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ICSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET','PUT','DELETE'])
@jwt_accept
def IC(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        one_IC = Instructors_Courses.objects.get(pk=pk)
    except Instructors_Courses.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ICSerializer(one_IC)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ICSerializer(one_IC, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        one_IC.delete()
        return HttpResponse(status=204)


@csrf_exempt
@api_view(['GET','POST'])
@jwt_accept
def add_view_SC(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        all_SC = Students_Courses.objects.all()
        serializer = SCSerializer(all_SC, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SCSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'PUT','DELETE'])
@jwt_accept
def SC(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        one_SC = Students_Courses.objects.get(pk=pk)
    except Students_Courses.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SCSerializer(one_SC)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SCSerializer(one_SC, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        one_SC.delete()
        return HttpResponse(status=204)


@csrf_exempt
@api_view(['GET', 'POST'])
@jwt_accept
def add_view_events(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        all_events = Events.objects.all()
        serializer = EventsSerializer(all_events, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EventsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'PUT','DELETE'])
@jwt_accept
def event(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        one_event = Events.objects.get(pk=pk)
    except Events.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = EventsSerializer(one_event)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = EventsSerializer(one_event, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        one_event.delete()
        return HttpResponse(status=204)


@csrf_exempt
@api_view(['GET', 'POST',])
@jwt_accept
def add_view_SP(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        all_SP = Student_Period.objects.all()
        serializer = SPSerializer(all_SP, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SPSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'PUT','DELETE'])
@jwt_accept
def SP(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        one_SP = Student_Period.objects.get(pk=pk)
    except Student_Period.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SPSerializer(one_SP)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SPSerializer(one_SP, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        one_SP.delete()
        return HttpResponse(status=204)


@csrf_exempt
@api_view(['GET', 'POST'])
@jwt_accept
def add_view_attendance(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        all_attendance = Attendance.objects.all()
        serializer = AttendanceSerializer(all_attendance, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SPSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'PUT','DELETE'])
@jwt_accept
def attendance(request, SID):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        one_attendance = Attendance.objects.filter(Student_ID=SID)
    except Attendance.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AttendanceSerializer(one_attendance)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AttendanceSerializer(one_attendance, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        one_attendance.delete()
        return HttpResponse(status=204)


@csrf_exempt
@api_view(['GET', 'POST'])
@jwt_accept
def add_view_attendance_sessions(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        all_attendance_sessions = Attendance_Session.objects.all()
        serializer = Attendance_SessionSerializer(all_attendance_sessions, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Attendance_SessionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'POST'])
@jwt_accept
def add_view_timetable(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        all_timetable = Timetable.objects.all()
        serializer = TimetableSerializer(all_timetable, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TimetableSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def validate_user(request):
	if request.method == 'POST':
		print(request.META)
		data = JSONParser().parse(request)
		username = data['json_data']['username']
		password = data['json_data']['password']
		user = authenticate(request,username=username,password=password)
		if user is not None:
			payload = jwt_payload_handler(user)
			token = jwt_encode_handler(payload)
			print(token)
			serializer = UserSerializer(user)
			personaldet = PersonnelSerializer(Personnel.objects.filter(LDAP=user),many=True)
			dat = serializer.data
			dat.update(dict(personaldet.data[0]))
			dat["token"]=token
			return JsonResponse(dat,status=200)
		else:
			return HttpResponse(status=404)
@csrf_exempt
@api_view(['POST'])
@jwt_accept
def courses_rel_students(request):
	if request.method == 'POST':
		#print(request.META)
		token=request.META['HTTP_AUTHORIZATION'].split()[1]
		print(token)
		data = {}
		data1 = JSONParser().parse(request)
		ID = data1['course_id']
		data2 = SCSerializer(Students_Courses.objects.filter(Course_ID=ID), many=True).data
		x = 0
		for i in range(len(data2)):
			temp = PersonnelSerializer(Personnel.objects.get(Person_ID=data2[i]['Student_ID'])).data
			temp2 = User.objects.all()
			for b in temp2:
				try:
					if b.personnel.LDAP.id == temp['LDAP']:
						data[data2[i]['Student_ID']] = {'Username':b.username,'First_Name':b.first_name,'Last_Name':b.last_name,'Email':b.email}
				except:
					kill=1
			x += 1
		if len(data) != 0:
			return JsonResponse(data, status=200, safe=False)
		else:
			return HttpResponse(status=404)

@csrf_exempt
@api_view([ 'POST'])
@jwt_accept
def student_rel_courses(request):
	if request.method == 'POST':
		data={}
		data1 = JSONParser().parse(request)
		ID = data1['student_id']
		data2 = SCSerializer(Students_Courses.objects.filter(Student_ID=ID),many=True).data
		x = 0
		for i in range(len(data2)):
			temp = CoursesSerializer(Courses.objects.get(Course_ID=data2[i]['Course_ID'])).data
			data[x] = {'Course_ID':data2[i]['Course_ID'],'Course_Name':temp['Course_Name'],'Course_description':temp['Course_description'],'Course_Year':temp['Course_Year'],'Course_Status':temp['Course_Status']}
			x+=1
		if len(data) != 0:
			return JsonResponse(data,status=200,safe=False)
		else:
			return HttpResponse(status=404)

@csrf_exempt
@api_view([ 'POST'])
@jwt_accept
def faculty_rel_courses(request):
	if request.method == 'POST':
		data={}
		data1 = JSONParser().parse(request)
		ID = data1['faculty_id']
		data2 = ICSerializer(Instructors_Courses.objects.filter(Inst_ID=ID),many=True).data
		x = 0
		for i in range(len(data2)):
			temp = CoursesSerializer(Courses.objects.get(Course_ID=data2[i]['Course_ID'])).data
			data[x]=data2[i]['Course_ID']
			data[x] = {'Course_ID':data2[i]['Course_ID'],'Course_Name':temp['Course_Name'],'Course_description':temp['Course_description'],'Course_Credits':temp['Course_Credits'],'Course_Year':temp['Course_Year'],'Course_Status':temp['Course_Status']}
			x+=1
		if len(data) != 0:
			return JsonResponse(data,status=200,safe=False)
		else:
			return HttpResponse(status=404)
# Add any extra needed api views after this
@csrf_exempt
@api_view([ 'POST'])
@jwt_accept
def student_session(request):
	if request.method == 'POST':
		data1 = JSONParser().parse(request)
		id = data1['sess']
		data = AttendanceSerializer(Attendance.objects.filter(ASession_ID=id),many=True)
		print(data.data)
		return JsonResponse(data.data,status=200,safe=False)
	return HttpResponse(status=404)
def faculty_users(request):
	parser = LDIFParser(open('data.ldif', 'rb'))
	i=0
	for dn, Entry in parser.parse():
		dn.split(',')
		props=dict(item.split("=") for item in dn.split(","))
		#print('got entry record: %s' % dn)
		#print(props)
		#pprint(Entry)
		print (Entry["uid"],Entry["givenname"],Entry["sn"],Entry["mail"])
		u=User.objects.create_user(username=Entry["uid"][0],password="iiits@123",first_name=Entry["givenname"][0],last_name=Entry["sn"][0],email=Entry["mail"][0])
		p=Personnel(Dept_id=1,LDAP_id=u.id,Role_id=3)
		p.save()
def student_users(request):
    Start = 2014
    End = 2018
    for i in range(2):
        DEPT = 1
        parser = LDIFParser(open('data' + str(i + 1) + '.ldif', 'rb'))
        for dn, Entry in parser.parse():
            dn.split(',')
            props = dict(item.split("=") for item in dn.split(","))
            try:
                print (Entry["uid"], Entry["givenname"], Entry["sn"], Entry["mail"])
            except:
                DEPT = 2
                continue
            FName = Entry["givenname"][0]
            if (len(FName) > 30):
                FName = FName[:20]

            u = User.objects.create_user(username=Entry["uid"][0], password="iiits@123", first_name=FName,
                                         last_name=Entry["sn"][0], email=Entry["mail"][0],Rollnumber=Entry["gecos"][0])
            p = Personnel(Dept_id=DEPT, LDAP_id=u.id, Role_id=2)
            p.save()
            q = Student_Period(Student_ID_id=p.Person_ID, Start_Year=Start, End_Year=End)
            q.save()
        Start += 1
        End += 1
def student_rollno(request):
    Start = 2014
    End = 2018
    for i in range(2):
        DEPT = 1
        parser = LDIFParser(open('data' + str(i + 1) + '.ldif', 'rb'))
        for dn, Entry in parser.parse():
            dn.split(',')
            props = dict(item.split("=") for item in dn.split(","))
            try:
                print (Entry["uid"], Entry["givenname"], Entry["sn"], Entry["mail"],Entry["gecos"])
            except:
                DEPT = 2
                continue
            FName = Entry["givenname"][0]
            if (len(FName) > 30):
                FName = FName[:20]

            u = User.objects.get(username=Entry["uid"][0])
            p = Personnel.objects.get(LDAP_id=u.id)
	    p.RollNumber=Entry["gecos"][0]
            p.save()
        Start += 1
        End += 1

def EditProfile(request):
    obj = Personnel.objects.get(LDAP_id=request.user.id)
    personID=obj.Person_ID
    pObj = Personnel.objects.get(Person_ID=personID)
    fObj , created = NotificationTime.objects.get_or_create(Personnel_ID=pObj)
    #print fObj,'********************'
    if request.method == 'POST':
        form = ProfileForm( request.POST, user = request.user, instance = fObj)
        if form.is_valid():
            model_instance = form.save(commit=False)
            #print personID, request.user.username
            #print '########################'
            model_instance.Personnel_ID = pObj
            model_instance.save()
            return HttpResponseRedirect('/')
    else:
        form = ProfileForm(None,user = request.user, instance = fObj)
    return render(request, "home/profile.html", {'form': form})
