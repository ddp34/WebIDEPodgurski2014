from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return render(request, 'web_ide/login.html')

def admin(request):
    return HttpResponse("admin page")

def editor(request):
    return HttpResponse("editor page")
