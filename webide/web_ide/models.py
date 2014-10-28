from django.db import models
from django.contrib.auth.models import User

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()

    def __unicode__(self):
        return self.title

# This is to implement the Administrator functionality
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    isAdmin = models.BooleanField(blank=True)

    def __unicode__(self):
        return self.user.username