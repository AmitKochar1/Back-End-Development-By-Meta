from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def say_hello(request):
    return HttpResponse('Hello there!')

def welcome(request):
    return HttpResponse('Welcome to Little Lemon Restaruant!!')