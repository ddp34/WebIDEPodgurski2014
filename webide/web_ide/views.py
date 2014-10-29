from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from web_ide.forms import UserForm, UserProfileForm

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/web_ide/')
            else:
                return HttpResponse("Inactive account.")
        else:
            print "Login details invalid: {0}, {1}".format(username, password)
            return HttpResponse("Login details invalid")
    else:
        return render(request, 'web_ide/login.html', {})

    return render(request, 'web_ide/login.html')

def admin(request):
    return render(request, 'web_ide/admin.html')

def editor(request):
    return render(request, 'web_ide/editor.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()

    return render(request, 'web_ide/register.html',
                  {'user_form': user_form, 'registered': registered})

@login_required
def restricted(request):
    return HttpResponse("You are logged in.")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect