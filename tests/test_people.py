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

        self.data.create_living_spaces(['woodwing', 'westwing', 'eastwing'])

        new_fellow = self.data.create_fellow("John", "Kariuki", "y")
        self.assertTrue(new_fellow)

        fellows = self.data.fetch_data("fellows", False)
        self.assertEqual(1, len(fellows))

    def test_create_staff(self):
        """
        Assert that a user can add a new staff member
        """
        staff = self.data.fetch_data("staff", False)
        self.assertEqual(0, len(staff))

        self.data.create_office_spaces(['camelot', 'midgar'])
        new_staff = self.data.create_staff('Dej', 'Loaf')
        self.assertTrue(new_staff)

        staff = self.data.fetch_data("staff", False)
        self.assertEqual(1, len(staff))

    def tearDown(self):
        """Delete the test database"""
        if os.path.exists('room_alloc.db'):
            os.remove('room_alloc.db')

if __name__ == '__main__':
    unittest.main()
