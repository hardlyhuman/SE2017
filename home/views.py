from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django import template
from django.http import HttpResponse
from .forms import PersonnelForm
import datetime
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import *
from .models import *
# Create your views here.
PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', )
register = template.Library()

@login_required(login_url="login/")
def index(request):
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

	return render(request, "home/index.html", {'html': html,'now':now})

@csrf_exempt
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
		serializer = SnippetSerializer(person, data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		person.delete()
		return HttpResponse(status=204)

@csrf_exempt
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

@csrf_exempt
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
		serializer = SnippetSerializer(one_department, data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data)
		return JsonResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		one_department.delete()
		return HttpResponse(status=204)