from django.conf.urls import patterns, url, include
from django.contrib import admin
from web_ide import views

urlpatterns = patterns('',
                       url(r'login', views.user_login, name='login'),
                       url(r'^$', views.user_login, name='home'),
                       url(r'register', views.register, name='register'),
                       url(r'editor', views.editor, name='editor'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'restricted', views.restricted, name='restricted'),
                       url(r'logout', views.user_logout, name='logout'))
