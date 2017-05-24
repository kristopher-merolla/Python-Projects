# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserManager(models.Manager):
	def login(self, email, password):

		print ("Running a login function!")
		print ("If successful login occurs, maybe return {'theuser':user} where user is a user object?")
		print ("If unsuccessful, maybe return { 'errors':['Login unsuccessful'] }")
	def register(self, **kwargs):
		print ("Register a user here")
		print ("If successful, maybe return {'theuser':user} where user is a user object?")
		print ("If unsuccessful do something like this? return {'errors':['User first name to short', 'Last name too short'] ")

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	userManager = UserManager()

	def __unicode__(self):
		return "id:" + str(self.id) + ", first_name:" + self.first_name

class Message(models.Model):
	user_id = models.ForeignKey(User)
	message = models.TextField(max_length=1000)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "id:" + str(self.id) + ", user_id:" + str(self.user_id)

class Comment(models.Model):
	message_id = models.ForeignKey(Message)
	user_id = models.ForeignKey(User)
	comment = models.TextField(max_length=1000)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "id:" + str(self.id) + ", message_id:" + str(self.message_id) + ", user_id:" + str(self.user_id)