import unittest
import os
from people import Person
from data import Data


class PeopleTest(unittest.TestCase):
    """Tests for Person Class"""

    def setUp(self):
        self.data = Data()

    def test_unallocated_people(self):
        """
        Get a list of all unallocated people printed on the screen
        and in a text file
        """
        people = Person()

        self.data.create_office_spaces(['midgar'])
        self.data.create_living_spaces(['woodwing'])

        self.data.create_fellow("John", "Kariuki", "y")
        self.data.create_fellow("Judas", "Iscariot", "y")

        people.unallocated({'--o': 'y'})
        self.assertTrue(os.path.exists('unallocated.txt'))

        with open('unallocated.txt') as f:
            lines = f.readlines()
            self.assertTrue('All fellows have been assigned' in lines)
        os.remove('unallocated.txt')

        self.data.create_fellow("Blue", "October", "n")

        self.data.create_staff("John", "Kariuki")
        self.data.create_staff("Blue", "October")

        people.unallocated({'--o': 'y'})
        self.assertTrue(os.path.exists('unallocated.txt'))

        with open('unallocated.txt') as f:
            lines = f.readlines()
            self.assertTrue('All staff have been assigned\n' in lines)
            self.assertTrue('Blue October\t[N]' in lines)
        os.remove('unallocated.txt')

    def tearDown(self):
        """Delete the test database"""
        self.data.clear_test_db()

if __name__ == '__main__':
    unittest.main()
