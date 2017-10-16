from __future__ import unicode_literals
from django.db import models
from django import forms
from django import utils
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
# from compositekey import db
import datetime


@python_2_unicode_compatible
class Roles(models.Model):

    Role_ID = models.AutoField(primary_key=True)
    Role_name = models.CharField(max_length=50, default="")
    level = models.IntegerField(default=0)

    @property
    def __str__(self):
        return self.Role_name

@python_2_unicode_compatible
class Personnel(models.Model):
    Person_ID=models.AutoField(primary_key=True)
    LDAP=models.OneToOneField(User, on_delete=models.CASCADE)
    Role=models.ForeignKey(Roles,to_field='Role_ID',on_delete=models.CASCADE)#Make sure whether this has to be foreign key

    def __str__(self):
        return self.LDAP.username

    # Dept=models.ForeignKey(Department,on_delete=models.CASCADE)#Not sure about this too

    Dept = models.ForeignKey('Department', to_field='Dept_ID', on_delete=models.CASCADE)  # Not sure about this too
    Year = models.IntegerField(default=2013)

# Dept=models.ForeignKey(Department,to_field='Dept_ID',on_delete=models.CASCADE)#Not sure about this too


@python_2_unicode_compatible
class Department(models.Model):
    Dept_ID = models.AutoField(primary_key=True)
    Dept_Name = models.CharField(max_length=50, default="")

    #	Head_ID=models.ForeignKey('Personnel',to_field='Person_ID',on_delete=models.CASCADE)

    # Head_ID=models.ForeignKey('Personnel',to_field='Person_ID',on_delete=models.CASCADE)
    @property

    def __str__(self):
        return self.Dept_Name



@python_2_unicode_compatible
class Courses(models.Model):
    Course_ID = models.AutoField(primary_key=True)
    Course_Name = models.CharField(max_length=50, default="")

    # Inst_ID=models.ForeignKey(Personnel,to_field='Person_ID',on_delete=models.CASCADE)
    Course_description = models.CharField(max_length=255, default="")
    Course_Credits = models.IntegerField()
    Course_Year=models.IntegerField()
    Course_Status = models.BooleanField(default = True)
    #Course_Status = models.BooleanField(default= True)
    def __str__(self):
        return self.Course_Name


class Attendance(models.Model):
    Student_ID = models.ForeignKey(Personnel, to_field='Person_ID', on_delete=models.CASCADE)
    Course_ID = models.ForeignKey(Courses, to_field='Course_ID', on_delete=models.CASCADE)
    Date_time = models.DateTimeField(default=datetime.datetime.now())
    Marked = models.CharField(default="A", max_length=1)



class Attendance_Session(models.Model):
    Session_ID=models.AutoField(primary_key=True)
    Course_Slot=models.ForeignKey('Timetable',to_field='T_ID',on_delete=models.CASCADE)
    Date_time=models.DateTimeField(default=datetime.datetime.now())
    Status=models.IntegerField()
    Location=models.CharField(max_length=50,blank=True)
    def __str__(self):
        return str(self.Session_ID)

class Attendance(models.Model):
    Student_ID=models.ForeignKey(Personnel,to_field='Person_ID',on_delete=models.CASCADE)
    ASession_ID=models.ForeignKey(Attendance_Session,to_field='Session_ID',blank=True,null=True)
    Date_time=models.DateTimeField(default=datetime.datetime.now())
    Marked=models.CharField(default="A",max_length=1)


class Documents(models.Model):
    Doc_ID = models.AutoField(primary_key=True)
    Doc_Name = models.CharField(max_length=50, default="")
    Document = models.FileField(upload_to='uploaded_file/')


class LoginTable(models.Model):
    IP = models.CharField(default="", max_length=12)
    Start_time = models.DateTimeField(default=datetime.datetime.now())
    End_time = models.DateTimeField(null=True, blank=True)

@python_2_unicode_compatible
class Assignment(models.Model):
    Assign_ID=models.AutoField(primary_key=True)
    Assignment_File = models.FileField(upload_to='AssignmentsFolder/',default="hello.pdf")
    Course_ID=models.ForeignKey(Courses,to_field='Course_ID',on_delete=models.CASCADE)
    Start_Time=models.DateTimeField(default=utils.timezone.now)
    End_Time=models.DateTimeField(default=utils.timezone.now)
    def __str__(self):
        return str(self.Assign_ID)

class Submissions(models.Model):

    # Sub_ID=db.MultiFieldPK('Assign_ID','Student_ID')

    Sub_ID=models.AutoField(primary_key=True)
    Assign_ID=models.ForeignKey(Assignment,to_field='Assign_ID',on_delete=models.CASCADE)
    Student_ID=models.ForeignKey(Personnel,to_field='Person_ID',on_delete=models.CASCADE)
    Sub_Time=models.DateTimeField(default=utils.timezone.now)
    Sub_Status = models.BooleanField(default=False)
    Score=models.FloatField(default=0)

@python_2_unicode_compatible
class Instructors_Courses(models.Model):

    IC_id = models.AutoField(primary_key=True)
    Course_ID = models.ForeignKey(Courses, to_field='Course_ID', on_delete=models.CASCADE)
    Inst_ID = models.ForeignKey(Personnel, to_field='Person_ID', on_delete=models.CASCADE)
    Start_Date = models.DateField(datetime.date(2017, 1, 1))
    End_Date = models.DateField(datetime.date(2017, 1, 1))

    @property

    def __str__(self):
        return str((self.Inst_ID))

@python_2_unicode_compatible
class Students_Courses(models.Model):

    # SC_ID=db.MultiFieldPK('Student_ID','Course_ID')
    SC_ID = models.AutoField(primary_key=True)
    Student_ID = models.ForeignKey(Personnel, to_field='Person_ID', on_delete=models.CASCADE)
    Course_ID = models.ForeignKey(Courses, to_field='Course_ID', on_delete=models.CASCADE)
    Reg_Date = models.DateField(datetime.date(2017, 1, 1))

    @property
    def __str__(self):
        return str(self.Student_ID) + ' ' + str(self.Course_ID)


class Events(models.Model):
    Event_ID = models.AutoField(primary_key=True)
    Event_Date = models.DateField(auto_now_add=True)
    Event_Name = models.CharField(default='', max_length=50)


class Student_Period(models.Model):
    Student_ID = models.ForeignKey(Personnel, to_field='Person_ID')
    Start_Year = models.IntegerField(default=2013)
    End_Year = models.IntegerField(default=2017)
@python_2_unicode_compatible
class Timetable(models.Model):
    T_ID=models.AutoField(primary_key=True)
    DAYS_OF_WEEK = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
    )
    T_days = models.IntegerField(choices=DAYS_OF_WEEK)
    Start_time= models.TimeField(auto_now_add=True)
    End_time=models.TimeField(auto_now_add=True)
    Course_ID=models.ForeignKey(Courses,to_field='Course_ID',on_delete=models.CASCADE)
    Class_ID=models.CharField(max_length=10,default='')
    @property
    def __str__(self):
        return str(self.T_ID)
