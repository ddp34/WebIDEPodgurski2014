from django.db import models
from django.contrib.auth.models import User

# This is to implement the Administrator functionality
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    isAdmin = models.BooleanField(blank=False)

    def __unicode__(self):
        return self.user.username