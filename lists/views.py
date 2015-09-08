from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
	return HttpResponse('<html><title>Personal Webpage</title><body><h1>Hi! Dinda Susanti<br>1206253911<h1></body></html>')
