from rest_framework import serializers
from home.models import *
from django.contrib.auth.models import User
#serializer for User table
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields=('id','username','first_name','last_name','email')
		
#Serializer for Personnel table
class PersonnelSerializer(serializers.ModelSerializer):
	class Meta:
		model=Personnel
		fields=('Person_ID','LDAP','Role','Dept')
#Serializer for Department table
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
		fields=('Course_ID','Course_Name','Course_description','Course_Credits','Course_Year','Course_Status')

class DocumentsSerializer(serializers.ModelSerializer):
	class Meta:
		model=Documents
		fields=('Doc_ID','Doc_Name','Document')

class AssignmentSerializer(serializers.ModelSerializer):
	class Meta:
		model=Assignment
		fields=('Assign_ID','Assignment_File','Course_ID','Start_Time','End_Time')

class SubmissionsSerializer(serializers.ModelSerializer):
	class Meta:
		model=Submissions
		fields=('Sub_ID','Assign_ID','Student_ID','Sub_Time','Score')

class ICSerializer(serializers.ModelSerializer):
	class Meta:
		model=Instructors_Courses
		fields=('IC_id','Course_ID','Inst_ID','Start_Date','End_Date')

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

class AttendanceSerializer(serializers.ModelSerializer):
	class Meta:
		model=Attendance
		fields=('Student_ID','ASession_ID','Date_time','Marked')

class Attendance_SessionSerializer(serializers.ModelSerializer):
	class Meta:
		model=Attendance_Session
		fields=('Session_ID','Course_Slot','Date_time','Status','Location')

class TimetableSerializer(serializers.ModelSerializer):
	class Meta:
		model=Timetable
		fields=('T_days','Start_time','End_time','Course_ID','Class_ID')
