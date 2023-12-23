from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse('<html><h1> Welcome to Little Lemon! </h1></html>')