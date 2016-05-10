import unittest
import os
from data import Data


class RoomTest(unittest.TestCase):
    """Test for rooms (living spaces and Office spaces)"""

    def setUp(self):
        self.data = Data()

    def test_create_rooms(self):
        """
        Create test database and assert that there are no rooms in that table.

        Create 3 rooms and assert that there are now 3 rooms.

        Assert that woodwing is the first room in the list of rooms.

        Assert that woodwing is of type living space (L)
        """
        all_rooms = self.data.fetch_data("rooms", False)
        self.assertEqual(0, len(all_rooms))

        new_rooms = self.data.create_living_spaces()
        self.assertTrue(new_rooms)

        all_rooms = self.data.fetch_data("rooms", False)
        self.assertEqual(3, len(all_rooms))
        self.assertTrue('woodwing' in all_rooms[0])
        self.assertTrue('L' in all_rooms[0])

    def tearDown(self):
        """Delete the test database"""
        if os.path.exists('test.db'):
            os.remove('test.db')

if __name__ == '__main__':
    unittest.main()
