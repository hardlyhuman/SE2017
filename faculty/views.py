from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from home.models import *
import json
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from home.models import Assignment

def ViewProfs(request):
	ProfList=[]
	Prof=Personnel.objects.all()
	for x in range(0,len(Prof)):
		if Prof[x].Role.Role_name=='faculty':
        		ProfList.append(Prof[x].Person_ID)
			ProfList.append(Prof[x].Person_Name)
	
	template=loader.get_template('prof.html')                         
        context={'ProfList':json.dumps(ProfList)}
        return HttpResponse(template.render(context,request))

def IndexView(request):
        template=loader.get_template('faculty/success.html')                         
        context={}
        return HttpResponse(template.render(context,request))


def upload_file(request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                instance = Assignment(Assignment_File=request.FILES['file'])
                instance.save()
	        #return render(request,{'form':form,'request':request})
                #return HttpResponseRedirect('faculty:home/')
        else:
            form = UploadFileForm()
        #return render(request, 'forms.html', {'form': form,'request':request})
        return HttpResponse("Success")

def view(request):
        template=loader.get_template('prof1.html')
        context={}
        return HttpResponse(template.render(context,request))

def students_view(request):
	template=loader.get_template('student1.html')
        context={}
        return HttpResponse(template.render(context,request))

    
