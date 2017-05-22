# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
def index(request):
	return render(request, 'dissapearing_ninjas/index.html')

def ninja(request):
	return render(request, 'dissapearing_ninjas/all_turtles.html')

def color(request, turtle):
	context = {
		"color": turtle
	}
	return render(request, 'dissapearing_ninjas/turtle.html', context)