from __future__ import unicode_literals
from django.db import models
import datetime
'''
	Check all the foreign key constraints and whether the on_delete CASCADE makes sense.
	When should we write the functions to return data?
'''
class Roles(models.Model):
	Role_ID=models.AutoField(primary_key=True)
	Role_name=models.CharField(max_length=50,default="")
	level=models.IntegerField(default=0)

class Personnel(models.Model):
	Person_ID=models.IntegerField(primary_key=True)
	Person_Name=models.CharField(max_length=50,default="")
	Role=models.ForeignKey(Roles,to_field='Role_ID',on_delete=models.CASCADE)#Make sure whether this has to be foreign key
	Dept=models.ForeignKey(Department,to_field='Dept_ID',on_delete=models.CASCADE)#Not sure about this too

class Department(models.Model):
	Dept_ID=models.AutoField(primary_key=True)
	Dept_Name=models.CharField(max_length=50,default="")
	Head_ID=models.ForeignKey(Personnel,to_field='Person_ID',on_delete=models.CASCADE)

class Courses(models.Model):
	Course_ID=models.AutoField(primary_key=True)
	Course_Name=models.CharField(max_length=50,default="")
	Inst_ID=models.ForeignKey(Personnel,to_field='Person_ID',on_delete=models.CASCADE)

class Attendance(models.Model):
	Student_ID=models.ForeignKey(Personnel,to_field='Person_ID',on_delete=models.CASCADE)
	Course_ID=models.ForeignKey(Courses,to_field='Course_ID',on_delete=models.CASCADE)
	Date_time=models.DateTimeField(default=datetime.datetime.now())
	Marked=models.CharField(default="A")

class Documents(models.Model):
	Doc_ID=models.AutoField(primary_key=True)
	Doc_Name=models.CharField(max_length=50,default="")
	Document=models.FileField(upload_to='uploaded_file/')

class LoginTable(models.Model):
	IP=models.CharField(default="",max_length=12)
	Start_time=models.DateTimeField(default=datetime.datetime.now())
	End_time=models.DateTimeField(null=True,blank=True)

class Assignment(models.Model):
	Assign_ID=models.AutoField(primary_key=True)
	Course_ID=models.ForeignKey(Courses,to_field='Course_ID',on_delete=models.CASCADE)
	Start_time=models.DateTimeField(default=datetime.datetime.now())
	End_time=models.DateTimeField(default=(datetime.datetime.now()+datetime.timedelta(hours=24)))

class Submissions(models.Model):
	Assign_ID=models.ForeignKey(Assignment,to_field='Assign_ID',on_delete=models.CASCADE)
	Student_ID=models.ForeignKey(Personnel,to_field='Person_ID',on_delete=models.CASCADE)
	Sub_Time=models.DateTimeField(default=datetime.datetime.now())