from django.db import models
from django.contrib.auth.models import User

# This is to implement the Administrator functionality
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    isAdmin = models.BooleanField(blank=False)

    def __unicode__(self):
        return self.user.username

#class to represent the filesystem
class FileSystem(models.Model):
    filename = models.CharField(max_length=64)
    contents = models.CharField(max_length=2056)

    def getName(self):
        return self.name

    def getContents(self):
        return self.contents

    def isDir(self, path):
        return os.path.isdir(path)
