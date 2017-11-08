from django import template
from django.template.defaultfilters import *

register = template.Library()

@register.filter(name='multiply')	
def multiply(value,arg):
	return value*arg
