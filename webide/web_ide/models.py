from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.contrib.auth import hashers
from django.core.validators import RegexValidator
from datetime import datetime
import os
from django.core.files.storage import FileSystemStorage
from django.core.files.base import File


# This is to implement the Administrator functionality
class DeveloperManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Email address required')
        if not username:
            raise ValueError('Username required')

        user = self.model(username=username, email=self.normalize_email(email),)

        user.is_active = True
        user.set_password(password)
        user.save(using=self.db)
        return user

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

    def check_password(self, raw_pass):
        return hashers.check_password(raw_pass, self.password)


#class to represent the filesystem


class ProjectFiles(FileSystemStorage):

    def create_file(self, name, content=None):
        if content is None:
            f = open('temp.txt', 'w+')
        else:
            f = content

        return self.save(name, f)

    def list(self, path):
        contents = self.listdir(path)
        directories = contents[0]
        files = contents[1]
        return files, directories

    def open_file(self, name):
        if self.exists(name):
            return self.open(name, 'rb')
        else:
            return False

    def delete_file(self, name):
        return self.delete(name)

    def make_directory(self, path, name):
        try:
            os.mkdir(os.path.join(self.location, path, name))
        except OSError as e:
            if e.errno == 17:
                return False
        return True

    def write_file(self, name, content):
        temp = self.rename_file(name + '-temp', name)
        written = self.save(name, content)
        self.delete_file(temp)
        return written

    def rename_file(self, newname, oldname):
        new = self.create_file(newname, self.open_file(oldname))
        self.delete_file(oldname)
        return new


#chat message db entry
class ChatMessage(models.Model):
    message = models.TextField()
    author = models.CharField(max_length = 20)

    def getMessage(self):
        return self.message

    def getAuthor(self):
        return self.author

'''
class Room(models.Model):
    belongs_to_type = models.CharField(max_length=100, blank=True, null=True)
    belongs_to_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField()
    comment = models.TextField(blank=True, null=True)
    objects = RoomManager() # custom manager

    class Meta():
        unique_together = (('belongs_to_type', 'belongs_to_id'))

    def say(self, type, sender, message):
        #Say something in le chat
        m = Message(self, type, sender, message)
        m.save()
        return m

    def messages(self, after=None):
        m = Message.objects.filter(room=self)
        if after:
            m = m.filter(pk__gt=after)
        return m

    def __unicode__(self):
        return 'Chat for %s %d' % (self.belongs_to_type, self.belongs_to_id)
'''

class RoomManager(models.Manager):
    '''Custom model manager for rooms, this is used for "table-level" operations'''
    def create(self, parent_type, parent_id):
        '''Creates a new chat room and registers it to the calling object'''
        # the first none is for the ID
        r = self.model(None, parent_type, parent_id, datetime.now())
        r.save()
        return r

    def get_room(self, parent_type, parent_id):
        '''Get a room through its parent.'''
        return self.get(belongs_to_type=parent_type, belongs_to_id=parent_id)

class Message(models.Model):
    '''A message that belongs to a chat room'''
    MESSAGE_TYPE_CHOICES = (
    ('s','system'),
    ('a','action'),
    ('m', 'message'),
    ('j','join'),
    ('l','leave'),
    ('n','notification')
)
   # room = models.ForeignKey(Room)
    type = models.CharField(max_length=1, choices= MESSAGE_TYPE_CHOICES)
    sender = models.CharField(max_length=50, blank=True)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        '''Each message type has a special representation, return that representation.
        This will also be translator AKA i18l friendly.'''
        if self.type in ['s','m','n']:
            return u'*** %s' % self.message
        elif self.type == 'j':
            return '*** %s has joined...' % self.sender
        elif self.type == 'l':
            return '*** %s has left...' % self.sender
        elif self.type == 'a':
            return '*** %s %s' % (self.sender, self.message)
        return ''

class Build(models.Model):
    buildname = models.CharField(max_length=64)

#server text for differential sync. There should only be one instance of this per file.
class ServerText(models.Model):
    #filename
    filename = models.TextField(max_length=128)
    #text
    text = models.TextField(max_length=512)

#server shadow for differential sync. There will be a server shadow for each client/file access.
class ServerShadow(models.Model):
    #filename
    filename = models.TextField(max_length=128)
    #text
    text = models.TextField(max_length=512)
    #name, will be based on client's session token
    name = models.TextField(max_length=128)
