from django.urls import path
from . import views

app_name='jsite'
urlpatterns = [
	path('', views.jsite_index, name='jsite_index'),
	path('resume', views.jsite_resume, name='jsite_resume'),
]