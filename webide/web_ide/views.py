from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login

#import text sync engine and dependencies
from diffsync import DiffSync
from web_ide.models import *
from compilertest import WebCompiler
import json

#keep a static DiffSync object to run synchronizations
diff_sync_engine = DiffSync()

#filesystem controller
project_files = ProjectFiles()
compiler = WebCompiler()

def user_login(request):
    if request.user.is_authenticated():
        return render(request, 'web_ide/editor.html')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
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
                servertext = ServerText.objects.get(filename=request.POST['filename'])
            except ServerText.DoesNotExist:
                #if the file doesn't exist, create it
                servertext = ServerText(filename=request.POST['filename'], text="New file")
            #get server shadow, use the csrf token as a unique identifier
            try:
                servershadow = ServerShadow.objects.get(name=request.POST['csrfmiddlewaretoken'])
            except ServerShadow.DoesNotExist:
                #if the user doesn't have a server shadow for this file, create one
                servershadow = ServerShadow(filename=request.POST['filename'], text=request.POST['clienttext'], name=request.POST['csrfmiddlewaretoken'])

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

            return HttpResponse(json.dumps(response_data), content_type="application/json")
        
        #open a different file
        if request.POST['posttype'] == "openfile":

            try:
                #retrieve server text and push it to user
                servertext = ServerText.objects.get(filename=request.POST['filename'])
            except ServerText.DoesNotExist:
                #create buffer if it doesn't exist already
                servertext = ServerText(filename=request.POST['filename'], text=project_files.open_file(request.POST['filename']).read())
                servertext.save()
            response_data = {}
            response_data['clienttext'] = servertext.text
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        if request.POST['posttype'] == "snapshot":
            s = Snapshot()
            s.create_snap()

    else:
        #simple GET request

        try:
            #retrieve server text and push it to user
            servertext = ServerText.objects.get(filename="README.md")
        except ServerText.DoesNotExist:
            #create buffer if it doesn't exist already
            servertext = ServerText(filename="README.md", text=project_files.open_file("README.md").read())
            servertext.save()
        #list of files in root dir (for now)
        rootfilenames = project_files.list("")[0]
        context = {'filetext': servertext.text, 'clishadow': servertext.text, 'files': rootfilenames}

        return render(request, 'web_ide/editor.html', context)

@login_required
def restricted(request):
    return HttpResponse("You are logged in.")

@login_required
def user_logout(request):
    return logout_then_login(request, 'login')

def display_output(request):
    if request.POST['posttype'] == "sendcode":
        output = compiler.run_code(request.POST['src'])
        response_data = {}
        response_data['outputtext'] = output
    # run_code from WebCompiler takes source code as a string and
    # returns a string containing success confirmation and output
    # or java error message
