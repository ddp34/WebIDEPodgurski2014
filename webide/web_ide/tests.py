from django.test import TestCase
from web_ide.models import *
from web_ide.forms import CustomDeveloperCreationForm

from diffsync import DiffSync

'''
#test regexes for user credentials
class UserCredentialsTestCase(TestCase):

    #test username validation
    def test_username_validation(self):
        
        #valid fields
        user_form_valid = CustomDeveloperCreationForm({'username': "testusername", 'email': "email@abc.com", 'password': "password"})
        self.assertEqual(user_form_valid.is_valid(), True)

        #username longer than 30 characters, should be false
        user_form_too_long = CustomDeveloperCreationForm({'username': "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 'email': "email@abc.com", 'password': "password"})
        self.assertEqual(user_form_too_long.is_valid(), False)

    #test email validation
    def test_email_validation(self):
        
        #valid fields
        user_form_valid = CustomDeveloperCreationForm({'username': "testusername", 'email': "email@abc.com", 'password': "password"})
        self.assertEqual(user_form_valid.is_valid(), True)

        #email is invalid
        user_form_bad_email = CustomDeveloperCreationForm({'username': "testusername", 'email': "bademail", 'password': "password"})
        self.assertEqual(user_form_bad_email.is_valid(), False)

#tests for model 
class DeveloperTestCase(TestCase):
    def test_getter_methods(self):
        #create developer object
        user_form_valid = CustomDeveloperCreationForm({'username': "testusername", 'email': "email@abc.com", 'password': "password"})
        user = user_form_valid.save()
        user.set_password(user.password)
        
        #test the getter methods
        self.assertEqual(user.get_full_name(), "testusername")
        self.assertEqual(user.get_short_name(), "testusername")

'''

'''
Tests the differential synchronization engine,
written in diffsync.py
'''
class DiffSyncTestCase(TestCase):
    
    def setUp(self):

        #server text
        ServerText.objects.create(filename="test.txt", text="The quick brown fox jumps over the lazy dog.")

        #user a's server shadow
        ServerShadow.objects.create(filename="test.txt", text="The quick brown fox jumps over the lazy dog.", name="a")

        #user b's server shadow
        ServerShadow.objects.create(filename="test.txt", text="The quick brown fox jumps over the lazy dog.", name="b")
        
    #tests text sync for two users across a single file
    def test_single_file_sync(self):

        diff_sync = DiffSync()

        #user a variables
        a_clienttext = "The quick red fox jumps over the lazy dog."
        a_clientshadow = "The quick brown fox jumps over the lazy dog."
        a_servershadow = ServerShadow.objects.get(name="a")

        #user b variables
        b_clienttext = "The quick brown fox jumps above the lazy dog."
        b_clientshadow = "The quick brown fox jumps over the lazy dog."
        b_servershadow = ServerShadow.objects.get(name="b")

        #grab objects
        servertext = ServerText.objects.get(filename="test.txt")

        #suppose user a syncs their work, and then user b
        sync_results_1 = diff_sync.synchronizeDocs(a_clienttext, a_clientshadow, a_servershadow.text, servertext.text)

        #check that the resulting client text and shadow for a are valid
        self.assertEqual(sync_results_1[0], "The quick red fox jumps over the lazy dog.")

        self.assertEqual("", "")
