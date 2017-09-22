from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django import template	
from django.http import HttpResponse
from .forms import PersonnelForm
import datetime
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




