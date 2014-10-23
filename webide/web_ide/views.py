from django.template import render
from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return HttpResponse("login page")

def admin(request):
    return render(request, 'web_ide/admin.html')

def editor(request):
    return render(request, 'web_ide/editor.html')
