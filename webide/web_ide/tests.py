from django.test import TestCase
from web_ide.models import DeveloperManager
from web_ide.models import Developer
from web_ide.forms import DeveloperForm
#from web_ide.models import FileSystem

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

    #TODO: test password/email validation

# Django's example:
'''
class AnimalTestCase(TestCase):
    def setUp(self):
        Animal.objects.create(name="lion", sound="roar")
        Animal.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')
'''       
# Running tests:
'''
# Run all the tests in the animals.tests module
$ ./manage.py test animals.tests

# Run all the tests found within the 'animals' package
$ ./manage.py test animals

# Run just one test case
$ ./manage.py test animals.tests.AnimalTestCase

# Run just one test method
$ ./manage.py test animals.tests.AnimalTestCase.test_animals_can_speak
'''    
