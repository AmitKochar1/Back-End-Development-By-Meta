from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Welcome to Little Lemon")

def about(request):
    return HttpResponse("About us")

def menu(request):
    return HttpResponse("Our menu")

def book(request):
    return HttpResponse("Book your table")