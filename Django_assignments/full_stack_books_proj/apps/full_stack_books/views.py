# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

from .models import Book

# Create your views here.
def index(request):
	context = {
		"books":Book.objects.all()
	}
	return render(request, 'full_stack_books/index.html', context)

def add_book(request):
	# create a book object
	Book.objects.create(title=request.POST['title'],category=request.POST['category'],author=request.POST['author'])
	# update context from the database of books
	context = {
		"books":Book.objects.all()
	}
	# return the context to the index.html file to update the table
	return render(request, 'full_stack_books/index.html', context)