from rest_framework import serializers
from home.models import *
from django.contrib.auth.models import User

class PersonnelSerializer(serializers.ModelSerializer):
	class Meta:
		model=Personnel
		fields=('Person_ID','LDAP','Role','Dept')

class DepartmentSerializer(serializers.ModelSerializer):
	class Meta:
		model=Department
		fields=('Dept_ID','Dept_Name')

class RolesSerializer(serializers.ModelSerializer):
	class Meta:
		model=Roles
		fields=('Role_ID','Role_name','level')

class CoursesSerializer(serializers.ModelSerializer):
	class Meta:
		model=Courses
		fields=('Course_ID','Course_Name','Course_description','Course_Credits','Course_Status')

class DocumentsSerializer(serializers.ModelSerializer):
	class Meta:
		model=Documents
		fields=('Doc_ID','Doc_Name','Document')

class AssignmentSerializer(serializers.ModelSerializer):
	class Meta:
		model=Assignment
		fields=('Assign_ID','Assignment_File','Course_ID','Start_Time','End_time')

class SubmissionsSerializer(serializers.ModelSerializer):
	class Meta:
		model=Submissions
		fields=('Sub_ID','Assign_ID','Student_ID','Sub_Time','Score')

class ICSerializer(serializers.ModelSerializer):
	class Meta:
		model=Instructors_Courses
		fields=('IC_ID','Course_ID','Inst_ID','Start_Date','End_Date')

class SCSerializer(serializers.ModelSerializer):
	class Meta:
		model=Students_Courses
		fields=('SC_ID','Student_ID','Course_ID','Reg_Date')

class EventsSerializer(serializers.ModelSerializer):
	class Meta:
		model=Events
		fields=('Event_ID','Event_Date','Event_Name')

class SPSerializer(serializers.ModelSerializer):
	class Meta:
		model=Student_Period
		fields=('Student_ID','Start_Year','End_Year')
