from django.test import TestCase
from web_ide.models import DeveloperManager
from web_ide.models import Developer
from web_ide.models import ProjectFile
from web_ide.forms import DeveloperForm
from webide.web_ide.syntax.highlighting_engine import HighlightingEngine
from webide.web_ide.syntax.plyj.ply.lex import LexToken
#test regexes for user credentials
class UserCredentialsTestCase(TestCase):

    #test username validation
    def test_username_validation(self):
        
        #valid fields
        user_form_valid = DeveloperForm({'username': "testusername", 'email': "email@abc.com", 'password': "password"})
        self.assertEqual(user_form_valid.is_valid(), True)

        #username longer than 30 characters, should be false
        user_form_too_long = DeveloperForm({'username': "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 'email': "email@abc.com", 'password': "password"})
        self.assertEqual(user_form_too_long.is_valid(), False)

    #test email validation
    def test_email_validation(self):
        
        #valid fields
        user_form_valid = DeveloperForm({'username': "testusername", 'email': "email@abc.com", 'password': "password"})
        self.assertEqual(user_form_valid.is_valid(), True)

        #email is invalid
        user_form_bad_email = DeveloperForm({'username': "testusername", 'email': "bademail", 'password': "password"})
        self.assertEqual(user_form_bad_email.is_valid(), False)

#tests for model 
class DeveloperTestCase(TestCase):
    def test_getter_methods(self):
        #create developer object
        user_form_valid = DeveloperForm({'username': "testusername", 'email': "email@abc.com", 'password': "password"})
        user = user_form_valid.save()
        user.set_password(user.password)
        
        #test the getter methods
        self.assertEqual(user.get_full_name(), "testusername")
        self.assertEqual(user.get_short_name(), "testusername")

class SyntaxTestCase(TestCase):
    # tests for highlighting single element:
    ''' def highlight_element(self, token):
        type = token.type
        for k, v in self.color_table.iteritems():
            if (type == k): return v
            else: return 'default' '''

    def test_token_mapping(self):
        he = HighlightingEngine()
        hard_mapping = he.color_table["INT"]

        test_tok = LexToken('INT', 'int', 1, 1)
        test_mapping = he.highlight_element(test_tok)

        self.assertEqual(hard_mapping, test_mapping)

    # tests for tokenizing and mapping entire file:


