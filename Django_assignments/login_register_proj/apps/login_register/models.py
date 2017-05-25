# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserManager(models.Manager):
	def register_user(self, postData):
		print "registering user..."
		# grab the values from our postData dictionary
		first_name = postData['first_name']
		last_name = postData['last_name']
		email = postData['email']
		password = postData['password']
		password_confirm = postData['password_confirm']
		# Frist and last name need to be at least 2 characters, otherwise error
		if (len(first_name) < 2 or len(last_name) < 2):
			message = {
				"message":"<p style='color:red;'> NAME FIELDS MUST BE AT LEAST 2 CHARACTERS </p> "
			}
			return [False, message]
		# Frist and last name need to be only alpha (no numbers or special characters)
		if (not(first_name.isalpha()) or not(first_name.isalpha())):
			message = {
				"message":"<p style='color:red;'> NAME FIELDS CANT CONTAIN NUMBERS OR SPECIAL CHARACTERS </p> "
			}
			return [False, message]
		# Email address needs to be validated
		# email validation in Django added on models.py object, can also use REGEX to check form
		# https://docs.djangoproject.com/en/1.10/ref/validators/#django.core.validators.EmailValidator
		if (len(email) == 0):
			message = {
				"message":"<p style='color:red;'> INVALID EMAIL ENTRY, PLEASE ENTER A VALID EMAIL </p> "
			}
			return [False, message]
		try: # check if the user exists and if not, set the user to None
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			user = None
		if (user == None): # if the email is NOT in the database...
			if (True): # if the email IS valid...
				if (password == password_confirm): # if the password matches the confirmation password
					if (len(password) >= 8): # if the length of the password is 8 characters or more
						#build and execute the SQL insert for a new user creation
						user = User.objects.create(first_name=first_name,last_name=last_name, email=email,password=password)
						# if all validations are met and the data is updated, redirect to the home page for login
						message = {
							"message":"<p style='color:green;'> New User Registered, please login :) </p> "
						}
						return [True, message]
					else:
						# display error message password too short
						message = {
							"message":"<p style='color:red;'> PASSWORD TOO SHORT </p> "
						}
						return [False, message]
				else: # display error message password not matching password confirmation
					message = {
						"message":"<p style='color:red;'> PASSWORDS DO NOT MATCH </p> "
					}
					return [False, message]
			else: # display error message if email is not a valid email
				message = {
					"message":"<p style='color:red;'> INVALID EMAIL </p> "
				}
				return [False, message]
		else: # if the email IS in the database...
			message = {
				"message":"<p style='color:red;'> EMAIL ALREADY EXISTS </p> "
			}
			return [False, message]

	def login_successful(self, postData):
		# grab the email and password from the postData
		login_email = postData['email']
		login_password = postData['password']
		try: # check if the user exists and if not, set the user to None
			user = User.objects.get(email=login_email)
		except User.DoesNotExist:
			user = None
		# validate login credentials here
		if (user != None): # email is in the database
			if (login_password == user.password): # passwords match, login
				return [True, user]
			else: # display error message password invalid (does not match database entry)
				message = {
					"message":"<p style='color:red;'> INVALID PASSWORD </p> "
				}
				return [False, message]
		else: # display error message email does not exist in database
			message = {
				"message":"<p style='color:red;'> EMAIL NOT REGISTERED </p> "
			}
			return [False, message]

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

	def __unicode__(self):
		return "id:" + str(self.id) + ", first_name:" + self.first_name