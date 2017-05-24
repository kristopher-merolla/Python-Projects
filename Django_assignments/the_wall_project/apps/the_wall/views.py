# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

import md5 # imports the md5 module to generate a hash for password securing

import os, binascii # used for random generation // salt = binascii.b2a_hex(os.urandom(15))

from .models import User, Message, Comment

from django.http import HttpResponse

# Create your views here.
def index(request):
	if (request.session.get('active_user') == None):
		return render(request, 'the_wall/index.html')
	else:
		request.session['active_user'] = None
		return render(request, 'the_wall/index.html')

def register(request):
	return render(request, 'the_wall/register.html')

def active_user(request):
	if (request.session.get('active_user') == None): # if no active user, redirect to the login page
		return redirect('/')
	else:
		# if the user is logged in, pull all messages and all comments from all users, pass through render
		context = {
			"messages":Message.objects.all(),
			"comments":Comment.objects.all()
		}
		return render(request, 'the_wall/active.html', context) # if active user is available, go to the wall (active.html)

# PAGE TO LOGIN EXISTING USER
def login(request):
	email = request.POST['email']
	password = request.POST['password'] # password needs to be hashed here, use md5 and a salt

	# check if the user exists and if not, set the user to None
	try:
		user = User.objects.get(email=email)
	except User.DoesNotExist:
		user = None

	# validate login credentials here
	if (user != None): # email is in the database
		user_id = user.id # grab the user is for the email entered
		################################################################################################################
		# # IF we are protecting the password, which we SHOULD do, we need to have a salt in the db and hash the pw
		################################################################################################################
		# grab salt from the database and use it to rehash our submitted login password
		# grab_salt = "SELECT salt FROM users WHERE email = :email"
		# salt_data = {'email': email}
		# salt = mysql.query_db(grab_salt,salt_data)
		# login_password = md5.new(password + salt[0]['salt']).hexdigest() # the password entered at login screen, hashed with salt
		# # grab the registered hashed password from db
		# grab_hash = "SELECT password FROM users WHERE email = :email"
		# hash_data = {'email': email}
		# hashed_pw = mysql.query_db(grab_hash,hash_data) # the hashed password stored in the data for the given email
		################################################################################################################
		if (password == User.objects.get(id=user_id).password):
			#passwords match, login
			request.session['active_user'] = email
			return redirect('/thewall')
		else:
			# display error message password invalid (does not match database entry)
			error_message = {
				"error_message":"<p style='color:red;'> INVALID PASSWORD </p> "
			}
			return render(request, 'the_wall/index.html',error_message)
	else:
		# display error message email does not exist in database
		error_message = {
			"error_message":"<p style='color:red;'> EMAIL NOT REGISTERED </p> "
		}
		return render(request, 'the_wall/index.html',error_message)

# PAGE TO REGISTER NEW USER
def new_login(request):
	first_name = request.POST['first_name']
	last_name = request.POST['last_name']
	email = request.POST['email']
	# #password needs to be hashed here, use md5 and a salt
	password = request.POST['password']
	password_confirm = request.POST['password_confirmation']
	# salt =  binascii.b2a_hex(os.urandom(15)) # salt is stored in the database for validation
	# hashed_pw = md5.new(password + salt).hexdigest() # this is stored in the database as the password, now secure

	# Frist and last name need to be at least 2 characters, otherwise error
	if (len(first_name) < 2 or len(last_name) < 2):
		error_message = {
			"error_message":"<p style='color:red;'> NAME FIELDS MUST BE AT LEAST 2 CHARACTERS </p> "
		}
		return render(request, 'the_wall/register.html',error_message)
	# Frist and last name need to be only alpha (no numbers or special characters)
	if (not(first_name.isalpha()) or not(first_name.isalpha())):
		error_message = {
			"error_message":"<p style='color:red;'> NAME FIELDS CANT CONTAIN NUMBERS OR SPECIAL CHARACTERS </p> "
		}
		return render(request,'register.html',error_message)

	# check if the user exists and if not, set the user to None
	try:
		user = User.objects.get(email=email)
	except User.DoesNotExist:
		user = None
	if (user == None): # if the email is NOT in the database...
		# email validation in Django added on models.py object
		# https://docs.djangoproject.com/en/1.10/ref/validators/#django.core.validators.EmailValidator
		if (True): # if the email IS valid...
			if (password == password_confirm): # if the password matches the confirmation password
				if (len(password) >= 8): # if the length of the password is 8 characters or more
					#build and execute the SQL insert for a new user creation
					user = User.objects.create(first_name=first_name,last_name=last_name, email=email,password=password)
					user.save()
					# if all validations are met and the data is updated, redirect to the home page for login
					return redirect('/')
				else:
					# display error message password too short
					error_message = {
						"error_message":"<p style='color:red;'> PASSWORD TOO SHORT </p> "
					}
					return render(request,'the_wall/register.html',error_message)
			else:
				# display error message password not matching password confirmation
				error_message = {
					"error_message":"<p style='color:red;'> PASSWORDS DO NOT MATCH </p> "
				}
				return render(request,'the_wall/register.html',error_message)
		else:
			# display error message if email is not a valid email
			error_message = {
				"error_message":"<p style='color:red;'> INVALID EMAIL </p> "
			}
			return render(request,'the_wall/register.html',error_message)
	else:
		# display error message if email already exists
		error_message = {
			"error_message":"<p style='color:red;'> EMAIL ALREADY EXISTS </p> "
		}
		return render(request,'the_wall/register.html',error_message)


def new_post(request):
	if (session.get('active_user') == None): # if no active user, redirect to the login page
		return redirect('/')
	# if we are dealing with a new post (NOT a new comment)
	if (request.POST['new_post'] == 'new_post'):
		# set message to our POST submission
		message = request.POST['post']
		# check if the post was sent in blank
		if (message == ""):
			return	redirect('/thewall')
		else:
			# grab the user_id for the active user from the users table
			grab_user_id = "SELECT id FROM users WHERE email = :email"
			grab_data = {'email': session['active_user']}
			user_id = mysql.query_db(grab_user_id, grab_data)[0]['id']
			# add the new post into the posts table
			new_post = "INSERT INTO posts (user_id, message, created_at, updated_at) VALUES (:user_id, :message, NOW(), NOW())"
			post_data = {'user_id': user_id, 'message': message}
			mysql.query_db(new_post, post_data)
			return redirect('/thewall')
	# if we are dealing with a new comment (NOT a new post)
	if (request.POST['new_post'] == 'new_comment'):
		print "new comment coming..."
		# if the comment is blank, return to the wall
		if (len(request.POST['comment_post']) == 0):
			return redirect('/thewall')
		# else (if the comment is NOT blank) post the comment and return to the wall
		else:
			grab_user_id = "SELECT id FROM users WHERE email = :email"
			grab_data = {'email': session['active_user']}
			post_id = int(request.POST['post_index'])
			print "len not 0"
			user_id = mysql.query_db(grab_user_id, grab_data)[0]['id']
			comment = request.POST['comment_post']

			new_comment = "INSERT INTO comments (post_id, user_id, comment, created_at, updated_at) VALUES (:post_id, :user_id, :comment, NOW(), NOW())"
			comment_data = {'post_id': post_id, 'user_id': user_id, 'comment': comment}
			mysql.query_db(new_comment,comment_data)
			print "new comment added to database"
			return	redirect('/thewall')