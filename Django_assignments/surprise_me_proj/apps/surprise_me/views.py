# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from random import shuffle  # use to shuffle the values list

VALUES = ['Lobster Bisque','BBQ Sandwich','Salad','Cup of Water','Ice Cold Beer','Taco','$5']

# Create your views here.
def index(request):
	return render(request, 'surprise_me/index.html')

def surprise(request):
	request.session['n'] = int(request.POST['surprise_count']) #take our user input and convert to an int
	shuffle(VALUES)
	request.session['context'] = []
	for i in range (request.session['n']):
		request.session['context'].append(VALUES[i])

	return render(request, 'surprise_me/surprise.html')