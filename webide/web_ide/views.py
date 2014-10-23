from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return render(request, 'web_ide/login.html')

def admin(request):
    return render(request, 'web_ide/admin.html')

def editor(request):
    return render(request, 'web_ide/editor.html')
