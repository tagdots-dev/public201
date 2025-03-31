import unittest


# Class to be tested
class Person:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

# Test case class
class TestPersonClass(unittest.TestCase):

    def test_get_name(self):
        person = Person("Alice")
        self.assertEqual(person.get_name(), "Alice") # Test case: check name retrieval




