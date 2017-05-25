# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

import md5 # imports the md5 module to generate a hash for password securing

import os, binascii # used for random generation // salt = binascii.b2a_hex(os.urandom(15))

from .models import User

def index(request): # login / register (index) page
	if (request.session.get('active_user') == None):
		return render(request, 'login_register/index.html')
	else:
		request.session['active_user'] = None
		return render(request, 'login_register/index.html')

def register(request): # page to register new users
	return render(request, 'login_register/register.html')

# PAGE TO LOGIN EXISTING USER
def login(request):
	# grab the data entered in the login form (email and password) and put in the postData dictionary
	postData = {
		"email": request.POST['email'],
		"password": request.POST['password'] # password needs to be hashed here, use md5 and a salt	
	}
	# check the login success for email and password validations
	model_resp = User.objects.login_successful(postData)
	if model_resp[0] == True: # user login was successful (passed and email validations)
		request.session['active_user'] = model_resp[1].email # model_resp[1] here is the user (active user)
		return render(request, 'login_register/success.html')
	else: # user login was NOT successful
		return render(request, 'login_register/index.html', model_resp[1]) # model_resp[1] is the error_message

# PAGE TO REGISTER NEW USER
def new_login(request):
	# grab the data entered in the registration form and put it in the postData dictionary
	postData = {
		"first_name": request.POST['first_name'],
		"last_name" : request.POST['last_name'],
		"email" : request.POST['email'],
		"password" : request.POST['password'],
		"password_confirm" : request.POST['password_confirmation']
	}
	# check the registration success and if successful, return to login page for user to log in
	model_resp = User.objects.register_user(postData)
	if model_resp[0] == True: # user registration was successful
		return render(request,'login_register/index.html', model_resp[1]) # model_resp[1] is the registration_success message
	else: # user registration was NOT successful
		return render(request, 'login_register/register.html', model_resp[1]) # model_resp[1] is the error_message