import unittest
from db.dbManager import DBManager
from rooms import Rooms
import os


class RoomTest(unittest.TestCase):
    """Test for rooms (living spaces and Office spaces)"""

    def setUp(self):
        """Create a test database"""
        self.db = DBManager('test.db')

    def test_create_rooms(self):
        """
        Create test database and assert that there are no rooms in that table.

        Create 3 rooms and assert that there are now 3 rooms.

        Assert that woodwing is the first room in the list of rooms.

        Assert that woodwing is of type living space (L)
        """
        all_rooms = self.db.select("SELECT * FROM rooms")
        self.assertEqual(0, len(all_rooms))

        rooms = Rooms("test.db")
        arguments = {'<room_name>': ['woodwing', 'westwing', 'eastwing'],
                     'living': True,
                     'office': False}

        new_rooms = rooms.create_rooms(arguments)
        self.assertTrue(new_rooms)

        all_rooms = self.db.select("SELECT * FROM rooms")
        self.assertEqual(3, len(all_rooms))
        self.assertTrue('woodwing' in all_rooms[0])
        self.assertTrue('L' in all_rooms[0])

    def tearDown(self):
        """Delete the test database"""

        if os.path.exists('test.db'):
            os.remove('test.db')

if __name__ == '__main__':
    unittest.main()
