from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def my_post(request):
    return HttpResponse("Hello, this is a first test before deploying!")