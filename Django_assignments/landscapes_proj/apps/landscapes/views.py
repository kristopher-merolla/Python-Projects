# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.
def index(request):
	return render(request, 'landscapes/index.html')

def routed(request, id):
	context = {
		"id": int(id)
	}
	if (int(id) > 50):
		return redirect('/')
	elif (int(id) < 1):
		return redirect('/')
	else:
		return render(request, 'landscapes/routed.html', context)