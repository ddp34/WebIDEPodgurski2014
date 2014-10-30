from django.test import TestCase
from web_ide.models import DeveloperManager
from web_ide.models import Developer
from web_ide.models import FileSystem

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
 
 
# Test the DeveloperManager model
class DeveloperManagerTestCase(TestCase):    
    
# Test the Developer model
class DeveloperTestCase(TestCase):

# Test the FileSystem model
class FileSystemTestCase(TestCase):