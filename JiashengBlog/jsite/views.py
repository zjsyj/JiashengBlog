from django.shortcuts import render
from django.conf import settings

# Create your views here.
def jsite_index(request):
	return render(request, 'jsite/index.html', {})

def jsite_resume(request):
	return render(request, 'jsite/resume.html', {})