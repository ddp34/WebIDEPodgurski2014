from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return HttpResponse("login page")

def admin(request):
    return HttpResponse("admin page")

def editor(request):
    return HttpResponse("editor page")