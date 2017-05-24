# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Books(models.Model):
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	publish_date = models.DateTimeField()
	category = models.CharField(max_length=55)
	in_print = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "id: " + str(self.id) + ", title: " + self.title