from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.contrib.auth import hashers
from django.contrib.auth.models import User
from webide.settings import AUTH_USER_MODEL
from django.contrib.contenttypes.models import ContentType, ContentTypeManager
from django.contrib.contenttypes import generic

from django.core.validators import RegexValidator
from datetime import datetime
from django.core.files.storage import FileSystemStorage
import os
import shutil


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
#most of this is from the Django FileSystemStorage source code
#but with some changes, such as make_directory

class ProjectFiles(FileSystemStorage):
    location = os.path.join(os.path.abspath(os.path.abspath(os.path.dirname(__file__))), 'userfiles')

    #the save method throughout this class is inherited from FileSystemStorage

    def create_file(self, name, content=None):
        if content is None:
            f = open('temp.txt', 'w+')
        else:
            f = content

        return self.save(name, f)

    #list all files and directories in a directory
    #returns the files, then the directories
    def list(self, path):
        contents = self.listdir(path)
        directories = contents[0]
        files = contents[1]
        return files, directories
    
    #wrapper method for recursive directory listing
    def list_r(self, rootdir):
        #return self.list_recursive(path, {path: {'files': []}})
        """
        Creates a nested dictionary that represents the folder structure of rootdir
        """
        dir = {}
        rootdir = rootdir.rstrip(os.sep)
        start = rootdir.rfind(os.sep) + 1
        for path, dirs, files in os.walk(rootdir):
            folders = path[start:].split(os.sep)
            subdir = dict.fromkeys(files)
            parent = reduce(dict.get, folders[:-1], dir)
            parent[folders[-1]] = subdir
        return dir        

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
        #got this from a StackOverflow post
        except OSError as e:
            if e.errno == 17:
                return False
        return True

    def write_file(self, name, content):
        temp = self.rename_file(name + '-temp', name)
        written = self.save(name, content)
        self.delete_file(temp)
        return written

    def write_string_to_file(self, name, inputString):
        #intermediate file, for now this must be used to write to a file with this API
        intermed = open(name+ "-intermediate.txt", 'w+')
        intermed.write(inputString)
        #intermed.close()
        return self.write_file(name, intermed)

    def rename_file(self, newname, oldname):
        new = self.create_file(newname, self.open_file(oldname))
        self.delete_file(oldname)
        return new

    def get_path(self):
        return self.location


class SnapshotManager():

    def __init__(self):
        self.location = os.path.join(os.path.dirname(os.path.abspath(os.path.abspath(os.path.dirname(__file__)))),
                                     'snapshots')
        try:
            os.mkdir(self.location)
        except OSError as e:
            if e.errno == 17:
                pass

    def list_snaps(self):
        return os.listdir(self.location)


class Snapshot(ProjectFiles):

    title = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    dir = os.path.join(os.path.join(os.path.dirname(os.path.abspath(os.path.abspath(os.path.dirname(__file__)))),
                       'snapshots/'), title)

    def create_snap(self):
        shutil.copytree(os.path.join(os.path.dirname(os.path.abspath(os.path.abspath(os.path.dirname(__file__)))),
                                     'userfiles'), self.dir)

    def rename(self, new):
        self.title = new
        new_dir = os.path.join(os.path.dirname(self.dir), new)
        shutil.move(self.dir, new_dir)
        self.dir = new_dir
        return self.title

    def revert(self, relative_path):
        shutil.copyfile(os.path.join(self.dir, relative_path),
                        os.path.join(os.path.join(os.path.dirname(os.path.dirname(self.dir)),
                                                  'userfiles'), relative_path))


#chat message db entry
class ChatMessage(models.Model):
    message = models.TextField()
    author = models.CharField(max_length = 20)

    def getMessage(self):
        return self.message

    def getAuthor(self):
        return self.author

class RoomManager(models.Manager):

    def create(self, object):
        #Creates a new chat room and registers it to the calling object'''
        r = self.model(content_object=object)
        r.save()
        return r

    def get_for_object(self, object):
        #Try to get a room related to the object passed.
        return self.get(content_type=ContentType.objects.get_for_model(object), object_id=object.pk)

    def get_or_create(self, object):
        #Save us from the hassle of validating the return value of get_for_object and create a room if none exists
        try:
            return self.get_for_object(object)
        except Room.DoesNotExist:
            return self.create(object)

class Room(models.Model):
    #Representation of a generic chat room'''
    content_type = models.ForeignKey(ContentType, blank=True, null=True) # to what kind of object is this related
    object_id = models.PositiveIntegerField(blank=True, null=True) # to which instace of the aforementioned object is this related
    content_object = generic.GenericForeignKey('content_type','object_id') # use both up, USE THIS WHEN INSTANCING THE MODEL
    created = models.DateTimeField(default=datetime.now())
    comment = models.TextField(blank=True, null=True)
    objects = RoomManager() # custom manager

    def __add_message(self, type, sender, message=None):
        #Generic function for adding a message to the chat room'''
        m = Message(room=self, type=type, author=sender, message=message)
        m.save()
        return m

    def say(self, sender, message):
        #Say something in to the chat room'''
        return self.__add_message('m', sender, message)

    def join(self, user):
        #A user has joined'''
        return self.__add_message('j', user)

    def leave(self, user):
        #A user has leaved'''
        return self.__add_message('l', user)

    def messages(self, after_pk=None, after_date=None):
        #List messages, after the given id or date'''
        m = Message.objects.filter(room=self)
        if after_pk:
            m = m.filter(pk__gt=after_pk)
        if after_date:
            m = m.filter(timestamp__gte=after_date)
        return m.order_by('pk')

    def last_message_id(self):
        #Return last message sent to room'''
        m = Message.objects.filter(room=self).order_by('-pk')
        if m:
            return m[0].id
        else:
            return 0

    def __unicode__(self):
        return 'Chat for %s %d' % (self.content_type, self.object_id)

    class Meta:
        unique_together = (("content_type", "object_id"),)


MESSAGE_TYPE_CHOICES = (
    ('s','system'),
    ('a','action'),
    ('m', 'message'),
    ('j','join'),
    ('l','leave'),
    ('n','notification')
)


class Message(models.Model):
    #A message that belongs to a chat room'''
    room = models.ForeignKey(Room)
    type = models.CharField(max_length=1, choices=MESSAGE_TYPE_CHOICES)
    author = models.ForeignKey(AUTH_USER_MODEL, related_name='author', blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        #Each message type has a special representation, return that representation.

        if self.type == 's':
            return u'SYSTEM: %s' % self.message
        if self.type == 'n':
            return u'NOTIFICATION: %s' % self.message
        elif self.type == 'j':
            return 'JOIN: %s' % self.author
        elif self.type == 'l':
            return 'LEAVE: %s' % self.author
        elif self.type == 'a':
            return 'ACTION: %s > %s' % (self.author, self.message)
        return self.message


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
