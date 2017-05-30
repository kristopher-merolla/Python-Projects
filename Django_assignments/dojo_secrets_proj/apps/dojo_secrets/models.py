# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import bcrypt # for encrypting passwords

# Create your models here.
class UserManager(models.Manager):
	def register_user(self, postData):
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
		def validateEmail(email):
			from django.core.validators import validate_email
			from django.core.exceptions import ValidationError
			try:
				validate_email(email)
				return True
			except ValidationError:
				return False
		if (validateEmail(email)==False):
			print "email entry invalid"
			message = {
				"message":"<p style='color:red;'> INVALID EMAIL ENTRY, PLEASE ENTER A VALID EMAIL </p> "
			}
			return [False, message]
		try: # check if the user exists and if not, set the user to None
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			user = None
		if (user == None): # if the email is NOT in the database...
			if (password == password_confirm):
				if (len(password) >= 8):
					# encrypt the password
					hashed_pw = bcrypt.hashpw(postData['password'].encode('utf-8'), bcrypt.gensalt())
					# build and execute the SQL insert for a new user creation
					user = User.objects.create(first_name=first_name,last_name=last_name, email=email,password=hashed_pw)
					# if all validations are met and the data is updated, redirect to the home page for login
					message = {
						"message":"<p style='color:green;'> New User Registered, please login :) </p> "
					}
					return [True, message]
				else: # display error message password too short
					message = {
						"message":"<p style='color:red;'> PASSWORD TOO SHORT </p> "
					}
					return [False, message]
			else: # display error message password not matching password confirmation
				message = {
					"message":"<p style='color:red;'> PASSWORDS DO NOT MATCH </p> "
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
		try: # check if the user exists and if not, set the user to None
			user = User.objects.get(email=login_email)
		except User.DoesNotExist:
			user = None
		if (user != None): # email is in the database
			stored_hash = user.password
			input_hash = bcrypt.hashpw(postData['password'].encode(), stored_hash.encode())
			# validate login credentials here
			if (input_hash == user.password): # passwords match, login
				return [True, user]
			else: # display error message password invalid (does not match database entry)
				message = {
					"message":"<p style='color:red;'> INVALID PASSWORD </p> "
				}
				return [False, message]
		else:
			message = {
				"message":"<p style='color:red;'> EMAIL NOT REGISTERED </p> "
			}
			return [False, message]

class MessageManager(models.Manager):
	def message_maker(self, postData):
		# grab the message from the user
		message = postData['message']
		active_user = postData['active_user']
		# check that the message is at least 3 characters long
		if (len(message) < 4):
			return [False]
		else:
			user = User.objects.get(email=active_user)
			print user
			# create the message with the user_id as the id of the user
			self.create(message=message,author=user)
			# return True, post
			return [True]

	def newlike(self, secretid, useremail):
		# creating a new like, you first grab the secret using the id passed in
		try:
			secret = self.get(id=secretid)
		except:
			return False
		# grab the user
		user = User.objects.get(email=useremail)
		if (secret.author == user):
			return False
		secret.likers.add(user)
		return True

	def delete(self, secretid, useremail):
		# deleting, you first grab the secret using the id passed in
		try:
			secret = self.get(id=secretid)
		except:
			return False
		# grab the user
		user = User.objects.get(email=useremail)
		if (secret.author != user):
			print "user not author"
			return False
		secret.delete()
		return True

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

class Message(models.Model):
	message = models.CharField(max_length=255)
	author = models.ForeignKey(User)
	likers = models.ManyToManyField(User, related_name="likedsecrets")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = MessageManager()



