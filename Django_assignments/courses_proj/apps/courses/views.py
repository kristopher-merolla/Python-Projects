# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from .models import Course

# Create your views here.
def index(request):
	context = {
		"courses":Course.objects.all()
	}
	return render(request, 'courses/index.html', context)

def add_course(request):
	# create the course object using the Course class
	Course.objects.create(name=request.POST['name'],description=request.POST['description'])
	return redirect('/')

def remove_course(request, id):
	# pull the course object from the Course class
	context = {
		"course": Course.objects.get(id=id)
	}
	return render(request, 'courses/remove_course.html', context)

def delete(request, id):
	# delete the course object by the id
	course = Course.objects.get(id=id)
	course.delete()
	return redirect('/')