from django.contrib import admin
from web_ide.models import UserProfile

# Note that admin.py doesn't have anything to do with
# the Administrator user class -Gabe
# Register your models here.
admin.site.register(UserProfile)
