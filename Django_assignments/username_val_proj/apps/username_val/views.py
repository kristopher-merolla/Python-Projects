# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from .models import Username

# Create your views here.
def index(request):
	return render(request, 'username_val/index.html')

def validate(request):
	# validate username entered
	if (len(request.POST['username'])<8): # length must be at least 8 characters
		context = {
			"message":"<h1 style='background-color: red; border: 1px solid black; color:white;'>Username is not valid!</h1>"
		}
		return render(request, 'username_val/index.html', context)
	elif (len(request.POST['username'])>16): # length can be no more than 16 characters
		context = {
			"message":"<h1 style='background-color: red; border: 1px solid black; color:white;'>Username is not valid!</h1>"
		}
		return render(request, 'username_val/index.html', context)
	else: # if the length is good...
		# check if the username exists already in the db
		try:
			user = Username.objects.get(username=request.POST['username'])
		except Username.DoesNotExist:
			user = None
		# if the user is in the db already...
		if(user):
			context = {
				"message":"<h1 style='background-color: red; border: 1px solid black; color:white;'>Username is not valid!</h1>"
			}
			return render(request, 'username_val/index.html', context)
		else:
			# add the username to the database
			Username.objects.create(username=request.POST['username'])
			context = {
				"usernames":Username.objects.all(),
				"message":"<h1 style='background-color: green; border: 1px solid black; color:white;'>The username you entered is valid.  Thank you!</h1>"
			}
			return render(request, 'username_val/success.html', context)