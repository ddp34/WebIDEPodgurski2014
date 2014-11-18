from django.conf.urls import patterns, url, include
from web_ide.admin import admin_site
from web_ide import views

urlpatterns = patterns('',
                       url(r'login', views.user_login, name='login'),
                       url(r'^$', views.user_login, name='home'),
                       url(r'editor', views.editor, name='editor'),
                       url(r'^admin/', include(admin_site.urls)),
                       url(r'restricted', views.restricted, name='restricted'),
                       url(r'logout', views.user_logout, name='logout'))
