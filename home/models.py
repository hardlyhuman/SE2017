from __future__ import unicode_literals
from django.db import models
from compositekey import db
import datetime
'''
	Check all the foreign key constraints and whether the on_delete CASCADE makes sense.
	When should we write the functions to return data?
	
	#Review by Course Lead:
	1. This design is not addressing the following:
		a)which student belongs to which batch(say 2015-2019 batch)?
		b)which course belongs to which semester as well as year?
		c)different professors can take the same course in different years/semesters. on the other hand, multiple professors can take the same course.(not sure whether it is addressing the latter one or not)
	2. comments on existing fields of models:
		a) In personnel, for 'Dept field, ##on_delete should not be there because even after deleting the department the previous records should not get deleted.
		b) similarily, In Department model, If a person who is the head of the dept is deleted, that should not effect the dept. So, I think on_delete is not required for Head_Id
		c)
		
		
	#Review by Student Stakeholder Team:
	1. In attendance table, we need a course session Id since a single course will have multiple sessions in a semester. (student_Id, course_Id, course_Sess_Id) altogether should be unique.
	2. We don't need submission model because we are assuming only manual subissions (That's what we understood from business case document and client interaction
	    Probably, a similar table is required for faculty dept. to mark a particular student's submission status. ##needs to get review from faculty dept.
	3. We need a model which keeps in track of the info about the students and the courses they have taken.
'''
class Roles(models.Model):
	Role_ID=models.AutoField(primary_key=True)
	Role_name=models.CharField(max_length=50,default="")
	level=models.IntegerField(default=0)

class Personnel(models.Model):
	Person_ID=models.IntegerField(primary_key=True)
	Person_Name=models.CharField(max_length=50,default="")
	Role=models.ForeignKey(Roles,to_field='Role_ID',on_delete=models.CASCADE)#Make sure whether this has to be foreign key
<<<<<<< HEAD
i	Dept=models.ForeignKey(Department,to_field='Dept_ID',on_delete=models.CASCADE)#Not sure about this too 
=======
	Dept=models.ForeignKey(Department,to_field='Dept_ID',on_delete=models.CASCADE)#Not sure about this too 
>>>>>>> b999474ef17a537dd9e3541c298b2f5eeee5d46e

class Department(models.Model):
	Dept_ID=models.AutoField(primary_key=True)
	Dept_Name=models.CharField(max_length=50,default="")
	Head_ID=models.ForeignKey(Personnel,to_field='Person_ID',on_delete=models.CASCADE)

class Courses(models.Model):
	Course_ID=models.AutoField(primary_key=True)
	Course_Name=models.CharField(max_length=50,default="")
<<<<<<< HEAD
	#Inst_ID=models.ForeignKey(Personnel,to_field='Person_ID',on_delete=models.CASCADE) 
	Course_description = models.CharField(max_length = 255, default = "")
	Course_Credits = models.IntegerField()
	Course_Status = models.BooleanField(initial = True)
=======
>>>>>>> b999474ef17a537dd9e3541c298b2f5eeee5d46e

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
	Start_Time=models.DateTimeField(default=datetime.datetime.now())
	End_Time=models.DateTimeField(default=(datetime.datetime.now()+datetime.timedelta(hours=24)))

class Submissions(models.Model):
    Sub_ID=db.MultiFieldPK('Assign_ID','Student_ID')
	Assign_ID=models.ForeignKey(Assignment,to_field='Assign_ID',on_delete=models.CASCADE)
	Student_ID=models.ForeignKey(Personnel,to_field='Person_ID',on_delete=models.CASCADE)
	Sub_Time=models.DateTimeField(default=datetime.datetime.now())
<<<<<<< HEAD
=======
	Score=models.FloatField(default=0)

class Instructors_Courses(models.Models):
    IC_id=db.MultiFieldPK('Course_ID','Inst_ID')
    Course_ID=models.ForeignKey(Courses,to_field='Course_ID',on_delete=models.CASCADE)
    Inst_ID=models.ForeignKey(Personnel,to_field='Person_ID',on_delete=models.CASCADE)
    Start_Date=models.DateField(auto_now_add=True)
    End_Date=models.DateField(auto_now_add=True)

class Students_Courses(models.Models):
    SC_ID=db.MultiFieldPK('Student_ID','Course_ID')
    Student_ID=models.ForeignKey(Personnel,to_field='Person_ID',on_delete=models.CASCADE)
    Course_ID=models.ForeignKey(Courses,to_field='Cousre_ID',on_delete=models.CASCADE)
    Reg_Date=models.DateField(auto_now_add=True)

class Events(models.Models):
    Event_ID=db.MultiFieldPK('Event_Date','Event_Name')
    Event_Date=models.DateField(auto_now_add=True)
    Event_Name=models.CharField(default='',max_length=50)

class Student_Period(models.Model):
	Student_ID=models.ForeignKey(Personnel,to_field='Person_ID')
	Start_Year=models.IntegerField(default=2013)
	End_Year=models.IntegerField(default=2017)
>>>>>>> b999474ef17a537dd9e3541c298b2f5eeee5d46e
