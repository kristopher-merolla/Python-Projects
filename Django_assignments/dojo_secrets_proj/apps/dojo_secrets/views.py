# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

from django.db.models import Count

from .models import User, Message

def index(request): # login / register (index) page
	if (request.session.get('active_user') == None):
		return render(request, 'dojo_secrets/index.html')
	else:
		request.session['active_user'] = None
		return render(request, 'dojo_secrets/index.html')

def register(request): # page to register new users
	return render(request, 'dojo_secrets/register.html')

def main(request): # page once user is logged in
	context = {
		"recent_secrets": Message.objects.all().order_by('-id')[:5],
		"currentuser": User.objects.get(email=request.session['active_user'])
	}
	return render(request, 'dojo_secrets/success.html', context)

def post(request):
	# if request.method != POST (ie, user typed in the /post address instead of making a post)
	if (request.method == "POST"):
		# grab the message from the user
		post_data = {
			"message": request.POST['message'],
			"active_user": request.session['active_user']
		}
		# run the post_data through the message_maker function
		model_resp = Message.objects.message_maker(post_data)
		if (model_resp[0]): # message validated
			return redirect('main')
		else:
			return redirect('main')
	else:
		return redirect('main')

def newlike(request, id, sentby):
	# recieve id of the secret to like
	Message.objects.newlike(id, request.session['active_user'])
	if (sentby == "sec"):
		return redirect('/main')
	else:
		return redirect('/popular')

def delete(request, id, sentby):
	# recieve id of the secret to delete
	Message.objects.delete(id, request.session['active_user'])
	if (sentby == "sec"):
		return redirect('/main')
	else:
		return redirect('/popular')

def popular(request):
	allsecrets = Message.objects.annotate(num_likes=Count('likers')).order_by('-num_likes')
	context = {
		"recent_secrets":allsecrets,
		"currentuser": User.objects.get(email=request.session['active_user'])
	}
	return render(request, 'dojo_secrets/most_popular.html', context)

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
		request.session['active_user_name'] = model_resp[1].first_name + " " + model_resp[1].last_name
		return redirect('main')
	else: # user login was NOT successful
		return render(request, 'dojo_secrets/index.html', model_resp[1]) # model_resp[1] is the error_message

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
		return render(request,'dojo_secrets/index.html', model_resp[1]) # model_resp[1] is the registration_success message
	else: # user registration was NOT successful
		return render(request, 'dojo_secrets/register.html', model_resp[1]) # model_resp[1] is the error_message