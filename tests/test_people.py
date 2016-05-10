import unittest
import os
from data import Data


class PeopleTest(unittest.TestCase):
    """Test for Pople (Staff and People)"""

    def setUp(self):
        self.data = Data()

    def test_create_fellow(self):
        """
        Assert that a user can add a new fellow
        """
        fellows = self.data.fetch_data("fellows", False)
        self.assertEqual(0, len(fellows))

        self.data.create_living_spaces()

        new_fellow = self.data.create_fellow("John", "Kariuki", "y")
        self.assertTrue(new_fellow)

        fellows = self.data.fetch_data("fellows", False)
        self.assertEqual(1, len(fellows))

    def tearDown(self):
        """Delete the test database"""
        if os.path.exists('room_alloc.db'):
            os.remove('room_alloc.db')

if __name__ == '__main__':
    unittest.main()
