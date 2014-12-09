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

#class SyntaxTestCase(TestCase):

    #def test_token_mapping(self):
        #he = HighlightingEngine()
        #hard_mapping = he.color_table["INT"]

        #test_tok = LexToken('INT', 'int', 1, 1)
        #test_mapping = he.highlight_element(test_tok)

        #self.assertEqual(hard_mapping, test_mapping)
'''


class ProjectFilesTestCase(TestCase):

    def test_file_creation(self):
        name = 'test name'
        fs = ProjectFiles()
        fs.create_file(name)
        self.assertIn(u'test name', fs.list('')[0])

    def test_file_open(self):
        fs = ProjectFiles()
        fs.create_file('test')
        file_open_is_valid = fs.open_file('test')
        self.assertIsNotNone(file_open_is_valid)

    def test_file_deletion(self):
        fs = ProjectFiles()
        fs.delete_file('test')
        self.assertNotIn('test', fs.list(''))

    def test_make_directory(self):
        fs = ProjectFiles()
        fs.make_directory('', 'testname')
        self.assertIn(u'testname', fs.list('')[1])