from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.core.validators import RegexValidator


# This is to implement the Administrator functionality
class DeveloperManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Email address required')
        if not username:
            raise ValueError('Username required')

        developer = self.model(username=username, email=self.normalize_email(email),)

        developer.is_active = True
        developer.set_password(password)
        developer.save(using=self.db)
        return developer

    def create_superuser(self, username, email, password):
        administrator = self.create_user(username=username, email=email, password=password)
        administrator.is_superuser = True
        administrator.is_staff = True
        administrator.save(using=self.db)
        return administrator


class Developer(AbstractBaseUser, PermissionsMixin):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message='Alphanumeric characters only')
    username = models.CharField(unique=True, max_length=20, validators=[alphanumeric])
    email = models.EmailField(verbose_name='email address', unique=True, max_length=255)
    is_active = models.BooleanField(default=True, null=False)
    is_staff = models.BooleanField(default=False, null=False)

    # Custom user manager instead of the default
    objects = DeveloperManager()

    # This is the unique identifier for authentication (logging in)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # These two methods are required to be overridden
    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return self.username

#class to represent the filesystem

class ProjectFile(models.Model):
    filename = models.CharField(max_length=64)
    contents = models.CharField(max_length=2056)
    #pointers to contained files, if directory
    

    def getName(self):
        return self.name

    def getContents(self):
        return self.contents

    def isDir(self, path):
        return os.path.isdir(path)
        return self.email

#chat message db entry
class ChatMessage(models.Model):
    message = models.CharField()
    author = models.CharField()

    def getMessage(self):
        return self.message

    def getAuthor(self):
        return self.author
