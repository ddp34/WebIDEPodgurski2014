from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from web_ide.forms import DeveloperForm

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/web_ide/editor.html')
            else:
                return HttpResponse("Inactive account.")
        else:
            print "Login details invalid: {0}, {1}".format(username, password)
            return HttpResponse("Login details invalid")
    else:
        return render(request, 'web_ide/login.html', {})

    return render(request, 'web_ide/login.html')

def editor(request):
    return render(request, 'web_ide/editor.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = DeveloperForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True

        else:
            print user_form.errors

    else:
        user_form = DeveloperForm()

    return render(request, 'web_ide/register.html',
                  {'developer_form': user_form, 'registered': registered})

@login_required
def restricted(request):
    return HttpResponse("You are logged in.")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect