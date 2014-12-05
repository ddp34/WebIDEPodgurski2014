from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login

#import text sync engine and dependencies
from diffsync import DiffSync
from ideone import Ideone
from web_ide.models import *
import time
import os
import json

#keep a static DiffSync object to run synchronizations
diff_sync_engine = DiffSync()

#filesystem controller
project_files = ProjectFiles()
compiler = Ideone('lne1', 'eecs393')

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
                servershadow = ServerShadow.objects.get(name=request.POST['csrfmiddlewaretoken'], filename=request.POST['filename'])
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

            msg_list = []
            for txt in Msg.objects.values_list('text', flat=True):
                author = Msg.objects.get(text=txt).name
                msg_list.extend([author + ": " + txt])


            #return the client text and client shadow
            response_data = {}
            response_data['clienttext'] = syncresults[0]
            response_data['clientshadow'] = syncresults[1]
            response_data['chats'] = msg_list

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

        if request.POST['posttype'] == "sendcode":
            src = request.POST['src']
            sub = compiler.create_submission(src, language_name='Java')
            #time.sleep(5.0)
            link = sub['link']
            sub_det = compiler.submission_details(link)
            while sub_det['status'] != 0:
                sub_det = compiler.submission_details(link)
            if sub_det['output']:
                output = sub_det['output']
            else:
                output = sub_det['cmpinfo']
            return HttpResponse(repr(output))

        if request.POST['posttype'] == "chatmsg":
            #add to database

            author = request.META['USER']
            newmsg = Msg(name=author, text=request.POST['message'])
            newmsg.save()

            msg_list = []
            for txt in Msg.objects.values_list('text', flat=True):
                author = Msg.objects.get(text=txt).name
                msg_list.extend([author + ": " + txt])

            response_data = {}
            response_data['messages'] = msg_list #list(Msg.objects.values_list('text', flat=True))
            return HttpResponse(json.dumps(response_data), content_type="application/json")

    else:
        #initial GET request to editor page

        try:
            #retrieve server text and push it to user
            servertext = ServerText.objects.get(filename="README.md")
        except ServerText.DoesNotExist:
            #create buffer if it doesn't exist already
            servertext = ServerText(filename="README.md", text=project_files.open_file("README.md").read())
            servertext.save()

        #load chats
        msg_list = []
        for txt in list(Msg.objects.values_list('text', flat=True)):
            msg_list.extend([txt])

        #generate directory structure
        fs = json.dumps(project_files.list_r(os.getcwd() + "/webide/userfiles/"))

        context = {'filetext': servertext.text, 'clishadow': servertext.text, 'fs': fs}

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
