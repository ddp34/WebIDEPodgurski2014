from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login

#import text sync engine and dependencies
from diffsync import DiffSync
from textconvert import TextConvert
from web_ide.models import ServerText, ServerShadow

import json
import re

#keep a static DiffSync object to run synchronizations
diff_sync_engine = DiffSync()
text_convert = TextConvert()

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
    
    #handle post requests
    if request.method == "POST":

        #handle text sync requests
        #we may want the client to send a 'posttype' param to discern
        #between different kinds of pings
        if request.POST['posttype'] == "syncrequest":
            #get server text of file
            try:
                servertext = ServerText.objects.get(filename="dummyfile.txt")
            except ServerText.DoesNotExist:
                #if the file doesn't exist, create it
                servertext = ServerText(filename="dummyfile.txt", text="New file!")
            #get server shadow, use the csrf token as a unique identifier
            try:
                servershadow = ServerShadow.objects.get(name=request.POST['csrfmiddlewaretoken'])
            except ServerShadow.DoesNotExist:
                #if the user doesn't have a server shadow for this file, create one
                servershadow = ServerShadow(filename="dummyfile.txt", text=request.POST['clienttext'], name=request.POST['csrfmiddlewaretoken'])

            #now that we have all the components, run the sync algorithm
            syncresults = diff_sync_engine.synchronizeDocs(request.POST['clienttext'], request.POST['clientshadow'], servertext.text, servershadow.text)
            
            #save the resulting server text and shadow
            setattr(servertext, "text", syncresults[2])
            setattr(servershadow, "text", syncresults[3])
            servertext.save()
            servershadow.save()

            #return the client text and client shadow
            response_data = {}
            response_data['clienttext'] = syncresults[0] 
            response_data['clientshadow'] = syncresults[1] 

            return HttpResponse(json.dumps(response_data), content_type="appliation/json")
                
    else:
        #simple GET request

        #retrieve server text and push it to user
        servertext = ServerText.objects.get(filename="dummyfile.txt")
        context = {'filetext': servertext.text, 'clishadow': servertext.text}

        return render(request, 'web_ide/editor.html', context)

@login_required
def restricted(request):
    return HttpResponse("You are logged in.")

@login_required
def user_logout(request):
    return logout_then_login(request, 'login')
