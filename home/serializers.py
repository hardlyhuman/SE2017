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