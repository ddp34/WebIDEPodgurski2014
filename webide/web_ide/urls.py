from django.conf.urls import patterns, url
from web_ide import views

urlpatterns = patterns('',
                       url(r'login', views.login, name='login'),
                       url(r'admin', views.admin, name='admin'),
                       url(r'editor', views.editor, name='editor'))
