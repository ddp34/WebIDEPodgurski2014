from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login


def user_login(request):
    if request.user.is_authenticated():
        return render(request, 'web_ide/editor.html')

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
            return render(request, 'web_ide/login.html', {'invalid': True})
    else:
        return render(request, 'web_ide/login.html', {})

    return render(request, 'web_ide/login.html')

@login_required
def editor(request):
    
    #check if the user posted a chat message
    #if request.method == 'POST':
        #chat_message = ChatMessage()

    return render(request, 'web_ide/editor.html')

@login_required
def restricted(request):
    return HttpResponse("You are logged in.")

@login_required
def user_logout(request):
    return logout_then_login(request, 'login')
